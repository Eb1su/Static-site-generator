import sys

from textnode import TextNode, TextType
from copystatic import create_or_clear_public, copystatic
from markdown_extract import generate_page, generate_pages_recursive


def main(basepath = '/'):
    create_or_clear_public()
    copystatic("./static", "./docs")
    generate_pages_recursive(basepath, './content', './template.html', './docs')


main(sys.argv[1])
