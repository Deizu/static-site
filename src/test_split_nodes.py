import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, Delimiter


class TestTextNode(unittest.TestCase):
    def test_not_text_split(self):
        old_nodes = [TextNode("a", TextType.LINK, "https://www.boot.dev")]
        self.assertEqual(
            old_nodes,
            split_nodes_delimiter(old_nodes, Delimiter.DOUBLE_ASTERISKS, TextType.BOLD),
        )

    def test_split_bad_delimiter(self):
        old_nodes = [TextNode("a", TextType.LINK, "https://www.boot.dev")]
        with self.assertRaises(Exception) as t:
            split_nodes_delimiter(old_nodes, "/", TextType.BOLD)

    def test_pass_through_element(self):
        old_nodes = [TextNode("a", TextType.LINK, "https://www.boot.dev")]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, Delimiter.DOUBLE_ASTERISKS, TextType.BOLD),
            old_nodes,
        )

    def test_even_delimiters(self):
        old_nodes = [TextNode("a **this is bold** b", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, Delimiter.DOUBLE_ASTERISKS, TextType.BOLD),
            [
                TextNode("a ", TextType.TEXT),
                TextNode("this is bold", TextType.BOLD),
                TextNode(" b", TextType.TEXT),
            ],
        )

    def test_leading_delimiter(self):
        old_nodes = [TextNode("**this is bold**", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, Delimiter.DOUBLE_ASTERISKS, TextType.BOLD),
            [
                TextNode("", TextType.TEXT),
                TextNode("this is bold", TextType.BOLD),
                TextNode("", TextType.TEXT),
            ],
        )

    def test_odd_delimiters(self):
        old_nodes = [TextNode("a **this is bold** b**c", TextType.TEXT)]
        with self.assertRaises(Exception) as t:
            split_nodes_delimiter(old_nodes, Delimiter.DOUBLE_ASTERISKS, TextType.BOLD)
        self.assertEqual(
            t.exception.args[0], "invalid Markdown - unbalanced delimiters"
        )

    def test_bold_split(self):
        old_nodes = [TextNode("this is **bold** text", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, Delimiter.DOUBLE_ASTERISKS, TextType.BOLD),
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic_split(self):
        old_nodes = [TextNode("this is _emphasized_ in italics", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, Delimiter.UNDERSCORE, TextType.ITALIC),
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("emphasized", TextType.ITALIC),
                TextNode(" in italics", TextType.TEXT),
            ],
        )

    def test_code_split(self):
        old_nodes = [TextNode("this is `monospaced code` text", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, Delimiter.BACKTICK, TextType.CODE),
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("monospaced code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
