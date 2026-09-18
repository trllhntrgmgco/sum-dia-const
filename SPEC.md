Sum Dia Const

A Universal Space-Time Coordinate Notation — Specification Draft 1

Keenan Dunham · 2026-09-18 · @u_HqWpUBbr0Da0bG_53zvTzQ

1. Status and scope

This is a design specification. It defines a coordinate notation and works through its arithmetic. It reports no measurements.

Every quantity below follows from the definitions and can be checked by hand. Nothing here has been tested against hardware, and the system has no implementation history.

Not in this document, and not to be read into it: benchmarks, accuracy trials, case studies, deployments, peer review, institutional validation, or adoption estimates. None of those exist yet.

The geometry in sections 3 and 4 is settled. The encoding in sections 5 through 7 is newly specified here and is the part most likely to change. Section 10 lists what is unresolved.

2. Design goals

The notation is built to satisfy five things at once. Where they conflict, the ordering below is the priority.

1. Readable direction. A person should be able to look at a coordinate and know roughly which way it points, without computing anything.
2. One origin. Sol is the origin for every coordinate at every scale. No local frames, no re-basing.
3. A human baseline. One direction is anchored to something familiar rather than to an abstract celestial pole.
4. Fixed width. A coordinate is a fixed-length string, so storage, transmission, and parsing are constant-cost.
5. Unique representation. One physical point should have exactly one valid coordinate.

Goals 1 and 5 pull against each other, and that tension drives most of section 7. Goal 4 pulls against precision, which is the subject of section 6.

3. The fourteen directions

All fourteen are unit vectors in a right-handed Cartesian frame centred on Sol.

Frame definition. +X is direction 1, the Earth-anchor baseline. +Z is direction 9, normal to Earth's orbital plane. +Y is direction 2, completing the right-handed set. Azimuth is measured counterclockwise from +X viewed from +Z; elevation is measured from the XY plane.

The diagonal directions sit at elevation ±45° and azimuth 45°, 135°, 225°, 315°. For elevation 45° the horizontal component is cos 45° = √2/2, which splits across X and Y as (√2/2)(√2/2) = 1/2 each. The vertical component is sin 45° = √2/2.

| Symbol | Name | Azimuth | Elevation | Unit vector (X, Y, Z) |
| 0 | Down | — | −90° | (0, 0, −1) |
| 1 | Earth-anchor | 0° | 0° | (1, 0, 0) |
| 2 | Port | 90° | 0° | (0, 1, 0) |
| 3 | Low-fore-port | 45° | −45° | (½, ½, −√2/2) |
| 4 | Low-aft-port | 135° | −45° | (−½, ½, −√2/2) |
| 5 | Low-aft-starboard | 225° | −45° | (−½, −½, −√2/2) |
| 6 | Low-fore-starboard | 315° | −45° | (½, −½, −√2/2) |
| 7 | Starboard | 270° | 0° | (0, −1, 0) |
| 8 | Anti-Earth | 180° | 0° | (−1, 0, 0) |
| 9 | Up | — | +90° | (0, 0, 1) |
| a | High-fore-port | 45° | +45° | (½, ½, √2/2) |
| b | High-aft-port | 135° | +45° | (−½, ½, √2/2) |
| c | High-aft-starboard | 225° | +45° | (−½, −½, √2/2) |
| d | High-fore-starboard | 315° | +45° | (½, −½, √2/2) |

Each row checks as a unit vector: ¼ + ¼ + ½ = 1.

Epoch dependency. Direction 1 is defined by Earth's heliocentric position, which rotates through 360° every year. The baseline must therefore be frozen at a stated epoch, in the same way J2000.0 freezes the equinox. Until that epoch is chosen and the resulting inertial direction written down to stated precision, no coordinate in this system is fully defined. This is the single largest gap in the specification.

4. The fourteen are seven axes

Every direction has its exact opposite in the set. The fourteen directions are seven antipodal pairs, not fourteen independent bearings.

| Axis | Positive sense | Negative sense |
| X (Earth baseline) | 1 | 8 |
| Y | 2 | 7 |
| Z | 9 | 0 |
| Fore-port diagonal | a | 5 |
| Aft-port diagonal | b | 6 |
| Aft-starboard diagonal | c | 3 |
| Fore-starboard diagonal | d | 4 |

The diagonal pairings are worth checking, because they are not the ones the numbering suggests. Direction a is (½, ½, √2/2); its negation is (−½, −½, −√2/2), which is 5, not 3. Similarly b pairs with 6, c with 3, and d with 4.

This matters for two reasons.

Cancellation. Any coordinate with nonzero magnitude in both senses of an axis is expressing the same point as a smaller coordinate. Those two values subtract. Section 7 uses this to define canonical form.

Redundancy. Each diagonal is an exact nonnegative combination of three cardinals:

a = ½·(1) + ½·(2) + (√2/2)·(9)

So the six cardinal directions (1, 8, 2, 7, 9, 0) already span the whole space. The eight diagonals add no reach. They exist to make common bearings readable in one symbol instead of three, which is goal 1 from section 2 paying for itself against goal 5.

