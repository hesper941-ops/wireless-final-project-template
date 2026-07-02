"""Regression coverage for classroom-review boundary cases."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.pipeline import run_pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_METRICS = {
    "snr_db", "seed", "modulation", "channel", "payload_bits", "ber", "fer",
    "text_match_rate", "checksum_pass", "sync_start_index", "failure_reason",
}


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "main.py", *args],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )


@pytest.mark.parametrize(
    "content",
    [
        "无线通信技术期末项目",
        "A plain English payload.",
        "QPSK 链路 mixed text 🚀📡",
        "",
        "短",
        ("较长文本 mixed UTF-8 🌏\n" * 80),
    ],
    ids=["chinese", "english", "mixed_emoji", "empty", "short", "long"],
)
def test_utf8_round_trip_and_payload_length(tmp_path: Path, content: str):
    source = tmp_path / "source.txt"
    output = tmp_path / "nested" / "results" / "received.txt"
    source.write_bytes(content.encode("utf-8"))
    metrics = run_pipeline(
        input_path=source, output_path=output, snr_db=12, seed=2026,
        modulation="qpsk", channel="awgn", make_plots=False,
    )
    assert output.read_bytes() == source.read_bytes()
    assert metrics["payload_bits"] == len(source.read_bytes()) * 8
    assert metrics["ber"] == metrics["fer"] == 0.0
    assert metrics["checksum_pass"] is True
    assert metrics["failure_reason"] is None
    assert REQUIRED_METRICS <= metrics.keys()


@pytest.mark.parametrize("seed", [0, 1, 7, 2026, 65537])
def test_awgn_12db_multiple_seeds(tmp_path: Path, seed: int):
    source = tmp_path / f"input-{seed}.txt"
    output = tmp_path / f"out-{seed}" / "received.txt"
    source.write_text("Seed 回归 📶 " * 12, encoding="utf-8")
    metrics = run_pipeline(
        input_path=source, output_path=output, snr_db=12, seed=seed,
        modulation="qpsk", channel="awgn", make_plots=False,
    )
    assert output.read_bytes() == source.read_bytes()
    assert metrics["sync_start_index"] == metrics["prefix_offset_symbols"]


@pytest.mark.parametrize("snr", ["-1", "nan", "inf"])
def test_invalid_snr_is_rejected(tmp_path: Path, snr: str):
    source = tmp_path / "input.txt"
    source.write_text("data", encoding="utf-8")
    result = run_cli("--input", str(source), "--output", str(tmp_path / "out.txt"), "--snr", snr)
    assert result.returncode != 0
    assert "snr must be a finite non-negative number" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()


@pytest.mark.parametrize(
    ("option", "value"),
    [("--mod", "bpsk"), ("--channel", "rician")],
)
def test_invalid_choice_is_rejected(tmp_path: Path, option: str, value: str):
    source = tmp_path / "input.txt"
    source.write_text("data", encoding="utf-8")
    result = run_cli(
        "--input", str(source), "--output", str(tmp_path / "out.txt"), option, value,
    )
    assert result.returncode != 0
    assert "invalid choice" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()


def test_missing_input_has_clear_error(tmp_path: Path):
    missing = tmp_path / "missing.txt"
    result = run_cli("--input", str(missing), "--output", str(tmp_path / "out.txt"))
    assert result.returncode != 0
    assert "input file does not exist" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()


@pytest.mark.parametrize("channel", ["awgn", "rayleigh"])
def test_failure_metrics_schema_is_stable(tmp_path: Path, channel: str):
    source = tmp_path / "input.txt"
    source.write_text("low SNR failure payload " * 20, encoding="utf-8")
    output = tmp_path / "low" / "received.txt"
    metrics = run_pipeline(
        input_path=source, output_path=output, snr_db=0, seed=2026,
        modulation="qpsk", channel=channel, make_plots=False,
    )
    stored = json.loads((output.parent / "metrics.json").read_text(encoding="utf-8"))
    assert REQUIRED_METRICS <= metrics.keys()
    assert REQUIRED_METRICS <= stored.keys()
    assert metrics["failure_reason"] is not None
