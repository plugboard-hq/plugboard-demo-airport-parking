"""This instance: who it is for, which agents it has, which systems it reaches.

Everything else comes from plugboard.settings. Run it with ``uv run plugboard run``.
"""

from pathlib import Path

from plugboard.settings import *  # noqa: F403

BASE_DIR = Path(__file__).resolve().parent
DATABASES["default"]["NAME"] = BASE_DIR / "data" / "app.sqlite"  # noqa: F405

# The agents installed: a package each. The docs agent lives in this repository as the
# smallest example; the rest are dependencies in pyproject.toml.
PLUGBOARD_AGENTS = [
    "agents.docs",
    "plugboard_genbi",
    "plugboard_weather",
    "plugboard_hotel",
    *PLUGBOARD_AGENTS,  # noqa: F405  (PLUGBOARD_EXTRA_AGENTS from the environment)
]
PLUGBOARD_DOCS_DIR = BASE_DIR / "data" / "docs"

# The systems agents reach, behind provider contracts. Names are what manifests require.
PLUGBOARD_PROVIDERS = {
    # The roastery's sales warehouse: a seeded SQLite file (python data/seed_demo.py).
    "warehouse": {"connector": "sqlite", "path": str(BASE_DIR / "data" / "demo.sqlite")},
    # Simulated Entra ID tenant: the sign-in and the directory are a fixture.
    "directory": {
        "connector": "entra",
        "tenant_id": "roastery.onmicrosoft.com",
        "client_id": "plugboard-console",
        "domain": "roastery.example",
    },
    # The hotel's guest accounts: who signs in to the guest-facing organisation.
    "guests": {"connector": "guestbook", "domain": "guest.aurora.example"},
    # The checkouts beside this one: where the agent repositories live.
    "repos": {"connector": "local", "root": str(BASE_DIR.parent)},
}

# Who the assistant is for. Two faces of one host.
PLUGBOARD_ORGANISATIONS = [
    {
        "slug": "roastery",
        "name": "Nowhere Roastery",
        "identity_provider": "directory",
        "agents": [],  # empty on the default: every agent installed
        "branding": {"product_name": "Plugboard", "tagline": "the board you patch agents into"},
        "is_default": True,
    },
    {
        "slug": "aurora",
        "name": "Hotel Aurora",
        "identity_provider": "guests",
        "agents": [
            "reservations",
            "checkin",
            "cancellation",
            "extras",
            "requests",
            "property",
            "weather",
        ],
        "branding": {
            "product_name": "Hotel Aurora",
            "tagline": "your stay, in one conversation",
            "accent": "#8b5a2b",
            "header_background": "#fbf7f1",
            "header_border": "#e8dccb",
            "header_foreground": "#8a7a68",
            "background": "#f6f1ea",
            "surface": "#fffdfa",
        },
    },
]
