from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'

def markdown_to_blocks(markdown):
    blocks = markdown.strip().split('\n\n')
    return [b.strip() for b in blocks if b.strip()]

def block_to_block_type(markdown):
    if len(markdown) == 0:
        raise Exception('Block is empty')
    
    if markdown[0] == '#':
        num_of_hashtags = 0

        for char in markdown:
            if char == '#':
                num_of_hashtags += 1
            else:
                break
        
        if 0 < num_of_hashtags <= 6 and markdown[num_of_hashtags] == ' ':
            return BlockType.HEADING
    
    elif markdown.startswith('```') and markdown.endswith('```'):
        return BlockType.CODE
    
    elif markdown[0] == '>':
        markdown_lines = markdown.splitlines()
        for line in markdown_lines:
            if len(line) == 0:
                return BlockType.PARAGRAPH
            if not line.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    elif markdown[0] == '-':
        markdown_lines = markdown.splitlines()
        for line in markdown_lines:
            if len(line) == 0:
                return BlockType.PARAGRAPH
            if not line.startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    
    markdown_lines = markdown.splitlines()
    if markdown_lines and markdown_lines[0].startswith('1. '):
        for i, line in enumerate(markdown_lines, start=1):
            if not line.startswith(f'{i}. '):
                break
        else:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH