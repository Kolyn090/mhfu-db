import os


def get_valid_nol_in(file):
    def is_valid_line(line):
        stripped_line = line.strip()
        return (stripped_line != '' and
                stripped_line != '{' and
                stripped_line != '}' and
                stripped_line != '[' and
                stripped_line != ']' and
                stripped_line != '},' and
                stripped_line != '],' and
                '"id":' not in stripped_line)

    content = file.read().split("\n")
    content = list(filter(is_valid_line, content))
    return len(content)


def count_number_of_lines(root, number):
    """
    | Recursion used to iterate through provided
    | directory, and count the total number of
    | valid lines in all .json files.
    :param root: String
    :param number: Int
    :return: Void
    """
    if os.path.isdir(root):
        subdirs = os.listdir(root)
        total = number
        for subdir in subdirs:
            total += count_number_of_lines(f"{root}/{subdir}", number)
        return total
    else:
        if not root.endswith('.json'):
            return number
        # Ignore tables
        if root.endswith('-dt.json'):
            return number

        filedir = root
        with open(filedir, 'r') as file:
            return number + get_valid_nol_in(file)


if __name__ == "__main__":
    with open("./README.md", 'r') as readme:
        lines = readme.readlines()

    index_of_count_line = -1
    for index, item in enumerate(lines):
        if item.strip().startswith("Current valid number of lines in DB:"):
            index_of_count_line = index

    if index_of_count_line != -1:
        lines[index_of_count_line] = (f"Current valid number of lines in DB: "
                                      f"{count_number_of_lines('.', 0)}\n")
        with open("./README.md", 'w') as readme:
            readme.writelines(lines)
