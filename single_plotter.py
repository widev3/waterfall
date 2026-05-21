#!/usr/bin/env python3
"""
IQ Waterfall Plot
-----------------
Plots a frequency vs. time waterfall (spectrogram) from an IQ recording.

Supports:
  - Raw binary: interleaved float32, int16, int8, or uint8 samples
  - SigMF (.sigmf-data / .sigmf-meta)

Usage:
  python iq_waterfall.py <iq_file> [options]

Examples:
  python iq_waterfall.py capture.iq
  python iq_waterfall.py capture.iq --dtype float32 --sample-rate 2e6 --center-freq 915e6
  python iq_waterfall.py capture.sigmf-data --sigmf capture.sigmf-meta
  python iq_waterfall.py capture.iq --dtype int16 --fft-size 1024 --colormap inferno
"""

import argparse
import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── helpers ──────────────────────────────────────────────────────────────────

DTYPE_MAP = {
    "float32": np.float32,
    "float64": np.float64,
    "int16": np.int16,
    "int8": np.int8,
    "uint8": np.uint8,
}


def load_raw(path: str, dtype_str: str) -> np.ndarray:
    """Load interleaved I/Q samples from a raw binary file."""
    dtype = DTYPE_MAP[dtype_str]
    raw = np.fromfile(path, dtype=dtype)
    if raw.size % 2 != 0:
        raw = raw[:-1]  # drop trailing odd sample

    # Normalise integer types to float32 [-1, 1]
    if dtype in (np.int16,):
        raw = raw.astype(np.float32) / 32768.0
    elif dtype == np.int8:
        raw = raw.astype(np.float32) / 128.0
    elif dtype == np.uint8:
        raw = (raw.astype(np.float32) - 127.5) / 127.5

    iq = raw[0::2] + 1j * raw[1::2]
    return iq.astype(np.complex64)


def load_sigmf(data_path: str, meta_path: str):
    """Load SigMF file pair and return (iq, sample_rate, center_freq)."""
    with open(meta_path) as f:
        meta = json.load(f)

    global_meta = meta.get("global", {})
    sr = global_meta.get("core:sample_rate", None)
    cf = global_meta.get("core:frequency", None)
    datatype = global_meta.get(
        "core:datatype", "cf32_le"
    )  # default: complex float32 LE

    # Map SigMF datatype to numpy
    sigmf_dtype_map = {
        "cf32_le": "float32",
        "cf32": "float32",
        "ci16_le": "int16",
        "ci16": "int16",
        "ci8": "int8",
        "cu8": "uint8",
    }
    dtype_str = sigmf_dtype_map.get(datatype, "float32")
    iq = load_raw(data_path, dtype_str)
    return iq, sr, cf


def compute_spectrogram(iq: np.ndarray, fft_size: int, overlap: float = 0.0):
    """
    Compute power spectrogram.

    Returns
    -------
    spec : 2-D array, shape (n_frames, fft_size)  — power in dBFS
    """
    step = max(1, int(fft_size * (1.0 - overlap)))
    n_frames = (len(iq) - fft_size) // step + 1
    if n_frames < 1:
        raise ValueError(
            f"Signal too short ({len(iq)} samples) for FFT size {fft_size}."
        )

    window = np.hanning(fft_size).astype(np.float32)
    # Pre-allocate
    spec = np.empty((n_frames, fft_size), dtype=np.float32)

    for i in range(n_frames):
        seg = iq[i * step : i * step + fft_size] * window
        f = np.fft.fftshift(np.fft.fft(seg, n=fft_size))
        spec[i] = 20.0 * np.log10(np.abs(f) + 1e-12)

    return spec


def format_freq(hz: float) -> str:
    if hz >= 1e9:
        return f"{hz/1e9:.6g} GHz"
    if hz >= 1e6:
        return f"{hz/1e6:.6g} MHz"
    if hz >= 1e3:
        return f"{hz/1e3:.6g} kHz"
    return f"{hz:.6g} Hz"


