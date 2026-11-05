#!/usr/bin/env python3
"""Generate the small temperature fixtures used by the NumPy notebooks."""

from pathlib import Path

import numpy as np


ARRAY_OUTPUT_PATH = Path(__file__).with_name("temperature_grid.npy")
TEXT_OUTPUT_PATH = Path(__file__).with_name("temperature_morning.csv")


def create_temperature_grid() -> np.ndarray:
    """Return a deterministic grid with axes ordered as (time, y, x)."""
    x = np.linspace(0.0, 3.0, num=4)
    y = np.arange(3, dtype=np.float64)
    time_offset = np.array([0.0, 2.9])

    morning = 18.2 + 0.25 * x[None, :] - 0.45 * y[:, None]
    temperature = morning[None, :, :] + time_offset[:, None, None]
    return np.round(temperature, decimals=1)


def main() -> None:
    """Write the binary cube and a text export of its morning slice."""
    temperature = create_temperature_grid()
    np.save(ARRAY_OUTPUT_PATH, temperature, allow_pickle=False)
    np.savetxt(
        TEXT_OUTPUT_PATH,
        temperature[0],
        delimiter=",",
        fmt="%.1f",
        header="temperature_c; rows=y; columns=x; time=06:00",
    )


if __name__ == "__main__":
    main()
