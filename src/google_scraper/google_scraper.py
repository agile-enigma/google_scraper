from bs4 import BeautifulSoup
import datetime
from langdetect import detect
import pandas as pd
import pytz
import re
from selenium import webdriver
import chromedriver_binary


def get_date_published(block):
    if block.find("span", class_="LEwnzc"):
        date_published = to_datetime(block.find("span", class_="LEwnzc").text)
    elif block.find("div", class_="gqF9jc"):
        date_published = to_datetime(block.find("div", class_="gqF9jc").text)
    elif block.find("cite", class_="qLRx3b") and re.search(
        r", \d{4}|ago", block.find("cite", class_="qLRx3b").text
    ):
        date_published = to_datetime(block.find("cite", class_="qLRx3b").text)
    else:
        date_published = None

    return date_published


def to_datetime(date_published):
    if date_published is not None:
        if re.search(r"months? ago", date_published):
            months_ago = int(re.search(r"\d", date_published).group())
            dt_object = datetime.datetime.now(
                pytz.timezone("US/Eastern")
            ) - datetime.timedelta(months=months_ago)
            dt_object = datetime.datetime.strptime(
                dt_object.strftime("%B %d, %Y"), "%B %d, %Y"
            )
        elif re.search(r"weeks? ago", date_published):
            weeks_ago = int(re.search(r"\d{,2} (?=week)", date_published).group())
            dt_object = datetime.datetime.now(
                pytz.timezone("US/Eastern")
            ) - datetime.timedelta(weeks=weeks_ago)
            dt_object = datetime.datetime.strptime(
                dt_object.strftime("%B %d, %Y"), "%B %d, %Y"
            )
        elif re.search(r"days? ago", date_published):
            days_ago = int(re.search(r"\d{,2} (?=day)", date_published).group())
            dt_object = datetime.datetime.now(
                pytz.timezone("US/Eastern")
            ) - datetime.timedelta(days=days_ago)
            dt_object = datetime.datetime.strptime(
                dt_object.strftime("%B %d, %Y"), "%B %d, %Y"
            )
        elif re.search(r"hours? ago", date_published):
            hours_ago = int(re.search(r"\d{,2} (?=hour)", date_published).group())
            dt_object = datetime.datetime.now(
                pytz.timezone("US/Eastern")
            ) - datetime.timedelta(hours=hours_ago)
            dt_object = datetime.datetime.strptime(
                dt_object.strftime("%B %d, %Y"), "%B %d, %Y"
            )
        elif re.search(r"minutes? ago", date_published):
            minutes_ago = int(re.search(r"\d{,2} (?=minute)", date_published).group())
            dt_object = datetime.datetime.now(
                pytz.timezone("US/Eastern")
            ) - datetime.timedelta(hours=minutes_ago)
            dt_object = datetime.datetime.strptime(
                dt_object.strftime("%B %d, %Y"), "%B %d, %Y"
            )
        else:
            if date_published and re.search(
                r'[a-zA-Z]{3} \d{,2},', date_published
                ):
                date_published = re.sub(r" — ", "", date_published)
                dt_object = datetime.datetime.strptime(date_published, "%b %d, %Y")
            else:
                dt_object = None

    return dt_object


def get_description(block):
    if re.search(r".*— ", str(block.find("div", class_="VwiC3b"))):
        description = re.sub(r".*— ", "", block.find("div", class_="VwiC3b").text)
    elif block.find("div", class_="ITZIwc"):
        description = block.find("div", class_="ITZIwc").text
    else:
        description = block.find("div", class_="VwiC3b").text

    return description


def df_to_excel(
    urls, domains, dates_published, dates_scraped, languages, titles, descriptions
):
    df = pd.DataFrame(
        {
            "url": urls,
            "domain": domains,
            "date_published": dates_published,
            "date_scraped": dates_scraped,
            "language": languages,
            "title": titles,
            "description": descriptions,
        }
    )
    df.sort_values(by=["date_published"], inplace=True, ascending=False)
    df.to_excel("output.xlsx", index=False)
    print('done!')


def scrape(start_date, end_date, query):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")

    urls = []
    titles = []
    dates_published = []
    descriptions = []
    dates_scraped = []
    languages = []
    domains = []

    print('...working...')
    results_page = 0
    done = False
    while not done:
        query_url = (
            "https://www.google.com/search?&tbs=cdr:1,cd_min:"
            + start_date.strftime("%m/%d/%Y")
            + ",cd_max:"
            + end_date.strftime("%m/%d/%Y")
            + "&q="
            + query
            + "&start="
            + str(results_page)
        )
        driver.get(query_url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        try:
            soup.find("div", {"id": "rso", "class": "dURPMd"}).children
        except AttributeError:
            done = True
            continue

        for block in soup.find("div", {"id": "rso", "class": "dURPMd"}).children:
            if (
                not block.get("class")[0] == "ULSxyf"
                and not block.find("span", {"id": "fld_1"})
                and not len(block.contents) == 0
            ):
                url = block.find("a", {"jsname": "UWckNb"}).get("href")
                domain = re.sub(r"https?://(www\.)?|(?<!/)/.*", "", url)
                title = block.find("h3", class_="LC20lb").text
                language = detect(title)
                date_published = get_date_published(block)
                date_scraped = datetime.datetime.strptime(
                    datetime.datetime.now(pytz.timezone("US/Eastern")).strftime(
                        "%B %d, %Y"
                    ),
                    "%B %d, %Y",
                )
                description = get_description(block)
                domains += [domain]
                urls += [url]
                titles += [title]
                dates_published += [date_published]
                languages += [language]
                dates_scraped += [date_scraped]
                descriptions += [description]

        results_page += 10

    df_to_excel(
        urls,
        domains,
        dates_published,
        dates_scraped,
        languages,
        titles,
        descriptions
    )