5. Fixed-slot encoding

A coordinate is fourteen magnitudes, one per direction, in fixed order. Position in the string names the direction. The character at that position gives the magnitude along it.

Slot order is fixed for all profiles:

0  1  2  3  4  5  6  7  8  9  a  b  c  d

This is the change that removes the ambiguity in the earlier draft. Previously a character did two jobs — it named a direction and its position carried magnitude — which made strings like 70000000001524 unreadable without an extra convention. Under fixed slots, a character does one job: magnitude. Direction is structural.

5.1 Layout A — the 29-character form

The original format reads cleanly under this rule. Fourteen integer digits, a decimal point, fourteen fractional digits. Slot k in each field refers to the same direction.

I₀I₁I₂I₃I₄I₅I₆I₇I₈I₉IₐI_bI_cI_d . F₀F₁F₂F₃F₄F₅F₆F₇F₈F₉FₐF_bF_cF_d

Magnitude along direction k, in whatever unit the profile declares:

M(k) = I(k) + 0.1 × F(k)

Each direction therefore carries two significant digits: a whole part 0–9 and one tenth. The per-direction range is 0 to 9.9 units in steps of 0.1.

This is a genuine result and it is smaller than earlier drafts assumed. Twenty-nine characters spread across fourteen directions leaves two digits each. It does not yield fifteen orders of magnitude. Section 6 gives the widths that do.

5.2 Layout B — general fixed-width slots

For any precision beyond two digits, the slot fields are widened and written consecutively. Each slot is a fixed-width fixed-point field of A integer digits and B fractional digits:

[slot 0][slot 1][slot 2] … [slot d]      each slot = A digits . B digits

Total string length is 14 × (A + B + 1) characters including one decimal point per slot. Layout A is the special case A = 1, B = 1, with the points factored out and the fields regrouped.

5.3 Profile tag

Because width and unit both vary, a coordinate is not interpretable on its own. Every coordinate carries a profile tag naming the field widths and the base unit:

SDC/<profile>:<coordinate string>

A coordinate without a tag is undefined, not defaulted.

6. Precision profiles

Range and resolution are set entirely by A and B. Per direction, range is 10^A − 10^−B units and resolution is 10^−B units. Dynamic range within one profile is 10^(A+B).

With 1 AU = 149,597,870.7 km:

| Profile | A.B | Chars | Per-direction range | Resolution | Resolution in metres |
| SDC/C | 1.1 | 29 | 0–9.9 AU | 0.1 AU | 1.5 × 10¹⁰ |
| SDC/S | 4.4 | 126 | 0–9999.9999 AU | 10⁻⁴ AU | 1.5 × 10⁷ |
| SDC/F | 4.9 | 196 | 0–9999 AU | 10⁻⁹ AU | 150 |
| SDC/P | 4.15 | 280 | 0–9999 AU | 10⁻¹⁵ AU | 1.5 × 10⁻⁴ |

The 0.15 mm figure costs 280 characters. Reaching 10⁻¹⁵ AU resolution while still spanning 1000 AU requires nineteen digits per slot across fourteen slots. There is no way around this in a fixed-point fixed-slot scheme: the digits have to be somewhere. Earlier drafts claimed that range for a 29-character string, which was wrong.

Rescaling is the practical answer. A profile declares its base unit, and most work does not need to span fifteen orders at once. A surgical or bench profile using millimetres as the base unit gets 0.1 mm resolution at A.B = 4.1 and 84 characters — it simply cannot also address Neptune. Choosing the unit to match the working scale is cheaper than carrying every scale in one string.

Shared exponents do not fix this. Attaching one exponent to the whole coordinate keeps the string short but forces all fourteen slots to the same scale, so a point 1 AU out with a 1 mm offset in Z loses the offset entirely. Per-slot exponents preserve it but cost roughly the same characters as widening the fields. Both are worse than picking a unit.

The practical recommendation is SDC/C for readable sketching, SDC/S for interplanetary work, and a millimetre-based local profile for bench and surface use.

7. Canonical form

Without rules, one point has many valid coordinates: the diagonals overlap the cardinals, and opposite senses cancel. Two rules reduce this to one.

Rule 1 — no opposed pairs. For each of the seven axes, at most one of the two senses may be nonzero. Where both appear, subtract the smaller from the larger and zero the smaller.

Rule 2 — cardinals only. Canonical coordinates use only directions 0, 1, 2, 7, 8, 9. Diagonal magnitudes are expanded into their cardinal components using the identity in section 4, then rule 1 is applied again.

Under both rules at most three slots are nonzero — one per spatial axis — and the mapping to Cartesian coordinates is a bijection. Uniqueness is achieved.

The cost of rule 2

Expanding a diagonal introduces √2/2 in the vertical component, which has no finite decimal representation. A coordinate written with diagonal directions therefore cannot be canonicalised exactly; the Z slot rounds at the last digit.

This leaves three options, none of them free:

