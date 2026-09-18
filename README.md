# sum-dia-const

A coordinate notation that locates any point relative to Sol using fourteen fixed directions.

> **Status: draft specification.** The geometry is settled. The encoding is new and expected to change. Nothing here has been implemented in hardware, deployed, or checked against an independent system. There are no benchmarks, trials, or third-party reviews, and none are claimed. Section 10 of the specification lists what is unresolved.

## The idea

One origin — Sol. One frozen baseline direction — where Earth sat at J2000.0. Fourteen directions radiating from the origin: six cardinal, eight diagonal at ±45° elevation. A coordinate is fourteen magnitudes, one per direction, and **position in the string names the direction**.

The fourteen turn out to be seven antipodal pairs, and every diagonal is an exact combination of three cardinals. That redundancy is deliberate. Diagonals make common bearings readable in one symbol; canonical form drops to cardinals only, so each physical point has exactly one representation.

## Quick look

```python
from sumdiaconst import from_cartesian, to_spherical

# Earth at J2000.0 — 0.98331 AU along the baseline
earth = from_cartesian(0.98331, 0.0, 0.0)
print(earth)                # 01000000000000.00000000000000
print(to_spherical(earth))  # (1.0, 0.0, 0.0)
```

Slot order is `0 1 2 3 4 5 6 7 8 9 a b c d`. The `1` lands in the second position because that is slot 1, the Earth-anchor direction. Characters are magnitudes 0–9; the letters `a`–`d` name slots, never values.

## Layout

| Path | What it holds |
| --- | --- |
| `paper/SPEC.md` | The notation — geometry, encoding, frames, canonical form, open problems |
| `paper/TRACKING.md` | SDC-Track draft 0: a proposed tracking layer. Anticipated design, nothing built |
| `sumdiaconst.py` | Reference implementation of the notation |
| `ephemeris.py` | Planet positions from JPL elements, in the SDC frame |
| `test_sumdiaconst.py` | Geometry invariants, round-trips, and the position tables |

```
pip install numpy pytest
pytest test_sumdiaconst.py
```

## Precision, honestly

Range and resolution come entirely from the field widths. The 29-character form gives each direction two significant digits — a whole part and one tenth — so at AU scale it resolves 0.1 AU and reaches 9.9 AU per direction. That is coarse, and it is what 29 characters across fourteen slots buys.

Finer work changes the profile, not the scheme. Millimetre resolution across a 1000 AU span needs nineteen digits per slot, or 280 characters. Choosing a base unit matched to the working scale is far cheaper than carrying every scale in one string.

## Accuracy of the bundled positions

The planet tables derive from [JPL's approximate Keplerian elements](https://ssd.jpl.nasa.gov/planets/approx_pos.html), whose own error runs from roughly 20 arcseconds of longitude for the inner planets to 600 for Saturn. They were computed by hand and cross-checked against each body's sidereal period; the test suite re-derives them from code. Where hand and code disagree, [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/) arbitrates.

## Review wanted

This is published to be checked, not admired. Both documents are drafts by one author working alone, and the failure mode of that is a mistake nobody catches until something is built on it.

The specific things worth an outside eye:

**The position tables were computed by hand.** Sections 12 and 13 of the spec give Sol and the eight planets at J2000.0 and at 2026-09-18, derived from JPL's approximate elements. Every mean longitude was cross-checked against the body's sidereal period, and every distance against its orbit bounds — but hand arithmetic across sixteen Kepler solves deserves independent verification. `test_sumdiaconst.py` re-derives them from code; a disagreement means one of the two is wrong and does not say which. JPL Horizons settles it.

**The encoding is new.** Fixed-slot — position in the string names the direction, and the value alphabet is digits 0–9 only. It replaces an earlier scheme where a character named both a direction and a magnitude, which was ambiguous. The replacement has not been stress-tested by anyone but its author.

**Thirteen open problems in the spec**, numbered OP1–OP13 in its section 16 feedback register — covering epoch ratification, the canonical-form fork, the Sol-centre versus barycentre origin, whether magnitudes should be base-14, sparse versus fixed-width encoding, relativistic treatment, the error model, the frame split, prior art, and independent verification of the position tables.

**Nine open questions in SDC-Track**, numbered Q1–Q9 in its section 9 — velocity units, uncertainty representation, ballistic propagation, light-time correction, clock discipline, wire format trade-offs, batching, track correlation, and source trust. Most have established answers in the tracking literature; pointers to prior art beat agreement.

Every marker is a stable identifier. **Cite the ID in the issue title** — `OP4: base-14 magnitudes` — so discussion stays attached to the question rather than scattering.

Issues and pull requests welcome. Corrections are more valuable here than stars.

## Licence

MIT. Use, modify, and redistribute the code freely; keep the copyright notice.

© 2026 Keenan Dunham.
