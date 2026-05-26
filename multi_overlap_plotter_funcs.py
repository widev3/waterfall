#!/usr/bin/env python3
"""
IQ Waterfall Stitcher
=====================
Stitches multiple SDR IQ files into a single wideband waterfall display.

Supported IQ file formats:
  - Raw interleaved float32 (default)
  - Raw interleaved int16  (--dtype int16)
  - Raw interleaved uint8 / RTL-SDR  (--dtype uint8)
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

# Choose an overlap mode:
python iq_waterfall.py --files *.iq --auto-parse --overlap-mode median

# Full option reference:
python iq_waterfall.py --help
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

# ── optional deps ─────────────────────────────────────────────────────────────
try:
    import matplotlib

    # matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize

    HAS_MPL = True
except ImportError:
    HAS_MPL = False

try:
    from scipy.ndimage import zoom as scipy_zoom

    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ─────────────────────────────────────────────────────────────────────────────
# IQ loading
# ─────────────────────────────────────────────────────────────────────────────


def load_iq(path: str, dtype: str = "float32") -> np.ndarray:
    """Load an IQ file and return a complex64 numpy array."""
    path = Path(path)
    if path.suffix == ".sigmf-meta":
        return _load_sigmf(path)
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
    re.compile(
        r"(\d+(?:\.\d+)?)\s*([kmg]?)hz[_\-](\d+(?:\.\d+)?)\s*([kmg]?)hz", re.IGNORECASE
    ),
    re.compile(r"(\d{6,})_(\d{4,})(?:\D|$)"),
]
_MULT = {"": 1, "k": 1e3, "K": 1e3, "m": 1e6, "M": 1e6, "g": 1e9, "G": 1e9}


def parse_freq_bw_from_name(filename: str) -> Tuple[Optional[float], Optional[float]]:
    name = Path(filename).name
    m = _PATTERNS[0].search(name)
    if m:
        return (
            float(m.group(1)) * _MULT.get(m.group(2), 1),
            float(m.group(3)) * _MULT.get(m.group(4), 1),
        )
    m = _PATTERNS[1].search(name)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None


# ─────────────────────────────────────────────────────────────────────────────
# Spectrogram
# ─────────────────────────────────────────────────────────────────────────────


def compute_spectrogram(
    iq: np.ndarray, fft_size: int = 1024, overlap: float = 0.5
) -> np.ndarray:
    """Return 2-D power spectrogram (dB), shape (n_time, fft_size)."""
    step = max(1, int(fft_size * (1.0 - overlap)))
    n_frames = (len(iq) - fft_size) // step + 1
    if n_frames <= 0:
        iq = np.pad(iq, (0, fft_size - len(iq)))
        n_frames = 1
    window = np.hanning(fft_size).astype(np.float32)
    spec = np.zeros((n_frames, fft_size), dtype=np.float32)
    for i in range(n_frames):
        frame = iq[i * step : i * step + fft_size] * window
        spec[i] = np.abs(np.fft.fftshift(np.fft.fft(frame, n=fft_size))) ** 2
    return 10.0 * np.log10(np.maximum(spec, 1e-20))


# ─────────────────────────────────────────────────────────────────────────────
# Overlap-mode helpers
# ─────────────────────────────────────────────────────────────────────────────


def _time_resample(arr: np.ndarray, n_time: int) -> np.ndarray:
    """Resample rows of a 2-D array to n_time using scipy or numpy fallback."""
    if arr.shape[0] == n_time:
        return arr
    if HAS_SCIPY:
        return scipy_zoom(arr, (n_time / arr.shape[0], 1), order=1)
    # numpy fallback: nearest-neighbour row selection
    idx = np.round(np.linspace(0, arr.shape[0] - 1, n_time)).astype(int)
    return arr[idx]


def _to_linear(spec_db: np.ndarray) -> np.ndarray:
    return np.power(10.0, spec_db / 10.0).astype(np.float64)


def _freq_resample(lin: np.ndarray, n_cols: int) -> np.ndarray:
    """Resample frequency axis (columns) of a linear-power array to n_cols."""
    if lin.shape[1] == n_cols:
        return lin
    x_src = np.linspace(0, lin.shape[1] - 1, n_cols)
    xi = np.arange(lin.shape[1])
    return np.array(
        [np.interp(x_src, xi, lin[t]) for t in range(lin.shape[0])], dtype=np.float64
    )


def _estimate_noise_floor(lin: np.ndarray) -> np.ndarray:
    """
    Estimate per-column noise floor as the median across time rows.
    Returns shape (n_cols,).
    """
    return np.median(lin, axis=0)


def _snr_weights(lin: np.ndarray) -> np.ndarray:
    """
    Per-bin SNR weight: mean_power / noise_floor, clipped to [epsilon, inf].
    Shape (n_time, n_cols).  Each column's noise floor is the per-column median.
    """
    noise = _estimate_noise_floor(lin)  # (n_cols,)
    noise = np.maximum(noise, 1e-30)
    snr = lin / noise  # broadcast
    return np.maximum(snr, 1e-6)


def _variance_weights(lin: np.ndarray) -> np.ndarray:
    """
    Inverse-variance weight: 1 / temporal_variance per bin.
    Low-variance (stable) bins get higher weight.
    Shape (n_time, n_cols).
    """
    var = np.var(lin, axis=0, keepdims=True)  # (1, n_cols)
    var = np.maximum(var, 1e-30)
    return np.broadcast_to(1.0 / var, lin.shape).copy()


def _gaussian_taper(n_cols: int, sigma_frac: float = 0.4) -> np.ndarray:
    """
    Gaussian weight centred on the segment, decaying toward the band edges.
    sigma_frac controls the width: 0.4 means 1-sigma at 40% from centre.
    Returns shape (n_cols,).
    """
    x = np.linspace(-1.0, 1.0, n_cols)
    return np.exp(-0.5 * (x / sigma_frac) ** 2)


def _raised_cosine_taper(n_ovl: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Raised-cosine (Hann) cross-fade taper for an overlap zone of n_ovl bins.
    Returns (taper_right, taper_left) each shape (n_ovl,).
    """
    t = np.linspace(0.0, 1.0, n_ovl)
    taper_right = 0.5 * (1.0 - np.cos(np.pi * t))  # 0 → 1
    taper_left = 1.0 - taper_right  # 1 → 0
    return taper_right, taper_left


