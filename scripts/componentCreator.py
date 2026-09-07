"""
Super mass formatter script for all the
"""

from pathlib import Path

COMPONENTS = {
    # Tab autocomplete generated most of these. Will revisit soon(tm)
    "Position": "where the Instance is located in the world",
    "Rotation": "the rotation of the Instance",
    "Scale": "the size of the Instance",
    "Name": "the name of the Instance in the World Hierarchy. The name usually visible in the editor's [Outliner](../outliner.md)",
    "Velocity": "the velocity of the Instance",
    "Shape": "the shape of the Instance",
    "Collider": "the collider of the Instance",
    "RigidBody": "the general physical properties of the Instance",
    "Anchored": "whether the Instance is affected by physics",
    "CollisionGroup": "the collision group of the Instance",
    "Kinematic": "whether the Instance is kinematic",
    "Locked": "whether the Instance's other components can be modified",
    "BrickColor": "the color of the Instance",
    "Transparency": "the transparency of the Instance",
    "ShadowOff": "whether the Instance has shadows or not",
    "SurfaceMaterial": "the material of the Instance",
    "Mesh": "the mesh of the Instance",
    "SurfaceAppearance": "the texture of the Instance",
    "SpawnPoint": "whether Players can spawn at this Instance",
    "StableId": "the internal id of the Instance. Unsure why this is public but it is", # come back to this-- might be wrong
    "PrefabInstance": "keeping track of what prefab an Instance created from a [Prefab](../prefabs/index.md) belongs to",
    "PrefabNodeId": "", # unsure
    "PrefabAnchor": "", # unsure
    "Character": "telling the Engine that this Instance is a character model",
    "CharacterPhysics": "telling the Engine that this Instance can ragdoll based on their [rigidBody](rigidBody.md) information", # come back to this as its not clear about the difference between this and RigidBody
    "CharacterAnimation": "telling the Engine that this Instance has animation information. You must have at least 6 body parts, and falls back on R6 if not enough are provided", # needs fact checking
    "Health": "the health of the Instance. Requires a [Character](character.md) component to function",
    "Locomotion": "the locomotion of the Instance",
    "HumanoidState": "the humanoid state of the Instance",
    "AutoRotate": "the auto rotate of the Instance",
    "NoContactFriction": "whether the Instance can be affected by contact friction or not.", # Apparently, the FSM holds it during GettingUp. Research is needed to tell what that means
    "CharacterRig": "the active character rig of the Instance",
    "AutoLocomotion": "the auto locomotion of the Instance",
    "LimbAttachment": "the limb attachment of the Instance",
    "SwingTwistJoint": "the swing twist joint of the Instance",
    "BodyPart": "the body part of the Instance",
    "CharacterAppearance": "controls the decal information for the Instance (specifically the face, shirt, and pants decals). Requires a [Character](character.md) component to function",
    "CharacterPose": "the character pose of the Instance",
    "Identity": "the identity of the Instance",
    "DisplayName": "the display name of the Instance",
    "Admin": "the admin of the Instance",
    "RenderDisabled": "the render disabled of the Instance",
    "Attachment": "the attachment of the Instance",
    "UIRect": "the UI rect of the Instance",
    "UIOrder": "the UI order of the Instance",
    "UIHidden": "the UI hidden of the Instance",
    "UIFrame": "the UI frame of the Instance",
    "UIStroke": "the UI stroke of the Instance",
    "UICorner": "the UI corner of the Instance",
    "UIClips": "the UI clips of the Instance",
    "UITextStyle": "the UI text style of the Instance",
    "UITextSource": "the UI text source of the Instance",
    "UITextInput": "the UI text input of the Instance",
    "UIRoot": "the UI root of the Instance",
    "UIClickable": "the UI clickable of the Instance",
    "UIListLayout": "the UI list layout of the Instance",
    "UIScrollingFrame": "the UI scrolling frame of the Instance",
    "UISlider": "the UI slider of the Instance",
    "UISliderState": "the UI slider state of the Instance",
    "UIToggle": "the UI toggle of the Instance",
    "UIToggleOn": "the UI toggle on of the Instance",
    "UIDisabled": "the UI disabled of the Instance",
    "CoreMenuAction": "the core menu action of the Instance",
    "CoreSettingBind": "the core setting bind of the Instance",
    "CoreMenuPage": "the core menu page of the Instance",
    "Light": "the light of the Instance",
    "SpotCone": "the spot cone of the Instance",
    "LightShadowOff": "the light shadow off of the Instance",
    "SunLight": "the sun light of the Instance",
    "AmbientLight": "the ambient light of the Instance",
    "SkyBackground": "the sky background of the Instance",
    "SunShadows": "the sun shadows of the Instance",
    "Exposure": "the exposure of the Instance",
    "Stars": "the stars of the Instance",
    "LensFlare": "the lens flare of the Instance",
    "WorldConfig": "the world config of the Instance",
}

QUERY_VALUES = {
    "Position": ("vector", "read/write"),
    "Scale": ("vector", "read/write"),
    "BrickColor": ("vector", "read/write"),
    "Velocity": ("vector", "read-only"),
}

