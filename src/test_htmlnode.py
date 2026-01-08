import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_no_inputs(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = HTMLNode("a", "b", [HTMLNode("c")], {"d": "e"})
        node_str = str(node)
        expected = "HTMLNode | Tag: a | Value: b | Children: 1 | Props: {'d': 'e'}"
        self.assertEqual(node_str, expected)
        node_blank = HTMLNode()
        node_blank_str = str(node_blank)
        expected_blank = "HTMLNode | Tag: - | Value: - | Children: - | Props: -"
        self.assertEqual(node_blank_str, expected_blank)

    def test_props_to_html(self):
        node = HTMLNode("a", "b", [HTMLNode("c")], {"d": "e"})
        self.assertEqual(node.props_to_html(), ' d="e" ')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Test b.")
        self.assertEqual(node.to_html(), "<b>Test b.</b>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_greatgrandchildren(self):
        great_grandchild_node = LeafNode("b", "grandchild")
        grandchild_node = ParentNode("em", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><em><b>grandchild</b></em></span></div>",
        )

    def test_parent_no_children(self):
        with self.assertRaises(ValueError) as t:
            ParentNode("p", []).to_html()


if __name__ == "__main__":
    unittest.main()
