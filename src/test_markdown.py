import unittest
from markdown_extract import extract_title

class TestMarkdown(unittest.TestCase):
    def test_correct_title_extract(self):
        md = '''
# h1 is located at the top
'''
        md_title = extract_title(md)
        self.assertEqual(
            md_title,
            'h1 is located at the top'
        )
    
    def test_hidden_title(self):
        md = '''
## not the title
### not the title
# title
## not the title
'''
        md_title = extract_title(md)
        self.assertEqual(
            md_title,
            'title'
        )