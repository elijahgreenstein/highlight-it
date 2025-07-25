"""Test of Highlight-It plugin."""

from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
import pytest

from highlight_it import highlight_plugin
from highlight_it.index import highlight_code

DATA = Path(__file__).parent / "data"


@pytest.fixture
def md() -> MarkdownIt:
    """Parser extended with plugin."""
    return MarkdownIt().use(front_matter_plugin).use(highlight_plugin)


@pytest.fixture
def options() -> dict[str, Any]:
    """Expected options with highlight configured."""
    return {
        "maxNesting": 20,
        "html": True,
        "linkify": False,
        "typographer": False,
        "quotes": "“”‘’",
        "xhtmlOut": True,
        "breaks": False,
        "langPrefix": "language-",
        "highlight": highlight_code,
    }


def test_options(md: MarkdownIt, options: dict[str, Any]) -> None:
    """Test options are properly configured."""
    assert md.options == options


def test_parser(md: MarkdownIt) -> None:
    """Test parser with syntax highlighting configured."""
    with open(DATA / "test.md", encoding="utf-8") as f:
        source: str = f.read()
    with open(DATA / "test.html", encoding="utf-8") as f:
        html: str = f.read()
    assert md.render(source) == html
