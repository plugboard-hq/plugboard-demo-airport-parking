"""Docs agent: answers from a folder of markdown files.

A deliberately small agent so the plug-in contract is obvious: a manifest, a
persona, and a tool factory. Nothing here knows about the supervisor.
"""

from agents.docs.tools import make_tools
from plugboard import AgentManifest, register

register(
    AgentManifest(
        name="docs",
        title="Docs",
        routing_description=(
            "Answers questions from the team's internal documentation: how Plugboard works, "
            "onboarding, the data dictionary, the SQL style guide. Use for 'how does', "
            "'what is', 'where is it documented' questions. Give it the user's question; "
            "it returns an answer with the document it came from."
        ),
        persona=(
            "You answer questions strictly from the documentation you can search and read. "
            "Search first, read the most relevant document, then answer in a few sentences "
            "and name the document. If the docs do not cover it, say so plainly."
        ),
        tools=make_tools,
        examples=["how do I add an agent?", "what is the SQL style guide?"],
        config_schema={
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "title": "Search results",
                    "description": "How many documents a search returns",
                    "default": 3,
                }
            },
        },
        max_iters=5,
    )
)
