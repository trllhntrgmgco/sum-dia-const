"""Tests for the Sum Dia Const reference implementation.

The geometry tests check properties that follow from the definitions, so a
failure means the implementation is wrong.

The ephemeris tests compare the code against position tables computed by
hand. A failure there means one of the two is wrong and does not say which.
JPL Horizons arbitrates.

Copyright (c) 2026 Keenan Dunham.
"""

import numpy as np
import pytest

import ephemeris
from sumdiaconst import (
    ANTIPODES, CARDINALS, DIRECTIONS, SLOTS,
    canonicalise, distance, format_c, from_cartesian, parse,
    to_cartesian, to_spherical, validate,
)


# --- geometry ---------------------------------------------------------

def test_fourteen_directions():
    assert len(DIRECTIONS) == 14
    assert set(DIRECTIONS) == set(SLOTS)


@pytest.mark.parametrize("symbol", list(SLOTS))
def test_every_direction_is_a_unit_vector(symbol):
    assert np.linalg.norm(DIRECTIONS[symbol]) == pytest.approx(1.0)


@pytest.mark.parametrize("symbol", list(SLOTS))
def test_antipodes_negate(symbol):
    """The fourteen are seven axes: each direction's opposite is in the set."""
    opposite = DIRECTIONS[ANTIPODES[symbol]]
    assert DIRECTIONS[symbol] == pytest.approx(-opposite)


def test_seven_distinct_axes():
    axes = {frozenset((k, ANTIPODES[k])) for k in SLOTS}
    assert len(axes) == 7


@pytest.mark.parametrize("diagonal,cardinals", [
    ("a", (("1", 0.5), ("2", 0.5), ("9", 2 ** -0.5))),
    ("b", (("8", 0.5), ("2", 0.5), ("9", 2 ** -0.5))),
    ("c", (("8", 0.5), ("7", 0.5), ("9", 2 ** -0.5))),
    ("d", (("1", 0.5), ("7", 0.5), ("9", 2 ** -0.5))),
    ("3", (("1", 0.5), ("2", 0.5), ("0", 2 ** -0.5))),
])
def test_diagonals_are_cardinal_combinations(diagonal, cardinals):
    """Every diagonal is an exact nonnegative sum of three cardinals.

    This is why canonical form can drop the diagonals without losing reach.
    """
    rebuilt = sum(
        (weight * DIRECTIONS[c] for c, weight in cardinals),
        np.zeros(3),
    )
    assert rebuilt == pytest.approx(DIRECTIONS[diagonal])


def test_cardinals_span_three_space():
    basis = np.array([DIRECTIONS[c] for c in ("1", "2", "9")])
    assert np.linalg.matrix_rank(basis) == 3


# --- encoding ---------------------------------------------------------

def test_letters_are_slot_names_not_values():
    """a-d name directions. They are never magnitudes, so they never appear
    inside a coordinate string."""
    assert not validate("0a00000000000d.00000000000000")
    assert validate("01000000000000.00000000000000")


@pytest.mark.parametrize("bad", [
    "",
    "0100000000000.00000000000000",    # 13 integer slots
    "01000000000000.0000000000000",    # 13 fractional slots
    "0100000000000000000000000000",    # no decimal point
    "-1000000000000.00000000000000",
])
def test_validate_rejects_malformed(bad):
    assert not validate(bad)


def test_origin_is_all_zeros():
    origin = "00000000000000.00000000000000"
    assert to_cartesian(origin) == pytest.approx(np.zeros(3))
    assert from_cartesian(0.0, 0.0, 0.0) == origin


def test_earth_sits_on_the_baseline():
    """Slot 1 is the second character, so a leading digit means direction 0."""
    earth = from_cartesian(0.98331, 0.0, 0.0)
    assert earth == "01000000000000.00000000000000"
    r, azimuth, elevation = to_spherical(earth)
    assert r == pytest.approx(1.0)
    assert azimuth == pytest.approx(0.0)
    assert elevation == pytest.approx(0.0)


def test_leading_digit_means_down_not_forward():
    """Guards the encoding change: position names the direction."""
    down = "10000000000000.00000000000000"
    assert to_cartesian(down) == pytest.approx(np.array([0.0, 0.0, -1.0]))


def test_parse_and_format_round_trip():
    coord = "01200000000000.03400000000000"
    assert format_c(parse(coord)) == coord


def test_format_rejects_out_of_range():
    with pytest.raises(ValueError):
        format_c({"1": 12.0})


@pytest.mark.parametrize("point", [
    (1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 2.5, 0.0),
    (0.0, -2.5, 0.0), (0.0, 0.0, 3.1), (1.4, -2.2, 0.7),
    (-0.3, -0.6, -0.9),
])
def test_cartesian_round_trip(point):
    """Error is bounded by half the last digit on each of three axes."""
    back = to_cartesian(from_cartesian(*point))
    assert back == pytest.approx(np.array(point), abs=0.05)


