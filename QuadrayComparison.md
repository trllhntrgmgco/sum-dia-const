# Sum Dia Const (SDC) and Quadray Comparison

**Document:** QuadrayComparison.md  
**Subject:** Mathematical and architectural comparison of Sum Dia Const (SDC) and Quadray  
**Date:** September 18, 2026

## 1. Purpose

This document compares **Sum Dia Const (SDC)** with **Quadray coordinates**, with particular attention to their mathematical structures, canonicalization methods, notation, implementation, and intended applications.

The comparison is intended to distinguish shared mathematical principles from the parts of SDC that constitute its particular design.

This is a technical comparison, not a claim that either system replaces the other.

---

## 2. Executive Summary

SDC and Quadray share an important mathematical characteristic: both represent ordinary three-dimensional space using an **overcomplete, non-orthogonal directional representation**.

They are nevertheless different systems.

Quadray uses **four tetrahedral basis directions** associated with the vertices of a regular tetrahedron. SDC uses **fourteen fixed spatial directions**: six cardinal directions and eight diagonal directions.

The central difference is the reason for the directional vocabulary:

- **Quadray:** tetrahedral geometry is the organizing principle.
- **SDC:** human-readable directional notation is the organizing principle, with the coordinate system additionally anchored to Sol for astronomical use.

SDC further defines a fixed-width textual representation, an astronomical reference frame, precision profiles, a Python reference implementation, planetary ephemeris calculations, and the proposed SDC-Track layer.

Accordingly, SDC is best described as a **fourteen-direction spatial coordinate notation and reference implementation for representing positions relative to Sol**, rather than simply as "Base-14 Quadray."

---

# 3. What the SDC Repository Defines

The current SDC repository contains more than a mathematical description. It includes:

- `README.md` — overview and design rationale
- `SPEC.md` — the main specification
- `TRACKING.md` — SDC-Track proposal
- `sumdiaconst.py` — reference implementation
- `ephemeris.py` — planetary-position calculations
- `test_sumdiaconst.py` — geometry and computational tests
- `LICENSE` — MIT license

The implementation provides functionality including validation, parsing/formatting, canonicalization, Cartesian conversion, spherical conversion, distance calculations, and astronomical position calculations.

The test suite checks the direction set, antipodal relationships, diagonal/cardinal relationships, three-dimensional span, canonicalization, Cartesian round trips, distance calculations, orbital calculations, planetary positions, and the fixed Earth J2000 baseline.

The original specification also explicitly states that SDC's architecture is not presented as wholly unprecedented. It identifies Quadray as the closest prior mathematical precedent and describes SDC as a new arrangement of established components.

---

# 4. Mathematical Structure

## 4.1 Quadray

Quadray represents three-dimensional space using four non-orthogonal directions corresponding to the rays from the center of a regular tetrahedron to its four vertices.

One convenient normalized Cartesian realization is:

\[
A=\frac{(1,1,1)}{\sqrt3}
\]

\[
B=\frac{(1,-1,-1)}{\sqrt3}
\]

\[
C=\frac{(-1,1,-1)}{\sqrt3}
\]

\[
D=\frac{(-1,-1,1)}{\sqrt3}
\]

These four vectors satisfy:

\[
A+B+C+D=0
\]

Consequently, a Quadray coordinate tuple is not unique before normalization. Adding the same quantity \(k\) to every component does not change the represented vector:

\[
(a,b,c,d)\equiv(a+k,b+k,c+k,d+k)
\]

A common positive normalization is obtained by subtracting the minimum component so that at least one coordinate becomes zero.

This gives Quadray four coordinates for a three-dimensional vector: an intentionally redundant representation.

---

## 4.2 SDC

SDC defines fourteen fixed unit directions:

- six cardinal directions:
  - +X
  - -X
  - +Y
  - -Y
  - +Z
  - -Z
- eight diagonal directions at ±45° elevation and azimuths 45°, 135°, 225°, and 315°.

The fourteen directions form seven antipodal pairs.

The six cardinal directions already span all of three-dimensional Cartesian space. The eight diagonals therefore do not add independent dimensions. Instead, they provide additional directional vocabulary.