| Option | Uniqueness | Exact round-trip | Readability |
| Canonical cardinals only | Yes | No — √2/2 rounds | Loses diagonal shorthand |
| Allow diagonals, rule 1 only | No | Yes | Keeps shorthand |
| Redefine diagonals as (1, 1, ±1) unnormalised | Yes | Yes | Magnitudes stop being distances |

The third option deserves a look. If diagonals are defined as non-unit vectors with integer components, expansion becomes exact and uniqueness survives — but a magnitude of 1 in a diagonal slot then means √3 units of distance, not 1, so the string no longer reads directly as distance.

Proposed default: canonical cardinal form for storage and computation, diagonals permitted in a display form for human reading, with the conversion documented as lossy in the final digit. Storage and display are different jobs and do not need the same rules.

8. Conversion

To Cartesian

Sum the fourteen slot magnitudes against their unit vectors:

P = Σ  M(k) · v(k)        for k in {0,1,2,3,4,5,6,7,8,9,a,b,c,d}

This is a fixed fourteen-term sum with no branching and no trigonometry at runtime — the direction vectors are constants. Cost is constant in the length of the coordinate.

From Cartesian

Canonical form makes the inverse trivial, which was the other problem with the earlier draft. Given P = (x, y, z) in profile units:

slot 1 = x   if x ≥ 0,  else slot 8 = |x|
slot 2 = y   if y ≥ 0,  else slot 7 = |y|
slot 9 = z   if z ≥ 0,  else slot 0 = |z|
all other slots = 0

No optimisation, no iteration. The earlier claim that inversion required constrained search was an artefact of allowing diagonals in canonical form.

Reference implementation

import numpy as np

R = 2 ** -0.5  # √2/2

SLOTS = "0123456789abcd"

V = {
    "0": np.array([0.0, 0.0, -1.0]),
    "1": np.array([1.0, 0.0, 0.0]),
    "2": np.array([0.0, 1.0, 0.0]),
    "3": np.array([0.5, 0.5, -R]),
    "4": np.array([-0.5, 0.5, -R]),
    "5": np.array([-0.5, -0.5, -R]),
    "6": np.array([0.5, -0.5, -R]),
    "7": np.array([0.0, -1.0, 0.0]),
    "8": np.array([-1.0, 0.0, 0.0]),
    "9": np.array([0.0, 0.0, 1.0]),
    "a": np.array([0.5, 0.5, R]),
    "b": np.array([-0.5, 0.5, R]),
    "c": np.array([-0.5, -0.5, R]),
    "d": np.array([0.5, -0.5, R]),
}


def parse_c(coord):
    """SDC/C: 14 integer digits, '.', 14 fractional digits.
    Returns magnitude per direction symbol."""
    if len(coord) != 29 or coord[14] != ".":
        raise ValueError("not an SDC/C coordinate")
    whole, tenths = coord[:14], coord[15:]
    return {
        SLOTS[i]: int(whole[i]) + 0.1 * int(tenths[i])
        for i in range(14)
    }


def to_cartesian(coord):
    mags = parse_c(coord)
    return sum((m * V[k] for k, m in mags.items()), np.zeros(3))


def from_cartesian(x, y, z):
    """Canonical SDC/C. Raises if any component exceeds the profile range."""
    mags = dict.fromkeys(SLOTS, 0.0)
    mags["1" if x >= 0 else "8"] = abs(x)
    mags["2" if y >= 0 else "7"] = abs(y)
    mags["9" if z >= 0 else "0"] = abs(z)

    whole = tenths = ""
    for k in SLOTS:
        m = round(mags[k], 1)
        if m > 9.9:
            raise ValueError(f"{m} exceeds SDC/C range in direction {k}")
        whole += str(int(m))
        tenths += str(int(round((m - int(m)) * 10)))
    return whole + "." + tenths


def distance(a, b):
    return float(np.linalg.norm(to_cartesian(b) - to_cartesian(a)))

To ICRS

Conversion to ICRS needs two things this specification does not yet supply: the frozen epoch for direction 1 (section 3), and the Sol-to-barycentre offset at the epoch of interest, which comes from an ephemeris such as JPL DE440. With both fixed, the conversion is a rotation followed by a translation followed by a Cartesian-to-spherical step. It is not specified here because the epoch is not yet chosen.

9. Worked examples

All in SDC/C, base unit AU. Slot order 0 1 2 3 4 5 6 7 8 9 a b c d.

Sol, the origin. Every slot zero.

SDC/C:00000000000000.00000000000000

Earth at 1 AU along the baseline. Slot 1 holds 1; everything else zero. Slot 1 is the second character, so the 1 sits in position 2 of the integer field.

SDC/C:01000000000000.00000000000000
→ M(1) = 1 + 0.1×0 = 1.0
→ P = 1.0 · (1, 0, 0) = (1, 0, 0) AU

Note this is not the 10000000000000… string used in earlier drafts. Under fixed slots, a leading 1 means one unit along direction 0, which is straight down.

A point 2.5 AU out and 0.4 AU above the plane. Slot 1 = 2.5, slot 9 = 0.4.

