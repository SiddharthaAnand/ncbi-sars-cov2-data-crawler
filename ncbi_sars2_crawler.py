
import time
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


if __name__ == '__main__':
    import sys
    import json
    print("Starting time\t", time.asctime())
    t0 = time.time()
    complete_gnome_url_dict = store_gnome_urls(url=sys.argv[1], chromepath=sys.argv[2])
    tf = time.time()
    print(complete_gnome_url_dict)
    print('Time taken for the crawl\t', (tf-t0) / 3600)
    with open("complete_gnome_urls_store", "w") as gnome_url_data_store:
        json.dump(complete_gnome_url_dict, gnome_url_data_store)

    print(json.dumps(complete_gnome_url_dict, indent=4))