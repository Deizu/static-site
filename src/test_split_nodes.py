import unittest
from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_delimiter,
    Delimiter,
    split_nodes_image,
    split_nodes_link,
)


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

    def test_split_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]

        self.assertListEqual(
            expected,
            new_nodes,
        )

    def test_split_three_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and ![can you believe it](actually another one)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("can you believe it", TextType.IMAGE, "actually another one"),
        ]

        self.assertListEqual(
            expected,
            new_nodes,
        )

    def test_duplicate_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image](https://i.imgur.com/zjjcJKZ.png) a dupe",
            TextType.TEXT,
        )
        with self.assertRaises(Exception) as t:
            new_nodes = split_nodes_image([node])

    def test_split_two_links(self):
        node = TextNode(
            "This is text with some [linky text](https://i.imgur.com/zjjcJKZ.png) and some [dinky text](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with some ", TextType.TEXT),
            TextNode("linky text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and some ", TextType.TEXT),
            TextNode("dinky text", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
        ]

        self.assertListEqual(
            expected,
            new_nodes,
        )

    def test_split_three_links(self):
        node = TextNode(
            "This is text with some [linky text](https://i.imgur.com/zjjcJKZ.png) and some [dinky text](https://i.imgur.com/3elNhQu.png) and whaaaat [bro](do you even url?)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with some ", TextType.TEXT),
            TextNode("linky text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and some ", TextType.TEXT),
            TextNode("dinky text", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" and whaaaat ", TextType.TEXT),
            TextNode("bro", TextType.LINK, "do you even url?"),
        ]

        self.assertListEqual(
            expected,
            new_nodes,
        )

    def test_split_link_not_image(self):
        node = TextNode(
            "This is text with one [linky text](https://i.imgur.com/zjjcJKZ.png) and one ![image text](https://i.imgur.com/3elNhQu.png) at the same time.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with one ", TextType.TEXT),
            TextNode("linky text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(
                " and one ![image text](https://i.imgur.com/3elNhQu.png) at the same time.",
                TextType.TEXT,
            ),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_image_not_link(self):
        node = TextNode(
            "This is text with one [linky text](https://i.imgur.com/zjjcJKZ.png) and one ![image text](https://i.imgur.com/3elNhQu.png) at the same time.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode(
                "This is text with one [linky text](https://i.imgur.com/zjjcJKZ.png) and one ",
                TextType.TEXT,
            ),
            TextNode("image text", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" at the same time.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
