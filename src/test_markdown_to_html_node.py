import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote.
> It has multiple lines.
> We don't care about multiple lines.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote. It has multiple lines. We don't care about multiple lines.</blockquote></div>",
        )

    def test_heading(self):
        md1 = "# H1"
        md2 = "## H2"
        md3 = "### H3"
        md4 = "#### H4"
        md5 = "##### H5"
        md6 = "###### H6"

        node1 = markdown_to_html_node(md1)
        node2 = markdown_to_html_node(md2)
        node3 = markdown_to_html_node(md3)
        node4 = markdown_to_html_node(md4)
        node5 = markdown_to_html_node(md5)
        node6 = markdown_to_html_node(md6)

        self.assertEqual(
            node1.to_html(),
            "<div><h1>H1</h1></div>",
        )
        self.assertEqual(
            node2.to_html(),
            "<div><h2>H2</h2></div>",
        )
        self.assertEqual(
            node3.to_html(),
            "<div><h3>H3</h3></div>",
        )
        self.assertEqual(
            node4.to_html(),
            "<div><h4>H4</h4></div>",
        )
        self.assertEqual(
            node5.to_html(),
            "<div><h5>H5</h5></div>",
        )
        self.assertEqual(
            node6.to_html(),
            "<div><h6>H6</h6></div>",
        )

    def test_unordered_list(self):
        md = """- one
- unordered
- list"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>unordered</li><li>list</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. one
2. ordered
3. list"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li>ordered</li><li>list</li></ol></div>",
        )
