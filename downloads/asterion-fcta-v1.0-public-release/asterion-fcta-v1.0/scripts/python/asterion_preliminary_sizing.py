"""Preliminary ASTERION sizing checks.

This script intentionally performs only transparent first-order calculations.
It is not a flight-design or certification tool.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class AsterionBaseline:
    ring_radius_m: float = 12.0
    ring_speed_rpm: float = 4.3
    thruster_count: int = 12
    thruster_power_kw: float = 12.0
    total_power_low_kw: float = 200.0
    total_power_high_kw: float = 300.0


def artificial_gravity(radius_m: float, speed_rpm: float) -> tuple[float, float]:
    if radius_m <= 0 or speed_rpm < 0:
        raise ValueError("Radius must be positive and speed cannot be negative.")
    omega = speed_rpm * 2.0 * math.pi / 60.0
    acceleration = omega**2 * radius_m
    return acceleration, acceleration / 9.80665


def propulsion_power(count: int, unit_power_kw: float) -> float:
    if count < 0 or unit_power_kw < 0:
        raise ValueError("Thruster count and power must be non-negative.")
    return count * unit_power_kw


def main() -> None:
    baseline = AsterionBaseline()
    acceleration, gravity_fraction = artificial_gravity(
        baseline.ring_radius_m, baseline.ring_speed_rpm
    )
    prop_power = propulsion_power(
        baseline.thruster_count, baseline.thruster_power_kw
    )

    print("ASTERION FCTA-1 preliminary sizing")
    print(f"Ring acceleration: {acceleration:.3f} m/s^2")
    print(f"Artificial gravity: {gravity_fraction:.3f} g")
    print(f"Propulsion power: {prop_power:.1f} kW")
    print(
        "Non-propulsion power margin: "
        f"{baseline.total_power_low_kw - prop_power:.1f} to "
        f"{baseline.total_power_high_kw - prop_power:.1f} kW"
    )


if __name__ == "__main__":
    main()
