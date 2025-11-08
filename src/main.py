from textnode import TextNode, TextType
from copystatic import create_or_clear_public, copystatic
from markdown_extract import generate_page, generate_pages_recursive


def main():
    create_or_clear_public()
    copystatic("./static", "./public")
    generate_pages_recursive('./content', './template.html', './public')


main()
