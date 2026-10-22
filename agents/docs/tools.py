"""Tools for the docs agent: keyword search over markdown and read-by-name."""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path

from django.conf import settings

from plugboard.registry import registry
from plugboard.turn import current_turn


def _docs_dir() -> Path:
    return Path(settings.PLUGBOARD_DOCS_DIR)


def _load() -> dict[str, str]:
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(_docs_dir().glob("*.md"))}


def make_tools() -> list[Callable]:
    def list_docs() -> str:
        """List the documents available, one per line with their first heading."""
        docs = _load()
        lines = []
        for name, text in docs.items():
            heading = next(
                (ln.lstrip("# ").strip() for ln in text.splitlines() if ln.startswith("#")), ""
            )
            lines.append(f"{name}: {heading}")
        current_turn().tool_call("list_docs", {}, f"{len(docs)} documents")
        return "\n".join(lines) or "no documents"

    def search_docs(query: str) -> str:
        """Search all documents for the query words. Returns the best matching
        documents with a short excerpt each. Call read_doc to read one in full."""
        words = [w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2]
        scored = []
        for name, text in _load().items():
            low = text.lower()
            score = sum(low.count(w) for w in words)
            if score:
                idx = min((low.find(w) for w in words if low.find(w) >= 0), default=0)
                excerpt = text[max(0, idx - 80) : idx + 200].replace("\n", " ")
                scored.append((score, name, excerpt))
        scored.sort(reverse=True)
        top = scored[: int(registry.get("docs").settings.get("max_results", 3))]
        current_turn().tool_call(
            "search_docs",
            {"query": query},
            f"{len(top)} match(es): {', '.join(n for _, n, _ in top)}",
        )
        if not top:
            return "no documents match"
        return "\n\n".join(f"[{name}] ...{excerpt}..." for _, name, excerpt in top)

    def read_doc(name: str) -> str:
        """Read one document in full by file name, as returned by search_docs or list_docs."""
        docs = _load()
        text = docs.get(name) or docs.get(f"{name}.md")
        current_turn().tool_call("read_doc", {"name": name}, "read" if text else "not found")
        return text or f"no document named {name}; available: {', '.join(docs)}"

    return [list_docs, search_docs, read_doc]