OTHER_ROUTES = {
    # These are all exceptions to the default "You can't interact with those component at all" text copy/pasted from all of them
    "Rotation": {"`Instance.Orientation: vector`": ["instance.md#appearence"]},
    "Scale": {"`Instance.Size: vector`": ["instance.md#appearence"]},
    "Name": {"`Instance.Name: string`": ["instance.md#world-hierarchy"]},
    "Velocity": {
        "`Instance.Velocity: vector` and the `numerous velocity methods`": [
            "instance.md#physics-and-gameplay"
        ]
    },
    "Shape": {
        "`Instance.Kind: string` decides the shape of the object": [
            "instance.md#world-hierarchy"
        ]
    },
    "RigidBody": {
        "`Instance.Density`, `Friction`, `Restitution`, `LinearDamping`, and `AngularDamping`": [
            "instance.md#physics-and-gameplay"
        ]
    },
    "Anchored": {"`Instance.Anchored: boolean`": ["instance.md#physics-and-gameplay"]},
    "CollisionGroup": {
        "`Instance.CollisionGroup: string`": ["instance.md#physics-and-gameplay"]
    },
    "Kinematic": {
        "`Instance:SetBodyMotion(...)`": ["instance.md#physics-and-gameplay"]
    },
    "BrickColor": {"`Instance.Color: vector`": ["instance.md#appearance"]},
    "Transparency": {"`Instance.Transparency: number`": ["instance.md#appearance"]},
    "Mesh": {"`Instance.MeshId: number`": ["instance.md#appearance"]},
    "SurfaceAppearance": {
        "`Instance.TextureId`, `EmissiveTextureId`, and `UnderlayTextureId`": [
            "instance.md#appearance"
        ]
    },
    "SpawnPoint": {
        "`Instance.SpawnPoint: boolean`": ["instance.md#physics-and-gameplay"]
    },
    "CharacterAnimation": {
        "the Instance `animation methods`": ["instance.md#animation"]
    },
    "SwingTwistJoint": {
        "`Instance:GetSwingTwistJoint()` and `SetSwingTwistJoint(...)`": [
            "instance.md#physics-and-gameplay"
        ]
    },
    "Identity": {"`Instance:GetIdentity().userId`": ["instance.md#identity"]},
    "DisplayName": {"`Instance:GetIdentity().displayName`": ["instance.md#identity"]},
    "Admin": {"`Instance:GetIdentity().isAdmin`": ["instance.md#identity"]},
    "UIClickable": {
        "`Instance.Activated: Signal`": ["instance.md#physics-and-gameplay"]
    },
    "SunLight": {"`game.Lighting.Sun`": ["game.md#lighting"]},
    "AmbientLight": {"`game.Lighting.Ambient`": ["game.md#lighting"]},
    "SkyBackground": {"`game.Lighting.Sky`": ["game.md#lighting"]},
    "SunShadows": {"`game.Lighting.Shadows`": ["game.md#lighting"]},
    "Exposure": {"`game.Lighting.Exposure`": ["game.md#lighting"]},
    "Stars": {"`game.Lighting.Stars`": ["game.md#lighting"]},
    "LensFlare": {"`game.Lighting.Flare`": ["game.md#lighting"]},
    "WorldConfig": {
        "`game.Physics.Gravity` and `FallenPartsDestroyHeight`": ["game.md#physics"]
    },
}


def render(name: str) -> str:
    if name in QUERY_VALUES:
        value_type, access = QUERY_VALUES[name]
        query_text = f"Queries expose `query.{name}[i]` as `{value_type}` ({access})."
    else:
        query_text = "This component can filter Query rows, but as of Luduvo dirty 37, it isn't available to read or write in the scripting's Query API."

    route = OTHER_ROUTES.get(name)
    if route:
        route_text = "For details on how to use this component, see "
        for text, link in route.items():
            link = link[0]
            text = text.split("`")
            for i, t in enumerate(text):
                if i % 2 != 0:
                    t = f"[`{t}`]({link}){{data-preview}}"
                route_text += t
    else:
        route_text = (
            "No separate fixed Instance property, Instance method, or game-service "
            "binding was found for its stored fields."
        )

    return f"""---
icon: lucide/box
---

!!! note
    This is still a stub. The scripting routes below are confirmed, but the component's editor behavior and serialized fields are not fully documented.

!!! note
    Studio's property groups and the scripting component API are different. A label shown in the Properties panel is not automatically a component name or a Luau field.

# {name}

`{name}` is a built-in Luduvo [Component](index.md){{data-preview}} responsible for dictating {responsibility}.

You can use it with [`game.World.Query`](../query.md), [`game.World.Each`](../query.md#gameworldeach), Query object methods (`Query:With` and `Query:Without`), and Instance/game component properties/methods (though this may change in future releases of Luduvo).

## Script access

{query_text} {route_text}
"""


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "docs" / "api" / "components"
    for component in COMPONENTS:
        (output / f"{component}.md").write_text(
            render(component), encoding="utf-8", newline="\n"
        )


if __name__ == "__main__":
    main()