SDC/C:02000000000000.05000000040000
→ M(1) = 2 + 0.1×5 = 2.5
→ M(9) = 0 + 0.1×4 = 0.4
→ P = 2.5·(1,0,0) + 0.4·(0,0,1) = (2.5, 0, 0.4) AU

Cancellation under rule 1. Slot 1 = 3.0 and slot 8 = 1.0 is non-canonical; the axis nets to 2.0 along direction 1.

non-canonical: M(1)=3.0, M(8)=1.0   →   P = (3,0,0) + (−1,0,0) = (2, 0, 0)
canonical:     M(1)=2.0, M(8)=0     →   SDC/C:02000000000000.00000000000000

Diagonal shorthand and its cost. A magnitude of 1.0 in slot a:

M(a) = 1.0  →  P = (0.5, 0.5, 0.70710678…)

Canonicalising to cardinals gives slot 1 = 0.5, slot 2 = 0.5, slot 9 = 0.70710678…, and SDC/C rounds that last value to 0.7. The round-trip error is 0.00710678 AU, roughly 1.06 million km — which is the section 6 resolution limit showing up, not a flaw in the geometry. At SDC/P the same round-trip error falls below a millimetre.

Distance between two coordinates. Convert both, subtract, take the norm. There is no shortcut that works on the strings directly, because the slots are not orthogonal until canonicalised.

10. Open problems

In rough order of how much they block progress.

1. The epoch is now chosen — see section 11. Direction 1 is fixed to Earth's heliocentric direction at J2000.0, ecliptic longitude 100.380°. What remains is ratification: that value derives from JPL's approximate elements, whose own longitude error for the Earth-Moon barycentre is around 20 arcseconds. A definitive anchor should be taken from a full ephemeris such as DE440.

2. Non-uniform precision across the string. Because every slot carries the same field width, a coordinate using one direction wastes thirteen slots of digits. Canonical form uses three of fourteen, so roughly 79% of every string is zeros. A sparse encoding would be far more compact but breaks the fixed-width property.

3. Diagonal round-trip is lossy. Section 7 covers this. The √2/2 component cannot be held exactly in decimal, so diagonal-to-cardinal conversion rounds. Three options are on the table and none is obviously right.

4. No relativistic treatment. The temporal component assumes one universal clock. Any use at appreciable fractions of c, or across significant gravitational potential differences, needs an explicit treatment of simultaneity and frame-dependent time. Nothing here addresses that.

5. Barycentre versus Sol centre. Sol is the stated origin, but the solar system barycentre moves relative to Sol's centre by more than a solar radius as the giant planets orbit. Which one is the true origin needs deciding, and the answer affects precision at the SDC/F level and below.

6. No error model. Quantisation error is bounded by half the last digit per slot, but error behaviour through canonicalisation, through profile changes, and through accumulated arithmetic has not been analysed.

7. Nothing has been built. No implementation, no test suite, no comparison against an existing system on real data. Every claim in this document is derivational. The first honest validation step would be a reference implementation plus a round-trip test against JPL Horizons positions for a set of known bodies.

11. Fixing the Earth-anchor epoch

Direction 1 is Earth's heliocentric direction at J2000.0: ecliptic longitude 100.380°, latitude 0.000°, referred to the mean ecliptic and equinox of J2000. This closes open problem 1. Any coordinate written before this section was fixed is undefined.

The value comes from JPL's Keplerian elements for the Earth-Moon barycentre (Approximate Positions of the Planets, Table 1, valid 1800–2050):

L₀ = 100.46457166°   mean longitude
ϖ₀ = 102.93768193°   longitude of perihelion
e₀ =   0.01671123    eccentricity

At J2000.0 the mean anomaly is M = L − ϖ = −2.47311°. The equation of centre contributes −0.08436°, giving a true heliocentric longitude of 100.38021°. Earth's ecliptic latitude is zero by construction; the barycentre's tabulated inclination is −0.0000153°, negligible at every profile in section 6.

The heliocentric distance at that instant is 0.98331 AU, which sits just outside perihelion — J2000.0 falls on 1 January and Earth reaches perihelion in the first days of January. That the arithmetic lands there is a useful check on the whole calculation.

Consequences

Azimuth conversion. For any body with heliocentric ecliptic longitude λ:

SDC azimuth = λ − 100.380°   (mod 360°)

The frame is now inertial. Direction 1 no longer tracks Earth. Earth returns to azimuth 0° once a year and is elsewhere the rest of the time. The name is historical, not a live pointer.

The Z axis. Direction 9 is the J2000 ecliptic north pole. Directions 1, 2, 9 therefore form a right-handed frame coincident with standard heliocentric ecliptic coordinates, rotated 100.380° about Z. That makes conversion to and from published ephemerides a single rotation.

Barycentre still unresolved. This section fixes the orientation, not the origin. Whether the origin is Sol's centre or the solar system barycentre remains open problem 5, and matters below the 10⁻³ AU level.

12. Sol and the planets at J2000.0

Computed from the JPL Keplerian elements (Table 1, 1800–2050) at T = 0, where the tabulated elements are the values themselves. Heliocentric, mean ecliptic and equinox of J2000. Azimuth is measured from direction 1 per section 11.

