# How Plugboard works

Plugboard is a supervisor you plug agents into. The supervisor talks to the user and
decides, each turn, whether to answer directly, delegate to one agent, or ask the user a
question. Agents do the work.

## Registry

An agent is a package that registers a manifest: a name, a routing description written
for the supervisor, a persona the agent runs under, and a tool factory. The supervisor
never imports agents. At the start of each turn it asks the registry for the enabled
agents and generates one `call_<name>` tool per agent. Disabling an agent in the board
removes its tool on the next turn.

## Worker shell

Every agent runs inside the same shell: a ReAct loop built from the manifest, capped at
`max_iters`, returning a typed outcome of success, error, max iterations reached, or
awaiting user. The supervisor sees the outcome as the tool result.

## Widgets

Tools can put typed widgets on screen. A display widget such as a table is emitted and
the tool carries on. A blocking widget such as a question pauses the agent until the
user answers, and the answer becomes the tool's return value. That is how human-in-the-loop
works without special-casing it in the supervisor.

## Event stream

A turn streams events over server-sent events: status, routing, tool_call, widget, hitl,
message, done. The chat UI renders them as they arrive, and the assistant message stores
the tool calls and widgets so a reloaded conversation shows the same trail.