For example, one SDC diagonal is:

\[
a=\frac12(1)+\frac12(2)+\frac{\sqrt2}{2}(9)
\]

where directions 1 and 2 provide horizontal components and direction 9 provides the positive Z component.

Thus SDC is also an overcomplete representation of three-dimensional space, but its redundancy is organized differently from Quadray's tetrahedral redundancy.

---

# 5. The Key Similarity: Overcomplete Representation

The deepest mathematical similarity is:

> Both systems represent three-dimensional vectors using more directional components than are mathematically necessary and then require a normalization/canonicalization concept to obtain a preferred representation.

Quadray uses four coordinates for three dimensions.

SDC provides fourteen directional slots for three dimensions.

Neither system should be interpreted as having fourteen or four independent spatial dimensions.

They are alternative representations of the same underlying three-dimensional vector space.

---

# 6. The Key Difference: Why the Redundancy Exists

The source of the redundancy differs.

### Quadray

Quadray's four directions are tied directly to regular tetrahedral geometry.

Its equivalence arises from the relationship:

\[
A+B+C+D=0
\]

and therefore equal quantities can be added to all four coordinates without changing the represented point.

### SDC

SDC's redundancy comes from its directional vocabulary.

The system includes:

- antipodal directions, which can cancel;
- diagonal directions that can be expanded into cardinal components;
- six cardinal directions that already completely span 3D.

SDC canonicalization therefore proceeds through antipodal cancellation and conversion to cardinal directions.

This means:

> **Quadray redundancy is tetrahedral-coordinate redundancy; SDC redundancy is directional-representation redundancy.**

That is an important distinction.

---

# 7. Explicit SDC-to-Quadray Mapping

SDC and Quadray can be connected through their common Cartesian vector space.

Using the tetrahedral Quadray basis above, every SDC direction has an exact Quadray representation at the vector level.

## 7.1 SDC Cardinal Directions

The six cardinal directions map to normalized Quadray tuples as follows:

| SDC | Cartesian direction | Canonical Quadray representation |
|---|---|---|
| `1` | +X | `(√3/2, √3/2, 0, 0)` |
| `8` | -X | `(0, 0, √3/2, √3/2)` |
| `2` | +Y | `(√3/2, 0, √3/2, 0)` |
| `7` | -Y | `(0, √3/2, 0, √3/2)` |
| `9` | +Z | `(√3/2, 0, 0, √3/2)` |
| `0` | -Z | `(0, √3/2, √3/2, 0)` |

Therefore every SDC cardinal direction has an exact Quadray equivalent.

## 7.2 Example Diagonal

SDC direction `a` is:

\[
a=(0.5,0.5,\frac{\sqrt2}{2})
\]

Under the selected Quadray basis, one normalized nonnegative representation is:

\[
a=
\left(
\frac{\sqrt3}{4}(1+\sqrt2),
0,
0,
\frac{\sqrt3}{4}(\sqrt2-1)
\right)
\]

Numerically this is approximately:

\[
(1.04538514,0,0,0.17935973)
\]

Thus the SDC diagonal also has an exact vector-level Quadray representation.

The presence of \(\sqrt2\) in the diagonal representation illustrates the geometric difference between SDC's 45° diagonals and Quadray's tetrahedral directions.

---

# 8. SDC Is Not Simply "14-Coordinate Quadray"

Although a conversion exists, describing SDC as "Quadray with fourteen coordinates" would obscure the important design differences.

A simplified conceptual pipeline for SDC is:

```text
14-direction representation
          ↓
      Cartesian vector
          ↓
canonical cardinal representation
```

Quadray instead follows the conceptual structure:

```text
4 tetrahedral components
          ↓
  redundant 4-coordinate vector
          ↓
  tetrahedral normalization
```

The two can therefore coexist as alternative representations of a Cartesian vector.

A conversion layer could theoretically allow software using one representation to consume positions expressed in the other.

---

# 9. SDC's Human-Readable Directional Vocabulary

One of SDC's most important design choices is that the fourteen directions are intended to be meaningful as directions, not merely as abstract mathematical basis vectors.

