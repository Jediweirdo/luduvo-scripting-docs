```luau title="Notice.server.lua"
local notices = EventTable("Notice", ToClients, {
    {"code", I32},
    {"position", Vec3},
})

notices:Push(1, Vector3.new(0, 5, 0)) -- broadcast
notices:PushTo(123456, 2, Vector3.new(10, 5, 0)) -- one user
```

The client declares the identical `ToClients` table and reads `notices.code[i]` and `notices.position[i]` during `Update`.
