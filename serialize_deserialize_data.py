import json
import time


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


def read_urls_from_serialized_json_file(file_path=None):
    """
    Read the relative urls from the serialized json file.
    Those urls contain the atcg sequence data.
    :param file_path: The path to the file which stores the serialized url.
    :return:
    """
    if file_path is not None:
        with open(file_path, 'r') as data_file:
            accession_url_mapper = json.load(data_file)
        return accession_url_mapper
    raise FileNotFoundError
