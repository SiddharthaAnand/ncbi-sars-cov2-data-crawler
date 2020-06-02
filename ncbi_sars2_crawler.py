import re
import time
import json
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from serialize_data_to_file import read_as_json


def store_gnome_urls(url=None, chromepath=None):
    """
    This method is used to store the relative urls for visiting those pages
    which contain the atcg sequences.
    :param url: The ncbi url page which enlists the newly added sars cov-2 anchor
    links and other meta-data.
    :param chromepath: Absolute path to the chromedriver which is stored in your system.
    :return: None
    """
    if url is None or chromepath is None:
        return {'parameter': 'is None'}
    else:
        urls_stored = 0
        gnome_urls_store = {}
        ########################################################
        #               Get the page first                     #
        ########################################################
        driver = webdriver.Chrome(chromepath)
        driver.get(url)
        url_count = 0
        c = 0
        pages = range(16)
        nucleotide_details_dict = {}
        try:
            for page in range(16):
                ########################################################
                #               Get the page first                     #
                ########################################################
                print("Scraping page \t: %d" % page)
                ########################################################
                #           Choose the accession column                #
                ########################################################
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Expand record details"]'))
                )
                time.sleep(2)
                accession_column_links = driver.find_elements_by_css_selector('[title="Expand record details"]')
                urls_stored += len(accession_column_links)
                if urls_stored >= 200:
                    time.sleep(5)
                    accession_column_links = driver.find_elements_by_css_selector('[title="Expand record details"]')
                print(" total number f accessions\t: %d" % urls_stored)

                for link in accession_column_links:
                    try:
                        url_count += 1
                        link.click()
                    except selenium.common.exceptions.StaleElementReferenceException:
                        print("Exception encountered! \tRe-loading the page...")
                        new_accession_col_links = driver.find_elements_by_css_selector('[title="Expand record details"]')
                        link = new_accession_col_links[url_count]
                        time.sleep(2)
                        link.click()
                    source_code = BeautifulSoup(driver.page_source, features='html.parser')
                    details_panel_for_accession = source_code.find('a', attrs={'title': 'Go to GenBank record'})
                    gnome_urls_store.update({details_panel_for_accession.text: details_panel_for_accession['href']})
                    ################################################################################
                    #           Store other details as well                                        #
                    ################################################################################
                    nucleotide_details_panel = source_code.find('span', attrs={'id': 'detailProp'})
                    div_data = nucleotide_details_panel.findAll('div')
                    temp_dict = {}
                    c += 1
                    for data in div_data:
                        key, value = data.text.split(':')
                        temp_dict[key] = value

                    nucleotide_details_dict.update({details_panel_for_accession.text: temp_dict})
                    if c == 1:
                        print(nucleotide_details_dict)
                        print("temp: ", temp_dict)
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@id='cmscontent']/section/uswds-ncbi-app-root/uswds-ncbi-app-report/div/div[2]/uswds-ncbi-app-report-data/div/div[2]/div[1]/div[2]/div[1]/i"))
                    )
                    time.sleep(2)
                    close = driver.find_element_by_xpath("//*[@id='cmscontent']/section/uswds-ncbi-app-root/uswds-ncbi-app-report/div/div[2]/uswds-ncbi-app-report-data/div/div[2]/div[1]/div[2]/div[1]/i")
                    close.click()
                print("%s urls stored\t" % (len(gnome_urls_store)))
                if len(accession_column_links) < 200:
                    break
                ###############################################################################################
                #               Find the button to go the next page                                           #
                ###############################################################################################
                next_page_button = driver.find_element_by_xpath("//button[@aria-label=\"Next Page\"]")
                next_page_button.send_keys('\n')
        except selenium.common.exceptions.InvalidElementStateException:
            return gnome_urls_store
    return gnome_urls_store, nucleotide_details_dict


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


