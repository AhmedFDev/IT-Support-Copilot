import json
import re
from pathlib import Path
from typing import Any


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "solutions.json"
)


def load_solutions() -> list[dict[str, Any]]:
    """Load troubleshooting solutions from the JSON knowledge base."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_words(text: str) -> set[str]:
    """Convert text into a normalized set of words."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def search_solutions(
    query: str,
    limit: int = 3,
) -> list[dict[str, Any]]:
    """Return the most relevant troubleshooting articles."""

    if not query.strip():
        return []

    query_words = get_words(query)
    solutions = load_solutions()
    results: list[dict[str, Any]] = []

    for solution in solutions:
        searchable_text = " ".join(
            [
                solution["title"],
                *solution["keywords"],
                *solution["steps"],
            ]
        )

        solution_words = get_words(searchable_text)

        # Count how many query words also appear in the article.
        score = len(query_words.intersection(solution_words))

        if score > 0:
            result = solution.copy()
            result["score"] = score
            results.append(result)

    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return results[:limit]