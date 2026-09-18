"""Sum Dia Const - a fourteen-direction coordinate notation.

Reference implementation of specification draft 1.

Status: draft. The encoding is new and may change. Nothing here has been
validated against an independent coordinate system.

Copyright (c) 2026 Keenan Dunham.
"""

from __future__ import annotations

import re

import numpy as np

__all__ = [
    "SLOTS", "DIRECTIONS", "ANTIPODES", "CARDINALS",
    "AU_METRES", "ANCHOR_DEG",
    "validate", "parse", "format_c", "canonicalise",
    "to_cartesian", "from_cartesian", "distance", "to_spherical",
]

R = 2 ** -0.5  # sqrt(2)/2, the component of a 45 degree diagonal

#: Slot order. Position in a coordinate string names the direction.
SLOTS = "0123456789abcd"

#: Unit vector per direction in the SDC frame. See SPEC section 3.
DIRECTIONS = {
    "0": np.array([0.0, 0.0, -1.0]),   # down
    "1": np.array([1.0, 0.0, 0.0]),    # Earth-anchor
    "2": np.array([0.0, 1.0, 0.0]),    # port
    "3": np.array([0.5, 0.5, -R]),
    "4": np.array([-0.5, 0.5, -R]),
    "5": np.array([-0.5, -0.5, -R]),
    "6": np.array([0.5, -0.5, -R]),
    "7": np.array([0.0, -1.0, 0.0]),   # starboard
    "8": np.array([-1.0, 0.0, 0.0]),   # anti-Earth
    "9": np.array([0.0, 0.0, 1.0]),    # up
    "a": np.array([0.5, 0.5, R]),
    "b": np.array([-0.5, 0.5, R]),
    "c": np.array([-0.5, -0.5, R]),
    "d": np.array([0.5, -0.5, R]),
}

#: The fourteen directions are seven axes. See SPEC section 4.
ANTIPODES = {
    "1": "8", "8": "1",
    "2": "7", "7": "2",
    "9": "0", "0": "9",
    "a": "5", "5": "a",
    "b": "6", "6": "b",
    "c": "3", "3": "c",
    "d": "4", "4": "d",
}

#: Canonical form uses these only. See SPEC section 7.
CARDINALS = ("1", "8", "2", "7", "9", "0")

AU_METRES = 149_597_870_700.0

#: Direction 1 is Earth's heliocentric ecliptic longitude at J2000.0,
#: mean ecliptic and equinox of J2000. See SPEC section 11.
ANCHOR_DEG = 100.38021

# In SDC/C a character is a MAGNITUDE, 0-9. The letters a-d name slots and
# are never values, so the value alphabet is decimal digits only.
_C_PATTERN = re.compile("^[0-9]{14}[.][0-9]{14}$")


def validate(coordinate):
    """Return True if the string is a well-formed SDC/C coordinate."""
    return bool(_C_PATTERN.match(coordinate))


def parse(coordinate):
    """SDC/C string -> {direction symbol: magnitude in profile units}."""
    if not validate(coordinate):
        raise ValueError("malformed SDC/C coordinate: %r" % (coordinate,))
    whole, tenths = coordinate[:14], coordinate[15:]
    return {
        SLOTS[i]: int(whole[i]) + 0.1 * int(tenths[i])
        for i in range(14)
    }


def format_c(magnitudes):
    """{direction: magnitude} -> SDC/C string.

    Rounds to 0.1. Raises if any magnitude falls outside 0 to 9.9, which is
    this profile's per-direction ceiling.
    """
    whole = tenths = ""
    for k in SLOTS:
        m = round(magnitudes.get(k, 0.0), 1)
        if not 0.0 <= m <= 9.9:
            raise ValueError(
                "%s outside the SDC/C range 0-9.9 in direction %s; "
                "use a wider profile" % (m, k)
            )
        whole += str(int(m))
        tenths += str(int(round((m - int(m)) * 10)))
    return whole + "." + tenths


def to_cartesian(coordinate):
    """SDC/C string -> (x, y, z) in profile units, SDC frame."""
    mags = parse(coordinate)
    return sum((m * DIRECTIONS[k] for k, m in mags.items()), np.zeros(3))


def from_cartesian(x, y, z):
    """(x, y, z) -> canonical SDC/C string.

    Canonical form uses cardinals only, so at most three slots are nonzero
    and the inverse is direct. No search, no iteration. See SPEC section 7.
    """
    mags = dict.fromkeys(SLOTS, 0.0)
    mags["1" if x >= 0 else "8"] = abs(x)
    mags["2" if y >= 0 else "7"] = abs(y)
    mags["9" if z >= 0 else "0"] = abs(z)
    return format_c(mags)


def canonicalise(magnitudes):
    """Expand diagonals into cardinals and cancel opposed senses.

    Lossy in the final digit: the diagonals carry sqrt(2)/2, which has no
    finite decimal form. See SPEC section 7.
    """
    v = sum(
        (m * DIRECTIONS[k] for k, m in magnitudes.items()),
        np.zeros(3),
    )
    out = dict.fromkeys(SLOTS, 0.0)
    out["1" if v[0] >= 0 else "8"] = abs(float(v[0]))
    out["2" if v[1] >= 0 else "7"] = abs(float(v[1]))
    out["9" if v[2] >= 0 else "0"] = abs(float(v[2]))
    return out


def distance(a, b):
    """Distance between two SDC/C coordinates, in profile units."""
    return float(np.linalg.norm(to_cartesian(b) - to_cartesian(a)))


def to_spherical(coordinate):
    """Return (r, azimuth_deg, elevation_deg) in the SDC frame."""
    x, y, z = to_cartesian(coordinate)
    r = float(np.sqrt(x * x + y * y + z * z))
    if r == 0.0:
        return 0.0, 0.0, 0.0
    return (
        r,
        float(np.degrees(np.arctan2(y, x)) % 360.0),
        float(np.degrees(np.arcsin(z / r))),
    )
