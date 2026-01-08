from textnode import TextNode, TextType


def main():
    dummy = TextNode("Lorem ipsum", TextType.LINK.value, "https://www.boot.dev")
    print(dummy)


if __name__ == "__main__":
    main()