# ─────────────────────────────────────────────────────────────────────────────
# Overlap modes catalogue
# ─────────────────────────────────────────────────────────────────────────────

OVERLAP_MODES = (
    # ── Averaging family ──────────────────────────────────────────────────────
    "average",  # arithmetic mean in linear power (default)
    "median",  # median in linear power — rejects RFI / spurs
    "trimmed_mean",  # mean after discarding top+bottom 10 % outliers
    "geometric_mean",  # mean in log-power (dB) — de-emphasises spurs
    "min_power",  # minimum power per bin — noise-floor mapping
    "max_power",  # maximum power per bin — catches intermittent signals
    # ── Weighted family ──────────────────────────────────────────────────────
    "snr_weighted",  # weight by local SNR (signal / noise-floor estimate)
    "variance_weighted",  # weight inversely by temporal variance (stable wins)
    # ── Taper / fade family ──────────────────────────────────────────────────
    "crossfade",  # linear cross-fade taper at band edges
    "raised_cosine",  # Hann-window cross-fade (no slope discontinuity)
    "gaussian_taper",  # Gaussian weight centred on each segment
    # ── Priority family ──────────────────────────────────────────────────────
    "left",  # keep lower-fc segment in overlap
    "right",  # keep higher-fc segment in overlap
    "strongest",  # keep higher mean-power segment, per time row
)

