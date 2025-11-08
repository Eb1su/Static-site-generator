import os

from block_markdown import markdown_to_html_node


def extract_title(markdown):
    markdown_lines = markdown.splitlines()
    for line in markdown_lines:
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("h1 header is not present")


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as markdown_file:
        markdown_file_string = markdown_file.read()
    with open(template_path, "r") as template_file:
        template_file_string = template_file.read()
    
    markdown_to_html = markdown_to_html_node(markdown_file_string).to_html()
    title = extract_title(markdown_file_string)
    
    replaced_template = template_file_string.replace(
        "{{ Title }}", title
    ).replace(
        "{{ Content }}", markdown_to_html
        ).replace(
            'href="/', f'href="{basepath}'
        ).replace(
            'src="/', f'src="{basepath}'
        )

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as html_page:
        html_page.write(replaced_template)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    children = os.listdir(dir_path_content)
    for child in children:
        child_path = os.path.join(f'{dir_path_content}/{child}')
        if os.path.isdir(child_path):
            os.mkdir(f'{dest_dir_path}/{child}')
            dst_path = os.path.join(f'{dest_dir_path}/{child}')
            generate_pages_recursive(basepath, child_path, template_path, dst_path)
        else:
            generate_page(basepath, child_path, template_path, f'{dest_dir_path}/{child[:-3]}.html')