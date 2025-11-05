def markdown_to_blocks(markdown):
    markdown = markdown.strip('\n')
    blocks = markdown.split('\n\n')
    return blocks