import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_image_extractions(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and also ![another](https://fake.fake) as a surprise"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://fake.fake"),
            ],
            matches,
        )

    def test_no_image_matches(self):
        matches = extract_markdown_images(
            "This is text with an ![imagehttps://i.imgur.com/zjjcJKZ.png and also ![another]) as a surprise"
        )
        self.assertListEqual(
            [],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and also an ![image](https://notcaptured.fake)) as a surprise"
        )
        self.assertListEqual(
            [("link", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_multiple_markdown_links(self):
        mmatches = extract_markdown_links("abcd[a](b) ---[c](d)....![not](this)")
        self.assertEqual(
            [
                ("a", "b"),
                ("c", "d"),
            ],
            mmatches,
        )

    def test_extract_no_link_matches(self):
        matches = extract_markdown_links(
            "This is text with an ![imagehttps://i.imgur.com/zjjcJKZ.png and also ![another]) as a surprise"
        )
        self.assertListEqual(
            [],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
