# General Space Travel with Sum Dia Const (SDC)

**Document:** GeneralSpaceTravel.md  
**Subject:** Using SDC as a general spatial and piloting notation  
**Date:** September 18, 2026

## 1. Purpose

Sum Dia Const (SDC) can be used not only as a fixed astronomical coordinate notation, but also as a **general spatial language for navigation, piloting, targeting, and object-to-object travel**.

The central idea is that SDC's directional vocabulary can be associated with different reference frames without changing the underlying fourteen-direction notation.

A frame can be established globally, relative to an object, relative to a target, or relative to an object's direction of travel.

This allows the same notation to remain useful as the observer and navigation context change.

---

# 2. The Basic Spatial Concept

SDC provides fourteen directional positions:

- six cardinal directions;
- eight diagonal directions.

The directions form seven opposing pairs.

The important navigation pair is:

- **`1` — forward/reference direction**
- **`8` — opposite/reverse direction**

The remaining directions describe the surrounding spatial environment.

The origin object is represented by the frame's zero/reference position.

Conceptually:

```text
                    9
                    ↑
              a     │     b
                    │
        2 ←──────── 0 ────────→ 7
                    │
              c     │     d
                    ↓
                    0
```

The exact interpretation of the directional slots depends on the declared reference frame.

---

# 3. The Piloted Ship as the Origin

For a piloted spacecraft, the spacecraft can be treated as the **origin object**.

Conceptually:

```text
                  1
                  ↑
                  │
                  │
                  0
             PILOTED SHIP
```

Here:

- `0` represents the piloted ship / origin.
- `1` represents the forward or reference direction.
- `8` represents the reverse direction.

The important distinction is that **`0` identifies the object at the origin**, while **`1` establishes the direction from that origin**.

---

# 4. Unreferenced Direction of Travel

A second useful mode does not require a designated target object.

If a spacecraft is traveling through space without a specific reference object being selected:

> **`1` can represent the spacecraft's current direction of travel.**

Then:

> **`8` represents directly behind the spacecraft.**

This creates a natural piloting frame:

```text
                    9
                    ↑

              a     │     b
                    │
                    1
                    ↑
                    │
                    0
               SHIP / ORIGIN
                    │
                    ↓
                    8
```

The frame therefore gives a pilot an immediately understandable concept:

- forward = `1`
- reverse = `8`

The frame can rotate with the spacecraft's direction of travel.

---

# 5. Referenced Travel

SDC can also establish a direction using another object.

For example:

```text
OBJECT A                         OBJECT B
    0 ───────────────────────────→ 1
             reference direction
```

The frame is established by the relationship:

> **Object A → Object B = direction `1`.**

Object A remains the origin, represented by `0`.

Object B establishes the forward/reference direction.

The other SDC directions then describe space around that relationship.

---

# 6. Resetting the Frame Between Any Two Objects

A major feature of this concept is that the frame does not have to remain permanently attached to Sol, Earth, or any other single reference.

It can be reset between any two objects.

For example:

```text
Ship A (0) ─────────────→ Ship B
                          1
```

The system establishes:

```text
origin = Ship A
direction 1 = Ship A → Ship B
```

The frame can subsequently be re-established for another pair:

```text
Ship B (0) ─────────────→ Ship C
                          1
```

The directional vocabulary has not changed.

Only the **reference frame** has changed.

This allows SDC to be used between arbitrary objects.

Examples include:

- spacecraft → spacecraft;
- spacecraft → asteroid;
- spacecraft → planet;
- satellite → station;
- Moon → Earth;
- Earth → spacecraft;
- planet → surface vehicle;
- one autonomous vehicle → another autonomous vehicle.

---

# 7. Global and Local Frames

SDC can therefore be understood as supporting both global and local spatial frames.

## Global frame

The existing SDC astronomical frame can establish a fixed Solar System reference.

Conceptually:

```text
                 SDC GLOBAL FRAME
                        │
                       Sol
                        │
                Solar-system position
```

This is useful for describing where an object is in the larger astronomical environment.

## Local frame

A local frame can instead be established around an object:

```text
                 LOCAL SDC FRAME
                       │
                    Ship A
                       0
                       │
                  direction 1
                       │
                    Target
```

The local frame is useful for navigation and piloting.

---

# 8. Same Vocabulary, Different Reference

The key architectural principle is:

> **The SDC directional vocabulary remains constant while the reference frame changes.**

This can be represented as:

```text
                         SDC
                          │
             ┌────────────┼────────────┐
             │            │            │
          GLOBAL        TARGET       TRAVEL
           FRAME         FRAME        FRAME
             │            │            │
            Sol       Object A→B    Current motion
             │            │            │
             └────────────┼────────────┘
                          │
                 Same SDC directions
```

The notation does not need a completely different coordinate language for each navigation situation.

Instead, the frame declaration tells the system what the directions mean.

---

# 9. Why This Matters for Space Piloting

Traditional Cartesian coordinates are excellent for computation but are not always intuitive as a human piloting language.

