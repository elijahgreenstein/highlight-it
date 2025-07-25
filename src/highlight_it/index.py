"""Configuration for syntax highlighting with Pygments.

Adapted from <https://github.com/executablebooks/markdown-it-py> and solution to
<https://github.com/executablebooks/markdown-it-py/issues/256#issuecomment-2937277893>.

MIT License
Copyright (c) 2014 Vitaly Puzrin, Alex Kocharin.
Copyright (c) 2020 ExecutableBookProject

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from collections.abc import Sequence
from collections.abc import MutableMapping
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.utils import OptionsDict
from markdown_it.common.utils import escapeHtml, unescapeAll
from markdown_it.token import Token
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def tag(code):
    """Tag code, with HTML escaped, with `<pre>` and `<code>`."""
    return f"<pre><code>{escapeHtml(code)}</code></pre>"


def highlight_code(code: str, name: str, attrs: dict[str, str]) -> str | None:
    """Highlight code with Pygments.

    Adapted from solution to
    <https://github.com/executablebooks/markdown-it-py/issues/256#issuecomment-2937277893>.
    """
    if name == "":
        return None
    return pygments.highlight(code, get_lexer_by_name(name), HtmlFormatter())


def fence_modified(
    self,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: MutableMapping[str, Any],
) -> str:
    """Modified "fence" rule.

    This is an adaptation of the original Markdown-It-Py "fence" rule. The
    original rule places ``<pre>`` and ``<code>`` tags around the output code;
    when combined with the output from Pygments, this results in duplication of
    those tags. This modified rule returns either the direct output from
    Pygments (with syntax highlighting) or, when the code is left without
    highlighting, code with ``<pre>`` and ``<code>`` tags.

    Adapted from <https://github.com/executablebooks/markdown-it-py> and solution to
    <https://github.com/executablebooks/markdown-it-py/issues/256#issuecomment-2937277893>.

    .. note::

        This rule removes all attributes from the original "fence" token.
    """
    token = tokens[idx]
    info = unescapeAll(token.info).strip() if token.info else ""
    lang_name = ""

    if info:
        arr = info.split(maxsplit=1)
        lang_name = arr[0]

    if options.highlight:
        return options.highlight(token.content, lang_name, "") or tag(token.content)
    return tag(token.content)


def highlight_plugin(md: MarkdownIt) -> None:
    """Configure syntax highlighting with Pygments."""
    md.options["highlight"] = highlight_code
    md.add_render_rule("fence", fence_modified)
