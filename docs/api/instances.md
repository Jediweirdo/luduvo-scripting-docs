---
icon: lucide/box
---

# Instances

An `Instance` is Luduvo's slight spin on an ECS entity. Like with normal ECS entities, every asset and object that interacts directly with the engine and not other scripts with in Luduvo (whether visible or not) likely do so through Instances, and you find yourself making and using them constantly.

Similiarly to an entity, Instances are also still largely defined by the [Components](components/index.md){ data-preview } you attach to it. However, Luduvo Instances also take a more OOP approach to their design and bundles many operations and helper functions into methods and properties you can directly call on the instance itself.

## Obtaining Instances

### From Existing Instances

There are several ways to get existing Instances in Luduvo. If you don't have a reference to an instance already, you can use the following methods:

- `[game.World.Each](queries.md#query-for-instances){ data-preview }` and by extension [its `Query` counterpart](queries.md#query-for-components){ data-preview } for getting instances based on their Components
- [Script handles](scripts.md#script-handles){ data-preview } and the global [`self` parenting](scripts.md) for getting instances hand-made in the editor

And if you already have a reference to an Instance, you can use its special hierarchy-related methods and properties to decuce the locations of other instances from its parent or sibling relationships:

- `Instance.Parent`, which returns the Instance the called Instance is nested under 
- `Instance:FindFirstChild`, which returns the first child Instance with the given name
- `Instance:GetChildren`, which returns all nested Instances of the called Instance
- `Instance:IsDescendantOf`, which checks whether the called Instance is a descendant of the given ancestor Instance

More details on these methods and properties can be found in the [Lifecycle and Hierarchy section](instances.md#lifecycle-and-hierarchy)

### From New Instances

As of writing, there is such thing as `Instance.new()` or constructor that allows you to directly create an entity. Instead, Instances must be created through these routes:

- Make the Instance through the Editor
- [`game.Prefabs.Spawn`](prefabs/index.md#spawning-prefabs){ data-preview } to spawn a premade Instance from a Luduvo object file
- `Instance:Clone()` to duplicate an existing Instance

#### Cloning

`Clone()` makes a new Instance with identical values to the source Instance wherever possible. 

```luau
local copy = self:Clone()
copy.Parent = self.Parent --(1)!
```

1. `self:Clone()` only creates the Instance. To be able to see the Instance in the engine, it still needs to be parented to the World hierarchy to correctly render

`Clone` is callable from both the server and client scripts, but its implementation for client-sided scripts has no server check and isn't automatically replicated.

!!! warning 
    The only way to detroy Instances (`Destroy()`) is a server-script-only method. For now, it is reccomended to create clones on the Client by sending an [Event](events.md#client-to-server-example) requesting to do so to the Server.


## Component Management

Instances come built in with methods for managing Components:

```luau
instance:AddComponent(name: string) -> ()
instance:RemoveComponent(name: string) -> ()
instance:HasComponent(name: string) -> boolean
```

As you might expect, `AddComponent()` adds a component to the Instance, `RemoveComponent()` removes it, and `HasComponent()` checks whether the given component is attached to the Instance. All 3 methods take a string `name` parameter, which requires the (case sensitive) name of the component you are looking to manage. 

A full list of available components can be found in the [Component reference](components/index.md).

!!! warning
    `HasComponent()` isn't properly implemented and always returns false regardless of if the component exists on the Instance or not.

These methods work differently depending on where they are called:

- Only server scripts can add or remove replicated and server-only components. Changes to replicated components are replicated to all clients.
- A client script can change only client-only components, but those changes stay local to that client's World.
  - If a client attempts to write to a replicated component, Luduvo rejects it with `'<name>' is replicated; only server scripts may write it`.

Queries are not the only way to access component values. Fixed properties above expose selected built-ins. Platform custom components expose nested field proxies:

```luau
self.PlayerSpawner.character = "Character"
self.PlayerSpawner.respawnDelay = 3

self.Tool.equipped = 1 --(1)! 
```
1. Note that this is an 8 bit integer, so this value can only go from 0 through 255

## Attributes

Currently, you cannot create your own components. However, if you need to store custom data on an Instance, you can still do so through the use of Attributes:

```luau
self.attr.Speed = 3
print(self.attr.Speed)
```

Attributes are a key-value dictionary for storing custom data on an Instance stored in a `attr` field. They act exactly like regular Lua tables, which means you can create, read, and modify them using standard table operations.

The only exception is that you cannot directly print the entire `attr` table through `print(self.attr)`. Instead, you can use `game.World.DumpAttributes(Instance)`:
```luau
game.World.DumpAttributes(self)
```

Replication rules still apply to attributes, so clients cannot write Attributes on a server-owned or replicated Instance.

## Signals

Signals are Luduvo's equivalent of BindableEvents/RBXScriptSignals, or some other game engine's "hook" event equivalent. Luduvo uses them internally to hook scripts into engine events, but they can also be created by you directly:

```luau
local damaged = self:GetSignal("Damaged")

damaged:Connect(function(amount, source)
    print(amount, source)
end)

damaged:Emit(10, self)
self:Emit("Damaged", 10, self) -- equivalent after GetSignal registered the name
```

| Method | Behavior |
| --- | --- |
| `GetSignal(name: string) -> Signal` | Finds or creates a signal name for this Instance. |
| `Signal:Connect(callback: (...any) -> ()) -> ()` | Appends a local callback. It returns no connection object. |
| `Signal:Emit(...any) -> ()` | Synchronously calls the local callbacks with the supplied arguments. |
| `Instance:Emit(name: string, ...any) -> ()` | Triggers an already registered name on this Instance. |


!!! warning
    Custom signals cannot be deleted, and will remain in memory until the instance is destroyed. You need to make your own "deleted" check in custom signals if you plan on using them without causing memory leaks in your game.

Interstingly, `:GetSignal()` is the only way to create a signal, so they are likely intended to only be usable in conjunction with Instances.

### Emitting Signals

Once a signal is attached to an instance, it can be fired using `Signal:Emit(...args: any)`, and you can connect listeners to run callback functions on successful emission using `Signal:Connect(callback: (...args: any) -> ())`. 

The `args` defied in `GetSignal` are the exact args that you must emit in `Signal:Emit()` as well as the arguments given to the signal's `:Connect()` listeners.

Signal connections and emmissions are completely local to where they are created, so they will **not** be replicated to other clients nor the server. If the server emits a signal on an instance that is replicated to and seen by other clients, only the server's signals will be emitted. If a client emits a signal on an instance that multiple clients and the server are listening to, only that client's signals will be emitted. 

!!! tip
    If you need a signal to emit across multiple clients and the server, you will need to do so by using [Events](events.md) or by putting emmission logic in a `game.World.Server` that polls for changes to the instance's components (which is likely how Luduvo's own signals are handled).

### Built-in Signals


- `Instance.Changed:Connect()`, which does nothing
- `Instance.ChildAdded:Connect(child: Instance)`, which fires when an instance is repareted to this instance via `Instance.Parent`. The `child` argument is the new instance that is being repareted to it.
- `Instance.ChildRemoved:Connect(child: Instance)`, which fires when an instance under it is repareted to another instance or `nil` via `Instance.Parent`. The `child` argument is the old instance that is leaving your hierarchy.
- `Instance.Activated:Connect(activator: Instance)`, which fires when the instance is clicked on. This signal is only relevant to UI Instances that have the [UIClickable](components/UIClickable.md) component attached to them. UIs with the [UIDisabled](components/UIClickable.md) component attached will be ignored and not trigger `Activated`.

??? warning "Signal Jank"
    There are a few oddities about these signals that are worth noting:

    - `ChildAdded`/`ChildRemoved` does not check if the instance being repareted to is itself and will fire even if the instance is being repareted to itself.

    - `Changed` does nothing, has no arguments, and will not fire unless you manually `:Emit()` it.

    - `Activated` will not fire if the character/player that activated is actively being destroyed or doesn't have a [Health](components/Health.md) component attached to it. It doesn't actually care if the character is dead or not, or is even a player at all (though you kind of have to be a player to click on it).

Currently, the `Emit` method will work on ANY signal, even if the Signal is supposed to be managed by Luduvo itself.

Alongside `signal:Emit()`, Instances also have `Instance:Emit(name: string, ...args: any)` that can be used to fire any signal by name you gave it when running `Instance:GetSignal()`.

## Reference

??? note "Replication Rules"
    `Read/write, client and server` in the property tables means that the native setter is exposed in both runtimes. It does not mean a client write is sent to the server.
    
    - A client property write changes that client's local World. It is non-authoritative, is not sent to the server or other clients, and may be replaced by a later server update.
    - A server write to a replicated component follows normal server-to-client replication.
    - Server-only setters raise an error from client scripts.
    - A client must use a `ToServer` [EventTable](events.md) to request an authoritative change.
!!! note
    `vector` below is Luau's native vector type. Luduvo's `Vector3.new`, `Vector2.new`, and `Color3.new` all create that same runtime value.

### World Hierarchy

#### Properties

```luau

type Kind = "Part" | "ScreenGui"

```


| Property | Scope | Behavior |
| --- | --- | --- |
| `Kind: string` | Read-only, client and server | Returns a creator-facing "kind". |
| `Name: string` | Read/write, client and server | Reads or writes the `Name` component. |
| `Parent: Instance?` | Read/write, client and server | Reads or replaces the Instance that is currently nested under. `nil` completelt detaches the Instance from the World Hierarchy. Assignment drives the local `ChildRemoved` and `ChildAdded` notifications described below. |

#### Methods

| Method | Scope | Behavior |
| --- | --- | --- |
| `Clone() -> Instance` | Client and server | Copies the Instance's children and registered components and prepares the Instance for replication by assigning it a fresh internal `NetworkID` if created on the server. |
| `Destroy() -> ()` | Server only | Deletes the Instance, its components, and its all its nested children. You cannot read or write a destroyed Instance or any of its children. |
| `FindFirstChild(name: string) -> Instance?` | Client and server | Returns the first child with the given name, or `nil` if no such child exists.|
| `GetChildren() -> {Instance}` | Client and server | Returns all children that are nested under the Instance. |
| `IsDescendantOf(ancestor: Instance) -> boolean` | Client and server | Checks if the Instance is nested under the given ancestor. |

### Appearance

#### Properties

| Property | Scope | Behavior |
| --- | --- | --- |
| `Position: vector` | Read/write, client and server | Reads or writes the [`Position`](components/position.md){ data-preview } Component. If the Instance is a ScreenGui instead of a part, the setter also handles the [`UIRect`](components/UIRect.md) position fields. |
| `Orientation: vector` | Read/write, client and server | Reads or writes the [`Rotation`](components/rotation.md){ data-preview }. Currently, you cannot rotate UIs. |
| `Size: vector` | Read/write, client and server | Reads or writes the [`Scale`](components/scale.md){ data-preview }. If the Instance is a ScreenGui instead of a part, the setter also handles the [`UIRect`](components/UIRect.md) size fields. |
| `Color: vector` | Read/write, client and server | Reads or writes the [`BrickColor`](components/brickcolor.md){ data-preview } Component. |
| `Transparency: number` | Read/write, client and server | Reads or writes the [`Transparency`](components/transparency.md){ data-preview } Component. |
| `MeshId: number` | Read both; write server | Reads or writes the asset ID stored in the [`Mesh`](components/mesh.md) Component. Unsure of the exact field name. |
| `TextureId: number` | Read both; write server | Reads or writes the [`SurfaceAppearance.Albedo`](components/surfaceappearance.md){ data-preview } field as a numeric asset ID. |
| `EmissiveTextureId: number` | Read both; write server | Reads or writes the [`SurfaceAppearance.Emissive`](components/surfaceappearance.md){ data-preview } field as a numeric asset ID. |
| `UnderlayTextureId: number` | Read both; write server | Reads or writes the [`SurfaceAppearance.Underlay`](components/surfaceappearance.md){ data-preview } field as a numeric asset ID. |

### Physics and gameplay

#### Properties

| Property | Scope | Behavior |
| --- | --- | --- |
| `Anchored: boolean` | Read/write, client and server | Reports if the [`Anchored`](components/anchored.md) Component tag is present. Writing `true` adds it, and writing `false` removes it. |
| `CollisionGroup: string` | Read/write, client and server | Reads or writes the [`CollisionGroup.Group`](components/collisiongroup.md) by registered group name. |
| `Density: number` | Read/write, client and server | Reads or writes the [`RigidBody.Density`](components/rigidbody.md) field. |
| `Friction: number` | Read/write, client and server | Reads or writes the [`RigidBody.Friction`](components/rigidbody.md) field. |
| `Restitution: number` | Read/write, client and server | Reads or writes the [`RigidBody.Restitution`](components/rigidbody.md) field. |
| `LinearDamping: number` | Read/write, client and server | Reads or writes the [`RigidBody.LinearDamping`](components/rigidbody.md) field. |
| `AngularDamping: number` | Read/write, client and server | Reads or writes the [`RigidBody.AngularDamping`](components/rigidbody.md) field. |
| `Velocity: vector` | Read-only, client and server | Reads the [`Velocity`](components/velocity.md) Component, but cannot be written directly. Use `SetLinearVelocity()` to write. |
| `SpawnPoint: boolean` | Read-only, client and server | Reports whether the [`SpawnPoint`](components/spawnpoint.md) Component tag is present. Writing `true` adds it, and writing `false` removes it. |

#### Signal properties

| Property | Scope | Behavior |
| --- | --- | --- |
| `Activated: Signal<Instance>` | Read-only, client and server | Emits a signal event when UI with a [`UIClickable`](components/uiclickable.md) Component detects user input. Only automatically emmits when on the client. |
| `Changed: Signal<>` | Read-only, client and server | Emits a signal event presumably when an Instance's component changes. However, it currently has no arguments and cannot go off on its own under any circumstances. |
| `ChildAdded: Signal<Instance>` | Read-only, client and server | Emits a signal event containing the new Instance gets nested under it via `Parent` reassignment. |
| `ChildRemoved: Signal<Instance>` | Read-only, client and server | Emits a signal event containing the old Instance when a `Parent` reassignment no longer points to itself. |

### Identity, input, joints, and physics

```luau
type IdentityResult = {
    userId: number,
    displayName: string,
    isAdmin: boolean,
}

type MoveIntent = {
    x: number,
    z: number,
    jump: boolean,
    shiftLock: boolean,
    targetYaw: number,
}

type SwingTwistJoint = {
    Anchor: vector,
    TwistAxis: vector,
    PlaneAxis: vector,
    RestAxis: vector,
    PlaneCone: number,
    NormalCone: number,
    TwistMin: number,
    TwistMax: number,
    Friction: number,
}
```
#### Methods

| Method | Scope | Behavior |
| --- | --- | --- |
| `GetIdentity() -> IdentityResult` | Client and server | Reads [`Identity`](components/identity.md), [`DisplayName`](components/displayname.md), and [`Admin`](components/admin.md) Components. If direct identity data is absent, it follows internal `SessionOwner`. |
| `GetMoveIntent() -> MoveIntent` | Server only | Reads an internal `CharacterMoveIntent` Component. |
| `GetSwingTwistJoint() -> SwingTwistJoint?` | Client and server | Reads the [`SwingTwistJoint`](components/swingtwistjoint.md) Component, or returns `nil` when absent. |
| `SetSwingTwistJoint(value: SwingTwistJoint) -> ()` | Server only | Adds the [`SwingTwistJoint`](components/swingtwistjoint.md) Component if needed, then replaces all its fields. |
| `GetLinearVelocity() -> vector` | Server only | Reads live internal `PhysicsBody` velocity, or zero when no live body exists. Strangely, it does not read the public [`Velocity`](components/velocity.md) Component directly. |
| `SetLinearVelocity(value: vector) -> ()` | Server only | Changes internal `PhysicsBody` velocity and writes public [`Velocity`](components/velocity.md) Component. It is ignored when there is no dynamic body. |
| `GetAngularVelocity() -> vector` | Server only | Reads live internal `PhysicsBody` angular velocity, or zero when no live body exists. |
| `SetAngularVelocity(value: vector) -> ()` | Server only | Changes the internal `PhysicsBody` and `AngVelocity` Components. It is ignored when there is no physics body. |
| `ApplyForce(force: vector, point: vector?) -> ()` | Server only | Applies force to internal `PhysicsBody`, presumably based on the point's (currently unknown) coordinate space. It does not rewrite the public [`RigidBody`](components/rigidbody.md) Component. |
| `ApplyImpulse(impulse: vector, point: vector?) -> ()` | Server only | Applies an impulse to internal `PhysicsBody` Component. It is ignored when no dynamic body exists. |
| `ApplyTorque(torque: vector) -> ()` | Server only | Applies torque to internal `PhysicsBody`. It is ignored when no dynamic body exists. |
| `SetBodyMotion(mode: "dynamic" \| "kinematic") -> ()` | Server only | Adds or removes the public [`Kinematic`](components/kinematic.md) Component and changes the internal `PhysicsBody` Component's motion. Switching to `dynamic` clears live linear and angular velocity. |
| `Rotate(axis: vector, angle: number) -> ()` | Client and server | Multiplies the public [`Rotation`](components/rotation.md) Component by an axis-angle rotation and marks the internal body "dirty" if present. |

### Animation

```luau
type AnimationPreviewState = {
    clip: string,
    time: number,
    speed: number,
    playing: boolean,
    shared: boolean,
}
```

#### Methods

| Method | Scope | Behavior |
| --- | --- | --- |
| `PlayAnimation(clip: string, fadeSeconds: number?, speed: number?) -> ()` | Server only | Changes the manually controlled animation layer in an internal `Animator` Component. It does not add or change the public [`CharacterAnimation`](components/characteranimation.md) Component. |
| `StopAnimation() -> ()` | Server only | Stops the manual layer in internal `Animator` and may close related preview state. |
| `ActiveAnimation() -> string?` | Server only | Reads an internal `AnimLayerSet` Component and returns the active manual clip, or `nil`. |
| `AnimationWeight(clip: string) -> number?` | Server only | Reads a clip's weight from an internal `AnimLayerSet` Component. |
| `PreviewAnimation(clip: string, speed: number?, timeSeconds: number?) -> ()` | Server only | Starts or positions animation playback. |
| `AnimationPreview() -> AnimationPreviewState?` | Server only | Reads this entity's scripting preview record. |
| `AdvancePreview() -> boolean` | Server only | Advances the preview record and applies the new state. Boolean return value likely indicates success. |
| `StopPreview() -> boolean` | Server only | Removes the preview record and closes the preview. Boolean return value likely indicates success. |