A pilot naturally thinks in concepts such as:

- ahead;
- behind;
- above;
- below;
- left;
- right;
- diagonal forward;
- diagonal backward.

SDC's fourteen-direction vocabulary provides a compact standardized set of such spatial relationships.

A pilot could therefore reason about an object as being:

```text
forward
behind
left
right
above
below
or one of the eight diagonal bearings
```

while the underlying system can still convert the notation into Cartesian vectors for computation.

---

# 10. Human Layer and Machine Layer

SDC can therefore provide two simultaneous interpretations.

### Human layer

A pilot sees:

> forward, behind, above, below, left, right, and diagonals.

### Machine layer

The system sees:

> a defined three-dimensional vector.

Conceptually:

```text
              PILOT
                │
        readable direction
                │
               SDC
                │
        Cartesian vector
                │
        navigation system
```

This allows the same representation to be useful to both humans and software.

---

# 11. Target Navigation

Suppose a spacecraft is approaching another spacecraft.

The reference frame can be established as:

```text
                 TARGET
                   1
                   ↑
                   │
                   │
                   0
                 SHIP
```

The target becomes the reference direction.

A navigation system can then describe objects relative to the ship-target relationship.

If the pilot changes the intended target, the frame can be reset.

```text
Before:

Ship A (0) ─────────→ Target B
                       1


After target change:

Ship A (0) ─────────→ Target C
                       1
```

The notation remains unchanged.

Only the reference relationship changes.

---

# 12. Autonomous Navigation

The same concept can apply to autonomous systems.

An autonomous spacecraft could establish:

```text
origin = current vehicle
direction 1 = current velocity vector
```

Then the SDC frame would automatically represent the vehicle's surrounding environment relative to its current motion.

Alternatively:

```text
origin = current vehicle
direction 1 = target vector
```

The navigation software could switch between these modes without changing the underlying directional vocabulary.

---

# 13. Object-to-Object Navigation

SDC is especially suited conceptually to object-to-object navigation because the frame can be defined by a pair.

The general relationship is:

```text
A = origin
B = reference
A → B = direction 1
```

Then:

```text
0 = A
1 = A → B
8 = B → A
```

This provides a natural directional interpretation of the two objects.

The same mechanism can be applied recursively across a network of objects.

For example:

```text
Earth → Station → Ship → Asteroid
```

Each relationship can establish its own local frame.

---

# 14. Relationship to the Existing Sol Frame

This local-frame concept does not require abandoning SDC's existing astronomical frame.

Instead, the systems can coexist.

### Sol frame

Used for:

- Solar System navigation;
- planetary positions;
- astronomical coordinates;
- global reference.

### Object-relative frame

Used for:

- piloting;
- targeting;
- docking;
- formation flight;
- autonomous navigation;
- local spatial awareness.

### Travel frame

Used for:

- current direction of travel;
- forward/reverse navigation;
- trajectory-relative observations.

The common element is the SDC directional vocabulary.

---

# 15. Frame Transformation

Conceptually, a navigation system can perform:

```text
             GLOBAL SDC FRAME
                    │
                    ↓
             Cartesian vector
                    │
                    ↓
             Local frame
                    │
                    ↓
             Local SDC notation
```

The reverse operation is also possible:

```text
             Local SDC notation
                    │
                    ↓
             Local Cartesian vector
                    │
                    ↓
             Global Cartesian vector
                    │
                    ↓
             Global SDC notation
```

This allows local piloting notation to coexist with global astronomical positioning.

---

# 16. Direction 1 Has a Defined Context

The most important rule for this concept is that **direction 1 must be interpreted in the context of the declared frame**.

Possible meanings include:

### Astronomical frame

`1` = the fixed SDC astronomical reference direction.

### Object-reference frame

`1` = direction from the origin object toward the reference object.

### Travel frame

`1` = current direction of travel.

The system therefore should not assume that the symbol `1` has one universal physical orientation in every context.

Instead:

> **The frame defines what direction 1 means.**

This preserves the simplicity of the notation while allowing it to operate in multiple navigation environments.

---

# 17. Direction 8 as the Reverse Direction

Because `1` establishes the forward/reference direction, `8` naturally represents its opposite.

Thus:

\[
1 \leftrightarrow 8
\]

This relationship is especially useful for piloting.

If:

```text
1 = forward
```

then:

```text
8 = behind
```

If:

```text
1 = target direction
```

then:

```text
8 = direction back toward the origin
```

The same antipodal relationship remains valid regardless of the frame.

---

# 18. Why Fourteen Directions Are Useful

The six cardinal directions provide the basic spatial axes.

The eight diagonals add intermediate directional vocabulary.

This means a pilot does not necessarily have to describe every bearing as three independent Cartesian components.

Instead, a direction can first be expressed through a recognizable spatial bearing and then converted to an exact Cartesian vector for computation.

The intended benefit is therefore not that fourteen directions replace continuous three-dimensional mathematics.

Rather:

