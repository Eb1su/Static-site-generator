import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_grandchildren_children(self):
        grand_grandchildren_children_node = LeafNode('b', 'grand-grandchildren')
        grandchild_node = ParentNode('span', [grand_grandchildren_children_node])
        child_node = ParentNode('div', [grandchild_node])
        parent_node = ParentNode('div', [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><div><span><b>grand-grandchildren</b></span></div></div>'
        )
    
    def test_to_html_with_grandchildren_and_children(self):
        grandchild_node = LeafNode('i', 'grandchild')
        child_node = LeafNode('b', 'Lowest child:')
        child_node2 = ParentNode('span', [grandchild_node])
        parent_node = ParentNode('div', [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            '<div><b>Lowest child:</b><span><i>grandchild</i></span></div>'
        )

if __name__ == "__main__":
    unittest.main()