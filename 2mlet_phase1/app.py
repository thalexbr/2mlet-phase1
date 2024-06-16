import json
import os
from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from modules.export import download_file

# User Modules
from modules.scraping import scrape_url
from modules.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
)

app = FastAPI()

# Loads variables from .env file, but does not overwrite existing ones
# Not overwriting will support dockerization in the future (hopefully)
# Environment variables will be provided by static .env file or by arguments
load_dotenv(override=True)


base_url = os.getenv('BASE_URL')


@app.get('/list_links', status_code=HTTPStatus.OK)
def list_links(current_user = Depends(get_current_user)):

    if not current_user['username']: 
        raise HTTPException (
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Unauthorized'
        )

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
def export_files(current_user = Depends(get_current_user)):
    # Scraping the links to the files to be downloaded
    # Later a POST method could be implemented passing the list on its body

    if not current_user['username']: 
        raise HTTPException (
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Unauthorized'
        )
    
    url_list = list_links(current_user)

    downloaded_files = {'file_list': []}

    for page in url_list['pages']:
        for link in page['page_links']:
            downloaded_files['file_list'].append(download_file(link))

    return downloaded_files


@app.get('/encrypt_pwd')
def encript_pwd():
    return {'password': get_password_hash(os.getenv('TEMP_PASSWORD'))}


@app.post('/token')
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):

    if form_data.username != os.getenv('TEMP_USER'):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password'
        )

    if not verify_password(
            form_data.password, os.getenv('TEMP_HASHED_PASSWORD')):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': form_data.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
