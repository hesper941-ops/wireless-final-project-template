"""AWGN channel model."""

from __future__ import annotations

import numpy as np


def awgn(symbols: np.ndarray | list[complex], snr_db: float, seed: int | None = None) -> np.ndarray:
    """Add complex AWGN using SNR = signal power / complex noise power."""
    tx = np.asarray(symbols, dtype=complex)
    if tx.size == 0:
        return tx.copy()

    rng = np.random.default_rng(seed)
    signal_power = float(np.mean(np.abs(tx) ** 2))
    noise_power = signal_power / (10.0 ** (float(snr_db) / 10.0))
    sigma = np.sqrt(noise_power / 2.0)
    noise = sigma * (rng.normal(size=tx.shape) + 1j * rng.normal(size=tx.shape))
    return tx + noise


def add_prefix(symbols: np.ndarray | list[complex], offset_symbols: int, seed: int | None = None) -> np.ndarray:
    """Insert a deterministic complex-noise prefix before valid symbols."""
    if offset_symbols < 0:
        raise ValueError("offset_symbols must be non-negative")
    tx = np.asarray(symbols, dtype=complex)
    rng = np.random.default_rng(seed)
    prefix = (rng.normal(size=offset_symbols) + 1j * rng.normal(size=offset_symbols)) / np.sqrt(2.0)
    return np.concatenate([prefix, tx])


awgn_channel = awgn
add_awgn = awgn
add_noise = awgn
