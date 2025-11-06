import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from text_to_html import text_node_to_html_node_test
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
        node = TextNode(
            "This is not a text node", TextType.TEXT, "https://www.boot.dev"
        )
        node2 = TextNode(
            "This is not a text node", TextType.TEXT, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node_test(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node_test(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node_test(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node_test(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("Link to boot.dev", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node_test(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link to boot.dev")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode(
            "Picture of cat",
            TextType.IMAGE,
            "https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg",
        )
        html_node = text_node_to_html_node_test(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg",
                "alt": "Picture of cat",
            },
        )

    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
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
            ],
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
            ],
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
            ],
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
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
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
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
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
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node,
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
        node = """
### Testing
"""
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual((BlockType.HEADING, "### Testing", 3), block_type)

    def test_code_to_code_block(self):
        node = """
```
This is a code block
```
"""
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual((BlockType.CODE, "```\nThis is a code block\n```"), block_type)

    def test_quote_to_quote_block(self):
        node = """
> test
> test
"""
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual((BlockType.QUOTE, "> test\n> test"), block_type)

    def test_unordered_to_unordered_block(self):
        node = """
- test
- test
"""
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual((BlockType.UNORDERED_LIST, "- test\n- test"), block_type)

    def test_ordered_to_ordered_block(self):
        node = """
1. test
2. test
"""
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual((BlockType.ORDERED_LIST, "1. test\n2. test"), block_type)

    def test_not_ordered_to_ordered_block(self):
        node = """
3. test
2. test
4. test
"""
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertNotEqual(
            (BlockType.ORDERED_LIST, "3. test\n2. test\n4. test"), block_type
        )

    def test_paragraph_to_paragraph_block(self):
        node = """
Hello world! This is a test!
"""
        block = markdown_to_blocks(node)
        block_type = block_to_block_type(block[0])
        self.assertEqual(
            (BlockType.PARAGRAPH, "Hello world! This is a test!"), block_type
        )

    def test_multiple_blocks(self):
        block_types = []
        node = """
This is **bolded** paragraph

> Quote
> test

- Another
- List
- Test
"""
        blocks = markdown_to_blocks(node)
        for block in blocks:
            block_type = block_to_block_type(block)
            block_types.append(block_type)
        self.assertEqual(
            [
                (BlockType.PARAGRAPH, "This is **bolded** paragraph"),
                (BlockType.QUOTE, "> Quote\n> test"),
                (BlockType.UNORDERED_LIST, "- Another\n- List\n- Test"),
            ],
            block_types,
        )

    def test_paragraphs(self):
        md = '''
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>',
        )

    def test_codeblock(self):
        md = '''
```
This is text that _should_ remain
the **same** even with inline stuff
```
'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>',
        )
    
    def test_heading(self):
        md = '''
### Test Heading
'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h3>Test Heading</h3></div>',
        )
    
    def test_quote(self):
        md = '''
> Test
> has
> passed
'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>Test\nhas\npassed</blockquote></div>',
        )

    def test_unordered(self):
        md = '''
- Test
- this
- list
'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>Test</li><li>this</li><li>list</li></ul></div>'
        )
    
    def test_ordered(self):
        md = '''
1. Test
2. ordered
3. list
'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>Test</li><li>ordered</li><li>list</li></ol></div>'
        )

if __name__ == "__main__":
    unittest.main()
