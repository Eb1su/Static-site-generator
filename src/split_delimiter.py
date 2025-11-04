from textnode import TextNode, TextType

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