OVERLAP_HELP = {
    "average": "arithmetic mean in linear power across all overlapping segments (default)",
    "median": "median in linear power — robust against RFI spurs and transient interference",
    "trimmed_mean": "mean after discarding the top and bottom 10 % power outliers per bin",
    "geometric_mean": "mean in log (dB) domain — equivalent to geometric mean of power",
    "min_power": "keep the minimum power per bin — useful for noise-floor mapping",
    "max_power": "keep the maximum power per bin — catches weak intermittent signals",
    "snr_weighted": "weight each segment by its local SNR (signal / noise-floor estimate)",
    "variance_weighted": "weight inversely by temporal variance — stable/quiet receiver wins",
    "crossfade": "linear cross-fade taper across the overlap band edge",
    "raised_cosine": "Hann-window cross-fade — smooth taper with no slope discontinuity",
    "gaussian_taper": "Gaussian weight centred on each segment's centre frequency",
    "left": "keep only the lower-fc segment in the overlap region",
    "right": "keep only the higher-fc segment in the overlap region",
    "strongest": "keep the segment with higher mean power, resolved per time row",
}


# ─────────────────────────────────────────────────────────────────────────────
# Core stitching engine
# ─────────────────────────────────────────────────────────────────────────────


def _map_segments(
    segments: List[dict], f_min: float, total_bw: float, output_fft: int, n_time: int
) -> List[dict]:
    """
    Resample every segment onto the global grid and convert to linear power.
    Returns list of dicts: col_lo, col_hi, data (n_time, n_cols) float64 linear.
    """
    mapped = []
    for seg in sorted(segments, key=lambda s: s["center_hz"]):
        fc = seg["center_hz"]
        bw = seg["bw_hz"]
        f_lo = fc - bw / 2
        f_hi = fc + bw / 2

        col_lo = int(round((f_lo - f_min) / total_bw * output_fft))
        col_hi = int(round((f_hi - f_min) / total_bw * output_fft))
        col_lo = max(0, min(col_lo, output_fft - 1))
        col_hi = max(col_lo + 1, min(col_hi, output_fft))
        n_cols = col_hi - col_lo

        spec_db = _time_resample(seg["spec"], n_time)
        spec_lin = _to_linear(spec_db)
        spec_lin = _freq_resample(spec_lin, n_cols)

        mapped.append(
            {
                "col_lo": col_lo,
                "col_hi": col_hi,
                "data": spec_lin,  # (n_time, n_cols) linear power
                "center_hz": fc,
            }
        )
    return mapped


def stitch_spectrograms(
    segments: List[dict],
    output_fft: int = 1024,
    overlap_mode: str = "average",
    trimmed_mean_pct: float = 10.0,
    gaussian_sigma: float = 0.4,
) -> Tuple[np.ndarray, float, float]:
    """
    Stitch per-segment spectrograms onto a common frequency grid.

    Parameters
    ----------
    segments          : list of dicts {center_hz, bw_hz, spec (dB ndarray)}
    output_fft        : output frequency resolution in bins
    overlap_mode      : one of OVERLAP_MODES (see OVERLAP_HELP for descriptions)
    trimmed_mean_pct  : percentage to trim from each tail for 'trimmed_mean'
    gaussian_sigma    : sigma fraction (0–1) for 'gaussian_taper'

    Returns
    -------
    stitched  : (n_time, output_fft) float32 dB, NaN where no data
    f_min_hz, f_max_hz : float
    """
    if overlap_mode not in OVERLAP_MODES:
        raise ValueError(
            f"overlap_mode must be one of {OVERLAP_MODES}, " f"got {overlap_mode!r}"
        )

    f_min = min(s["center_hz"] - s["bw_hz"] / 2 for s in segments)
    f_max = max(s["center_hz"] + s["bw_hz"] / 2 for s in segments)
    total_bw = f_max - f_min
    n_time = max(s["spec"].shape[0] for s in segments)

    mapped = _map_segments(segments, f_min, total_bw, output_fft, n_time)

    # ── Modes that need the full stack of overlapping layers ─────────────────
    # For median / trimmed_mean / min_power / max_power we collect all
    # contributing layers into a 3-D stack first, then collapse.
    if overlap_mode in (
        "median",
        "trimmed_mean",
        "min_power",
        "max_power",
        "geometric_mean",
    ):
        return _stitch_stack(
            mapped, output_fft, n_time, f_min, f_max, overlap_mode, trimmed_mean_pct
        )

    # ── All other modes use the weighted accumulator ──────────────────────────
    return _stitch_accumulator(
        mapped, output_fft, n_time, f_min, f_max, overlap_mode, gaussian_sigma
    )


