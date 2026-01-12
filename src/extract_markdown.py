import re


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def extract_title(markdown):
    title_matches = re.findall(r"^# (.+)", markdown)
    if len(title_matches) == 0:
        raise Exception("No H1 title found in markdown.")
    if len(title_matches) > 1:
        raise Exception("Multiple H1 titles found.")
    return title_matches[0].replace("# ", "").strip()
