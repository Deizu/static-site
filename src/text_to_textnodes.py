from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    Delimiter,
)


def text_to_textnodes(text):
    return split_nodes_image(
        split_nodes_link(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, TextType.TEXT)],
                        Delimiter.DOUBLE_ASTERISKS,
                        TextType.BOLD,
                    ),
                    Delimiter.UNDERSCORE,
                    TextType.ITALIC,
                ),
                Delimiter.BACKTICK,
                TextType.CODE,
            )
        )
    )
