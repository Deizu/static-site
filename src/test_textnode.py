import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node_str = str(node)
        expected = "TextNode(This is a text node, link, https://www.boot.dev)"
        self.assertEqual(node_str, expected)

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