# ── main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="IQ Waterfall Plot")
    parser.add_argument("iq_file", help="Path to IQ file")
    parser.add_argument(
        "--sigmf",
        metavar="META",
        default=None,
        help="SigMF metadata file (.sigmf-meta)",
    )
    parser.add_argument(
        "--dtype",
        choices=list(DTYPE_MAP),
        default="float32",
        help="Sample dtype for raw files (default: float32)",
    )
    parser.add_argument(
        "--sample-rate", type=float, default=None, help="Sample rate in Hz (e.g. 2e6)"
    )
    parser.add_argument(
        "--center-freq",
        type=float,
        default=None,
        help="Centre frequency in Hz (e.g. 915e6)",
    )
    parser.add_argument(
        "--fft-size",
        type=int,
        default=1024,
        help="FFT size / number of frequency bins (default: 1024)",
    )
    parser.add_argument(
        "--overlap",
        type=float,
        default=0.5,
        help="Fractional overlap between FFT windows 0–<1 (default: 0.5)",
    )
    parser.add_argument(
        "--vmin", type=float, default=None, help="Colour scale minimum in dBFS"
    )
    parser.add_argument(
        "--vmax", type=float, default=None, help="Colour scale maximum in dBFS"
    )
    parser.add_argument(
        "--colormap", default="viridis", help="Matplotlib colormap (default: viridis)"
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=4000,
        help="Downsample time axis to at most this many rows (default: 4000)",
    )
    parser.add_argument(
        "--output", default=None, help="Save figure to file instead of displaying"
    )
    args = parser.parse_args()

    # ── load ──────────────────────────────────────────────────────────────────
    sample_rate = args.sample_rate
    center_freq = args.center_freq

    if args.sigmf:
        print(f"Loading SigMF: {args.iq_file} + {args.sigmf}")
        iq, sr, cf = load_sigmf(args.iq_file, args.sigmf)
        if sample_rate is None and sr:
            sample_rate = sr
        if center_freq is None and cf:
            center_freq = cf
    else:
        print(f"Loading raw IQ ({args.dtype}): {args.iq_file}")
        iq = load_raw(args.iq_file, args.dtype)

    print(f"  Samples loaded : {len(iq):,}")
    if sample_rate:
        duration = len(iq) / sample_rate
        print(f"  Sample rate    : {format_freq(sample_rate)}")
        print(f"  Duration       : {duration:.4f} s")
    if center_freq:
        print(f"  Centre freq    : {format_freq(center_freq)}")

    # ── spectrogram ───────────────────────────────────────────────────────────
    fft_size = args.fft_size
    print(f"\nComputing spectrogram (FFT={fft_size}, overlap={args.overlap:.0%}) …")
    spec = compute_spectrogram(iq, fft_size, overlap=args.overlap)
    print(f"  Spectrogram shape : {spec.shape[0]} frames × {spec.shape[1]} bins")

    # Downsample time axis if needed to keep plotting fast
    if spec.shape[0] > args.max_frames:
        factor = spec.shape[0] // args.max_frames
        spec = spec[::factor]
        print(f"  Downsampled to    : {spec.shape[0]} frames (factor {factor})")

    n_frames, n_bins = spec.shape

    # ── axis values ───────────────────────────────────────────────────────────
    cf = center_freq or 0.0
    sr = sample_rate or fft_size  # fall back: 1 bin = 1 Hz

    freq_axis = cf + np.linspace(-sr / 2, sr / 2, n_bins)  # Hz

    step_real = max(1, int(fft_size * (1.0 - args.overlap)))
    if sample_rate:
        time_per_frame = step_real / sample_rate  # seconds
        time_axis = np.arange(n_frames) * time_per_frame  # seconds
    else:
        time_axis = np.arange(n_frames)  # frame index

    # ── colour limits ─────────────────────────────────────────────────────────
    vmin = args.vmin if args.vmin is not None else np.percentile(spec, 5)
    vmax = args.vmax if args.vmax is not None else np.percentile(spec, 99)

    # ── plot ──────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(12, 6))

    extent = [
        freq_axis[0] / 1e6,  # MHz
        freq_axis[-1] / 1e6,
        time_axis[-1],
        time_axis[0],
    ]

    img = ax.imshow(
        spec,
        aspect="auto",
        origin="upper",
        extent=extent,
        cmap=args.colormap,
        vmin=vmin,
        vmax=vmax,
        interpolation="nearest",
    )

    cbar = fig.colorbar(img, ax=ax, pad=0.01, fraction=0.03)
    cbar.set_label("Power (dBFS)")

    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Time (s)" if sample_rate else "Frame index")

    title_parts = []
    if center_freq:
        title_parts.append(f"Centre: {format_freq(center_freq)}")
    if sample_rate:
        title_parts.append(f"BW: {format_freq(sample_rate)}")
    title_parts.append(f"FFT: {fft_size}")
    ax.set_title("IQ Waterfall  —  " + "  |  ".join(title_parts))

    # Nice frequency tick labels
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.3f"))

    plt.tight_layout()

    if args.output:
        fig.savefig(args.output, dpi=150, bbox_inches="tight")
        print(f"\nFigure saved → {args.output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
