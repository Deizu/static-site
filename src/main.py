import os, logging, shutil
from markdown_to_html_node import markdown_to_html_node
from extract_markdown import extract_title

PUBLIC = "public"
LOGFILE = "logs/main.log"
TEMPLATE = "template.html"
STATIC = "static"
logger = logging.getLogger(__name__)


def copy_to_public(start_dir, structure):
    logger.info("Recursive Copy Routine")
    for fp in os.listdir(start_dir):
        source_path = os.path.join(start_dir, fp)
        target_path = os.path.join(structure, fp)
        if os.path.isdir(source_path):
            logger.debug("Copy - Directory")
            os.mkdir(target_path)
            copy_to_public(source_path, target_path)
        elif os.path.isfile(source_path):
            logger.debug("Copy - File")
            logger.info(f"Filepath: {source_path}\n\tStructure: {target_path}")
            shutil.copy(source_path, target_path)
        else:
            logger.debug("Copy - ???")
            print(f"Uh....{source_path} is neither a file nor directory. Now what?")


def generate_page(from_path, template_path, dest_path):
    placeholder_title = "{{ Title }}"
    placeholder_content = "{{ Content }}"
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    markdown = open(from_path, "r").read()
    template = open(template_path, "r").read()
    mhtml = markdown_to_html_node(markdown)
    html = mhtml.to_html()
    title = extract_title(markdown)
    page = template.replace(placeholder_title, title).replace(placeholder_content, html)
    dir = os.path.split(dest_path)[0]
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(dest_path, "w") as o:
        o.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("Content directory not found!")
    if len(os.listdir(dir_path_content)) == 0:
        raise Exception("Content directory is empty!")
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        target_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(source_path) and "." in item and item.split(".")[1] == "md":
            target_path = target_path.replace(".md", ".html")
            generate_page(source_path, template_path, target_path)
        elif os.path.isdir(source_path):
            generate_pages_recursive(source_path, template_path, target_path)


def main():
    if os.path.exists(LOGFILE):
        os.remove(LOGFILE)
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)

    logger.info("Started")

    if os.path.exists(PUBLIC):
        logger.info("Deleting public folder and its contents.")
        shutil.rmtree(PUBLIC)
    os.mkdir(PUBLIC)
    if os.path.exists(PUBLIC):
        logger.info("Created fresh public folder.")

    if not os.path.exists(STATIC):
        raise Exception("Source directory not found!")
    elif len(os.listdir(STATIC)) == 0:
        raise Exception("No files found to copy from source directory!")

    copy_to_public(STATIC, PUBLIC)

    generate_pages_recursive("content", TEMPLATE, "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    # generate_page(
    #     "content/blog/glorfindel/index.md",
    #     "template.html",
    #     "public/blog/glorfindel/index.html",
    # )
    # generate_page(
    #     "content/blog/majesty/index.md",
    #     "template.html",
    #     "public/blog/majesty/index.html",
    # )
    # generate_page(
    #     "content/blog/tom/index.md", "template.html", "public/blog/tom/index.html"
    # )
    # generate_page(
    #     "content/contact/index.md", "template.html", "public/contact/index.html"
    # )

    logger.info("Finished")


if __name__ == "__main__":
    main()
