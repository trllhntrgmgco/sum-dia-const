"""Planet positions in the Sum Dia Const frame.

Keplerian elements from JPL, Approximate Positions of the Planets, Table 1,
valid 1800-2050: https://ssd.jpl.nasa.gov/planets/approx_pos.html

Accuracy is bounded by those elements - roughly 20 arcseconds of longitude
for the inner planets, rising to 600 for Saturn. For tighter work query JPL
Horizons directly.

Copyright (c) 2026 Keenan Dunham.
"""

from __future__ import annotations

import numpy as np

from sumdiaconst import ANCHOR_DEG, from_cartesian

__all__ = ["ELEMENTS", "julian_centuries", "kepler", "heliocentric",
           "to_sdc_frame", "position", "table"]

# body -> (elements at J2000.0, change per Julian century)
#   a    semi-major axis, AU
#   e    eccentricity
#   I    inclination, degrees
#   L    mean longitude, degrees
#   peri longitude of perihelion, degrees
#   node longitude of ascending node, degrees
ELEMENTS = {
    "Mercury": (
        (0.38709927, 0.20563593, 7.00497902, 252.25032350, 77.45779628, 48.33076593),
        (0.00000037, 0.00001906, -0.00594749, 149472.67411175, 0.16047689, -0.12534081),
    ),
    "Venus": (
        (0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718, 76.67984255),
        (0.00000390, -0.00004107, -0.00078890, 58517.81538729, 0.00268329, -0.27769418),
    ),
    "Earth": (
        (1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0.0),
        (0.00000562, -0.00004392, -0.01294668, 35999.37244981, 0.32327364, 0.0),
    ),
    "Mars": (
        (1.52371034, 0.09339410, 1.84969142, -4.55343205, -23.94362959, 49.55953891),
        (0.00001847, 0.00007882, -0.00813131, 19140.30268499, 0.44441088, -0.29257343),
    ),
    "Jupiter": (
        (5.20288700, 0.04838624, 1.30439695, 34.39644051, 14.72847983, 100.47390909),
        (-0.00011607, -0.00013253, -0.00183714, 3034.74612775, 0.21252668, 0.20469106),
    ),
    "Saturn": (
        (9.53667594, 0.05386179, 2.48599187, 49.95424423, 92.59887831, 113.66242448),
        (-0.00125060, -0.00050991, 0.00193609, 1222.49362201, -0.41897216, -0.28867794),
    ),
    "Uranus": (
        (19.18916464, 0.04725744, 0.77263783, 313.23810451, 170.95427630, 74.01692503),
        (-0.00196176, -0.00004397, -0.00242939, 428.48202785, 0.40805281, 0.04240589),
    ),
    "Neptune": (
        (30.06992276, 0.00859048, 1.77004347, -55.12002969, 44.96476227, 131.78422574),
        (0.00026291, 0.00005105, 0.00035372, 218.45945325, -0.32241464, -0.00508664),
    ),
}

J2000_JD = 2451545.0
DAYS_PER_CENTURY = 36525.0


def julian_centuries(julian_date):
    """Julian centuries elapsed since J2000.0."""
    return (julian_date - J2000_JD) / DAYS_PER_CENTURY


def kepler(mean_anomaly_deg, e, tol=1e-10, max_iter=200):
    """Solve M = E - e* sin E for E. All angles in degrees."""
    e_star = np.degrees(e)
    M = (mean_anomaly_deg + 180.0) % 360.0 - 180.0
    E = M + e_star * np.sin(np.radians(M))
    for _ in range(max_iter):
        dM = M - (E - e_star * np.sin(np.radians(E)))
        dE = dM / (1.0 - e * np.cos(np.radians(E)))
        E += dE
        if abs(dE) < tol:
            return E
    raise RuntimeError("Kepler solve did not converge for e=%s" % (e,))


def heliocentric(body, T):
    """Heliocentric ecliptic (x, y, z) in AU, J2000 mean ecliptic."""
    (a0, e0, I0, L0, p0, O0), (da, de, dI, dL, dp, dO) = ELEMENTS[body]
    a, e = a0 + da * T, e0 + de * T
    I, L = I0 + dI * T, L0 + dL * T
    peri, node = p0 + dp * T, O0 + dO * T

    arg = peri - node
    E = np.radians(kepler(L - peri, e))

    # position in the orbital plane
    xp = a * (np.cos(E) - e)
    yp = a * np.sqrt(1.0 - e * e) * np.sin(E)

    cw, sw = np.cos(np.radians(arg)), np.sin(np.radians(arg))
    cO, sO = np.cos(np.radians(node)), np.sin(np.radians(node))
    cI, sI = np.cos(np.radians(I)), np.sin(np.radians(I))

    return np.array([
        (cw * cO - sw * sO * cI) * xp + (-sw * cO - cw * sO * cI) * yp,
        (cw * sO + sw * cO * cI) * xp + (-sw * sO + cw * cO * cI) * yp,
        (sw * sI) * xp + (cw * sI) * yp,
    ])


def to_sdc_frame(v):
    """Rotate ecliptic coordinates into the SDC frame.

    A single rotation about Z by the anchor longitude - the frames share
    their Z axis, so only azimuth shifts. See SPEC section 11."""
    t = np.radians(ANCHOR_DEG)
    c, s = np.cos(t), np.sin(t)
    return np.array([c * v[0] + s * v[1], -s * v[0] + c * v[1], v[2]])


def position(body, T):
    """Body position in the SDC frame, AU."""
    return to_sdc_frame(heliocentric(body, T))


def table(T):
    """Every body at epoch T: name -> (x, y, z, r, azimuth, elevation)."""
    rows = {}
    for body in ELEMENTS:
        x, y, z = position(body, T)
        r = float(np.sqrt(x * x + y * y + z * z))
        rows[body] = (
            float(x), float(y), float(z), r,
            float(np.degrees(np.arctan2(y, x)) % 360.0),
            float(np.degrees(np.arcsin(z / r))),
        )
    return rows


if __name__ == "__main__":
    for T, label in ((0.0, "J2000.0"), (0.2671184, "2026-09-18")):
        print(label)
        print("  %-9s %11s %11s %11s %9s %9s"
              % ("body", "x", "y", "z", "r", "azimuth"))
        for body, (x, y, z, r, az, el) in table(T).items():
            print("  %-9s %11.5f %11.5f %11.5f %9.5f %9.3f"
                  % (body, x, y, z, r, az))
        print()

    # Only the inner planets fit SDC/C, whose ceiling is 9.9 AU per direction
    print("SDC/C coordinates, J2000.0")
    for body, (x, y, z, r, az, el) in table(0.0).items():
        try:
            print("  %-9s %s" % (body, from_cartesian(x, y, z)))
        except ValueError as exc:
            print("  %-9s (%s)" % (body, exc))
