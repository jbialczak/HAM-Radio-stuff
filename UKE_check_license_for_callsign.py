#!/usr/bin/python3
import os
import sys
import requests


def checkLicense(call: str):
    params = {
        'draw': 1,
        'columns[0][data]': 'id',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]' : 'true',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'number',
        'columns[1][name]': '',
        'columns[1][searchable]' : 'true',
        'columns[1][orderable]' : 'true',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'valid_to',
        'columns[2][name]': '',
        'columns[2][searchable]' : 'true',
        'columns[2][orderable]' : 'true',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'call_sign',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'true',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'category',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'true',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'transmitter_power',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'true',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'station_location',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'true',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'order[0][column]': 3,
        'order[0][dir]': 'ASC',
        'start': 0,
        'length': 10,
        'search[value]': '{}'.format(call),     # tutaj może być znak, nazwa miejscowości
        'search[regex]': 'false'
    }
    r = requests.get(
        'https://amator.uke.gov.pl/pl/individuals.json',
        params=params
    )
    if r.status_code == 200:
        data = r.json()
        if data['recordsFiltered'] == 1:
            formatData(data['data'][0])
        elif data['recordsFiltered'] > 1:
            print('Znalazłem kilka licencji:\n')
            for r in data['data']:
                formatData(r)
        else:
            print('Nie znaleziono licencji!!!')
    else:
        print('Request ErrorCode: {}'.format(r.status_code))


def formatData(data):
    """
    Formatowanie danych do wyświetlenia
    :param data: Dict
    """
    li = data['number'].split('<a href=')
    li2 = li[1].split('>')
    data['href'] = li2[0]
    li3 = li2[1].split('</a')
    data['license_number'] = li3[0]

    print("[{}] \n\tWażność licencji: {}\n\tNr licencji: {}\n\tKategotia: {}\n\tLokalizacja: {}\n\tTX power: {}".format(
        data['call_sign'],
        data['valid_to'],
        data['license_number'],
        data['category'],
        data['station_location'],
        data['transmitter_power'])
    )


if len(sys.argv) > 1:
    checkLicense(sys.argv[1])
else:
    print('Składnia:\n\t./{} {}'.format(os.path.basename(__file__), 'CALLSIGN'))
