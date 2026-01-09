import unittest
from block_to_block_type import block_to_block_type, BlockType
from test_constants import multiline_code_block


class TestBlockToBlockType(unittest.TestCase):
    def test_block_heading(self):
        h0 = block_to_block_type("#a")  # invalid
        h1 = block_to_block_type("# a")
        h2 = block_to_block_type("## a")
        h3 = block_to_block_type("### a")
        h4 = block_to_block_type("#### a")
        h5 = block_to_block_type("##### a")
        h6 = block_to_block_type("###### a")
        h7 = block_to_block_type("####### a")  # invalid
        self.assertNotEqual(h0, BlockType.HEADING)
        self.assertEqual(h1, BlockType.HEADING)
        self.assertEqual(h2, BlockType.HEADING)
        self.assertEqual(h3, BlockType.HEADING)
        self.assertEqual(h4, BlockType.HEADING)
        self.assertEqual(h5, BlockType.HEADING)
        self.assertEqual(h6, BlockType.HEADING)
        self.assertNotEqual(h7, BlockType.HEADING)

    def test_block_multiline_code(self):
        mlc0 = block_to_block_type("none")  # invalid
        mlc1 = block_to_block_type(multiline_code_block)
        mlc2 = block_to_block_type("```\nleading only")  # invalid (leading only)
        mlc3 = block_to_block_type("\ntrailing only```")  # invalid (trailing only)
        mlc4 = block_to_block_type("``\nnope```")  # invalid
        mlc5 = block_to_block_type("```\nnope``")  # invalid
        self.assertNotEqual(mlc0, BlockType.CODE)
        self.assertEqual(mlc1, BlockType.CODE)
        self.assertNotEqual(mlc2, BlockType.CODE)
        self.assertNotEqual(mlc3, BlockType.CODE)
        self.assertNotEqual(mlc4, BlockType.CODE)
        self.assertNotEqual(mlc5, BlockType.CODE)

    def test_block_quote(self):
        q0 = block_to_block_type(">nope")  # invalid
        q1 = block_to_block_type("> something something\n> something else")
        q2 = block_to_block_type("> a\nb")  # invalid
        q3 = block_to_block_type("a\n> b")  # invalid
        self.assertNotEqual(q0, BlockType.QUOTE)
        self.assertEqual(q1, BlockType.QUOTE)
        self.assertNotEqual(q2, BlockType.QUOTE)
        self.assertNotEqual(q3, BlockType.QUOTE)

    def test_block_unordered_list(self):
        ul0 = block_to_block_type("-nope")  # invalid
        ul1 = block_to_block_type("- something something\n- something else")
        ul2 = block_to_block_type("- a\nb")  # invalid
        ul3 = block_to_block_type("a\n- b")  # invalid
        self.assertNotEqual(ul0, BlockType.UNORDERED_LIST)
        self.assertEqual(ul1, BlockType.UNORDERED_LIST)
        self.assertNotEqual(ul2, BlockType.UNORDERED_LIST)
        self.assertNotEqual(ul3, BlockType.UNORDERED_LIST)

    def test_block_ordered_list(self):
        ol0 = block_to_block_type("Z.")  # invalid
        ol1 = block_to_block_type("1. a\n2. b")
        ol2 = block_to_block_type("1.no\n2.no")  # invalid
        ol3 = block_to_block_type("0. no\n1. no")  # invalid
        ol4 = block_to_block_type("1. no\n3. no")  # invalid
        ol5 = block_to_block_type("1. no\nmore")  # invalid
        self.assertNotEqual(ol0, BlockType.ORDERED_LIST)
        self.assertEqual(ol1, BlockType.ORDERED_LIST)
        self.assertNotEqual(ol2, BlockType.ORDERED_LIST)
        self.assertNotEqual(ol3, BlockType.ORDERED_LIST)
        self.assertNotEqual(ol4, BlockType.ORDERED_LIST)
        self.assertNotEqual(ol5, BlockType.ORDERED_LIST)

    def test_block_paragraph(self):
        p0 = block_to_block_type("# a")  # invalid (heading)
        p1 = block_to_block_type(multiline_code_block)  # invalid (multiline code block)
        p2 = block_to_block_type(
            "> something something\n> something else"
        )  # invalid (block quote)
        p3 = block_to_block_type(
            "- something something\n- something else"
        )  # invalid (unordered list)
        p4 = block_to_block_type("1. a\n2. b")  # invalid (ordered list)
        p5 = block_to_block_type("just plan text, yo")
        self.assertNotEqual(p0, BlockType.PARAGRAPH)
        self.assertEqual(p0, BlockType.HEADING)
        self.assertNotEqual(p1, BlockType.PARAGRAPH)
        self.assertEqual(p1, BlockType.CODE)
        self.assertNotEqual(p2, BlockType.PARAGRAPH)
        self.assertEqual(p2, BlockType.QUOTE)
        self.assertNotEqual(p3, BlockType.PARAGRAPH)
        self.assertEqual(p3, BlockType.UNORDERED_LIST)
        self.assertNotEqual(p4, BlockType.PARAGRAPH)
        self.assertEqual(p4, BlockType.ORDERED_LIST)
        self.assertNotEqual(p5, BlockType.HEADING)
        self.assertNotEqual(p5, BlockType.CODE)
        self.assertNotEqual(p5, BlockType.QUOTE)
        self.assertNotEqual(p5, BlockType.UNORDERED_LIST)
        self.assertNotEqual(p5, BlockType.ORDERED_LIST)
        self.assertEqual(p5, BlockType.PARAGRAPH)
