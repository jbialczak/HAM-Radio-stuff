import requests
import pandas as pd
import io


def download_pota_reference_list() -> object:
    """
    Download POTA Ref csv from POTA website
    :return: Dictionary of POTA references
    """
    r = requests.get(url='https://pota.app/all_parks_ext.csv')
    url_content = r.content
    with open('data/potaref.csv', 'wb') as csv_file:
        csv_file.write(url_content)
        csv_file.close()
    rawData = pd.read_csv(io.StringIO(url_content.decode('utf-8')))
    pl = rawData.values.tolist()
    potalist = []
    for r in pl:
        potalist.append({
            'reference': r[0],
            'name': r[1],
            'active': r[2],
            'entityId': r[3],
            'locationDesc': r[4],
            'latitude': r[5],
            'longtitude': r[6],
            'grid': r[7]
        })
    return potalist
