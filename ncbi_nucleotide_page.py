class NcbiNucleotidePage(object):

    def __init__(self):
        self.nucleotide_element = ''
        self.accession_element = '[title="Expand record details"]'
        self.close_button_on_details_modal = "//*[@id='cmscontent']/section/uswds-ncbi-app-root/uswds-ncbi-app-report/div/div[2]/uswds-ncbi-app-report-data/div/div[2]/div[1]/div[2]/div[1]/i"
        self.next_page_button_element = "//button[@aria-label=\"Next Page\"]"


    @staticmethod
    def __getinstance__(self):
        return NcbiNucleotidePage()