def test_canonical_form_uses_cardinals_only():
    mags = dict.fromkeys(SLOTS, 0.0)
    mags["a"] = 1.0
    result = canonicalise(mags)
    assert all(result[k] == 0.0 for k in SLOTS if k not in CARDINALS)


def test_canonical_form_cancels_opposed_senses():
    mags = dict.fromkeys(SLOTS, 0.0)
    mags["1"], mags["8"] = 3.0, 1.0
    result = canonicalise(mags)
    assert result["1"] == pytest.approx(2.0)
    assert result["8"] == pytest.approx(0.0)


def test_distance_is_symmetric_and_correct():
    a = from_cartesian(1.0, 0.0, 0.0)
    b = from_cartesian(0.0, 1.0, 0.0)
    assert distance(a, b) == pytest.approx(np.sqrt(2.0), abs=0.01)
    assert distance(a, b) == pytest.approx(distance(b, a))


# --- ephemeris ----------------------------------------------------------

def test_epoch_conversion():
    assert ephemeris.julian_centuries(2451545.0) == 0.0
    assert ephemeris.julian_centuries(2461301.5) == pytest.approx(
        0.2671184, abs=1e-6
    )


@pytest.mark.parametrize("e", [0.0, 0.0068, 0.0934, 0.2056, 0.6])
def test_kepler_solution_satisfies_its_own_equation(e):
    for M in range(-180, 180, 17):
        E = ephemeris.kepler(float(M), e)
        residual = E - np.degrees(e) * np.sin(np.radians(E))
        wrapped = (M + 180.0) % 360.0 - 180.0
        assert residual == pytest.approx(wrapped, abs=1e-6)


# perihelion and aphelion, AU
ORBIT_BOUNDS = {
    "Mercury": (0.3075, 0.4667), "Venus": (0.7184, 0.7282),
    "Earth": (0.9833, 1.0167), "Mars": (1.3814, 1.6660),
    "Jupiter": (4.9501, 5.4570), "Saturn": (9.0241, 10.0860),
    "Uranus": (18.2861, 20.0965), "Neptune": (29.8107, 30.3300),
}


@pytest.mark.parametrize("T", [0.0, 0.2671184])
@pytest.mark.parametrize("body", sorted(ORBIT_BOUNDS))
def test_distance_lies_within_the_orbit(body, T):
    r = ephemeris.table(T)[body][3]
    low, high = ORBIT_BOUNDS[body]
    assert low - 0.01 <= r <= high + 0.01


# Hand-computed SDC frame components, AU. See SPEC sections 12 and 13.
# These are the values to distrust first if a test here fails.
HAND_J2000 = {
    "Mercury": (-0.41691, 0.20786, -0.02458),
    "Venus": (0.09761, 0.71241, 0.04102),
    "Earth": (0.98331, 0.0, 0.0),
    "Mars": (-0.26454, -1.36535, -0.03447),
    "Jupiter": (2.17441, -4.46492, -0.10177),
    "Saturn": (5.28091, -7.48865, -0.36913),
    "Uranus": (-16.11486, -11.70957, -0.23802),
    "Neptune": (-27.60430, -12.04180, 0.12740),
}

HAND_2026 = {
    "Mercury": (-0.29710, 0.34399, -0.00286),
    "Venus": (-0.44260, -0.57633, -0.04187),
    "Earth": (-0.27106, -0.96774, 0.00001),
    "Mars": (1.43270, -0.56819, 0.02431),
    "Jupiter": (4.60207, 2.62880, 0.05956),
    "Saturn": (0.01489, -9.42972, -0.39891),
    "Uranus": (15.33795, -11.94060, -0.05240),
    "Neptune": (-4.06257, -29.59121, -0.71523),
}


@pytest.mark.parametrize("T,expected,label", [
    (0.0, HAND_J2000, "J2000.0"),
    (0.2671184, HAND_2026, "2026-09-18"),
])
def test_code_agrees_with_the_hand_computed_tables(T, expected, label):
    """Tolerance is 0.01 AU, loose enough for hand rounding and tight enough
    to catch a slipped digit in the mean-longitude multiplications."""
    computed = ephemeris.table(T)
    for body, hand in expected.items():
        x, y, z = computed[body][:3]
        assert (x, y, z) == pytest.approx(hand, abs=0.01), (
            "%s at %s: code says %s, hand table says %s. "
            "Check against JPL Horizons before trusting either."
            % (body, label, (x, y, z), hand)
        )


def test_earth_leaves_the_baseline_over_time():
    """Direction 1 is frozen at J2000.0, not a pointer that tracks Earth."""
    assert ephemeris.table(0.0)["Earth"][4] == pytest.approx(0.0, abs=0.01)
    assert ephemeris.table(0.2671184)["Earth"][4] == pytest.approx(
        254.354, abs=0.1
    )


def test_outer_planets_do_not_fit_the_compact_profile():
    x, y, z = ephemeris.position("Neptune", 0.0)
    with pytest.raises(ValueError, match="wider profile"):
        from_cartesian(x, y, z)
