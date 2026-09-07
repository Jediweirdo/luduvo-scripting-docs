---
icon: lucide/panel-top
---

# Menu

!!! note
    This page is a stub. Contributions are welcome!

Menus are a Luduvo built-in [Prefab](index.md){ data-preview } for creating 2D UI components in a game.

```luau
local menu = game.Prefabs.Spawn("Menu")
```

!!! warning
    `Spawn` can only be called from server scripts and must be parented to an [Instance](luduvo-scripting-docs/docs/api/classes/Instance.md){ data-preview } in the world hierarchy to be seen.

Menu descendants use the registered UI and core-menu components documented in the [component registry](../components/index.md).

Luduvo's built-in item-validation rules require a place to contain exactly one core Menu and enforce UI node and depth budgets. Those validation rules do not imply that every menu component is readable as a Luau field.
