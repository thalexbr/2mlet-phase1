import pandas as pd


def read_file(filename: str):
    if not filename:
        filename = 'downloads/20240615172009-Producao.csv'

    # Add try / except block
    file_dataframe = pd.read_csv(filename,sep=';')

    return file_dataframe.to_dict()
