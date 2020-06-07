import json
import os


def read_urls_from_serialized_json_file(rel_file_path=None):
    """
    Read the relative urls from the serialized json file.
    Those urls contain the atcg sequence data.
    :param rel_file_path: The path to the file which stores the serialized url.
    :return:
    """
    if not os.path.exists(rel_file_path):
        print('FILE PATH DOES NOT EXIST TO BE READ:\t %s' % rel_file_path)
        raise FileNotFoundError
    with open(rel_file_path + "/genome_to_url_mapper_dict", 'r') as data_file:
        accession_url_mapper = json.load(data_file)
    return accession_url_mapper


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
            print('NUCLEOTIDE DETAILS DUMPED IN FILE:\t%s' % 'nucleotide_details_dict')


def serialize_to_json(rel_file_path=None, genome_to_url_mapper_dict=None):
    if not os.path.exists(rel_file_path):
        created = create_directory_if_not_present(rel_file_path)
    if created is True:
        with open(rel_file_path + "/genome_to_url_mapper_dict", "w") as fp:
            json.dump(genome_to_url_mapper_dict, fp)
            print('URL MAPPER DUMPED IN FILE:\t%s' % genome_to_url_mapper_dict)


def create_directory_if_not_present(rel_path):
    os.makedirs(rel_path)
    print("Directory %s created successfully!" % rel_path)
    return os.path.exists(rel_path)


def read_as_json(relative_file_path=None):
    if relative_file_path is not None:
        print('READING TIMED OUT PAGES AND CRAWLING AGAIN')
        try:
            with open(relative_file_path + '/pages_timed_out', 'r') as reader:
                return json.load(reader)
        except IOError as e:
            print('Exception while reading/loading file into json', e)
    raise FileNotFoundError

