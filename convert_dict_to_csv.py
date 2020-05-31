def get_json_from_file(filename='nucleotide_details_dict'):
    import json
    with open('data/third_run/' + filename, 'r') as fp:
        x = json.load(fp)
    return x

def dict_to_csv(filename='metadata_20200531.csv', dict={}):
    with open('data/third_run/' + filename, 'w') as fp:
        fp.write('Accession,Collection Date,Geo Location\n')
        for i in dict:
            temp = ""
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