import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from text_to_html import text_node_to_html_node
from inline_markdown import *
from block_markdown import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is not a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_type_not_eq(self):
        node = TextNode("This is not a text node", TextType.ITALIC)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_url_eq(self):
        node = TextNode("This is not a text node", TextType.TEXT, 'https://www.boot.dev')
        node2 = TextNode("This is not a text node", TextType.TEXT, 'https://www.boot.dev')
        self.assertEqual(node, node2)
    
    def test_text(self):
        node = TextNode('This is a text node', TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, 'This is a text node')
    
    def test_bold(self):
        node = TextNode('This is a text node', TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'This is a text node')

    def test_italic(self):
        node = TextNode('This is a text node', TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'This is a text node')
    
    def test_code(self):
        node = TextNode('This is a text node', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, 'This is a text node')
    
    def test_link(self):
        node = TextNode('Link to boot.dev', TextType.LINK, 'https://www.boot.dev')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'Link to boot.dev')
        self.assertEqual(html_node.props, {'href': 'https://www.boot.dev'})
    
    def test_image(self):
        node = TextNode('Picture of cat', TextType.IMAGE, 'https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src': 'https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg', 'alt': 'Picture of cat'})

    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_split_delimiter_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_split_code_then_bold(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with a **bold block** word", TextType.TEXT),
        ]
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_not_images(self):
        matches = extract_markdown_images(
            "This is text with an incorrect [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertNotEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches)

    def test_split_images(self):
        node = TextNode(
            'This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)',
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            'This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)',
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode('This is text with a link ', TextType.TEXT),
                TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
                TextNode(' and ', TextType.TEXT),
                TextNode(
                    'to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev'),
            ],
            new_nodes
        )


    def test_text_to_nodes(self):
        text = (
            'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        )
        node = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node
        )


    def test_markdown_to_block(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_heading_to_heading_block(self):
        node = '''
### Testing
'''
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual(BlockType.HEADING, block_type)


    def test_code_to_code_block(self):
        node = '''
```
This is a code block
```
'''
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual(BlockType.CODE, block_type)


    def test_quote_to_quote_block(self):
        node = '''
> test
> test
'''
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual(BlockType.QUOTE, block_type)


    def test_unordered_to_unordered_block(self):
        node = '''
- test
- test
'''
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)


    def test_ordered_to_ordered_block(self):
        node = '''
1. test
2. test
'''
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual(BlockType.ORDERED_LIST, block_type)


    def test_not_ordered_to_ordered_block(self):
        node = '''
3. test
2. test
4. test
'''
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertNotEqual(BlockType.ORDERED_LIST, block_type)


    def test_paragraph_to_paragraph_block(self):
        node = '''
Hello world! This is a test!
'''
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual(BlockType.PARAGRAPH, block_type)



if __name__ == "__main__":
    unittest.main()