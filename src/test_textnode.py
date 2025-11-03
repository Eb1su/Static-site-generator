import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from text_to_html import text_node_to_html_node

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



if __name__ == "__main__":
    unittest.main()