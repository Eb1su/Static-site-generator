import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "This is a text value", None, {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("a", "This is a text value", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("a", "This is a text value", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode ('a', 'click me!', {'href': 'https://www.google.com'})
        print(node.to_html())
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">click me!</a>')

if __name__ == "__main__":
    unittest.main()