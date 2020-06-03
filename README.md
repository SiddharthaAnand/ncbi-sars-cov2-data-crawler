# NCBI SARS COV-2 Data Crawler
A crawler which crawls the atcg sequence of the novel corona-virus2
found all over the world. This data is being uploaded at the [ncbi
website](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=Severe%20acute%20respiratory%20syndrome%20coronavirus%202,%20taxid:2697049&Completeness_s=complete) and being updated everyday.

## What it scrapes exactly?
It scrapes data from the [ncbi website](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=Severe%20acute%20respiratory%20syndrome%20coronavirus%202,%20taxid:2697049&Completeness_s=complete) and currently only crawls the atcg
sequence data being uploaded on the website. Other meta-data is not collected
currently.

The atcg sequence is stored in XXX.txt files in a directory given as
input by the user. So, if there are 2000 accessions, then there would be
2000 .txt files.

## How?
Using selenium and beautifulsoup.

We use selenium to simulate the user session on the browser.
BeautifulSoup is used to parse the html content from the page source, and
extract what we exactly need.

## Why use selenium?

In order to come up with this code quickly, I have used selenium. This could
have been done in several other ways as well wherein the exact request
could have been replicated in the python module and sent to the ncbi server.

Another way, is to create an exact Request being sent to the server, including
proper handling of cookies and other headers. Just a simple GET does not
return the data in html which we need. This ncbi web page is high on
javascript, which executes once it opens up in the web browser.


## Installation
Set up a virtual environment.(virtualenv needs to be present in your system.)
```
$ virtualenv -p /usr/bin/python3.5 venv
```
- Install requirements.
- Understand command-line arguments with the help option.
- Run the code.

## How to run?
```
$ python ncbi_sars2_crawler.py --url 'https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=Severe%20acute%20respiratory%20syndrome%20coronavirus%202,%20taxid:2697049&Completeness_s=complete' --chromepath /home/sid/github/chromedriver --filepath fourth_run >> logs_20200602
```
- To better understand the arguments from the command line, type the following command.
```
$ python ncbi_sars2_crawler.py -h
```

## Work in progress
- Add option arguments parser to handle the code with command-line
arguments.
- Figure out ways to use headless browser and use multiple requests
at the same time.
- Incremental crawling by checking the newly updated dates and new data.
- Create a directory if not present, when reading file path from the command line.
