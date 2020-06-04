import json
import os


def serialize_metadata_of_nucleotide(rel_file_path=None, nucleotide_details_dict=None):
    """
    Store metadata for the nucleotide
    :param rel_file_path:
    :param nucleotide_details_dict:
    :return: None
    """
    if not os.path.exists(rel_file_path):
        created = create_directory_if_not_present(rel_file_path)
    if created is True:
        with open(rel_file_path + "/nucleotide_details_dict", "w") as fp:
            json.dump(nucleotide_details_dict, fp)


def serialize_accession_to_rel_url_mapper(rel_file_path=None, genome_to_url_mapper_dict=None):
    if not os.path.exists(rel_file_path):
        created = create_directory_if_not_present(rel_file_path)
    if created is True:
        with open(rel_file_path + "/genome_to_url_mapper_dict", "w") as fp:
            json.dump(genome_to_url_mapper_dict, fp)
            print('URL MAPPER DUMPED IN FILE:\t%s' % rel_file_path)


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

