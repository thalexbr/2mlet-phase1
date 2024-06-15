import os

import requests
from bs4 import BeautifulSoup


def scrape_url(base_url: str, context: str) -> list:
    """
    Scrapes a URL looking for downloadable contents

    Args:
        base_url (str): The base URL without any context
        context  (str): An optional context in case it exists
    Returns:
        str: The customized file name prefixed with the current date and time
    """

    full_url = base_url + context

    # Sending a GET request to the website
    r = requests.get(full_url)

    # Parsing the HTML content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Extracting archors (elements with the <a> tag)
    archors = soup.find_all('a')

    tags = []

    # Selects anchors which start with the prefix specified in the .env file
    for archor in archors:
        if archor.get('href').startswith(os.getenv('FILE_DOWNLOAD_PREFIX')):
            tags.append(base_url + archor.get('href'))
    return tags