# ── Stack-based collapse (median / trimmed_mean / min / max / geometric) ─────


def _stitch_stack(mapped, output_fft, n_time, f_min, f_max, mode, trimmed_mean_pct):
    """
    Build a per-bin list of contributing linear-power values, then collapse
    with the chosen statistical operator.
    """
    # We'll store: for each output column, a list of (n_time,) arrays
    col_layers: List[List[np.ndarray]] = [[] for _ in range(output_fft)]

    for seg_m in mapped:
        col_lo = seg_m["col_lo"]
        col_hi = seg_m["col_hi"]
        data = seg_m["data"]  # (n_time, n_cols)
        for c_out, c_loc in enumerate(range(col_lo, col_hi)):
            col_layers[c_out + col_lo - col_lo].append(data[:, c_out])
        # fix: index correctly
        for local_c in range(col_hi - col_lo):
            col_layers[col_lo + local_c].append(data[:, local_c])

    # Build result
    result_lin = np.full((n_time, output_fft), np.nan, dtype=np.float64)

    for c in range(output_fft):
        layers = col_layers[c]
        if not layers:
            continue
        stack = np.stack(layers, axis=0)  # (n_layers, n_time)

        if mode == "min_power":
            result_lin[:, c] = stack.min(axis=0)

        elif mode == "max_power":
            result_lin[:, c] = stack.max(axis=0)

        elif mode == "median":
            result_lin[:, c] = np.median(stack, axis=0)

        elif mode == "geometric_mean":
            # Mean in log domain = geometric mean of power
            log_stack = np.log10(np.maximum(stack, 1e-30))
            result_lin[:, c] = np.power(10.0, log_stack.mean(axis=0))

        elif mode == "trimmed_mean":
            if stack.shape[0] < 3:
                # Not enough layers to trim — fall back to mean
                result_lin[:, c] = stack.mean(axis=0)
            else:
                k = max(1, int(round(stack.shape[0] * trimmed_mean_pct / 100.0)))
                sorted_s = np.sort(stack, axis=0)
                trimmed = sorted_s[k:-k]  # drop k from top and bottom
                result_lin[:, c] = trimmed.mean(axis=0)

    # Convert back to dB
    stitched = np.where(
        np.isfinite(result_lin) & (result_lin > 0),
        10.0 * np.log10(result_lin),
        np.nan,
    ).astype(np.float32)
    return stitched, f_min, f_max


# ── Accumulator-based blending ────────────────────────────────────────────────