The cardinal directions have direct geometric interpretation.

The diagonal directions provide one-symbol directional bearings rather than requiring a user to mentally combine multiple axes.

This is especially relevant to SDC's stated use in location and telemetry.

Quadray's tetrahedral basis has a strong geometric rationale, but SDC's basis is deliberately chosen around a directional vocabulary that can be read by a human.

Therefore the systems optimize for different things:

- Quadray emphasizes tetrahedral geometric structure.
- SDC emphasizes directional readability and a standardized spatial notation.

---

# 10. Fixed-Width Text Encoding

SDC adds an encoding layer that is not intrinsic to Quadray.

The SDC specification defines fixed directional slots:

```text
0 1 2 3 4 5 6 7 8 9 a b c d
```

The position of a character identifies the direction, while the character's magnitude represents the amount associated with that direction.

The specification defines fixed precision profiles and requires a profile tag because unit and width can vary.

This creates a machine-readable textual notation in addition to the underlying vector mathematics.

Quadray itself does not inherently require SDC's fixed-width 14-slot string format.

---

# 11. An Important Terminology Issue: "Base-14"

The current SDC design uses fourteen direction slots, but its magnitude encoding is not yet a pure radix-14 numerical system.

The direction identifiers use:

```text
0 1 2 3 4 5 6 7 8 9 a b c d
```

while the current magnitude digits are decimal.

The specification itself identifies this as an open problem and considers a future true base-14 magnitude system in which `0–d` would also be numerical digits.

Therefore the most technically precise current description is:

> **fourteen-direction SDC notation**

or:

> **SDC's 14-direction coordinate encoding**

rather than implying that the present magnitude system is already fully radix-14.

---

# 12. Astronomical Reference Frame

This is one of the strongest distinctions between SDC and Quadray.

SDC explicitly defines:

- **Sol as the origin**
- direction `1` as Earth's heliocentric direction at J2000.0
- direction `9` as J2000 ecliptic north.

The astronomical implementation then uses this frame when converting planetary positions.

Quadray does not inherently specify this astronomical reference frame.

This means SDC is not merely defining a mathematical basis. It defines a particular **astronomical coordinate context**.

A useful conceptual comparison is:

```text
Quadray:
    geometric coordinate framework

SDC:
    geometric coordinate framework
             +
    directional notation
             +
    fixed textual encoding
             +
    astronomical reference frame
```

---

# 13. SDC Reference Implementation

The GitHub repository turns the specification into executable software.

The reference implementation handles the SDC direction definitions and coordinate operations, including:

- coordinate validation;
- parsing and formatting;
- canonicalization;
- conversion to Cartesian coordinates;
- conversion from Cartesian coordinates;
- spherical conversion;
- distance calculation.

This is significant because it makes SDC testable as an implemented notation rather than only as a theoretical proposal.

The test suite checks both individual geometric properties and round-trip behavior.

---

# 14. Astronomical / Ephemeris Layer

The repository also contains an ephemeris component.

This allows astronomical positions to be expressed through the SDC frame rather than treating the coordinate system as an abstract geometry exercise.

The distinction is important:

> Quadray answers how a point can be represented geometrically.

> SDC additionally asks how a point can be represented in a standardized astronomical frame centered on Sol.

That application layer is outside the basic Quadray concept.

---

# 15. SDC-Track

`TRACKING.md` extends the architecture further.

It distinguishes a coordinate from a track:

> A coordinate describes a place; a track describes an object's state at a particular instant, including time and uncertainty.

This creates a conceptual separation between:

```text
SDC
=
position representation
```

and:

```text
SDC-Track
=
position
+
time
+
velocity/state information
+
uncertainty
+
source/context
```

The proposed tracking architecture also separates the SOL reference frame from craft-relative frames and treats attitude as something that clients can derive rather than making it part of the central positional coordinate.

This is an application/protocol architecture rather than something directly corresponding to Quadray's mathematical definition.

---

# 16. Canonicalization and Exactness

SDC's geometry is exact at the vector-definition level.

However, the compact decimal textual profiles introduce finite precision.

