# google_scraper

google_scraper is a command-line utiility that automates the process of scraping google search results and associated 
metadata. Results are output into an xlsx file in the directory from which the script is run in reverse chronological order.

Data scraped by google_scraper includes urls, titles, content snippets, and date published. It will additionally
detect the language of a result, extract the domain from a url, and output the date the scrape was conducted.

## Installation

To install google_scraper directly into the site-packages directory of your virtual environment, run:

```shell
pip install git+https://github.com/agile-enigma/google_scraper.git
```

urlFormatter can now be used a command-line utility from anywhere in your directory structure or accessed 
as a module via `import google_scraper`.

## Usage
### Use Python Environment
```shell
source gscraper_env/bin/activate
python3 -m venv gscraper_env
```
The command-line arguments taken by google_scraper are as follows:
* **-s/--start_date**: The earliest date for which search results are desired (format: mm/dd/yyyy)
* **-s/--end_date**  : The latest date for which search results are desired (format: mm/dd/yyyy)
* **-q/--query**     : Google search string. If it contains multiple terms/operators, enclose it in single quotes

Here is an example query:

```shell
python3 -m google_scraper -s 05/01/2024 -e 05/10/2024 -q '"Georgia" AND "protests" AND "foreign agents law"'
```

## Example Output

<img width="762" alt="Screenshot 2024-05-13 at 11 05 59 PM" src="https://github.com/agile-enigma/google_scraper/assets/110642777/364a3894-1ecc-42a9-9adf-2d3f839ed941">