def store_atcg_string(base_url=None, query_param=None, accession_url_mapper=None, chromepath=None, directory=None):
    if accession_url_mapper is not None:
        accessions_read = 0
        empty_read = {}
        driver = webdriver.Chrome(chromepath)
        for accession in accession_url_mapper:
            try:
                driver.get(base_url + accession_url_mapper[accession] + query_param)
            except selenium.common.exceptions.TimeoutException as e:
                empty_read[accession] = accession_url_mapper[accession]
                continue
            time.sleep(4)
            atcg_page_html = BeautifulSoup(driver.page_source, features='html.parser')
            seq_list = atcg_page_html.findAll('span', attrs={'id': re.compile(accession + '.\d+_\d+')})
            print('Reading atcg sequence for accession %s' % accession)
            temp_seq_store = ""
            for seq in seq_list:
                if 'UTR' in seq.text:
                    continue
                temp_seq_store += seq.text
            temp_seq_store = temp_seq_store.replace(' ', '')

            if len(temp_seq_store) == 0:
                empty_read[accession] = accession_url_mapper[accession]
            with open(directory + accession + '.txt', 'w') as writer:
                writer.write(temp_seq_store)
            accessions_read += 1
            if accessions_read % 10 == 0:
                print('%d/%d accessions written to file' % (accessions_read,len(accession_url_mapper)))

        ######################################################################
        #           Write empty accessions in a file                        ##
        ######################################################################
        if len(empty_read) != 0:
            with open('empty_accessions_read', 'w') as writer:
                json.dump(empty_read, writer)

        ######################################################################
        #                           Some stats                              ##
        ######################################################################
        print('#' * 60)
        print('%d/%d accessions written' % (len(accession_url_mapper) - len(empty_read), len(accession_url_mapper)))
        print('Empty accessions read \t: %d' % len(empty_read))


def serialize_metadata_of_nucleotide(rel_file_name="data/third_run/nucleotide_details_dict", nucleotide_details_dict=None):
    """
    Store metadata for the nucleotide
    :param rel_file_name:
    :return: None
    """
    with open(rel_file_name, "w") as fp:
        json.dump(nucleotide_details_dict, fp)


def serialize_accession_to_rel_url_mapper(rel_file_path="data/third_run/genome_to_url_mapper_dict", genome_to_url_mapper_dict=None):
    with open(rel_file_path, "w") as fp:
        json.dump(genome_to_url_mapper_dict, fp)


def init_args_parser_with_commands():
    import argparse
    parser = argparse.ArgumentParser(description="Crawl atgc sequence of sars2 coronavirus from ncbi!")
    parser.add_argument('--url', type=str, help='Enter the ncbi url')
    parser.add_argument('--chromepath', type=str, help='Path to chrome driver')
    parser.add_argument('--filepath', type=str, help='Enter the relative file address to store the results.')
    args = parser.parse_args()
    chrome_path = args.chromepath
    absolute_ncbi_url = args.url
    file_name = args.filepath
    return absolute_ncbi_url, chrome_path, file_name


if __name__ == '__main__':
    """
    https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=Severe%20acute%20
    respiratory%20syndrome%20coronavirus%202,%20taxid:2697049&Completeness_s=complete
    """
    url, chrome_driver_path, relative_file_path = init_args_parser_with_commands()
    start_time = time.asctime()
    t0 = time.time()
    genome_rel_url_mapper, nucleotide_details_dict = store_gnome_urls(url=url, chromepath=chrome_driver_path)
    serialize_accession_to_rel_url_mapper(rel_file_path=relative_file_path,
                                          genome_to_url_mapper_dict=genome_rel_url_mapper)
    serialize_metadata_of_nucleotide(nucleotide_details_dict=nucleotide_details_dict)
    json_data = read_urls_from_serialized_json_file(file_path=relative_file_path)
    ##################################################################
    #       Read the empty accessions and store atcg strings again   #
    ##################################################################
    # json_data = read_as_json(filename='empty_accessions_read')
    # store_atcg_string(base_url='https://www.ncbi.nlm.nih.gov',
    #                   query_param='?expands-on=true',
    #                   accession_url_mapper=json_data,
    #                   chromepath=sys.argv[1],
    #                   directory=sys.argv[2])
    tf = time.time()
    end_time = time.asctime()
    print('Time taken for the crawl \t: %f' % ((tf - t0) / 3600))
    print('Start time in human terms\t:%s' % start_time)
    print('End time in human terms  \t:%s' % end_time)
    print('#' * 60)

