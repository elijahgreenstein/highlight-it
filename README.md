# Highlight-It

Highlight-It is a plugin extension for the [Markdown-It-Py][mditpy] parser. The plugin configures an instance of `MarkdownIt` to use the [Pygments][pygments] syntax highlighter. It is adapted from the solution to <https://github.com/executablebooks/markdown-it-py/issues/256#issuecomment-2937277893>.
 
## Installation

Clone this repository. Change into the repository directory, type the following command, and press enter:

```bash
pip install .
```

## Usage

Import the Markdown-It-Py parser and the Highlight-It plugin:

```python
from markdown_it import MarkdownIt
from highlight_it import highlight_plugin
```

Follow [Markdown-It-Py conventions][mditpy-doc-plugins] to load the plugin:

```python
md = MarkdownIt().use(highlight_plugin)
```

Use the parser to render Markdown text as HTML:

````python
text = '''```python
x = 1
```
'''

html = md.render(text)
````

The parser renders the code block with syntax highlighted:

```html
<div class="highlight"><pre><span></span><span class="n">x</span> <span class="o">=</span> <span class="mi">1</span>
</pre></div>
```

[mditpy]: https://markdown-it-py.readthedocs.io/en/latest/
    "Markdown-It-Py"
[mditpy-doc-plugins]: https://markdown-it-py.readthedocs.io/en/latest/plugins.html
    "Markdown-It-Py: Plugin Extensions"
[pygments]: https://pygments.org
    "Pygments"

