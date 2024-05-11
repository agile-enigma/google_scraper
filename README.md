# google_scraper

google_scraper is a command-line utiility that automates the process of scraping google search results and associated 
metadata. Results are output into an xlsx file in the directory from which the script is run in reverse chronological order.

Data scraped by google_scraper includes urls, titles, content snippets, and date published. It will additionally
detect the language of a result, extract the domain from a url, and output the date the scrape was conducted.

# Usage

The command-line arguments taken by google_scraper are as follows:
* **-s/--start_date**: The earliest date for which search results are desired (format: mm/dd/yyyy)
* **-s/--end_date**  : The latest date for which search results are desired (format: mm/dd/yyyy)
* **-q/--query**     : Google search string. If it contains multiple terms/operators, enclose it in single quotes

Here is an example query:

`python3 -m google_scraper -s 05/01/2024 -e 05/10/2024 -q '"Georgia" AND "protests" AND "foreign agents law"'`
