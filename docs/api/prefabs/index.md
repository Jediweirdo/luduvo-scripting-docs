---
icon: lucide/package
---

# Prefabs

!!! note
    If you are familiar with Unity, Luduvo prefabs are conceptually similar to [Unity prefabs](https://docs.unity3d.com/6000.7/Documentation/Manual/Prefabs.html).

Prefabs are premade/serialized [Instances](/luduvo-scripting-docs/api/instances) that can be easily reused between Luduvo projects, and are required for Luduvo scripts to programmatically spawn non-cloned instances in your game.

Luduvo ships these core prefabs:

- [Part](part.md)
- [SpawnLocation](spawnlocation.md)
- [PlayerSpawner](playerspawner.md)
- [Menu](menu.md)
- [Character](character.md)

## Storage

Prefabs are stored in the `core://prefabs/` and `project://prefabs/` virtual mounts. Both `core://` and `project://` are virtual mounts Luduvo uses as aliases, not directories literally named `core:` or `project:`. Prefabs and other core files are versioned and updated by Luduvo, so do not edit their physical cache files.

## Creating and editing prefabs

Opening a core prefab for editing creates a project copy at `project://prefabs/<Name>.ldv` and opens it in a prefab-edit world. Edit the project copy, not the installed core content.

To create a prefab from scene content, stop playtesting, select exactly one root entity, and use **File > Export Model...**. The exported `.ldv` can then be stored under the project's prefab directory. Prefab lookup reads the registered core/project store; inserting a prefab into the current scene is not required to make `Exists` or `Spawn` find it.

There is no Luau API for defining or saving prefab files at runtime.

## Spawning prefabs

Service functions use dot syntax:

```luau
if game.Prefabs.Exists("MyPrefab") then
    local root = game.Prefabs.Spawn("MyPrefab")

    if root ~= nil then
        root.Parent = self
    end
end
```

| Method | Scope | Behavior |
| --- | --- | --- |
| `game.Prefabs.Exists(name: string) -> boolean` | Client and server | Checks a logical, case-sensitive name without creating anything. |
| `game.Prefabs.Spawn(name: string) -> Instance?` | Server only | Instantiates the complete tree and returns its detached root, or `nil` on failure. |

Pass `"MyPrefab"`, not a `.ldv` path or URI. The returned root is not automatically parented or positioned.