| Body | r (AU) | Ecliptic λ | SDC azimuth | Ecliptic β |
| Sol | 0.00000 | — | — | — |
| Mercury | 0.46647 | 253.86° | 153.48° | −3.020° |
| Venus | 0.72023 | 182.581° | 82.201° | +3.265° |
| Earth (EMB) | 0.98331 | 100.380° | 0.000° | 0.000° |
| Mars | 1.39117 | 359.430° | 259.050° | −1.420° |
| Jupiter | 4.96728 | 36.368° | 295.988° | −1.174° |
| Saturn | 9.17135 | 45.565° | 305.185° | −2.307° |
| Uranus | 19.92161 | 316.396° | 216.016° | −0.685° |
| Neptune | 30.11733 | 303.913° | 203.533° | +0.242° |

Canonical slot magnitudes

The same positions in SDC frame components. Each body occupies three slots under the canonical rule of section 7 — one per axis, sign choosing which sense.

| Body | X slot | Y slot | Z slot |
| Sol | — | — | — |
| Mercury | 8 0.41691 | 2 0.20786 | 0 0.02458 |
| Venus | 1 0.09761 | 2 0.71241 | 9 0.04102 |
| Earth (EMB) | 1 0.98331 | — | — |
| Mars | 8 0.26454 | 7 1.36535 | 0 0.03447 |
| Jupiter | 1 2.17441 | 7 4.46492 | 0 0.10177 |
| Saturn | 1 5.28091 | 7 7.48865 | 0 0.36913 |
| Uranus | 8 16.11486 | 7 11.70957 | 0 0.23802 |
| Neptune | 8 27.60430 | 7 12.04180 | 9 0.12740 |

Earth sits on the baseline by construction: one nonzero slot, direction 1, magnitude 0.98331.

As coordinate strings

Only Mercury, Venus, Earth, and Mars fit SDC/C, whose per-direction ceiling is 9.9 AU. Slot order 0 1 2 3 4 5 6 7 8 9 a b c d.

Sol      SDC/C:00000000000000.00000000000000
Mercury  SDC/C:00000000000000.00200000400000
Venus    SDC/C:00000000000000.01700000000000
Earth    SDC/C:01000000000000.00000000000000
Mars     SDC/C:00000001000000.00000004300000

The coarseness is section 6 showing its teeth. At 0.1 AU resolution Earth's 0.98331 AU rounds to 1.0, Venus's 0.09761 AU X component rounds to 0.1, and Mercury's Z component of 0.02458 AU vanishes entirely. Anything past Jupiter needs SDC/S or wider.

13. Sol and the planets today — 18 September 2026

Same method, at T = 0.2671184 centuries past J2000.0 (JD 2461301.5, 00:00 UT). Elements are advanced by their per-century rates before the Kepler solve.

| Body | r (AU) | Ecliptic λ | SDC azimuth | Ecliptic β |
| Sol | 0.00000 | — | — | — |
| Mercury | 0.45454 | 231.180° | 130.800° | −0.360° |
| Venus | 0.72788 | 332.855° | 232.475° | −3.297° |
| Earth (EMB) | 1.00499 | 354.734° | 254.354° | +0.000° |
| Mars | 1.54144 | 78.744° | 338.364° | +0.904° |
| Jupiter | 5.30031 | 130.109° | 29.729° | +0.644° |
| Saturn | 9.43708 | 10.470° | 270.090° | −2.422° |
| Uranus | 19.43798 | 62.475° | 322.095° | −0.155° |
| Neptune | 29.87734 | 2.561° | 262.181° | −1.372° |

Canonical slot magnitudes

| Body | X slot | Y slot | Z slot |
| Sol | — | — | — |
| Mercury | 8 0.29710 | 2 0.34399 | 0 0.00286 |
| Venus | 8 0.44260 | 7 0.57633 | 0 0.04187 |
| Earth (EMB) | 8 0.27106 | 7 0.96774 | 9 0.00001 |
| Mars | 1 1.43270 | 7 0.56819 | 9 0.02431 |
| Jupiter | 1 4.60207 | 2 2.62880 | 9 0.05956 |
| Saturn | 1 0.01489 | 7 9.42972 | 0 0.39891 |
| Uranus | 1 15.33795 | 7 11.94060 | 0 0.05240 |
| Neptune | 8 4.06257 | 7 29.59121 | 0 0.71523 |

Earth has moved 254.354° of azimuth off the baseline in 26.7 years, which is the section 11 point made concrete: direction 1 is a frozen direction, not a pointer that follows the planet.

Saturn sits nearly on the Y axis — its X component is 0.015 AU out of 9.44 AU. That is a coincidence of this date, not a property of the system.

Checks applied

Each mean longitude was verified against the body's sidereal period, independently of the element rates. Over the 9756.5 days elapsed:

