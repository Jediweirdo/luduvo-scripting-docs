## Client-to-server example

Declare the same table in both scripts. The server validates the request and performs the authoritative mutation.

```luau title="Damage.client.lua"
local damage = EventTable("Damage", ToServer, {
    {"target", Entity},
    {"amount", F32},
})

local function requestDamage(target: Instance, amount: number)
    damage:Push(target, amount)
end
```

```luau title="Damage.server.lua"
local damage = EventTable("Damage", ToServer, {
    {"target", Entity},
    {"amount", F32},
})

function Update(_dt: number)
    for i = 1, damage.count do
        local senderId = damage.sender[i]
        local target = damage.target[i]
        local amount = damage.amount[i]

        if target ~= nil and amount > 0 and amount <= 100 then
            print(senderId, "requested damage to", target.Name, amount)
            -- Perform the validated server-side change here.
        end
    end
end
```

## Server-to-client example

```luau title="Notice.server.lua"
local notices = EventTable("Notice", ToClients, {
    {"code", I32},
    {"position", Vec3},
})

notices:Push(1, Vector3.new(0, 5, 0)) -- broadcast
notices:PushTo(123456, 2, Vector3.new(10, 5, 0)) -- one user
```

The client declares the identical `ToClients` table and reads `notices.code[i]` and `notices.position[i]` during `Update`.
