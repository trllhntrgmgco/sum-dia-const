# SDC-Track — a tracking layer over Sum Dia Const

**Draft 0. Anticipated design.**

> Nothing in this document has been implemented, prototyped, or tested. It is a proposal written to be attacked. Every number is derived from a definition, never measured. Sections marked **Q1**–**Q9** are open questions where the author does not know the right answer and is asking.

## 1. Scope

SPEC defines a notation for locating a point. This document proposes what sits on top of it: a record for tracking an object that *moves*, and the rules a hub and its clients follow when exchanging those records.

The separation is deliberate. A coordinate is a place. A track is a claim about an object, made by a particular sensor, at a particular instant, with a particular uncertainty. Those are different things and conflating them is how stale data gets treated as current.

## 2. Why the layers split

A bare coordinate cannot answer the three questions a tracking client actually asks:

- **When was this true?** Every observation has an age. At 40 AU, light alone puts a contact over five hours in the past before a hub sees it.
- **Where is it now?** That needs velocity, not just position.
- **How sure are we?** A contact known to 1,000 km and one known to 0.1 AU cannot be merged as equals.

Sum Dia Const answers none of these, correctly — it is a notation, not a protocol.

## 3. Frame rule

**A hub publishes in `SOL` only.**

The hub does not know any client's attitude, and a coordinate in one craft's `CRAFT` frame is noise to every other craft. Clients convert to their own frame locally, using their own attitude solution, at display time. Diagonals belong on the display side.

This has a useful consequence: the hub never needs attitude telemetry from anyone. It collects and redistributes positions, and orientation stays a local concern.

## 4. The track record

| Field | Type | Notes |
| --- | --- | --- |
| `id` | opaque string | Stable across observations of the same object |
| `frame` | `SOL` | Fixed for hub-published tracks (section 3) |
| `profile` | profile tag | Position profile, e.g. `S` |
| `position` | SDC coordinate | Canonical cardinals |
| `velocity` | SDC delta | Per second — see **Q1** |
| `epoch` | UTC, ms | When the observation was *true*, not when sent |
| `sigma` | scalar | Position uncertainty, profile units — see **Q2** |
| `corrected` | flag | Geometric or light-time corrected — see **Q4** |
| `source` | opaque string | Which sensor or hub produced this |

**Q1 — velocity units.** Position and velocity differ in natural scale by roughly eight orders of magnitude. Earth moves about 2×10⁻⁷ AU/s. A velocity expressed in the position profile would be all leading zeros. Velocity probably needs its own independent profile tag, but that means two tags per record and a conversion at every use. Is there a cleaner answer?

**Q2 — uncertainty shape.** A scalar radius is one number and throws away the fact that range error usually dwarfs cross-range error. A full covariance is six numbers and inflates every record by more than the position it qualifies. Is there a defensible middle — an along-track / cross-track / vertical triple?

## 5. Propagation and staleness

A client receiving a track propagates it to the current instant:

```
P(t) = P(t₀) + V · (t − t₀)
```

**This is linear and therefore wrong for anything ballistic.** An object in solar orbit follows a curve; over minutes the straight-line error is negligible, over hours at 1 AU it is not. The honest split:

- **Powered or short-horizon objects** — state vector, linear propagation, short validity window.
- **Ballistic objects** — publish Keplerian elements instead and let the client propagate properly. This is what the existing ephemeris module already does for the planets.

**Q3 — one record type or two?** Carrying both state vectors and orbital elements doubles the schema. Carrying only state vectors is wrong for most of what is out there. Carrying only elements is wrong for anything under thrust.

**Q4 — geometric or apparent position?** A hub can publish where an object *was* when the light left it, or where it is *now* by correction. Astronomy distinguishes astrometric from apparent place for exactly this reason. Both are defensible; publishing without declaring which is not. The `corrected` flag exists to force the declaration, but the default is undecided.

**Q5 — clock discipline.** Propagation is only as good as the agreement between hub and client clocks. At 0.25 c a one-second clock offset is 75,000 km of position error. What synchronisation does this protocol assume, and what does a client do when it detects drift?

## 6. Fast distance in `SOL`

SPEC section 9 says there is no shortcut for distance that works directly on coordinate strings. In canonical `SOL` form that is too pessimistic, and a hub filtering thousands of contacts needs the faster path.

Canonical form leaves at most three slots nonzero, one per axis, and those three are mutually orthogonal. So:

```
Δx = ±M(1 or 8) − ±M(1 or 8)
Δy = ±M(2 or 7) − ±M(2 or 7)
Δz = ±M(9 or 0) − ±M(9 or 0)
d  = √(Δx² + Δy² + Δz²)
```

Three subtractions and a norm, with no fourteen-term reconstruction. For range-gating a contact list, comparing `d²` avoids the square root entirely.

**This shortcut is valid only in canonical form.** A record carrying diagonals must be canonicalised first, which is why section 3 fixes hub output to `SOL` canonical.

## 7. Wire format

Fixed-width records, so a track list is a fixed allocation and parsing is branchless:

```
<id:16><profile:2><position:29><velocity:29><epoch:24><sigma:12><corrected:1><source:16>
```

**Q6 — is fixed-width worth it?** It gives constant-cost parsing and predictable memory, which is the whole reason SDC is fixed-width in the first place. It also wastes space on near-origin objects and caps `id` and `source` arbitrarily. A length-prefixed or binary encoding would be smaller. Which matters more for this workload?

**Q7 — batching and delta encoding.** Consecutive updates of the same track change only in the low digits. Transmitting only changed slots would cut bandwidth substantially and complicate loss recovery. Worth it?

## 8. Hub responsibilities

A conforming hub:

1. Publishes `SOL` canonical coordinates only.
2. Stamps every record with the observation epoch, never the transmission time.
3. Declares `corrected` on every record.
4. Never merges tracks from sources with incompatible `sigma` without re-deriving it.
5. Expires tracks whose epoch is older than a stated validity window rather than serving them indefinitely.

**Q8 — track identity across sources.** Two sensors observing the same object will assign different `id`s. Correlating them is the hard problem in every tracking system ever built, and this document does not solve it. Is correlation in scope for the protocol, or strictly a hub implementation concern?

**Q9 — trust.** Nothing above prevents a source injecting fabricated tracks. Signing records is the obvious answer and adds key distribution to a protocol that otherwise needs none. Is that in scope?

## 9. Review wanted

This draft is published to be corrected, and the author would rather be shown wrong now than have someone build on it first.

Particularly wanted:

- **Anyone who has built real tracking systems.** Q1 through Q5 are questions this field has answered before, and the answers are probably known. Pointers to prior art are more useful than agreement.
- **Orbital mechanics.** Section 5's linear-propagation limit is stated but not bounded. Over what interval, at what range, does the error exceed a given `sigma`? That is a computable answer and it is not computed here.
- **Protocol designers.** Q6 and Q7 are ordinary wire-format trade-offs with established practice behind them.
- **Anyone who thinks the layering is wrong.** If a track record should not be built on a coordinate notation at all, that is worth knowing before more is written on top of it.

Open an issue referencing the question number, or send a pull request. Corrections to the parent SPEC are equally welcome — its own open problems are listed in its section 10, and its position tables were computed by hand and deserve independent checking.

---

MIT licensed. © 2026 Keenan Dunham.