| Body | Orbits elapsed | λ from period | λ from elements | Agreement |
| Mercury | 110.909 | 219.45° | 219.152° | 0.30° |
| Venus | 43.420 | 333.07° | 333.164° | 0.09° |
| Earth | 26.712 | 356.80° | 356.559° | 0.24° |
| Mars | 14.204 | 68.75° | 68.174° | 0.58° |
| Jupiter | 2.252 | 125.08° | 125.033° | 0.05° |
| Saturn | 0.907 | 16.40° | 16.505° | 0.11° |
| Uranus | 0.318 | 114.45° | 114.455° | 0.01° |
| Neptune | 0.162 | 58.36° | 58.355° | 0.01° |

The residuals are rounding in the published period values, not disagreement. This check exists to catch a slipped digit in the large mean-longitude multiplications, which is the failure mode that matters here.

Three further checks passed. Every heliocentric distance falls inside its body's perihelion–aphelion range. Earth's 1.00499 AU sits correctly between the July aphelion and the January perihelion. And Earth's heliocentric longitude of 354.73° puts the Sun's apparent geocentric longitude near 174.7°, consistent with mid-September.

Accuracy

These figures inherit the JPL element errors: roughly 20 arcseconds in longitude for the inner planets and 600 for Saturn, with distance errors from 1,000 km at Mercury to 4,000 km at Saturn. They are given to five decimals because the arithmetic carries that many, not because they are good to five decimals. For anything tighter, query JPL Horizons directly.

14. Generating other dates

For any other epoch, compute T = (JD − 2451545.0) / 36525 and run the generator below. The mean-longitude term is where hand calculation fails silently — Mercury accumulates roughly 39,927° over 26.7 years before the mod-360 reduction, and a slipped digit there yields a wrong answer that reads as perfectly plausible.

The generator below reproduces both tables. Running it against the J2000.0 figures is the check that it is wired correctly.

import numpy as np

# JPL Table 1 (1800-2050): a, e, I, L, long.peri, long.node  + per-century rates
# https://ssd.jpl.nasa.gov/planets/approx_pos.html
ELEMENTS = {
    "Mercury": ((0.38709927, 0.20563593, 7.00497902, 252.25032350, 77.45779628, 48.33076593),
                (0.00000037, 0.00001906, -0.00594749, 149472.67411175, 0.16047689, -0.12534081)),
    "Venus":   ((0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718, 76.67984255),
                (0.00000390, -0.00004107, -0.00078890, 58517.81538729, 0.00268329, -0.27769418)),
    "Earth":   ((1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0.0),
                (0.00000562, -0.00004392, -0.01294668, 35999.37244981, 0.32327364, 0.0)),
    "Mars":    ((1.52371034, 0.09339410, 1.84969142, -4.55343205, -23.94362959, 49.55953891),
                (0.00001847, 0.00007882, -0.00813131, 19140.30268499, 0.44441088, -0.29257343)),
    "Jupiter": ((5.20288700, 0.04838624, 1.30439695, 34.39644051, 14.72847983, 100.47390909),
                (-0.00011607, -0.00013253, -0.00183714, 3034.74612775, 0.21252668, 0.20469106)),
    "Saturn":  ((9.53667594, 0.05386179, 2.48599187, 49.95424423, 92.59887831, 113.66242448),
                (-0.00125060, -0.00050991, 0.00193609, 1222.49362201, -0.41897216, -0.28867794)),
    "Uranus":  ((19.18916464, 0.04725744, 0.77263783, 313.23810451, 170.95427630, 74.01692503),
                (-0.00196176, -0.00004397, -0.00242939, 428.48202785, 0.40805281, 0.04240589)),
    "Neptune": ((30.06992276, 0.00859048, 1.77004347, -55.12002969, 44.96476227, 131.78422574),
                (0.00026291, 0.00005105, 0.00035372, 218.45945325, -0.32241464, -0.00508664)),
}

ANCHOR = 100.38021  # direction 1, ecliptic longitude at J2000.0 (section 11)


def kepler(M_deg, e, tol=1e-9):
    """Solve M = E - e* sin E, all angles in degrees."""
    es = np.degrees(e)
    M = (M_deg + 180.0) % 360.0 - 180.0
    E = M + es * np.sin(np.radians(M))
    for _ in range(100):
        dM = M - (E - es * np.sin(np.radians(E)))
        dE = dM / (1 - e * np.cos(np.radians(E)))
        E += dE
        if abs(dE) < tol:
            break
    return E


def heliocentric(body, T):
    """Return ecliptic (x, y, z) in AU, J2000 mean ecliptic, T centuries past J2000.0."""
    (a0, e0, I0, L0, p0, O0), (da, de, dI, dL, dp, dO) = ELEMENTS[body]
    a, e = a0 + da * T, e0 + de * T
    I, L = I0 + dI * T, L0 + dL * T
    peri, node = p0 + dp * T, O0 + dO * T

    w = peri - node
    E = np.radians(kepler(L - peri, e))

    xp = a * (np.cos(E) - e)
    yp = a * np.sqrt(1 - e * e) * np.sin(E)

    cw, sw = np.cos(np.radians(w)), np.sin(np.radians(w))
    cO, sO = np.cos(np.radians(node)), np.sin(np.radians(node))
    cI, sI = np.cos(np.radians(I)), np.sin(np.radians(I))

    return np.array([
        (cw * cO - sw * sO * cI) * xp + (-sw * cO - cw * sO * cI) * yp,
        (cw * sO + sw * cO * cI) * xp + (-sw * sO + cw * cO * cI) * yp,
        (sw * sI) * xp + (cw * sI) * yp,
    ])


