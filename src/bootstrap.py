"""Deterministic percentile bootstrap over matched run-level contrasts."""

from __future__ import annotations

import numpy as np


def paired_percentile_ci(seed_values, honest_values, *, draws: int = 10_000, seed: int = 20260804):
    treatment = np.asarray(seed_values, dtype=float)
    control = np.asarray(honest_values, dtype=float)
    if treatment.shape != control.shape or treatment.ndim != 1 or len(treatment) == 0:
        raise ValueError("paired one-dimensional nonempty inputs required")
    delta = treatment - control
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(delta), size=(draws, len(delta)))
    samples = delta[indices].mean(axis=1)
    low, high = np.percentile(samples, [2.5, 97.5])
    return float(delta.mean()), float(low), float(high)
