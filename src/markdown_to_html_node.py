from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from text_to_textnodes import text_to_textnodes
from text_to_html import text_node_to_html_node
from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    Delimiter,
)


def markdown_to_html_node(markdown):
    # split into blocks
    blocks = markdown_to_blocks(markdown)
    all_children = []

    def change_newlines_to_spaces(x):
        return x.replace("\n", " ")

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block)
            for text_node in text_nodes:
                text_node.text = change_newlines_to_spaces(text_node.text)
            parent = ParentNode(
                "p", [text_node_to_html_node(text_node) for text_node in text_nodes]
            )
        if block_type == BlockType.CODE:
            block = block.replace("```\n", "").replace("```", "")
            parent = ParentNode("pre", [LeafNode("code", block)])
        if block_type == BlockType.QUOTE:
            block = change_newlines_to_spaces(block.replace("> ", ""))
            parent = LeafNode("blockquote", block)
        if block_type == BlockType.HEADING:
            heading_level = block.count("#")
            block = change_newlines_to_spaces(block)
            block = block.replace(f"{'#'*heading_level} ", "")
            parent = LeafNode(f"h{heading_level}", block)
        if block_type == BlockType.UNORDERED_LIST:
            list_items = [
                LeafNode("li", x.replace("- ", "")) for x in block.split("\n")
            ]
            parent = ParentNode("ul", list_items)
        if block_type == BlockType.ORDERED_LIST:
            list_items = []
            ordered_items = block.split("\n")
            for i in range(0, len(ordered_items)):
                list_items.append(
                    LeafNode("li", ordered_items[i].replace(f"{i+1}. ", ""))
                )
            parent = ParentNode("ol", list_items)
        all_children.append(parent)
    top_level_parent = ParentNode("div", all_children)
    # print(f"\n\nMTHN -> HTML | {top_level_parent.to_html()}")
    return top_level_parent
