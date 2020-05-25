import re
import time
import json
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from empty_accessions import read_as_json


def store_gnome_urls(url=None, chromepath=None):
    if url is None:
        return {'url': 'is empty'}
    else:
        urls_stored = 0
        gnome_urls_store = {}
        ########################################################
        #               Get the page first                     #
        ########################################################
        driver = webdriver.Chrome(chromepath)
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
                    gnome_urls_store.update({details_panel_for_accession.text:details_panel_for_accession['href']})
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@id='cmscontent']/section/uswds-ncbi-app-root/uswds-ncbi-app-report/div/div[2]/uswds-ncbi-app-report-data/div/div[2]/div[1]/div[2]/div[1]/i"))
                    )
                    time.sleep(2)
                    close = driver.find_element_by_xpath("//*[@id='cmscontent']/section/uswds-ncbi-app-root/uswds-ncbi-app-report/div/div[2]/uswds-ncbi-app-report-data/div/div[2]/div[1]/div[2]/div[1]/i")
                    close.click()
                print("%s urls stored\t" % (len(gnome_urls_store)))
                if len(accession_column_links) < 200:
                    break
                next_page_button = driver.find_element_by_xpath("//button[@aria-label=\"Next Page\"]")
                next_page_button.send_keys('\n')
        except selenium.common.exceptions.InvalidElementStateException:
            return gnome_urls_store
    return gnome_urls_store


def read_urls_from_serialized_json_file(file_path=None):
    if file_path is not None:
        with open(file_path, 'r') as data_file:
            accession_url_mapper = json.load(data_file)
        return accession_url_mapper
    raise FileNotFoundError


def store_atcg_string(base_url=None, query_param=None, accession_url_mapper=None,
                      chromepath=None, directory=None):
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
    store_atcg_string(base_url='https://www.ncbi.nlm.nih.gov',
                      query_param='?expands-on=true',
                      accession_url_mapper=json_data,
                      chromepath=sys.argv[1],
                      directory=sys.argv[2])
    tf = time.time()
    end_time = time.asctime()
    print('Time taken for the crawl \t: %f' % ((tf - t0) / 3600))
    print('Start time in human terms\t:%s' % start_time)
    print('End time in human terms  \t:%s' % end_time)
    print('#' * 60)

