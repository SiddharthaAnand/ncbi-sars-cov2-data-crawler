import json
import time


def create_directory_if_not_present(rel_path):
    import os
    if not os.path.exists(rel_path):
        os.makedirs(rel_path)
        print("Directory %s created successfully!" % rel_path)

def read_as_json(filename=None):
    if filename is not None:
        print('#' * 20)
        print('Reading empty accessions file')
        try:
            with open(filename, 'r') as reader:
                return json.load(reader)
        except IOError as e:
            print('Exception while reading/loading file into json', e)
    raise FileNotFoundError

