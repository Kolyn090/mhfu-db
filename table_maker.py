import os
import json
import re

'''
    Creates a data table for the provided json file (Table).
    'Table' should be a list of objects with the same structure.
    For example:
    [
        {
            "name": "Joe"
        },
        {
            "name": "Danny"
        }
    ]
    is valid. While
    [
        {
            "name": "Joe
        },
        {
            "name": "Danny,
            "phone-number": 123456789
        }
    ]
    is invalid.

    The generated data will be put under table/ directory.

    The generated data tables should not be edited, as each time this script
    is run will override the changes. Therefore, you should only treat them
    as the place to inspect data type.

    Data table example:
    [
        {
            "name": "Joe",
            "phone-number": 777777777
        },
        {
            "name": "Danny",
            "phone-number": 123456789
        }
    ]
    will yield:
    [
        {
            "name": VARCHAR,
            "phone-number": INT
        }
    ]

    TODO:
    Note: Currently, once this script run, all json files will be subject for 
    data table creation, regardless its validness.
'''


def make_leaf_list(json_obj, keys):
    """
    | Make the last key in the nested keys
    | in json_obj a list of itself.
    :param json_obj: Object
    :param keys: str[]
    :return: void
    """
    d = json_obj
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = [d[keys[-1]]]


def convert_to_nested_json(flat_json):
    """
    | Make a complete json object based on
    | the provided flat (1D) json. If a
    | leaf in the json object is tagged
    | as an "ARRAY", it will be converted
    | to a list of itself.
    :param flat_json: str[]
    :return: JSON
    """

    nested_json = {}

    arrays = []
    for key, value in flat_json.items():
        if value == "ARRAY":
            arrays.append(key)

    for key, value in flat_json.items():
        parts = key.split('.')
        d = nested_json
        if value != "ARRAY":
            for part in parts[:-1]:
                if part not in d:
                    d[part] = {}
                d = d[part]
            d[parts[-1]] = value

    arrays.reverse()
    for arr in arrays:
        nested_arr = arr.split('.')
        make_leaf_list(nested_json, nested_arr)

    return nested_json


def get_all_property_name_val(data, parent_key=''):
    """
    | Convert the given json data to a special format.
    | This format treats primitive values in a list as
    | an object.
    |
    | Example:
    | {
    |     "name": "Max",
    |     "goods": [
    |         "milk",
    |         "apple"
    |     ]
    | } 
    | Will be converted to
    | {
    |     "name": "Max",
    |     "goods[0]": [
    |         "milk"
    |     ],
    |     "goods[1]": [
    |         "apple"
    |     ], 
    | } 
    :param data: JSON
    :param parent_key: str
    :return: dict
    """

    items = {}
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                items.update(get_all_property_name_val(v, new_key))
            else:
                items[new_key] = v
    elif isinstance(data, list):
        for i, v in enumerate(data):
            new_key = f"{parent_key}[{i}]"
            if isinstance(v, (dict, list)):
                items.update(get_all_property_name_val(v, new_key))
            else:
                # Can confirm that v is stored in a list, so make the
                # new_key's type as an "ARRAY" by making v as a list
                # of itself
                items[new_key] = [v]

    return items


def make_table_for_json(filedir, json_obj):
    """
    | Make a data table for the given json file.
    | For more details, please check the top of this script.
    :param filedir: str
    :param file: str
    :return: Void
    """

    def python_to_sql_type(py_type):
        type_mapping = {
            str: 'VARCHAR',
            int: 'INT',
            float: 'FLOAT',
            list: 'ARRAY',
            dict: 'JSON',
            type(None): 'NULL'
        }
        return type_mapping.get(py_type, 'UNKNOWN')

    def get_table_dir():
        split = filedir.split("/")
        os.makedirs('/'.join(split[:len(split)-1]) + "/table/", exist_ok=True)
        return '/'.join(split[:len(split)-1]) + "/table/" + split[len(split)-1].replace('.json', '-dt.json')

    # print(filedir)
    out = {}

    for element in json_obj:
        all_property_name_val = get_all_property_name_val(element)
        for key, value in all_property_name_val.items():
            # Remove the brackets to 'join' the keys
            real_key = re.sub(r'\[.*?\]', '', key)

            if key != real_key:
                # This key contains an array of objects,
                # store the key as an array in out for
                # later reference
                split_key = key.split('.')
                split_real_key = real_key.split('.')
                split_key.reverse()
                split_real_key.reverse()
                counter = 0
                for e1, e2 in zip(split_key, split_real_key):
                    if e1 != e2:
                        split_real_key.reverse()
                        array_key = '.'.join(str(item) for item in
                                             split_real_key[:len(split_real_key) - counter])
                        out[array_key] = [python_to_sql_type(list)]
                        break
                    counter += 1

            type_of_val = python_to_sql_type(type(value))
            if type_of_val == 'ARRAY':
                # Find out this is an array of what type
                first_element_type = type(value[0])
                type_of_val = f"ARRAY({python_to_sql_type(first_element_type)})"
                # Remove the 'ARRAY' in out since it's repetitive
                # For example, 'ARRAY(INT) is easier to read than 'ARRAY/ARRAY(INT)'
                out[real_key] = []

            if real_key not in out:
                out[real_key] = [type_of_val]
            elif type_of_val not in out[real_key]:
                # This property has a variant type
                out[real_key].append(type_of_val)

    # Convert [INT, VARCHAR] to INT/VARCHAR
    for key, value in out.items():
        out[key] = '/'.join(str(item) for item in out[key])

    # Write the table to -dt.json
    with open(get_table_dir(), 'w') as json_file:
        json.dump(convert_to_nested_json(out), json_file, indent=4)
        # json.dump(out, json_file, indent=4)


def make_table_for_all_json_files_under(root):
    if os.path.isdir(root):
        subdirs = os.listdir(root)
        for subdir in subdirs:
            make_table_for_all_json_files_under(f"{root}/{subdir}")
    else:
        if not root.endswith('.json'):
            return
        # Ignore special tables
        if root.endswith('-dt.json') or root.endswith('-di.json'):
            return

        filedir = root
        with open(filedir, 'r') as file:
            if file != '':
                make_table_for_json(filedir, json.loads(file.read()))


if __name__ == "__main__":
    make_table_for_all_json_files_under('.')
