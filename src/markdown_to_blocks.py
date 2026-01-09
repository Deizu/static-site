def markdown_to_blocks(markdown):
    return [
        x
        for x in [block.strip() for block in markdown.split("\n\n")]
        if len(x) > 0 and not x.isspace()
    ]
