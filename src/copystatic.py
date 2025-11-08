import os
import shutil


def create_or_clear_public():
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")
    os.mkdir("./docs")


def copystatic(src, dst):
    children = os.listdir(src)
    for child in children:
        child_path = os.path.join(f"{src}/{child}")
        if os.path.isdir(child_path):
            if not os.path.exists(f"{dst}/{child}"):
                os.mkdir(f"{dst}/{child}")
            dst_path = os.path.join(f"{dst}/{child}")
            copystatic(child_path, dst_path)
        elif os.path.isfile(child_path):
            shutil.copy(child_path, dst)
