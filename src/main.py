from textnode import TextNode, TextType
from copystatic import create_or_clear_public, copystatic


def main():
    create_or_clear_public()
    copystatic("./static", "./public")


main()
