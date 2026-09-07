---
icon: lucide/box
---

# Components

Components are the data attached to ECS entities. An [Instance](../instances.md) is
the Luau proxy for one entity, not a container holding generic component objects.

Studio labels such as **Transform**, **Data**, **Physics**, **Color**, and
**Material** are Inspector groups. They are not script component names. For
example, Transform corresponds to the separate `Position`, `Rotation`, and
`Scale` query terms.

## Script access

Every built-in name below can be used as an exact, case-sensitive filter with
[`game.World.Query`](../query.md), `Query:With`, `Query:Without`,
`game.World.Each`, `HasComponent`, `AddComponent`, and `RemoveComponent`, subject
to the component's write scope.

Only four built-ins expose a whole value through a Query column:

| Query column | Luau type | Writable through Query |
| --- | --- | :---: |
| `query.Position[i]` | `vector` | yes |
| `query.Scale[i]` | `vector` | yes |
| `query.BrickColor[i]` | `vector` | yes |
| `query.Velocity[i]` | `vector` | no |

Other built-ins are filter-only in a Query. Some still have a separate fixed
Instance property, method, or game-service route; each component page identifies
that route. Inspector fields are serialization and editor metadata. They do not
automatically become `instance.Component.field` Luau properties.

## Custom data

Projects cannot declare new component schemas in this build. Components are
registered in the engine, and `AddComponent` can attach only a registered name.
The installed platform defines two structured custom components:

```luau
type PlayerSpawnerComponent = {
    character: string,
    respawnDelay: number,
}

type ToolComponent = {
    equipped: number, -- U8, clamped to 0 through 255
}
```

These use nested Instance or Query field proxies. They are compiled platform
extensions, not examples of a public component-declaration API. Use
[`instance.attr`](../instances.md#components-and-attributes) for creator-defined
named data.

## Built-in component names

- [Admin](Admin.md)
- [AmbientLight](AmbientLight.md)
- [Anchored](Anchored.md)
- [Attachment](Attachment.md)
- [AutoLocomotion](AutoLocomotion.md)
- [AutoRotate](AutoRotate.md)
- [BodyPart](BodyPart.md)
- [BrickColor](BrickColor.md)
- [Character](Character.md)
- [CharacterAnimation](CharacterAnimation.md)
- [CharacterAppearance](CharacterAppearance.md)
- [CharacterPhysics](CharacterPhysics.md)
- [CharacterPose](CharacterPose.md)
- [CharacterRig](CharacterRig.md)
- [Collider](Collider.md)
- [CollisionGroup](CollisionGroup.md)
- [CoreMenuAction](CoreMenuAction.md)
- [CoreMenuPage](CoreMenuPage.md)
- [CoreSettingBind](CoreSettingBind.md)
- [DisplayName](DisplayName.md)
- [Exposure](Exposure.md)
- [Health](Health.md)
- [HumanoidState](HumanoidState.md)
- [Identity](Identity.md)
- [Kinematic](Kinematic.md)
- [LensFlare](LensFlare.md)
- [Light](Light.md)
- [LightShadowOff](LightShadowOff.md)
- [LimbAttachment](LimbAttachment.md)
- [Locked](Locked.md)
- [Locomotion](Locomotion.md)
- [Mesh](Mesh.md)
- [Name](Name.md)
- [NoContactFriction](NoContactFriction.md)
- [Position](Position.md)
- [PrefabAnchor](PrefabAnchor.md)
- [PrefabInstance](PrefabInstance.md)
- [PrefabNodeId](PrefabNodeId.md)
- [RenderDisabled](RenderDisabled.md)
- [RigidBody](RigidBody.md)
- [Rotation](Rotation.md)
- [Scale](Scale.md)
- [ShadowOff](ShadowOff.md)
- [Shape](Shape.md)
- [SkyBackground](SkyBackground.md)
- [SpawnPoint](SpawnPoint.md)
- [SpotCone](SpotCone.md)
- [StableId](StableId.md)
- [Stars](Stars.md)
- [SunLight](SunLight.md)
- [SunShadows](SunShadows.md)
- [SurfaceAppearance](SurfaceAppearance.md)
- [SurfaceMaterial](SurfaceMaterial.md)
- [SwingTwistJoint](SwingTwistJoint.md)
- [Transparency](Transparency.md)
- [UIClickable](UIClickable.md)
- [UIClips](UIClips.md)
- [UICorner](UICorner.md)
- [UIDisabled](UIDisabled.md)
- [UIFrame](UIFrame.md)
- [UIHidden](UIHidden.md)
- [UIListLayout](UIListLayout.md)
- [UIOrder](UIOrder.md)
- [UIRect](UIRect.md)
- [UIRoot](UIRoot.md)
- [UIScrollingFrame](UIScrollingFrame.md)
- [UISlider](UISlider.md)
- [UISliderState](UISliderState.md)
- [UIStroke](UIStroke.md)
- [UITextInput](UITextInput.md)
- [UITextSource](UITextSource.md)
- [UITextStyle](UITextStyle.md)
- [UIToggle](UIToggle.md)
- [UIToggleOn](UIToggleOn.md)
- [Velocity](Velocity.md)
- [WorldConfig](WorldConfig.md)
