#!/usr/bin/env python3
"""
IQ Waterfall Stitcher
=====================
Stitches multiple SDR IQ files into a single wideband waterfall display.

Supported IQ file formats:
  - Raw interleaved float32 (default)
  - Raw interleaved int16 (--dtype int16)
  - Raw interleaved uint8 / RTL-SDR format (--dtype uint8)
  - SigMF (.sigmf-meta + .sigmf-data) — auto-detected
  - GNU Radio complex float32 (.cfile) — same as float32

Usage examples
--------------
# Explicit frequency/bandwidth per file:
python iq_waterfall.py \
    --files seg1.iq seg2.iq seg3.iq \
    --freqs 100e6 102e6 104e6 \
    --bw    2e6   2e6   2e6

# Auto-parse frequency/bandwidth from filenames like:
#   capture_100.0MHz_2.0MHz.iq   or   sdr_433500000_250000.raw
python iq_waterfall.py --files *.iq --auto-parse

# SigMF bundles (reads metadata automatically):
python iq_waterfall.py --files rec1.sigmf-meta rec2.sigmf-meta

# Override FFT size, overlap, colormap, output file:
python iq_waterfall.py --files *.iq --auto-parse \
    --fft 2048 --overlap 0.5 --cmap inferno --output waterfall.png
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

# ── optional deps, checked at runtime ────────────────────────────────────────
try:
    import matplotlib

    matplotlib.use("TkAgg")  # interactive; falls back gracefully
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from matplotlib.colors import Normalize

    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# ─────────────────────────────────────────────────────────────────────────────
# IQ loading helpers
# ─────────────────────────────────────────────────────────────────────────────

DTYPE_MAP = {
    "float32": np.complex64,
    "int16": None,  # needs special handling
    "uint8": None,
    "cf32": np.complex64,
    "ci16": None,
    "cu8": None,
}


def load_iq(path: str, dtype: str = "float32") -> np.ndarray:
    """Load an IQ file and return a complex64 numpy array."""
    path = Path(path)

    # ── SigMF ────────────────────────────────────────────────────────────────
    if path.suffix == ".sigmf-meta":
        return _load_sigmf(path)

    # ── Raw binary ──────────────────────────────────────────────────────────
    if dtype in ("float32", "cf32"):
        raw = np.fromfile(path, dtype=np.float32)
        if len(raw) % 2:
            raw = raw[:-1]
        return raw.view(np.complex64)

    if dtype in ("int16", "ci16"):
        raw = np.fromfile(path, dtype=np.int16).astype(np.float32)
        if len(raw) % 2:
            raw = raw[:-1]
        raw /= 32768.0
        return raw.view(np.complex64)

    if dtype in ("uint8", "cu8"):
        raw = np.fromfile(path, dtype=np.uint8).astype(np.float32)
        if len(raw) % 2:
            raw = raw[:-1]
        raw = (raw - 127.5) / 128.0
        return raw.view(np.complex64)

    raise ValueError(f"Unknown dtype: {dtype!r}")


def _load_sigmf(meta_path: Path) -> np.ndarray:
    with open(meta_path) as f:
        meta = json.load(f)
    data_path = meta_path.with_suffix(".sigmf-data")
    fmt = meta.get("global", {}).get("core:datatype", "cf32_le")
    if "cf32" in fmt:
        return load_iq(str(data_path), "float32")
    if "ci16" in fmt:
        return load_iq(str(data_path), "int16")
    if "cu8" in fmt:
        return load_iq(str(data_path), "uint8")
    raise ValueError(f"Unsupported SigMF datatype: {fmt}")


def sigmf_center_bw(meta_path: Path) -> Tuple[float, float]:
    with open(meta_path) as f:
        meta = json.load(f)
    g = meta.get("global", {})
    cap = meta.get("captures", [{}])[0]
    fc = float(cap.get("core:frequency", g.get("core:frequency", 0)))
    bw = float(g.get("core:sample_rate", 0))
    return fc, bw


# ─────────────────────────────────────────────────────────────────────────────
# Filename auto-parser
# ─────────────────────────────────────────────────────────────────────────────

_PATTERNS = [
    # 100.0MHz_2.0MHz   or   100MHz_2MHz
    re.compile(
        r"(\d+(?:\.\d+)?)\s*([kmg]?)hz[_\-](\d+(?:\.\d+)?)\s*([kmg]?)hz",
        re.IGNORECASE,
    ),
    # 100000000_2000000  (bare integers, underscore-separated at end of name)
    re.compile(r"(\d{6,})_(\d{4,})(?:\D|$)"),
]

_MULT = {"": 1, "k": 1e3, "K": 1e3, "m": 1e6, "M": 1e6, "g": 1e9, "G": 1e9}


def parse_freq_bw_from_name(filename: str) -> Tuple[Optional[float], Optional[float]]:
    name = Path(filename).name
    m = _PATTERNS[0].search(name)
    if m:
        fc = float(m.group(1)) * _MULT.get(m.group(2), 1)
        bw = float(m.group(3)) * _MULT.get(m.group(4), 1)
        return fc, bw
    m = _PATTERNS[1].search(name)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None


# ─────────────────────────────────────────────────────────────────────────────
# Spectrogram computation
# ─────────────────────────────────────────────────────────────────────────────


def compute_spectrogram(
    iq: np.ndarray,
    fft_size: int = 1024,
    overlap: float = 0.5,
) -> np.ndarray:
    """
    Returns a 2-D power spectrogram (dB), shape = (n_time, fft_size).
    Frequency bins are in *baseband* order (DC-centred after fftshift).
    """
    step = max(1, int(fft_size * (1.0 - overlap)))
    n_frames = (len(iq) - fft_size) // step + 1
    if n_frames <= 0:
        # File shorter than one FFT — zero-pad to one frame
        iq = np.pad(iq, (0, fft_size - len(iq)))
        n_frames = 1

    window = np.hanning(fft_size).astype(np.float32)
    spec = np.zeros((n_frames, fft_size), dtype=np.float32)

    for i in range(n_frames):
        frame = iq[i * step : i * step + fft_size] * window
        fft = np.fft.fftshift(np.fft.fft(frame, n=fft_size))
        spec[i] = np.abs(fft) ** 2

    # Convert to dB, clamp to avoid log(0)
    spec = 10.0 * np.log10(np.maximum(spec, 1e-20))
    return spec


# ─────────────────────────────────────────────────────────────────────────────
# Stitching
# ─────────────────────────────────────────────────────────────────────────────

OVERLAP_MODES = ("crossfade", "average", "left", "right", "strongest")


def stitch_spectrograms(
    segments: List[dict],
    output_fft: int = 1024,
    overlap_mode: str = "crossfade",
) -> Tuple[np.ndarray, float, float]:
    """
    Stitch per-segment spectrograms onto a common frequency grid,
    with configurable handling of frequency-overlap bands.

    Each element of `segments` is a dict with keys:
        center_hz  : float   – centre frequency (Hz)
        bw_hz      : float   – bandwidth / sample-rate (Hz)
        spec       : ndarray – (n_time, fft_seg) power in dB

    overlap_mode : str
        "crossfade"  – linear weight taper across the overlap (default).
                       Best for SDR captures: it de-weights the anti-aliasing
                       filter rolloff at each segment's band edge naturally.
        "average"    – arithmetic mean of both segments in the overlap.
        "left"       – keep the left (lower-fc) segment in the overlap.
        "right"      – keep the right (higher-fc) segment in the overlap.
        "strongest"  – keep whichever segment has higher mean power per bin
                       (resolved per time-row for maximum adaptiveness).

    Returns
    -------
    stitched  : ndarray (n_time_max, output_fft)  power dB, NaN where no data
    f_min_hz  : float  – lowest frequency edge
    f_max_hz  : float  – highest frequency edge
    """
    if overlap_mode not in OVERLAP_MODES:
        raise ValueError(
            f"overlap_mode must be one of {OVERLAP_MODES}, got {overlap_mode!r}"
        )

    f_min = min(s["center_hz"] - s["bw_hz"] / 2 for s in segments)
    f_max = max(s["center_hz"] + s["bw_hz"] / 2 for s in segments)
    total_bw = f_max - f_min

    n_time = max(s["spec"].shape[0] for s in segments)

    # We work in linear power during blending to avoid dB-domain artefacts,
    # then convert back to dB at the end.
    # accumulator  : weighted sum of linear power per bin
    # weight_acc   : sum of weights per bin (for normalisation)
    accumulator = np.zeros((n_time, output_fft), dtype=np.float64)
    weight_acc = np.zeros((n_time, output_fft), dtype=np.float64)

    # Sort by centre frequency so "left" / "right" make sense
    ordered = sorted(segments, key=lambda s: s["center_hz"])

    # Pre-compute each segment's resampled linear power on the global grid
    resampled_segs = []
    for seg in ordered:
        fc = seg["center_hz"]
        bw = seg["bw_hz"]
        spec_db = seg["spec"]  # (t_seg, fft_seg) in dB
        fft_seg = spec_db.shape[1]

        # Normalise time axis
        if spec_db.shape[0] != n_time:
            from scipy.ndimage import zoom

            spec_db = zoom(spec_db, (n_time / spec_db.shape[0], 1), order=1)

        # Convert to linear power for blending
        spec_lin = np.power(10.0, spec_db / 10.0).astype(np.float64)

        # Frequency column mapping on the global grid
        f_lo = fc - bw / 2
        f_hi = fc + bw / 2
        col_lo = int(round((f_lo - f_min) / total_bw * output_fft))
        col_hi = int(round((f_hi - f_min) / total_bw * output_fft))
        col_lo = max(0, min(col_lo, output_fft - 1))
        col_hi = max(col_lo + 1, min(col_hi, output_fft))
        n_cols = col_hi - col_lo

        # Resample frequency axis to n_cols output bins
        x_src = np.linspace(0, fft_seg - 1, n_cols)
        xi = np.arange(fft_seg)
        resampled = np.array(
            [np.interp(x_src, xi, spec_lin[t]) for t in range(n_time)],
            dtype=np.float64,
        )
        resampled_segs.append(
            {
                "col_lo": col_lo,
                "col_hi": col_hi,
                "resampled": resampled,  # (n_time, n_cols) linear power
                "f_lo": f_lo,
                "f_hi": f_hi,
            }
        )

    # ── Accumulate with overlap handling ──────────────────────────────────────
    for idx, seg_r in enumerate(resampled_segs):
        col_lo = seg_r["col_lo"]
        col_hi = seg_r["col_hi"]
        n_cols = col_hi - col_lo
        data = seg_r["resampled"]  # (n_time, n_cols)

        # Base weight array for this segment: shape (n_cols,), all ones
        w = np.ones(n_cols, dtype=np.float64)

        if overlap_mode in ("crossfade", "average", "left", "right", "strongest"):
            # Check overlap with previously placed segments (those already in acc)
            for prev in resampled_segs[:idx]:
                ovl_lo = max(col_lo, prev["col_lo"])
                ovl_hi = min(col_hi, prev["col_hi"])
                if ovl_lo >= ovl_hi:
                    continue  # no overlap with this predecessor

                # Local indices within the current segment's column range
                local_lo = ovl_lo - col_lo
                local_hi = ovl_hi - col_lo
                n_ovl = local_hi - local_lo

                if overlap_mode == "crossfade":
                    # Current segment (right): weight ramps 0→1 across overlap
                    # The prev segment's weight was already applied as 1→0 when
                    # it was inserted; we match that taper here.
                    ramp_cur = np.linspace(0.0, 1.0, n_ovl)
                    w[local_lo:local_hi] = ramp_cur

                    # Retroactively taper the accumulated weight for the prev seg
                    prev_local_lo = ovl_lo - prev["col_lo"]
                    prev_local_hi = ovl_hi - prev["col_lo"]
                    ramp_prev = np.linspace(1.0, 0.0, n_ovl)
                    # weight_acc already has prev contribution; we need to rescale it
                    # from the original w=1 to the tapered value.
                    # Since accumulator[col] = prev_data * 1.0, we multiply by ramp:
                    accumulator[:, ovl_lo:ovl_hi] *= ramp_prev
                    weight_acc[:, ovl_lo:ovl_hi] *= ramp_prev

                elif overlap_mode == "average":
                    # Both segments contribute weight=0.5 in the overlap.
                    # Prev was inserted with w=1; rescale to 0.5.
                    accumulator[:, ovl_lo:ovl_hi] *= 0.5
                    weight_acc[:, ovl_lo:ovl_hi] *= 0.5
                    w[local_lo:local_hi] = 0.5

                elif overlap_mode == "left":
                    # Prev (left) segment wins — zero-weight current in overlap
                    w[local_lo:local_hi] = 0.0

                elif overlap_mode == "right":
                    # Current (right) segment wins — erase prev contribution
                    accumulator[:, ovl_lo:ovl_hi] = 0.0
                    weight_acc[:, ovl_lo:ovl_hi] = 0.0

                elif overlap_mode == "strongest":
                    # Per-time-row: keep whichever has higher mean power in the zone
                    # We do this lazily: insert current with w=1, then at the end
                    # we'll compare and zero out the loser row-by-row.
                    # Mark the overlap zone with a sentinel for post-processing.
                    # (handled below after the accumulation loop)
                    pass

        accumulator[:, col_lo:col_hi] += data * w
        weight_acc[:, col_lo:col_hi] += w

    # ── "strongest" post-processing ───────────────────────────────────────────
    if overlap_mode == "strongest":
        # Re-do without blending; pick winner per row per overlap zone
        accumulator[:] = 0.0
        weight_acc[:] = 0.0

        for idx, seg_r in enumerate(resampled_segs):
            col_lo = seg_r["col_lo"]
            col_hi = seg_r["col_hi"]
            data = seg_r["resampled"]
            w = np.ones(data.shape, dtype=np.float64)

            for prev_idx, prev in enumerate(resampled_segs[:idx]):
                ovl_lo = max(col_lo, prev["col_lo"])
                ovl_hi = min(col_hi, prev["col_hi"])
                if ovl_lo >= ovl_hi:
                    continue
                local_lo_cur = ovl_lo - col_lo
                local_hi_cur = ovl_hi - col_lo
                local_lo_prev = ovl_lo - prev["col_lo"]
                local_hi_prev = ovl_hi - prev["col_lo"]

                cur_power = data[:, local_lo_cur:local_hi_cur].mean(axis=1)
                prev_power = prev["resampled"][:, local_lo_prev:local_hi_prev].mean(
                    axis=1
                )

                # Where prev is stronger, zero out current in overlap
                prev_wins = prev_power >= cur_power  # (n_time,) bool
                w[prev_wins, local_lo_cur:local_hi_cur] = 0.0

                # Where current is stronger, zero out prev contribution
                cur_wins = ~prev_wins
                accumulator[cur_wins, ovl_lo:ovl_hi] = 0.0
                weight_acc[cur_wins, ovl_lo:ovl_hi] = 0.0

            accumulator[:, col_lo:col_hi] += data * w
            weight_acc[:, col_lo:col_hi] += w

    # ── Normalise and convert back to dB ─────────────────────────────────────
    with np.errstate(divide="ignore", invalid="ignore"):
        linear = np.where(weight_acc > 0, accumulator / weight_acc, np.nan)

    stitched = np.where(
        np.isfinite(linear) & (linear > 0),
        10.0 * np.log10(linear),
        np.nan,
    ).astype(np.float32)

    return stitched, f_min, f_max


# ─────────────────────────────────────────────────────────────────────────────
# Plotting
# ─────────────────────────────────────────────────────────────────────────────


def _fmt_hz(hz: float) -> str:
    if abs(hz) >= 1e9:
        return f"{hz/1e9:.3f} GHz"
    if abs(hz) >= 1e6:
        return f"{hz/1e6:.3f} MHz"
    if abs(hz) >= 1e3:
        return f"{hz/1e3:.3f} kHz"
    return f"{hz:.0f} Hz"


def plot_waterfall(
    stitched: np.ndarray,
    f_min: float,
    f_max: float,
    segments: List[dict],
    cmap: str = "inferno",
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    output: Optional[str] = None,
    sample_rate_hint: Optional[float] = None,
):
    if not HAS_MPL:
        print("[ERROR] matplotlib is not installed. Run:  pip install matplotlib")
        sys.exit(1)

    valid = stitched[np.isfinite(stitched)]
    if vmin is None:
        vmin = float(np.percentile(valid, 2))
    if vmax is None:
        vmax = float(np.percentile(valid, 98))

    n_time, n_freq = stitched.shape
    total_bw = f_max - f_min

    fig, ax = plt.subplots(figsize=(16, 8), facecolor="#0d0d0d")
    ax.set_facecolor("#0d0d0d")

    im = ax.imshow(
        stitched,
        aspect="auto",
        origin="upper",
        extent=[f_min / 1e6, f_max / 1e6, n_time, 0],
        cmap=cmap,
        norm=Normalize(vmin=vmin, vmax=vmax),
        interpolation="nearest",
    )

    # Segment boundary markers
    for seg in segments:
        lo = (seg["center_hz"] - seg["bw_hz"] / 2) / 1e6
        hi = (seg["center_hz"] + seg["bw_hz"] / 2) / 1e6
        ax.axvline(lo, color="#444", linewidth=0.5, linestyle="--", alpha=0.6)
        ax.axvline(hi, color="#444", linewidth=0.5, linestyle="--", alpha=0.6)
        ax.axvline(
            seg["center_hz"] / 1e6,
            color="#666",
            linewidth=0.4,
            linestyle=":",
            alpha=0.4,
        )

    # Colourbar
    cbar = fig.colorbar(im, ax=ax, pad=0.01, fraction=0.015)
    cbar.set_label("Power (dBFS)", color="#ccc", fontsize=9)
    cbar.ax.yaxis.set_tick_params(color="#ccc")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#ccc")

    # Labels
    ax.set_xlabel("Frequency (MHz)", color="#ccc", fontsize=10)
    ax.set_ylabel("Time (frames)", color="#ccc", fontsize=10)
    ax.tick_params(colors="#aaa", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")

    title = (
        f"Stitched Wideband Waterfall  "
        f"[{_fmt_hz(f_min)} – {_fmt_hz(f_max)}  |  BW {_fmt_hz(total_bw)}  "
        f"|  {len(segments)} segment(s)]"
    )
    ax.set_title(title, color="#eee", fontsize=11, pad=10)

    plt.tight_layout()

    if output:
        fig.savefig(output, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"[✓] Waterfall saved to: {output}")
    else:
        plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--files",
        nargs="+",
        required=True,
        metavar="FILE",
        help="IQ files to stitch (glob-expanded by your shell)",
    )
    p.add_argument(
        "--freqs",
        nargs="+",
        type=float,
        metavar="HZ",
        help="Centre frequency per file (Hz). Overrides auto-parse.",
    )
    p.add_argument(
        "--bw",
        nargs="+",
        type=float,
        metavar="HZ",
        help="Bandwidth (= sample rate) per file (Hz). Overrides auto-parse.",
    )
    p.add_argument(
        "--dtype",
        default="float32",
        choices=["float32", "int16", "uint8", "cf32", "ci16", "cu8"],
        help="IQ sample format (default: float32)",
    )
    p.add_argument(
        "--auto-parse",
        action="store_true",
        help="Try to parse frequency/bandwidth from filenames",
    )
    p.add_argument(
        "--fft", type=int, default=1024, help="FFT size per segment (default: 1024)"
    )
    p.add_argument(
        "--output-fft",
        type=int,
        default=0,
        help="Output frequency resolution (default: same as --fft)",
    )
    p.add_argument(
        "--overlap",
        type=float,
        default=0.5,
        help="Overlap fraction between FFT frames (default: 0.5)",
    )
    p.add_argument(
        "--cmap", default="inferno", help="Matplotlib colourmap (default: inferno)"
    )
    p.add_argument(
        "--vmin",
        type=float,
        default=None,
        help="Colour scale minimum dB (auto if omitted)",
    )
    p.add_argument(
        "--vmax",
        type=float,
        default=None,
        help="Colour scale maximum dB (auto if omitted)",
    )
    p.add_argument(
        "--output",
        default=None,
        metavar="PNG",
        help="Save waterfall to PNG instead of displaying it",
    )
    p.add_argument(
        "--overlap-mode",
        default="crossfade",
        choices=list(OVERLAP_MODES),
        help=(
            "How to handle frequency overlap between adjacent segments "
            "(default: crossfade). "
            "crossfade=linear taper, average=equal blend, "
            "left=keep lower-fc segment, right=keep higher-fc segment, "
            "strongest=keep higher-power segment per time row."
        ),
    )
    p.add_argument(
        "--sort",
        action="store_true",
        help="Sort segments by centre frequency before stitching",
    )
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    files = args.files
    n = len(files)

    # ── Resolve frequencies ──────────────────────────────────────────────────
    freqs = [None] * n
    bws = [None] * n

    if args.freqs:
        if len(args.freqs) != n:
            parser.error(f"--freqs needs {n} values, got {len(args.freqs)}")
        freqs = args.freqs
    if args.bw:
        if len(args.bw) != n:
            parser.error(f"--bw needs {n} values, got {len(args.bw)}")
        bws = args.bw

    for i, f in enumerate(files):
        # SigMF auto-meta
        if Path(f).suffix == ".sigmf-meta":
            fc, bw = sigmf_center_bw(Path(f))
            if freqs[i] is None:
                freqs[i] = fc
            if bws[i] is None:
                bws[i] = bw
            continue
        if args.auto_parse and (freqs[i] is None or bws[i] is None):
            fc, bw = parse_freq_bw_from_name(f)
            if freqs[i] is None:
                freqs[i] = fc
            if bws[i] is None:
                bws[i] = bw

    # Check we have all values
    missing = [files[i] for i in range(n) if freqs[i] is None or bws[i] is None]
    if missing:
        print("[ERROR] Could not determine frequency/bandwidth for:")
        for m in missing:
            print(f"   {m}")
        print("Use --freqs / --bw or --auto-parse, or use SigMF files.")
        sys.exit(1)

    # ── Load & compute spectrograms ──────────────────────────────────────────
    segments = []
    for i, f in enumerate(files):
        print(
            f"[{i+1}/{n}] Loading {Path(f).name} "
            f"  fc={_fmt_hz(freqs[i])}  bw={_fmt_hz(bws[i])}"
        )
        iq = load_iq(f, args.dtype)
        spec = compute_spectrogram(iq, fft_size=args.fft, overlap=args.overlap)
        segments.append(
            {"center_hz": freqs[i], "bw_hz": bws[i], "spec": spec, "file": f}
        )
        print(f"         → {len(iq)} samples, {spec.shape[0]} time frames")

    if args.sort:
        segments.sort(key=lambda s: s["center_hz"])

    # ── Stitch ───────────────────────────────────────────────────────────────
    out_fft = args.output_fft if args.output_fft > 0 else args.fft
    print(
        f"\n[~] Stitching {n} segments → {out_fft} freq bins  "
        f"(overlap mode: {args.overlap_mode}) …"
    )
    stitched, f_min, f_max = stitch_spectrograms(
        segments, output_fft=out_fft, overlap_mode=args.overlap_mode
    )
    print(
        f"[✓] Stitched shape: {stitched.shape}  "
        f"({_fmt_hz(f_min)} – {_fmt_hz(f_max)})"
    )

    # ── Plot ─────────────────────────────────────────────────────────────────
    plot_waterfall(
        stitched,
        f_min,
        f_max,
        segments,
        cmap=args.cmap,
        vmin=args.vmin,
        vmax=args.vmax,
        output=args.output,
    )


if __name__ == "__main__":
    main()
