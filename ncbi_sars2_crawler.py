import re
import sys
import time
import json
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from serializer_deserializer import *


def crawl_nucleotide_relative_url(url=None, chromepath=None):
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
            atgc_page_html = BeautifulSoup(driver.page_source, features='html.parser')
            seq_list = atgc_page_html.findAll('span', attrs={'id': re.compile(accession + '.\d+_\d+')})
            print('READING ATGC SEQUENCE GENOME FOR ACCESSION ID\t: %s' % accession)
            temp_seq_store = ""
            for seq in seq_list:
                if 'UTR' in seq.text:
                    continue
                temp_seq_store += seq.text
            temp_seq_store = temp_seq_store.replace(' ', '')

            if len(temp_seq_store) == 0:
                empty_read[accession] = accession_url_mapper[accession]
            with open(directory + "/" + accession + '.txt', 'w') as writer:
                writer.write(temp_seq_store)
            accessions_read += 1
            if accessions_read % 10 == 0:
                print('ATGC SEQUENCES WRITTEN ON FILE\t: %d/%d' % (accessions_read, len(accession_url_mapper)))

        ######################################################################
        #           Write timed out pages  in a file                        ##
        ######################################################################
        if len(empty_read) != 0:
            with open(relative_file_path + '/pages_timed_out', 'w') as writer:
                json.dump(empty_read, writer)

        ######################################################################
        #                           Some stats                              ##
        ######################################################################
        print('##' * 30)
        print('SIZE OF ATGC GENOME SEQUENCES WRITTEN\t\t: %d/%d' % (len(accession_url_mapper) - len(empty_read),
                                                                    len(accession_url_mapper)))
        print('WEB PAGES THAT TIMED OUT WHILE REQUESTING ATGC DATA\t: %d' % len(empty_read))


def init_args_parser_with_commands():
    import argparse
    parser = argparse.ArgumentParser(description="Crawl atgc sequence of sars2 coronavirus from ncbi!")
    parser.add_argument('--chromepath', type=str, help='Path to chrome driver')
    parser.add_argument('--filepath', type=str, help='Enter the relative file address to store the results.')
    parser.add_argument('crawl_timedout_pages', type=bool, help='Crawl the left over pages which were timed out')
    args = parser.parse_args()
    chrome_path = args.chromepath
    file_name = args.filepath
    crawl_timedout_pages = args.crawl_timed_out

    if file_name is None or chrome_path is None:
        print('Incorrect or empty parameters given')
        print('Please type \n\t $ python ncbi_sars2_crawler.py -h\n for more details')
        sys.exit(-1)

    return chrome_path, file_name, crawl_timedout_pages


if __name__ == '__main__':
    chrome_driver_path, relative_file_path, crawl_timedout_pages = init_args_parser_with_commands()
    base_url = "https://www.ncbi.nlm.nih.gov"
    path_params = "/labs/virus/vssi/#/virus"
    query_params = "?SeqType_s=Nucleotide&VirusLineage_ss=Severe%20acute%20respiratory%20syndrome%20coronavirus%202,%20taxid:2697049&Completeness_s=complete"
    url = base_url + path_params + query_params
    start_time = time.asctime()
    t0 = time.time()
    if chrome_driver_path is not None and relative_file_path is not None:
        nucleotide_relative_url_dict, nucleotide_details_dict = crawl_nucleotide_relative_url(url=url,
                                                                                              chromepath=chrome_driver_path)
        serialize_to_json(rel_file_path=relative_file_path,
                          genome_to_url_mapper_dict=nucleotide_relative_url_dict)

        serialize_metadata_of_nucleotide(rel_file_path=relative_file_path,
                                         nucleotide_details_dict=nucleotide_details_dict)

        json_data = read_urls_from_serialized_json_file(rel_file_path=relative_file_path)

        store_atcg_string(base_url='https://www.ncbi.nlm.nih.gov',
                          query_param='?expands-on=true',
                          accession_url_mapper=json_data,
                          chromepath=chrome_driver_path,
                          directory=relative_file_path)
    if crawl_timedout_pages is not None:
        json_data = read_as_json(rel_file_path=relative_file_path)
        store_atcg_string(base_url='https://www.ncbi.nlm.nih.gov',
                          query_param='?expands-on=true',
                          accession_url_mapper=json_data,
                          chromepath=chrome_driver_path,
                          directory=relative_file_path)

    tf = time.time()
    end_time = time.asctime()
    print('START TIME IN HUMAN TERMS     \t: %s' % start_time)
    print('END TIME IN HUMAN TERMS       \t: %s' % end_time)
    print('TIME(HRS) TAKEN FOR THE CRAWL \t: %f' % ((tf - t0) / 3600))
    print('##' * 30)

