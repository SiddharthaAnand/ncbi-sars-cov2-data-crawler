import json
import os


def serialize_accession_to_rel_url_mapper(rel_file_path=None, genome_to_url_mapper_dict=None):
    if not os.path.exists(rel_file_path):
        created = create_directory_if_not_present(rel_file_path)
    if created is True:
        with open(rel_file_path + "/genome_to_url_mapper_dict", "w") as fp:
            json.dump(genome_to_url_mapper_dict, fp)


def create_directory_if_not_present(rel_path):
    os.makedirs(rel_path)
    print("Directory %s created successfully!" % rel_path)
    return os.path.exists(rel_path)


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

