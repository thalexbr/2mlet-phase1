import os

import requests
from bs4 import BeautifulSoup


def scrape_url(base_url: str, context: str) -> list:
    full_url = base_url + context

    # Sending a GET request to the website
    r = requests.get(full_url)

    # Parsing the HTML content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Extracting archors (elements with the <a> tag)
    archors = soup.find_all('a')

    tags = []

    # Find elements by HTML tags which starts with 'download'
    for archor in archors:
        if archor.get('href').startswith(os.getenv('FILE_DOWNLOAD_PREFIX')):
            tags.append(base_url + archor.get('href'))
    return tags
