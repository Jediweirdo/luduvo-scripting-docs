---
icon: lucide/box
---

!!! note
    This is still a stub. The scripting routes below are confirmed, but the
    component's editor behavior and serialized fields are not fully documented.

!!! note
    Studio's property groups and the scripting component API are different. A
    label shown in the Properties panel is not automatically a component name or
    a Luau field.

# HumanoidState

`HumanoidState` is an exact, case-sensitive built-in component name. You can use it
with [`game.World.Query`](../query.md), `Query:With`, `Query:Without`,
[`game.World.Each`](../query.md#gameworldeach), and the Instance component
methods.

## Script access

This component can filter Query rows, but it does not expose a whole-value Query column in this build. No separate fixed Instance property, Instance method, or game-service binding was found for its stored fields.

Inspector fields are serialization/editor metadata and are not automatically
available as Luau fields. See [Components](index.md) for that distinction and
[Instances](../instances.md#properties) for fixed property types and write scope.
