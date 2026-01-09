from textnode import TextType, TextNode
from enum import Enum
from extract_markdown import extract_markdown_images, extract_markdown_links


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
            # raise Exception(f"delimiter {delimiter} not in target text {node}")
            new_nodes.append(node)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    def append_non_empty_text_node(text_node):
        if len(text_node.text) > 0 and text_node.text is not None:
            new_nodes.append(text_node)

    def split_on_single_images(images, node_string):
        remainder = node_string
        for i in range(len(images)):
            chunks = remainder.split(f"![{images[i][0]}]({images[i][1]})")
            if len(chunks) > 2:
                raise Exception("duplicate image strings detected")
            append_non_empty_text_node(TextNode(chunks[0], TextType.TEXT))
            new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            remainder = chunks[1]
        append_non_empty_text_node(TextNode(remainder, TextType.TEXT))

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            # not using append_non_empty_text_node in case of other types
            new_nodes.append(node)
            continue
        split_on_single_images(images, node.text)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    def append_non_empty_text_node(text_node):
        if len(text_node.text) > 0 and text_node.text is not None:
            new_nodes.append(text_node)

    def split_on_single_links(links, node_string):
        remainder = node_string
        for i in range(len(links)):
            chunks = remainder.split(f"[{links[i][0]}]({links[i][1]})")
            if len(chunks) > 2:
                raise Exception("duplicate link strings detected")
            append_non_empty_text_node(TextNode(chunks[0], TextType.TEXT))
            new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            remainder = chunks[1]
        append_non_empty_text_node(TextNode(remainder, TextType.TEXT))

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            # not using append_non_empty_text_node in case of other types
            new_nodes.append(node)
            continue
        split_on_single_links(links, node.text)

    return new_nodes
