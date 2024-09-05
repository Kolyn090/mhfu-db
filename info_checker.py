
import os
import json


'''
    Check for info files validness
    1. All info tables must be under 'info/../'
    2. Info must have the exact same structure as its Table

    For reference tables:
        3. Ensure that every referencing field in Table contains a value
        that exists in the Referenced Table's referenced field
    For unique tables:
        4. Ensure every field marked true in -uni-di.json is unique
        within its own scope
    
    Tip: Check data_info_reference_example.png for visualization
    Tip: di stands for 'data-info'
'''


def get_Table_dir(data_info_dir):
    """
    | Returns the directory of Table of the given data info directory.
    :param data_info_dir: str
    :return: str
    """
    split = data_info_dir.split('/')
    parent_dir = '/'.join(split[:-3])
    table_name_split = split[-1].split('-')
    table_name = '-'.join(table_name_split[:-2]) + table_name_split[-1].replace('di.json', '-dt.json')
    return parent_dir+'/table/'+table_name


def compare_json_structures_ignore_type(json1, json2):
    """
    | Returns True if the two given JSON objects have the same
    | field structure. The type of each value is insensitive.
    :param json1: JSON
    :param json2: JSON
    :return: boolean
    """

    # Check if both are dictionaries
    if isinstance(json1, dict) and isinstance(json2, dict):
        # Check if both have the same keys
        if set(json1.keys()) != set(json2.keys()):
            return False
        # Recursively check the structure of each key
        for key in json1:
            if not compare_json_structures_ignore_type(json1[key], json2[key]):
                return False
        return True
    # Check if both are lists
    elif isinstance(json1, list) and isinstance(json2, list):
        # Compare length of lists
        if len(json1) != len(json2):
            return False
        # Recursively check the structure of each item
        for item1, item2 in zip(json1, json2):
            if not compare_json_structures_ignore_type(item1, item2):
                return False
        return True
    # There is no need to compare types in this case
    else:
        return True


def replace_object_with_null(json_obj, target_fields):
    """
    | Replace all objects that exactly contains the given fields
    | with null for the given JSON object
    | Example:
    | {
    |   data: {
    |       "one": 1
    |       "two": 2
    |   }
    | }
    | replace_object_with_null(data, ["one", "two"])
    | >>
    | {
    |   data: null
    | }
    :param json_obj: JSON
    :param target_fields: List(str)
    :return: boolean
    """

    if isinstance(json_obj, dict):
        # Check if all required fields are present in the current dictionary
        if all(field in json_obj for field in target_fields):
            return None  # Replace the entire object with None if all required fields are found
        else:
            # Recursively apply the function to each value in the dictionary
            for key, value in json_obj.items():
                json_obj[key] = replace_object_with_null(value, target_fields)
    elif isinstance(json_obj, list):
        # If the current item is a list, recursively apply the function to each element
        json_obj = [replace_object_with_null(item, target_fields) for item in json_obj]

    return json_obj


def get_relative_path(base_path, relative_path):
    """
    | Return a new path from path that is relative to the
    | base path
    | Example:
    | base_path = "./Farm"
    | relative_path = "../items.json"
    | >> "items.json"
    :param base_path: str
    :param relative_path: str
    :return: str
    """

    # Join the base path with the relative path
    full_path = os.path.join(base_path, relative_path)
    # Normalize the path to remove any redundant components like '..' or '.'
    normalized_path = os.path.normpath(full_path)
    return normalized_path


def get_nested_value(data, fields):
    for field in fields:
        if isinstance(data, dict):
            # Access the dictionary value by the key
            data = data.get(field)
        elif isinstance(data, list):
            result = []
            for item in data:
                if isinstance(item, dict) or isinstance(item, list):
                    result.append(get_nested_value(item, [field]))
                else: # Primitive type 
                    result.append(item)
            data = result
        else:
            return None  # Return None if the structure is not as expected
    return data


def confirm_reference(json_obj, data_info_dir, parent_key=""):
    """
    | Confirm that each value in Table (that is referencing field from
    | another table) actually also exists in the Referenced Table's values.
    | Example:
    |
    | Referenced Table
    | {
    |   "key": 0
    | }
    |
    | Table
    | {
    |   "field" references "key" in Referenced Table
    | }
    |
    | The goal will be to check whether all "fields" contain values
    | only appeared in Reference Table "key" field values (in this
    | example, only 0 is possible).
    |
    :param json_obj: JSON
    :param data_info_dir: str
    :param parent_key: str
    :return: void
    """

    split = data_info_dir.split('/')
    parent_dir = '/'.join(split[:-3])

    # Referenced Table (in relative path)
    stored_references_dir = ''
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == 'REFERENCES':
                # Store the path, the next key must be REFERENCES-FIELD
                stored_references_dir = value
            elif key == 'REFERENCES-FIELD':
                # Goal: Open Referenced Table
                # 'Table' is guaranteed to be in the parent directory
                # The field is storing a relative path based on the above path
                # Combine them to get the path to Referenced Table (which can be opened)
                referenced_table_dir = get_relative_path(parent_dir, stored_references_dir)
                assert referenced_table_dir.endswith('.json')
                with (open(referenced_table_dir, 'r') as referenced_table_file):
                    referenced_table = json.loads(referenced_table_file.read())

                    # Goal: Open Table
                    table_dir = get_Table_dir(data_info_dir)
                    with open(table_dir, 'r') as table_file:
                        table = json.loads(table_file.read())
                        # 'parent_key' can lead to the referencing field in Table
                        # 'value' can lead to the referenced field in Referenced Table
                        split_parent_key = [field for field in parent_key.split('/') if field != '']
                        split_value = [field for field in value.split('/') if field != '']

                        def flatten_list(lst):
                            flattened = []
                            for sublist in lst:
                                if isinstance(sublist, list):  # Check if the element is a list or tuple
                                    flattened.extend(flatten_list(sublist))  # Flatten only lists or tuples
                                else:
                                    flattened.append(sublist)  # Append the element directly if it's not a list/tuple
                            return flattened

                        table_values = flatten_list(list(map(lambda x: get_nested_value(x, split_parent_key), table)))
                        referenced_table_values = \
                            flatten_list(list(map(lambda x: get_nested_value(x, split_value), referenced_table)))

                        # print(table_values)

                        for a in table_values:
                            result = False
                            for b in referenced_table_values:
                                if a == b:
                                    result = True
                                if a == None:
                                    result = True
                            
                            assert result, f'{a} in {table_dir} is invalid.'
            else:
                confirm_reference(value, data_info_dir, parent_key + '/' + key)  # Recursively read the value

    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            confirm_reference(item, data_info_dir, parent_key)  # Recursively read each item in the list


