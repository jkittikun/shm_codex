from __future__ import annotations

import numpy as np
import pytest

from shm_site.interactives.labs import (
    damped_sine,
    shear_building_mode_shape,
    single_sided_fft,
    strongest_sensor_floors,
)


def test_single_sided_fft_identifies_main_frequency() -> None:
    sample_rate = 100.0
    time = np.arange(0.0, 5.0, 1.0 / sample_rate)
    signal = np.sin(2.0 * np.pi * 4.0 * time)

    frequency, amplitude = single_sided_fft(signal, sample_rate)

    peak_frequency = frequency[np.argmax(amplitude)]
    assert peak_frequency == pytest.approx(4.0, abs=0.05)


def test_damped_sine_decay_reduces_late_amplitude() -> None:
    time = np.linspace(0.0, 10.0, 1000)

    undamped = np.abs(damped_sine(time, 2.0, 0.0))
    damped = np.abs(damped_sine(time, 2.0, 0.05))

    assert damped[-100:].max() < undamped[-100:].max() * 0.1


def test_mode_shape_is_normalized() -> None:
    shape = shear_building_mode_shape(stories=6, mode=2)

    assert np.max(np.abs(shape)) == pytest.approx(1.0)
    assert shape.shape == (6,)


def test_strongest_sensor_floors_returns_sorted_floor_numbers() -> None:
    shape = np.array([0.1, -0.9, 0.5, 0.8])

    sensors = strongest_sensor_floors(shape, count=2)

    assert sensors.tolist() == [2, 4]
