import json
import os
from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import FastAPI

from modules.export import download_file

# User Modules
from modules.scraping import scrape_url

app = FastAPI()

# Loads variables from .env file, but does not overwrite existing ones
# Not overwriting will support dockerization in the future (hopefully)
# Environment variables will be provided by static .env file or by arguments
load_dotenv(override=False)

base_url = os.getenv('BASE_URL')


@app.get('/list_links', status_code=HTTPStatus.OK)
def list_links():
    pages_file = open('static/pages.json', 'r', encoding='utf-8')

    pages = json.load(pages_file)

    url_list = {'pages': []}

    for page in pages['links']:
        context = 'index.php?opcao=' + page['option']
        url_list['pages'].append({
            'page_tab': page['tab'],
            'page_links': scrape_url(base_url, context),
        })
    return url_list

@app.get('/export_files', status_code=HTTPStatus.OK)
def export_files():
    
    # Scraping the links to the files to be downloaded
    # Later a POST method could be implemented passing the list on its body
    url_list = list_links()

    downloaded_files = { 'file_list' : []}

    for page in url_list['pages']:
        for link in page['page_links']:
            downloaded_files['file_list'].append(download_file(link))

    return downloaded_files


