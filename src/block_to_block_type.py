from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    starts_with_one = block[:3] == "1. "
    all_lines_start_with_digit_period_and_space = len(
        re.findall(r"\d+\.\s\n?", block)
    ) == len(block.split("\n"))
    all_numbers_are_incremented_by_one = list(range(1, len(block.split("\n")) + 1)) == [
        int(x) for x in list(re.findall(r"([0-9]+)\.\s\n?", block))
    ]

    if re.match(r"^\#{1,6} ", block) is not None:
        return BlockType.HEADING
    elif re.match(r"^```\n[^`]+```$", block) is not None:
        return BlockType.CODE
    elif len(re.findall(r"> .*\n?", block)) == len(block.split("\n")):
        return BlockType.QUOTE
    elif len(re.findall(r"- .*\n?", block)) == len(block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif (
        starts_with_one
        and all_lines_start_with_digit_period_and_space
        and all_numbers_are_incremented_by_one
    ):
        # print(
        #     f"Block: {block}\n\tStarts at 1?: {starts_with_one}\n\tAll lines start with a digit?: {all_lines_start_with_digit_period_and_space}\n\tAll numbers increment by one?: {all_numbers_are_incremented_by_one}"
        # )
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