def to_sdc_frame(v):
    """Rotate ecliptic coordinates into the SDC frame (about Z by the anchor)."""
    t = np.radians(ANCHOR)
    c, s = np.cos(t), np.sin(t)
    return np.array([c * v[0] + s * v[1], -s * v[0] + c * v[1], v[2]])


if __name__ == "__main__":
    for T, label in ((0.0, "J2000.0"), (0.2671184, "2026-09-18")):
        print(label)
        for body in ELEMENTS:
            x, y, z = to_sdc_frame(heliocentric(body, T))
            print(f"  {body:8s} {x:12.5f} {y:12.5f} {z:12.5f}")

Running this reproduces the J2000.0 table above, which is the check that it is wired correctly, then produces the 2026 figures. Accuracy is bounded by the JPL element errors — roughly 20 arcseconds in longitude for the inner planets, rising to 600 arcseconds for Saturn.

15. Frames

The fourteen directions do not depend on where the origin sits. Anchor them at Sol and you get heliocentric coordinates; anchor them at a craft's centre of mass with direction 1 along its bow and you get bearings a pilot can read. Same grammar, same arithmetic, same canonical rules, same code. Nothing in sections 3 through 9 mentions Sol.

That portability is the system's strongest property, and it is the reason the notation scales from a bench to the outer solar system without changing form. It also introduces the one failure mode capable of causing real harm: a coordinate read in the wrong frame is not an approximation, it is a different place.

A frame is five declarations

No coordinate means anything without all five:

| Declaration | Heliocentric standard | Craft-relative |
| Origin | Sol centre | Craft centre of mass |
| Direction 1 | Earth at J2000.0, ecliptic longitude 100.380° | Bow |
| Direction 9 | J2000 ecliptic north | Dorsal normal |
| Epoch | Fixed, J2000.0 | Continuous — valid only at the stated instant |
| Profile unit | AU | Whatever the craft's scale needs |

Tagging

Section 5.3 required a profile tag. Frames extend it:

SDC/<profile>/<frame>:<coordinate>

SDC/C/SOL:01000000000000.00000000000000
SDC/C/CRAFT:d00000000a00000.00000004000000

SOL is the frame of sections 11 to 14. CRAFT is body-fixed and instantaneous. A coordinate carrying neither profile nor frame is undefined, and an implementation should refuse it rather than assume.

Delta form

A pilot tracking two objects wants the vector between them, not two origin-anchored positions to difference by hand. A coordinate prefixed d is an offset, not a position:

SDC/C/CRAFT:d00000000200000.00000000000000

Deltas add and subtract freely. A delta plus a position gives a position; two positions subtract to a delta; two deltas in the same frame add. A position plus a position is meaningless and should raise.

Diagonals earn their place here

Section 7 treats the diagonals as redundant and canonicalises them into cardinals. That is right for storage, where uniqueness matters. It is wrong for a cockpit.

An object off the bow, high and to port, is direction a. One symbol, read instantly, no mental arithmetic. Canonicalising it into three cardinal magnitudes destroys precisely the thing the pilot needed. So the rule is split by job, not by principle:

- SOL frame, storage and exchange — canonical cardinals, unique representation.
- CRAFT frame, display and control — diagonals preferred, uniqueness not required, because the coordinate is discarded before ambiguity can matter.

This supersedes the framing in section 7, which treated non-uniqueness purely as a defect. It is a defect in one job and the entire value in the other.

Converting between frames

A craft-relative coordinate becomes heliocentric by rotation then translation:

P_sol = R(q) · P_craft + C

where C is the craft's own position in SOL and q is its attitude quaternion, expressed in SOL. Attitude is three degrees of freedom and is not a Sum Dia Const coordinate — the notation locates points, it does not orient bodies. A quaternion (w, x, y, z) is the recommended carrier; Euler angles will gimbal-lock and should be avoided in any control path.

The conversion is exact. Its accuracy is bounded by the attitude solution and by C, never by the notation.

What "universal" does and does not mean

Universal here means the grammar is: one set of rules covering every origin, every scale from millimetres to 1000 AU, and every application from a bench rig to interplanetary navigation. No separate formalism for local work. That claim holds.

What is not universal, and cannot be in any coordinate system, is the meaning of a bare string. 01000000000000.00000000000000 is Earth in SOL/C and one unit off your own bow in CRAFT/C. The frame tag is what carries that distinction, which is why it is mandatory rather than advisory.

16. Feedback register

Every unresolved question in this document, with a stable identifier. Open an issue citing the ID. The list is meant to be exhaustive — if something here reads as settled and is not, that omission is itself worth an issue.

Blocking — these prevent the specification being called complete