def check_uniqueness(json_obj, data_info_dir, parent_key=""):
    """
    | Confirm that each field marked 'unique' is unique in 
    | the Referenced Table within its own scope.
    | Example:
    |
    | -uni-di.josn
    | {
    |   "key": true
    | }
    | 
    | Referenced Table 1
    |  [
    |   {
    |    "key": "apple"
    |   }
    |   {
    |    "key": "banana"
    |   }
    | ]
    | >> True
    |
    | Referenced Table 2
    |  [
    |   {
    |    "key": "apple"
    |   }
    |   {
    |    "key": "apple"
    |   }
    | ]
    | >> False
    | 
    | Referenced Table 3
    | {
    |   key: [
    |       "apple"
    |       "banana"
    |   ]
    | }
    | >> True
    | 
    | Referenced Table 4
    | {
    |   key: [
    |       "apple"
    |       "apple"
    |   ]
    | }
    | >> False
    |
    | Referenced Table 5
    | {
    |   key: [
    |       "apple"
    |       "apple"
    |   ]
    | }
    | >> False
    :param json_obj: JSON
    :param data_info_dir: str
    :param parent_key: str
    :return: void
    """

    split = data_info_dir.split('/')
    parent_dir = '/'.join(split[:-3])

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if isinstance(value, list) or isinstance(value, dict):
                check_uniqueness(value, data_info_dir, parent_key + '/' + key)
            else:
                # print(parent_key)
                if value == True:
                    actual_Table = parent_dir + '/' + split[-1].replace('-uni-di.json', '.json')
                    with (open(actual_Table) as actual_file):
                        actual_json = json.loads(actual_file.read())
                        fields = [field for field in parent_key.split('/') if field != '']
                        fields.append(key)
                        nested_value = get_nested_value(actual_json, fields)
                        if isinstance(nested_value[0], list):
                            for smaller_list in nested_value:
                                # There won't be any smaller list by program design
                                 assert len(smaller_list) == len(set(smaller_list))
                        else:
                            assert len(nested_value) == len(set(nested_value))

    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            if isinstance(item, dict):
                check_uniqueness(item, data_info_dir, parent_key)
            

def test_data_info(data_info_dir, data_info_content):
    """
    | Check whether all 4 rules on the top of this script hold
    :param data_info_dir: str
    :param data_info_content: str
    :return: void
    """

    if data_info_content == "":
        return
    split = data_info_dir.split('/')
    # 1. Data Info must be under 'info/../'
    assert split[-3] == 'info'
    # 2. Info must have the exact same structure as its Table
    '''
    Replace all
    {
        "REFERENCES": xxx,
        "REFERENCES-FIELD": xxx
    }
    with null
    '''
    data_info = json.loads(data_info_content)
    data_info_simplified = (
        replace_object_with_null(data_info, ['REFERENCES', 'REFERENCES-FIELD'])
        if data_info_dir.endswith('-ref-di.json')
        else data_info
    )
    # Open Table
    with open(get_Table_dir(data_info_dir)) as data_table_file:
        data_table = json.loads(data_table_file.read())
        # Check if Data Info and Table have the same structure
        # note: type is not important, only the fields are
        assert compare_json_structures_ignore_type(data_info_simplified, data_table), "Table structures are different!"

    # 3. Ensure that every referencing field in Table contains a value
    #    that exists in the Referenced Table's referenced field
    confirm_reference(data_info, data_info_dir)

    # 4. Ensure every field marked true in -uni-di.json is unique
    # within its own scope
    if data_info_dir.endswith('-uni-di.json'):
        check_uniqueness(data_info, data_info_dir)


def test_all_data_info_under(root):
    """
    | Perform checks on all Data Info under the given root.
    :param root: str
    :return: void
    """

    if os.path.isdir(root):
        subdirs = os.listdir(root)
        for subdir in subdirs:
            # Recursively iterates through all files in the database
            test_all_data_info_under(f"{root}/{subdir}")
    else:
        # Return if it's not a data info file
        if not root.endswith('-di.json'):
            return

        data_info_dir = root
        with open(data_info_dir, 'r') as data_info_file:
            test_data_info(data_info_dir, data_info_file.read())


if __name__ == "__main__":
    test_all_data_info_under('Farm/info/beehive')
