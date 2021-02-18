"""Collect raw data from WFP."""

import shutil
import os
import pandas as pd
import requests
import bs4


BASE_URL = "https://data.humdata.org/dataset/wfp-food-prices"
ADM0_URL = "http://vam.wfp.org/sites/data/api/adm0code.csv"


def get_latest_data_url(url: str) -> str:
    """Find latest download link from button via bs4."""
    html_doc = requests.get(url).content
    soup = bs4.BeautifulSoup(html_doc, "html5lib")
    container = soup.find(
        "div", {"class": "hdx-btn-group hdx-btn-group-fixed"}
    )

    url_data = "https://data.humdata.org"
    for tag in container.find_all("a", href=True):
        if "wfpvam_foodprices.csv" in tag["href"]:
            url_data += tag["href"]

    if not url_data.endswith(".csv"):
        raise RuntimeError(f"Link doesn't look like .csv {url_data}")

    return url_data


def fetch_url_to_file(url: str, path: str) -> None:
    """ Fetch the file at url to path """

    print(f"Fetching file from {url} to {path}...")
    with requests.get(url, stream=True) as response:
        with open(path, "wb") as f:
            shutil.copyfileobj(response.raw, f)


def get_latest_data():
    """Fetch latest data from HDX."""
    if not os.path.isdir("./data"):
        os.makedirs("./data")

    data_url = get_latest_data_url(BASE_URL)
    # TODO: timestamp.
    fetch_url_to_file(data_url, "./data/wfp-food-prices.csv")
    fetch_url_to_file(ADM0_URL, "./data/wfp-countries.csv")


if __name__ == "__main__":
    get_latest_data()
    print("Finished collecting food price data.")
