class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise Exception(NotImplementedError)
    
    def props_to_html(self):
        htmlprops = ''
        for key in self.props:
            htmlprops += f' {key}="{self.props[key]}"'
        return htmlprops
    
    def __repr__(self):
        return f'tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}'
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            raise NotImplementedError
        return (
            self.tag == other.tag and 
            self.value == other.value and 
            self.props == other.props and 
            self.children == other.children
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super(LeafNode, self).__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f'{self.value}'
        
        if self.props == None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super(ParentNode, self).__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError

        if self.children == None:
            raise ValueError('ParentNode has no children')
        
        parent_string = f'<{self.tag}>'

        for child in self.children:
            parent_string += child.to_html()
        
        parent_string += f'</{self.tag}>'
        
        return parent_string