The diagonal vectors contain \(\sqrt2/2\). When diagonal components are converted to finite decimal magnitudes, exact values cannot generally be preserved indefinitely.

The repository's tests therefore account for numerical tolerance during compact-profile round trips.

This distinction should be maintained:

### Exact geometric definition

The SDC direction vectors can be defined mathematically.

### Finite textual representation

A fixed number of decimal digits necessarily introduces quantization/rounding.

This is an encoding limitation, not evidence that the underlying direction geometry is incorrect.

---

# 17. Comparison Table

| Property | Quadray | SDC |
|---|---|---|
| Spatial space | 3D | 3D |
| Components/directions | 4 | 14 |
| Basic geometry | Regular tetrahedron | 6 cardinals + 8 diagonals |
| Overcomplete | Yes | Yes |
| Non-orthogonal | Yes | Diagonal portion |
| Positive representation | Yes | Yes |
| Canonicalization | Tetrahedral normalization | Antipodal cancellation + cardinalization |
| Human directional vocabulary | Secondary | Central design goal |
| Fixed-width text notation | Not intrinsic | Defined |
| Precision profiles | Not intrinsic | Defined |
| Sol origin | Not intrinsic | Defined |
| Earth J2000 anchor | Not intrinsic | Defined |
| Planetary ephemeris | Not intrinsic | Included in SDC repository |
| Tracking layer | Not intrinsic | SDC-Track proposed |
| Primary geometric motivation | Tetrahedral structure | Readable spatial directions |
| Primary application context | General geometry / spatial representation | Astronomical location and telemetry |

---

# 18. Prior-Art Relationship

SDC's own specification identifies Quadray as the closest precedent for its overcomplete-coordinate architecture.

This should be treated as an important distinction between:

1. the **general mathematical principle** of an overcomplete non-orthogonal spatial representation;
2. the **specific SDC directional set**;
3. the **specific SDC textual encoding**;
4. the **specific SDC astronomical frame**;
5. the **specific SDC implementation and tracking architecture**.

The existence of Quadray does not make the specific SDC expression identical to Quadray.

Conversely, the existence of SDC should not be presented as evidence that the general overcomplete-coordinate concept was independently invented for the first time by SDC.

The technically defensible position is that SDC shares an established mathematical family resemblance with Quadray while implementing a substantially different directional and application architecture.

---

# 19. What Appears Distinctive About SDC

Within the scope examined here, the parts of SDC that are most specifically identifiable as its own design arrangement include:

- the particular fourteen-direction set;
- six cardinal directions plus eight 45° diagonal directions;
- seven antipodal pairs;
- fixed directional slots;
- the specific character/slot encoding concept;
- the Sol-centered astronomical framing;
- the Earth J2000 directional anchor;
- the defined precision-profile architecture;
- the separation of canonical storage from human-readable directional display;
- the SDC reference implementation;
- the proposed SDC-Track architecture.

These should be distinguished from broad mathematical concepts that have established precedent.

---

# 20. A Useful Conceptual Model

The relationship can be visualized as:

```text
                         3D VECTOR SPACE
                                │
                ┌───────────────┴───────────────┐
                │                               │
             QUADRAY                           SDC
                │                               │
       4 tetrahedral rays              14 directional rays
                │                               │
        4-coordinate tuple              14-slot notation
                │                               │
     tetrahedral normalization       canonical cardinalization
                │                               │
                └───────────────┬───────────────┘
                                │
                         Cartesian x/y/z
                                │
                        Common vector space
```

The important point is that the systems can be treated as **alternative coordinate representations of the same underlying three-dimensional geometry**.

---

# 21. Potential Interoperability

Because both systems ultimately represent ordinary 3D vectors, an interoperability layer is mathematically possible.

A conceptual converter would perform:

```text
SDC
 ↓
Cartesian
 ↓
Quadray
```

or:

```text
Quadray
 ↓
Cartesian
 ↓
SDC
```

This is preferable to treating either system as a competitor to the other.

It also provides a useful research opportunity: calculate the complete conversion table for all fourteen SDC direction vectors and examine the resulting Quadray coordinate complexity.

Such a table could quantify what SDC gains through its fourteen-direction vocabulary and what it gives up compared with Quadray's four-direction tetrahedral basis.

