import os
from datetime import datetime

import requests


def download_file(file_link: str) -> str:
    # file_link = 'http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv'
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')

    file_data = requests.get(file_link).content

    file_name = current_datetime + '-' + file_link.split('/')[-1]

    save_path = os.getenv('DOWNLOAD_FOLDER') + file_name

    with open(save_path, 'wb') as fp:
        fp.write(file_data)
    
    return file_name
