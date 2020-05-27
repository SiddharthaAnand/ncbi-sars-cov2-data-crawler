class NcbiSarsCov2DataPage(object):
    """
    URL which this class represents: https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&
    VirusLineage_ss=Severe%20acute%20respiratory%20syndrome%20coronavirus%202,%20taxid:2697049&Completeness_s=complete

    """
    def __init__(self):
        self.nucleotide_element = ''
        self.accession_element = '[title="Expand record details"]'
        self.close_button_on_details_modal = "//*[@id='cmscontent']/section/uswds-ncbi-app-root/uswds-ncbi-app-report/div/div[2]/uswds-ncbi-app-report-data/div/div[2]/div[1]/div[2]/div[1]/i"
        self.next_page_button_element = "//button[@aria-label=\"Next Page\"]"
        self.total_pages_element = ""
        return self

    @staticmethod
    def get_instance():
        return NcbiSarsCov2DataPage().__init__()


class GenbankCompleteGenomePage(object):
    """
    URL which this class represents: https://www.ncbi.nlm.nih.gov/nuccore/XXXXXXX
    where XXXXXX: is the accession id
    """
    def __init__(self):
        pass

