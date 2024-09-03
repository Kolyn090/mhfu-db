import os

# Replaces files' suffix under the given directory


to_be_replaced = input("Please enter the suffix to be replaced (ex. -dt.json):\n")
replacement = input("Please the new suffix (ex. -dt.json):\n")


def replace_suffix_of(directory):
    new_dir = directory.replace(to_be_replaced, replacement)
    os.rename(directory, new_dir)


def replace_suffix_for_all_files_under(root):
    if os.path.isdir(root):
        subdirs = os.listdir(root)
        for subdir in subdirs:
            replace_suffix_for_all_files_under(f"{root}/{subdir}")
    else:
        if not root.endswith(to_be_replaced):
            return
        filedir = root
        with open(filedir, 'r') as file:
            replace_suffix_of(filedir)


if __name__ == "__main__":
    replace_suffix_for_all_files_under('.')