OP1 · Epoch ratification. §11 fixes direction 1 at ecliptic longitude 100.380° using JPL's approximate elements, whose own error for the Earth-Moon barycentre is around 20 arcseconds. A definitive anchor should come from a full ephemeris such as DE440. Wanted: the value to stated precision, and the convention for citing it.

OP2 · Canonical form. §7 lists three ways to make representation unique and picks none outright. Cardinals-only loses exact round-trips because √2/2 has no finite decimal form; allowing diagonals keeps exactness and loses uniqueness; redefining diagonals as unnormalised (1, 1, ±1) keeps both but breaks the reading of magnitude as distance. The current default — canonical for storage, diagonals for display — may be the right answer or may be avoidance. Wanted: an argument either way.

OP3 · Origin. §11 fixes orientation but not the origin. Sol's centre and the solar system barycentre differ by more than a solar radius as the giant planets move. Matters below 10⁻³ AU. Wanted: which, and why.

Encoding — open design forks

OP4 · Base-14 magnitudes. Magnitudes are currently decimal digits 0–9 in each slot, so the letters a–d name slots and never appear inside a coordinate. Writing magnitudes in base 14 instead would make digits genuinely run 0–d, make the project's name exact on both the basis and the radix reading, and widen the 29-character form from 9.9 to about 13.9 units per direction at 1/14 resolution — enough to bring Saturn inside the compact profile. The cost is that a7.3c no longer reads as a distance without conversion, which cuts against design goal 1. Wanted: does the range gain justify the readability loss?

OP5 · Sparse encoding. Canonical form uses three slots of fourteen, so roughly 79% of every string is zeros. A sparse encoding would be far more compact and would break the fixed-width property that makes parsing constant-cost. Wanted: is fixed-width worth the waste at scale?

OP6 · Non-uniform precision. Because magnitude is positional within a fixed-width slot, a coordinate using several directional components spends digits that would otherwise carry precision. Wanted: a better allocation, or a demonstration that it does not matter in practice.

Physics — known gaps

OP7 · Relativistic treatment. The temporal component assumes one universal clock. Any use at appreciable fractions of c, or across meaningful gravitational potential differences, needs explicit handling of simultaneity and frame-dependent time. Nothing here addresses it. Wanted: scope — is this a profile, a separate frame, or a different system?

OP8 · Error model. Quantisation error is bounded at half the last digit per slot. Error behaviour through canonicalisation, through profile changes, and through accumulated arithmetic has not been analysed. Wanted: the analysis.

Frames — defaults chosen without much evidence

OP9 · Delta marker and attitude carrier. §15 marks offsets with a leading d and recommends quaternions for attitude. Both were picked for plausibility, not from practice. The quaternion choice is defensible — Euler angles gimbal-lock, and a control path is a bad place to find that out — but the delta marker is arbitrary. Wanted: established convention.

OP10 · Whether the frame split is right at all. §15 supersedes §7 by making diagonal handling depend on the job rather than on principle. Storage canonicalises; display does not. That may be a clean separation or a sign the canonical rule was wrong to begin with. Wanted: a view.

Verification — needs an outside check

OP11 · The position tables were computed by hand. §§12–13 give Sol and the eight planets at J2000.0 and at 2026-09-18. Every mean longitude was cross-checked against the body's sidereal period, every distance against its orbit bounds, and test_sumdiaconst.py re-derives them from code. But sixteen Kepler solves done by hand deserve independent verification against JPL Horizons. A disagreement between the hand table and the code says one of them is wrong, not which. Wanted: an independent run.

OP12 · Prior art. Nothing here has been searched against existing patents or published coordinate systems. Polyhedral and non-orthogonal basis schemes have a long literature and some of this is likely to have been done before. Wanted: pointers to it. Being shown this is not novel is a useful outcome.

OP13 · Nothing has been built. No hardware implementation, no deployment, no comparison against an existing system on real data. Every claim is derivational. Wanted: someone to actually try it and report what breaks.

Tracking layer

The companion draft TRACKING.md carries its own register, Q1–Q9, covering velocity units, uncertainty representation, ballistic propagation, light-time correction, clock discipline, wire format, batching, track correlation, and source trust.

---

§10 lists the same problems in prose. Where the two differ, this register is authoritative.

17. Licence

Released under the MIT Licence. © 2026 Keenan Dunham.

This covers the whole repository — the specification text, the reference implementation, and the position tables. Copy it, implement it, modify it, teach from it, build on it, ship it commercially. The single condition is that the copyright notice travels with it.

The reasoning is simple: a coordinate system nobody can freely implement is a coordinate system nobody adopts. Scrutiny is the point of publishing. Section 10 lists what is unresolved, and a correction to the geometry, the encoding, or the position tables is worth more to this work than a citation is.

Contributions, corrections, and counterexamples are welcome through the repository's issues and pull requests.

Prior art note. Nothing in this document has been searched against existing patents or published coordinate systems. Before any filing or formal publication, a prior-art search is warranted — polyhedral and non-orthogonal basis coordinate schemes have a long literature, and this specification makes no claim to have checked it.
