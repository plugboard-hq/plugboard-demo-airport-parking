# Onboarding FAQ

## How do I add an agent?

Create a package under `agents/`, build an `AgentManifest` and call `register`. Add the
package path to `PLUGBOARD_AGENTS` in settings. Restart, and the agent appears on the
board and in the supervisor's tools.

## Which model does it use?

Any model LiteLLM can reach. Set `MODEL_NAME` with a provider prefix, and `LLM_API_BASE`
if the model is served locally. The demo runs Qwen 3.6 on llama.cpp.

## Where does the demo data come from?

`data/seed_demo.py` builds a small SQLite sales warehouse with customers, products,
orders, order items and inventory. The numbers are seeded, so every run is identical.

## Who do I ask about access?

There is no access control in the demo. Everyone is an admin.