def _stitch_accumulator(mapped, output_fft, n_time, f_min, f_max, mode, gaussian_sigma):
    """
    Weighted accumulator: acc / wgt after all segments are added.
    Handles: average, snr_weighted, variance_weighted, crossfade,
             raised_cosine, gaussian_taper, left, right, strongest.
    """
    acc = np.zeros((n_time, output_fft), dtype=np.float64)
    wgt = np.zeros((n_time, output_fft), dtype=np.float64)

    for idx, seg_m in enumerate(mapped):
        col_lo = seg_m["col_lo"]
        col_hi = seg_m["col_hi"]
        n_cols = col_hi - col_lo
        data = seg_m["data"]  # (n_time, n_cols) linear

        # ── Per-segment base weight ───────────────────────────────────────────
        if mode == "snr_weighted":
            w = _snr_weights(data)  # (n_time, n_cols)

        elif mode == "variance_weighted":
            w = _variance_weights(data)  # (n_time, n_cols)

        elif mode == "gaussian_taper":
            w = _gaussian_taper(n_cols, sigma_frac=gaussian_sigma)  # (n_cols,)
            # broadcast to 2-D immediately so overlap logic works uniformly
            w = np.tile(w, (n_time, 1))  # (n_time, n_cols)

        else:
            w = np.ones((n_time, n_cols), dtype=np.float64)

        # ── Overlap zone adjustments with previously placed segments ──────────
        for prev_m in mapped[:idx]:
            ovl_lo = max(col_lo, prev_m["col_lo"])
            ovl_hi = min(col_hi, prev_m["col_hi"])
            if ovl_lo >= ovl_hi:
                continue

            loc_lo = ovl_lo - col_lo
            loc_hi = ovl_hi - col_lo
            n_ovl = loc_hi - loc_lo

            if mode == "average":
                pass  # weight=1 everywhere; accumulator normalises

            elif mode in ("snr_weighted", "variance_weighted", "gaussian_taper"):
                pass  # weights already encode quality; no special overlap logic

            elif mode == "crossfade":
                ramp_r = np.linspace(0.0, 1.0, n_ovl)
                ramp_l = 1.0 - ramp_r
                w[:, loc_lo:loc_hi] *= ramp_r
                acc[:, ovl_lo:ovl_hi] *= ramp_l
                wgt[:, ovl_lo:ovl_hi] *= ramp_l

            elif mode == "raised_cosine":
                ramp_r, ramp_l = _raised_cosine_taper(n_ovl)
                w[:, loc_lo:loc_hi] *= ramp_r
                acc[:, ovl_lo:ovl_hi] *= ramp_l
                wgt[:, ovl_lo:ovl_hi] *= ramp_l

            elif mode == "left":
                w[:, loc_lo:loc_hi] = 0.0

            elif mode == "right":
                acc[:, ovl_lo:ovl_hi] = 0.0
                wgt[:, ovl_lo:ovl_hi] = 0.0

            elif mode == "strongest":
                loc_lo_p = ovl_lo - prev_m["col_lo"]
                loc_hi_p = ovl_hi - prev_m["col_lo"]
                cur_pwr = data[:, loc_lo:loc_hi].mean(axis=1)
                prv_pwr = prev_m["data"][:, loc_lo_p:loc_hi_p].mean(axis=1)
                prev_wins = prv_pwr >= cur_pwr
                cur_wins = ~prev_wins
                w[prev_wins, loc_lo:loc_hi] = 0.0
                acc[cur_wins, ovl_lo:ovl_hi] = 0.0
                wgt[cur_wins, ovl_lo:ovl_hi] = 0.0

        acc[:, col_lo:col_hi] += data * w
        wgt[:, col_lo:col_hi] += w

    # ── Detect overlap and report ─────────────────────────────────────────────
    max_layers = int(np.round(wgt.max()))
    if max_layers > 1:
        multi = int((wgt.max(axis=0) > 1.001).sum())
        print(
            f"[i] Overlap: {multi} freq bin(s) covered by multiple segments "
            f"(up to {max_layers} layers) — mode: {mode}"
        )

    with np.errstate(divide="ignore", invalid="ignore"):
        linear = np.where(wgt > 0, acc / wgt, np.nan)

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
    stitched,
    f_min,
    f_max,
    segments,
    cmap="inferno",
    vmin=None,
    vmax=None,
    output=None,
    overlap_mode="average",
):
    if not HAS_MPL:
        print("[ERROR] matplotlib not installed.  Run: pip install matplotlib")
        sys.exit(1)

    valid = stitched[np.isfinite(stitched)]
    if vmin is None:
        vmin = float(np.percentile(valid, 2))
    if vmax is None:
        vmax = float(np.percentile(valid, 98))

    n_time, _ = stitched.shape
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

    # for seg in segments:
    #     lo = (seg["center_hz"] - seg["bw_hz"] / 2) / 1e6
    #     hi = (seg["center_hz"] + seg["bw_hz"] / 2) / 1e6
    #     ax.axvline(lo, color="#444", lw=0.5, ls="--", alpha=0.6)
    #     ax.axvline(hi, color="#444", lw=0.5, ls="--", alpha=0.6)
    #     ax.axvline(seg["center_hz"] / 1e6, color="#666", lw=0.4, ls=":", alpha=0.4)

    cbar = fig.colorbar(im, ax=ax, pad=0.01, fraction=0.015)
    cbar.set_label("Power (dBFS)", color="#ccc", fontsize=9)
    cbar.ax.yaxis.set_tick_params(color="#ccc")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#ccc")

    ax.set_xlabel("Frequency (MHz)", color="#ccc", fontsize=10)
    ax.set_ylabel("Time (frames)", color="#ccc", fontsize=10)
    ax.tick_params(colors="#aaa", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")

    title = (
        f"Stitched Wideband Waterfall  "
        f"[{_fmt_hz(f_min)} – {_fmt_hz(f_max)}  |  BW {_fmt_hz(total_bw)}  "
        f"|  {len(segments)} seg  |  mode: {overlap_mode}]"
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
    mode_list = "\n".join(f"  {m:<18} {OVERLAP_HELP[m]}" for m in OVERLAP_MODES)
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Overlap modes:\n{mode_list}",
    )
    p.add_argument("--files", nargs="+", required=True, metavar="FILE")
    p.add_argument(
        "--freqs",
        nargs="+",
        type=float,
        metavar="HZ",
        help="Centre frequency per file (Hz)",
    )
    p.add_argument(
        "--bw",
        nargs="+",
        type=float,
        metavar="HZ",
        help="Bandwidth / sample-rate per file (Hz)",
    )
    p.add_argument(
        "--dtype",
        default="float32",
        choices=["float32", "int16", "uint8", "cf32", "ci16", "cu8"],
    )
    p.add_argument(
        "--auto-parse", action="store_true", help="Parse frequency/BW from filenames"
    )
    p.add_argument("--fft", type=int, default=1024)
    p.add_argument(
        "--output-fft",
        type=int,
        default=0,
        help="Output freq resolution (default: same as --fft)",
    )
    p.add_argument(
        "--overlap",
        type=float,
        default=0.5,
        help="FFT frame overlap fraction (default: 0.5)",
    )
    p.add_argument(
        "--overlap-mode",
        default="average",
        choices=list(OVERLAP_MODES),
        help="How to blend overlapping frequency bands (default: average)",
    )
    p.add_argument(
        "--trimmed-mean-pct",
        type=float,
        default=10.0,
        help="Percentage to trim from each tail for trimmed_mean (default: 10)",
    )
    p.add_argument(
        "--gaussian-sigma",
        type=float,
        default=0.4,
        help="Sigma fraction for gaussian_taper (default: 0.4)",
    )
    p.add_argument("--cmap", default="inferno")
    p.add_argument("--vmin", type=float, default=None)
    p.add_argument("--vmax", type=float, default=None)
    p.add_argument(
        "--output",
        default=None,
        metavar="PNG",
        help="Save to PNG instead of displaying",
    )
    p.add_argument(
        "--sort", action="store_true", help="Sort segments by centre frequency"
    )
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    files = args.files
    n = len(files)
    freqs = [None] * n
    bws = [None] * n

    if args.freqs:
        if len(args.freqs) != n:
            parser.error(f"--freqs needs {n} values, got {len(args.freqs)}")
        freqs = list(args.freqs)
    if args.bw:
        if len(args.bw) != n:
            parser.error(f"--bw needs {n} values, got {len(args.bw)}")
        bws = list(args.bw)

    for i, f in enumerate(files):
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

    missing = [files[i] for i in range(n) if freqs[i] is None or bws[i] is None]
    if missing:
        print("[ERROR] Could not determine frequency/bandwidth for:")
        for m in missing:
            print(f"   {m}")
        print("Use --freqs / --bw, --auto-parse, or SigMF files.")
        sys.exit(1)

    segments = []
    for i, f in enumerate(files):
        print(
            f"[{i+1}/{n}] Loading {Path(f).name}"
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

    out_fft = args.output_fft if args.output_fft > 0 else args.fft
    print(
        f"\n[~] Stitching {n} segments → {out_fft} bins  "
        f"[mode: {args.overlap_mode}] …"
    )

    stitched, f_min, f_max = stitch_spectrograms(
        segments,
        output_fft=out_fft,
        overlap_mode=args.overlap_mode,
        trimmed_mean_pct=args.trimmed_mean_pct,
        gaussian_sigma=args.gaussian_sigma,
    )
    print(f"[✓] Stitched: {stitched.shape}  " f"({_fmt_hz(f_min)} – {_fmt_hz(f_max)})")

    plot_waterfall(
        stitched,
        f_min,
        f_max,
        segments,
        cmap=args.cmap,
        vmin=args.vmin,
        vmax=args.vmax,
        output=args.output,
        overlap_mode=args.overlap_mode,
    )


if __name__ == "__main__":
    main()
