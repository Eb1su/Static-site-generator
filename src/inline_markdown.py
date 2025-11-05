import re

from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_types):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception('Invalid Markdown Syntax')
        
        split_node = []
        content_text = node.text.split(delimiter)
        for i in range(len(content_text)):
            if i % 2 != 0:
                split_node.append(TextNode(content_text[i], text_types))
            else:
                split_node.append(TextNode(content_text[i], TextType.TEXT))
        new_nodes.extend(split_node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        all_images = extract_markdown_images(node.text)

        if len(all_images) == 0:
            new_nodes.append(node)
            continue

        current_txt = node.text

        for image in all_images:
            sections = current_txt.split(f'![{image[0]}]({image[1]})', 1)

            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            current_txt = sections[1]
        
        if len(current_txt) != 0:
            new_nodes.append(TextNode(current_txt, TextType.TEXT))
        return new_nodes




def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        all_links = extract_markdown_links(node.text)

        if len(all_links) == 0:
            new_nodes.append(node)
            continue

        current_txt = node.text

        for link in all_links:
            sections = current_txt.split(f'[{link[0]}]({link[1]})', 1)

            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            current_txt = sections[1]
        
        if len(current_txt) != 0:
            new_nodes.append(TextNode(current_txt, TextType.TEXT))
        return new_nodes