---

# 22. Research Questions

Several questions remain useful for further mathematical investigation:

### 22.1 Complete SDC ↔ Quadray conversion

Derive exact normalized Quadray tuples for all fourteen SDC directions.

### 22.2 Encoding efficiency

Compare the number of symbols/bits required to represent equivalent positions under:

- SDC compact profiles;
- true base-14 SDC;
- Quadray representations;
- Cartesian coordinates.

### 22.3 Numerical error

Quantify accumulated error from finite decimal SDC representations, particularly for diagonal vectors containing \(\sqrt2/2\).

### 22.4 Directional resolution

Compare angular separation among SDC directions with tetrahedral Quadray directions and with other established 14-direction spatial sets.

### 22.5 Astronomical interoperability

Implement a direct Quadray ↔ SDC astronomical conversion and verify it against the same Cartesian positions.

### 22.6 Tracking

Determine how SDC-Track's time, velocity, uncertainty, and frame metadata should be formally specified.

---

# 23. Terminology Recommended for SDC

For technical writing, the following terminology is recommended:

> **Sum Dia Const (SDC) is a fourteen-direction spatial coordinate notation and reference implementation for representing positions relative to Sol.**

When discussing the mathematical relationship to Quadray:

> **SDC is an overcomplete three-dimensional directional representation sharing structural characteristics with Quadray's tetrahedral coordinate system, but using a different directional geometry, canonicalization strategy, encoding architecture, and astronomical reference frame.**

A concise comparison statement is:

> **Quadray organizes 3D space around four tetrahedral directions; SDC organizes 3D spatial notation around fourteen human-readable directions and applies that notation to a defined Sol-centered astronomical frame.**

---

# 24. Conclusion

SDC and Quadray are mathematically related but architecturally distinct.

Both demonstrate that a three-dimensional point can be represented using an overcomplete directional system rather than conventional three-axis Cartesian coordinates.

Quadray does this with four tetrahedral directions and a normalization relationship arising from the geometry of the regular tetrahedron.

SDC does it with fourteen fixed directions—six cardinals and eight 45° diagonals—using antipodal cancellation and cardinalization to establish canonical storage.

The SDC repository then builds additional layers around that geometry:

```text
14-direction geometry
        ↓
coordinate notation
        ↓
canonical representation
        ↓
fixed-width encoding
        ↓
Sol/J2000 astronomical frame
        ↓
reference implementation
        ↓
ephemeris calculations
        ↓
SDC-Track proposal
```

Therefore the most useful way to understand the relationship is not **"SDC versus Quadray."**

It is:

> **Quadray and SDC are two different ways of organizing and encoding the same underlying three-dimensional vector space, with Quadray emphasizing tetrahedral geometry and SDC emphasizing human-readable directional notation and an astronomical coordinate application.**

The mathematical relationship is strong enough that exact vector-level conversion between them is possible, while the practical systems remain substantially different in purpose and architecture.

---

## Appendix A — Important Qualification

This comparison is a technical analysis of the SDC repository and publicly available descriptions of Quadray. It is not a patentability, copyrightability, or legal opinion.

Copyright protects expression rather than mathematical ideas themselves. The MIT license in the SDC repository governs use of the copyrighted repository material according to its terms.

Questions of patent prior art, novelty, ownership, or enforceability require a separate legal analysis.

---

## Appendix B — Source Materials

### SDC

- SDC specification and repository materials
- `SPEC.md`
- `README.md`
- `sumdiaconst.py`
- `ephemeris.py`
- `test_sumdiaconst.py`
- `TRACKING.md`
- MIT `LICENSE`

### Quadray

Publicly documented Quadray materials describing:

- four tetrahedral basis directions;
- four-coordinate representation of 3D space;
- nonnegative normalization;
- coordinate equivalence under addition of a common value;
- regular-tetrahedron geometry.

The Quadray concept is commonly associated with Darrel Jarmusch, who has described developing the system in 1981.

---

**Status:** Technical comparison / research document  
**SDC repository:** `https://github.com/trllhntrgmgco/sum-dia-const`
