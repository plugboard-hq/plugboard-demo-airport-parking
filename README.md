# plugboard-demo

A [Plugboard](https://github.com/plugboard-hq/plugboard) instance: a roastery's data team
and a hotel's guests on one host. This repository is what a company owns when it runs
Plugboard: which agents, which systems, who it is for. No Plugboard code.

```
uv sync                           # plugboard-ai and the agents
cp .env.example .env              # MODEL_NAME and its key
uv run python data/seed_demo.py   # the roastery's sales warehouse
uv run plugboard run              # migrate, seed, serve http://127.0.0.1:8010
```

Sign in from the header. The roastery's people are in a simulated Entra ID directory
(try `ana.ruiz`); the hotel's guests in a guest directory (`maya.lindqvist`). The
organisation follows who signed in, or pick one from the switcher.

## What is here

```
settings.py       from plugboard.settings import *, then the agents, providers and organisations
agents/docs/      the one agent that lives in this instance: the docs agent, over data/docs
data/seed_demo.py the roastery's warehouse, deterministic; data/docs the docs corpus
.env.example      the model and its key
```

The agents come from their own repositories, as dependencies in `pyproject.toml`:
[plugboard-genbi](https://github.com/plugboard-hq/plugboard-genbi) (Charts and the SQL
workbench), [plugboard-weather](https://github.com/plugboard-hq/plugboard-weather),
[plugboard-hotel](https://github.com/plugboard-hq/plugboard-hotel) (the guest agents). The
Data, People and Repos skill agents ship with the package. While the packages are
unpublished, `[tool.uv.sources]` points at checkouts beside this one; a released instance
pins versions instead.

Adding an agent: a dependency here, its module in `PLUGBOARD_AGENTS` in `settings.py`,
restart. Or, without an edit, `PLUGBOARD_EXTRA_AGENTS=<module>` in `.env`. A skill
repository: `PLUGBOARD_EXTRA_SKILLS=<path>`.

## The two organisations

**Nowhere Roastery** is the default: every agent installed, sign-in through the Entra ID
fixture, the Plugboard branding. **Hotel Aurora** is the guest-facing face of the same
host: the six hotel agents and Weather, sign-in through the guest directory, its own
colours. Both are declared in `settings.py` and seeded once; the console owns them after
that.
