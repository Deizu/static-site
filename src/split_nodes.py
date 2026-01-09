from textnode import TextType, TextNode
from enum import Enum


class Delimiter(Enum):
    BACKTICK = "`"
    UNDERSCORE = "_"
    DOUBLE_ASTERISKS = "**"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type not in TextType:
        raise Exception(f"invalid text type: {text_type}")
    if old_nodes is None or len(old_nodes) == 0:
        raise Exception("no nodes provided for splitting")
    if delimiter not in Delimiter:
        raise Exception("unknown delimiter")

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter.value in node.text:
            chunks = node.text.split(delimiter.value)
            if len(chunks) % 2 == 0:
                raise Exception("invalid Markdown - unbalanced delimiters")
            formatted = True if node.text[0] == delimiter else False
            for i in range(len(chunks)):
                new_nodes.append(
                    TextNode(chunks[i], text_type if formatted else TextType.TEXT)
                )
                formatted = not formatted
        else:
            raise Exception(f"delimiter {delimiter} not in target text {node}")

    return new_nodes
