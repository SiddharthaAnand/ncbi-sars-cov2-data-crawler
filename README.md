# NCBI SARS COV-2 Data Crawler
A crawler which crawls the atcg sequence of the novel corona-virus2
found all over the world. This data is being uploaded at the [ncbi
website](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=Severe%20acute%20respiratory%20syndrome%20coronavirus%202,%20taxid:2697049&Completeness_s=complete).

## What it scrapes exactly?
It scrapes data from the [ncbi website](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=Severe%20acute%20respiratory%20syndrome%20coronavirus%202,%20taxid:2697049&Completeness_s=complete) and currently only crawls the atcg
sequence data being uploaded on the website. Other meta-data is not collected
currently.

The atcg sequence is stored in XXX.txt files in a directory given as
input by the user. So, if there are 2000 accessions, then there would be
2000 .txt files.

## How?
Using selenium and beautifulsoup.

## Installation
- Set up a virtual environment.
```
$ virtualenv -p /usr/bin/python3.5 venv
```
- Install requirements.
- Understand command-line arguments with the help option.
- Run the code.

## How to run?
```
$ python ncbi_sars2_crawler.py
```
## Work in progress
- Add option arguments parser to handle the code with command-line
arguments.
- Figure out ways to use headless browser and use multiple requests
at the same time.
- Incremental crawling by checking the newly updated dates and new data.
