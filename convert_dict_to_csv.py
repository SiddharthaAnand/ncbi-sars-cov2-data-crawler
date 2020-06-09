import json
from datetime import datetime


def get_json_from_file(rel_file_path=None):
    with open(rel_file_path + "/nucleotide_details_dict", 'r') as fp:
        x = json.load(fp)
    return x


def dict_to_csv(rel_file_path=None, dict={}):
    with open(rel_file_path + "/metadata_" + datetime.today().strftime('%Y-%m-%d') + ".csv", 'w') as fp:
        fp.write('Accession,Collection Date,Geo Location\n')
        for i in dict:
            if 'Geo Location' not in dict[i]:
                temp = i + "," + dict[i]['Collection Date'] + "," + "NULL" + '\n'
            else:
                temp = i + "," + dict[i]['Collection Date'] + "," + dict[i]['Geo Location'] + '\n'
            fp.write(temp)
        print(temp)


if __name__ == '__main__':
    dict = get_json_from_file()
    print(dict)
    dict_to_csv(dict=dict)