> **The fourteen directions provide a human-oriented vocabulary layered over continuous three-dimensional space.**

---

# 19. Continuous Position vs. Directional Vocabulary

SDC should continue to distinguish between:

### Direction

The selected spatial bearing.

### Magnitude

How far in that direction.

### Position

The resulting three-dimensional location.

### Frame

What the directions mean.

This gives a conceptual model:

```text
Frame
  │
  ├── Origin
  │
  ├── Direction 1
  │
  └── Other SDC directions
          │
          ↓
      Magnitude
          │
          ↓
      3D position
```

This distinction becomes especially important when SDC is used for moving objects.

---

# 20. Space-Time Extension

For a traveling spacecraft, a complete navigation state eventually requires more than position.

A practical tracking representation may need:

- position;
- time;
- velocity;
- uncertainty;
- reference frame;
- source or measurement context.

This aligns naturally with the SDC-Track concept.

The basic SDC coordinate answers:

> **Where?**

A tracking layer can additionally answer:

> **When?**

and:

> **How is the object moving?**

and:

> **How certain is the measurement?**

---

# 21. Example: Interplanetary Travel

Consider a spacecraft traveling from Earth toward Mars.

A global SDC frame could describe the spacecraft's position relative to Sol.

At the same time, the spacecraft could maintain a local travel frame:

```text
0 = spacecraft
1 = current direction of travel
8 = reverse direction
```

When Mars becomes the immediate navigation target:

```text
0 = spacecraft
1 = spacecraft → Mars
8 = Mars → spacecraft
```

The local frame can therefore change while the global Sol-centered coordinate remains available.

Conceptually:

```text
                    GLOBAL
                 Sol-centered SDC
                       │
                       │
                    SPACECRAFT
                       0
                       │
              LOCAL TRAVEL FRAME
                       │
                 1 = forward
                 8 = reverse
                       │
                    TARGET
```

---

# 22. Example: Docking

For docking, the reference frame can become extremely local.

```text
              DOCKING PORT
                   1
                   ↑
                   │
                   │
                   0
               SPACECRAFT
```

The frame can be reset so that:

```text
1 = spacecraft → docking port
8 = reverse direction
```

Other SDC directions then describe lateral and vertical offsets around the docking approach.

This creates a consistent directional vocabulary without requiring the pilot to mentally redefine an entirely different coordinate system.

---

# 23. Example: Formation Flight

Suppose several spacecraft are traveling together.

Each spacecraft can have its own local origin:

```text
Ship A = 0
Ship B = reference direction 1
```

A second relationship can be:

```text
Ship B = 0
Ship C = reference direction 1
```

The same SDC vocabulary can describe each relationship.

This makes the frame **object-relative rather than permanently world-relative**.

---

# 24. General Principle

The broader principle can be stated as:

> **SDC describes spatial relationships, not merely fixed locations.**

A fixed global frame is one type of spatial relationship.

An object-to-object frame is another.

A direction-of-travel frame is another.

The notation remains useful because the directional vocabulary stays stable while the frame changes.

---

# 25. Relationship to Quadray

This piloting application also helps distinguish SDC from Quadray.

Quadray provides an alternative mathematical representation of three-dimensional space using four tetrahedral directions.

SDC adds a deliberately human-readable directional vocabulary and a frame architecture intended to make the notation useful for navigation and spatial relationships.

Therefore, even where the two systems can represent the same underlying vector, their intended human interaction can be different.

A pilot-oriented SDC system can interpret:

```text
0 = origin
1 = forward/reference
8 = reverse
```

while the mathematical conversion layer remains free to use Cartesian or another internal representation.

---

# 26. Design Principle

The central design principle for general space travel can therefore be summarized as:

> **One spatial vocabulary, many reference frames.**

The SDC directions do not have to be permanently tied to one spacecraft, one planet, or even Sol.

The frame can be:

- global;
- object-relative;
- target-relative;
- travel-relative;
- vehicle-relative;
- docking-relative;
- formation-relative.

The frame establishes the meaning of direction `1`.

Direction `8` is its antipodal reverse.

The remaining SDC directions provide the surrounding directional vocabulary.

---

# 27. Conclusion

SDC can be understood as more than a static astronomical coordinate notation.

Its frame architecture allows the same fourteen-direction vocabulary to be reused across different spatial situations.

For piloting:

```text
0 = piloted/origin object
1 = forward or selected reference direction
8 = reverse/opposite direction
```

When a second object is available, the frame can be established as:

```text
Origin A = 0
A → B = 1
B → A = 8
```

When no reference object is selected:

```text
Origin = 0
Direction of travel = 1
Reverse direction = 8
```

The frame can then be reset between any two objects without changing the underlying SDC directional vocabulary.

This creates a general concept for space navigation:

> **SDC provides a standardized directional language whose reference frame can move with the navigation problem.**

The same system can therefore describe a global Solar System position, a spacecraft's direction of travel, a target bearing, a docking approach, or an object-to-object relationship.

The coordinate vocabulary remains the same.

**Only the frame changes.**
