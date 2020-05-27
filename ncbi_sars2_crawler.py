import re
import time
import json
import argparse
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from ncbi_sars_cov2_datapage import NcbiSarsCov2DataPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from serialize_deserialize_data import read_as_json, read_urls_from_serialized_json_file


class NCBICrawler(object):
    def __init__(self, seed_url=None, chrome_path=None):
        self.driver = None
        self.seed_url = seed_url
        self.collected_urls_counter = 0
        self.nucleotide_urls_count = 0
        self.chrome_path = chrome_path
        self.genome_urls_store_dict = {}

    def open_chrome(self):
        self.driver = webdriver.Chrome(self.chrome_path)

    def go_to_seed_url(self):
        if self.seed_url is None or len(self.seed_url) == 0:
            print('Exception: self.seed_url is either None or empty')
            raise Exception
        if self.driver is None:
            print('Exception: self.driver is None')
            raise Exception
        self.driver.get(self.seed_url)

    def get_collected_urls_counter(self):
        return self.collected_urls_counter

    def set_collected_urls_counter(self):
        self.collected_urls_counter += 1

    def get_total_pages(self):
        pass

    def wait_for_element(self, element_to_wait_for, timeout_in_sec=5):
        WebDriverWait(self.driver, timeout_in_sec).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, element_to_wait_for))
        )



def store_genome_page_urls(url=None, chrome_path=None):
    """
    This method is used to store the relative urls for visiting those pages
    which contain the atcg sequences.
    :param url: The ncbi url page which enlists the newly added sars cov-2 anchor
    links and other meta-data.
    :param chrome_path: Absolute path to the chromedriver which is stored in your system.
    :return: None
    """
    if url is None or chrome_path is None:
        return {'parameter': 'is None'}
    else:
        urls_stored = 0
        gnome_urls_store = {}
        ncbi_nucleotide_page = NcbiSarsCov2DataPage.get_instance()
        ########################################################
        #               Get the page first                     #
        ########################################################
        driver = webdriver.Chrome(chrome_path)
        driver.get(url)
        url_count = 0
        pages = range(15)
        try:
            for page in range(15):
                ########################################################
                #               Get the page first                     #
                ########################################################
                print("Scraping page \t: %d" % page)
                ########################################################
                #           Choose the accession column                #
                ########################################################
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ncbi_nucleotide_page.accession_element))
                )
                time.sleep(2)
                accession_column_links = driver.find_elements_by_css_selector(ncbi_nucleotide_page.accession_element)
                urls_stored += len(accession_column_links)
                if urls_stored >= 200:
                    time.sleep(5)
                    accession_column_links = driver.find_elements_by_css_selector(ncbi_nucleotide_page.accession_element)
                print("Total number of accessions\t: %d" % urls_stored)

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
                    page_source = BeautifulSoup(driver.page_source, features='html.parser')
                    details_panel_for_accession = page_source.find('a', attrs={'title': 'Go to GenBank record'})
                    gnome_urls_store.update({details_panel_for_accession.text: details_panel_for_accession['href']})
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, ncbi_nucleotide_page.close_button_on_details_modal))
                    )
                    time.sleep(2)
                    close = driver.find_element_by_xpath(ncbi_nucleotide_page.close_button_on_details_modal)
                    close.click()
                print("%s urls stored\t" % (len(gnome_urls_store)))
                if len(accession_column_links) < 200:
                    break
                ###############################################################################################
                #               Find the button to go the next page                                           #
                ###############################################################################################
                next_page_button = driver.find_element_by_xpath(ncbi_nucleotide_page.next_page_button_element)
                next_page_button.send_keys('\n')
        except selenium.common.exceptions.InvalidElementStateException:
            return gnome_urls_store
    return gnome_urls_store


def crawl_atcg_sequence_page(base_url=None, query_param=None, accession_url_mapper=None, chrome_path=None, directory=None):
    if accession_url_mapper is not None:
        accessions_read = 0
        empty_read = {}
        driver = webdriver.Chrome(chrome_path)
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
                print('%d/%d accessions written to file' % (accessions_read, len(accession_url_mapper)))

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


def define_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-rel-url', 'collect_relative_urls')


if __name__ == '__main__':
    import sys

    start_time = time.asctime()
    t0 = time.time()
    ##################################################################
    #               Store genome urls from accession links          ##
    ##################################################################
    # url = https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=Severe%20acute%20respiratory%20syndrome%20coronavirus%202,%20taxid:2697049&Completeness_s=complete
    # complete_gnome_url_dict = store_gnome_urls(url=sys.argv[1], chromepath=sys.argv[2])
    # print(complete_gnome_url_dict)
    ##################################################################
    #       Store the gnome urls in a file                          ##
    ##################################################################
    # with open("complete_gnome_urls_store", "w") as gnome_url_data_store:
    #     json.dump(complete_gnome_url_dict, gnome_url_data_store)
    #
    # print(json.dumps(complete_gnome_url_dict, indent=4))
    ##################################################################
    #       Read stored urls and open and store atcg strings         #
    ##################################################################
    # json_data = read_urls_from_serialized_json_file('complete_gnome_urls_store')
    ##################################################################
    #       Read the empty accessions and store atcg strings again   #
    ##################################################################
    json_data = read_as_json(filename='empty_accessions_read')
    crawl_atcg_sequence_page(base_url='https://www.ncbi.nlm.nih.gov',
                             query_param='?expands-on=true',
                             accession_url_mapper=json_data,
                             chrome_path=sys.argv[1],
                             directory=sys.argv[2])
    tf = time.time()
    end_time = time.asctime()
    print('Time taken for the crawl \t: %f' % ((tf - t0) / 3600))
    print('Start time in human terms\t:%s' % start_time)
    print('End time in human terms  \t:%s' % end_time)
    print('#' * 60)

