import re

from enum import Enum
from htmlnode import *
from textnode import *
from inline_markdown import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.strip().split("\n\n")
    return [b.strip() for b in blocks if b.strip()]


def block_to_block_type(block):
    if len(block) == 0:
        raise Exception("Block is empty")

    if block[0] == "#":
        num_of_hashtags = 0

        for char in block:
            if char == "#":
                num_of_hashtags += 1
            else:
                break

        if 0 < num_of_hashtags <= 6 and block[num_of_hashtags] == " ":
            return BlockType.HEADING, block, num_of_hashtags

    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE, block

    elif block[0] == ">":
        markdown_lines = block.splitlines()
        for line in markdown_lines:
            if len(line) == 0:
                return BlockType.PARAGRAPH, block
            if not line.startswith(">"):
                return BlockType.PARAGRAPH, block
        return BlockType.QUOTE, block

    elif block[0] == "-":
        markdown_lines = block.splitlines()
        for line in markdown_lines:
            if len(line) == 0:
                return BlockType.PARAGRAPH, block
            if not line.startswith("- "):
                return BlockType.PARAGRAPH, block
        return BlockType.UNORDERED_LIST, block

    block_lines = block.splitlines()
    if block_lines and block_lines[0].startswith("1. "):
        for i, line in enumerate(block_lines, start=1):
            if not line.startswith(f"{i}. "):
                break
        else:
            return BlockType.ORDERED_LIST, block

    return BlockType.PARAGRAPH, block


def markdown_to_html_node(markdown):
    html_children = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        btype = block_type[0]
        btext = block_type[1]

        if btype == BlockType.CODE:
            lines = btext.splitlines()
            clean_text = '\n'.join(lines[1:-1]) + '\n'
            code_text = TextNode(clean_text, TextType.CODE)
            c_node = ParentNode(tag="pre", children=[text_node_to_html_node(code_text)])
            html_children.append(c_node)

        elif btype == BlockType.PARAGRAPH:
            clean_text = ' '.join(btext.split())
            p_node = ParentNode(tag="p", children=text_to_children(clean_text))
            html_children.append(p_node)

        elif btype == BlockType.HEADING:
            heading_num = block_type[2]
            clean_text = btext.strip("# ")
            h_node = ParentNode(
                tag=f"h{heading_num}", children=text_to_children(clean_text)
            )
            html_children.append(h_node)

        elif btype == BlockType.QUOTE:
            lines = btext.splitlines()
            clean_lines = []
            for line in lines:
                if line.startswith("> "):
                    clean_lines.append(line[2:])
                else:
                    clean_lines.append(line)
            clean_text = "\n".join(clean_lines)
            q_node = ParentNode(tag="blockquote", children=text_to_children(clean_text))
            html_children.append(q_node)

        elif btype == BlockType.UNORDERED_LIST:
            lines = btext.splitlines()
            li_nodes = []

            for line in lines:
                if line.startswith("- "):
                    item = line[2:]
                    li_node = ParentNode(tag="li", children=text_to_children(item))
                    li_nodes.append(li_node)

            ul_node = ParentNode(tag="ul", children=li_nodes)
            html_children.append(ul_node)

        elif btype == BlockType.ORDERED_LIST:
            lines = btext.splitlines()
            li_nodes = []
            for line in lines:
                match = re.match(r"^(\d+)\. (.*)$", line)
                if match:
                    item = match.group(2)
                    li_node = ParentNode(tag="li", children=text_to_children(item))
                    li_nodes.append(li_node)
            ol_node = ParentNode(tag="ol", children=li_nodes)
            html_children.append(ol_node)

    return ParentNode(tag="div", children=html_children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def text_node_to_html_node(node):
    if node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=node.text)
    if node.text_type == TextType.BOLD:
        return ParentNode(tag="b", children=[LeafNode(tag=None, value=node.text)])
    if node.text_type == TextType.ITALIC:
        return ParentNode(tag="i", children=[LeafNode(tag=None, value=node.text)])
    if node.text_type == TextType.CODE:
        return ParentNode(tag="code", children=[LeafNode(tag=None, value=node.text)])
    if node.text_type == TextType.LINK:
        return ParentNode(
            tag="a",
            props={"href": node.url},
            children=[LeafNode(tag=None, value=node.text)],
        )
    if node.text_type == TextType.IMAGE:
        return ParentNode(tag="img", children=[], props={"src": node.url, "alt": node.text})
    raise ValueError("Unknown text type")
