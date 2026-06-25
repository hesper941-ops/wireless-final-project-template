"""Minimal command-line entry point for the wireless project skeleton.

This phase intentionally exposes the CLI shape without implementing the full
end-to-end receiver pipeline yet.
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Wireless baseband simulator skeleton")
    parser.add_argument("--input", required=True, help="Input UTF-8 text file")
    parser.add_argument("--output", required=True, help="Output received text file")
    parser.add_argument("--snr", type=float, default=12.0, help="SNR in dB")
    parser.add_argument("--seed", type=int, default=2026, help="Random seed")
    parser.add_argument("--mod", default="qpsk", choices=["qpsk"], help="Modulation type")
    parser.add_argument("--channel", default="awgn", choices=["awgn"], help="Channel type")
    return parser


def main() -> int:
    parser = build_parser()
    parser.parse_args()
    print("Project skeleton ready. Full end-to-end pipeline is planned for a later phase.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
