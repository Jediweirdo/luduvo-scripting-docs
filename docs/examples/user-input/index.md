---
icon: lucide/mouse
---

# User Input

Curently, Luduvo has two methods of input:

- [`Instance.Activated`](../../api/instances.md#automatic-built-in-signal-scenarios) for accepted UI-control activation on the client.
- `Instance:GetMoveIntent()` for server-side character movement intent.

True input handling (mouse, keyboard, gamepad, etc.) is currently not implemented.
