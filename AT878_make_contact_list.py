#!/usr/bin/python3
import csv
import requests
import datetime

# Download data from radioID.net and save to CSV
r = requests.get('https://radioid.net/static/user.csv', allow_redirects=True)
with open('users.csv', 'wb') as f:
    f.write(r.content)

# Open downloaded data from csv and make list
with open('users.csv', newline='', encoding='utf-8') as csvfile:
    data = list(csv.DictReader(csvfile, delimiter=","))


# Rebuild data to Anytone format, remove polish letters
for r in data:
    r['FIRST_NAME'] = r['FIRST_NAME'].replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace(
        'ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z').replace('Ą', 'A').replace('Ć',
                                                                                                                    'C').replace(
        'Ę', 'E').replace('Ł', 'L').replace('Ń', 'N').replace('Ó', 'O').replace('Ś', 'S').replace('Ź', 'Z').replace('Ż',
                                                                                                                    'Z')
    r['LAST_NAME'] = r['LAST_NAME'].replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń',
                                                                                                                    'n').replace(
        'ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z').replace('Ą', 'A').replace('Ć', 'C').replace('Ę',
                                                                                                                    'E').replace(
        'Ł', 'L').replace('Ń', 'N').replace('Ó', 'O').replace('Ś', 'S').replace('Ź', 'Z').replace('Ż', 'Z')
    r['CITY'] = r['CITY'].replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń',
                                                                                                          'n').replace(
        'ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z').replace('Ą', 'A').replace('Ć', 'C').replace('Ę',
                                                                                                                    'E').replace(
        'Ł', 'L').replace('Ń', 'N').replace('Ó', 'O').replace('Ś', 'S').replace('Ź', 'Z').replace('Ż', 'Z')
    r['STATE'] = r['STATE'].replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń',
                                                                                                            'n').replace(
        'ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z').replace('Ą', 'A').replace('Ć', 'C').replace('Ę',
                                                                                                                    'E').replace(
        'Ł', 'L').replace('Ń', 'N').replace('Ó', 'O').replace('Ś', 'S').replace('Ź', 'Z').replace('Ż', 'Z')
    r['COUNTRY'] = r['COUNTRY'].replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń',
                                                                                                                'n').replace(
        'ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z').replace('Ą', 'A').replace('Ć', 'C').replace('Ę',
                                                                                                                    'E').replace(
        'Ł', 'L').replace('Ń', 'N').replace('Ó', 'O').replace('Ś', 'S').replace('Ź', 'Z').replace('Ż', 'Z')
    if r['LAST_NAME'] != '' and r['LAST_NAME'] != 'None':
        r['FIRST_NAME'] = '{} {}'.format(r['FIRST_NAME'], r['LAST_NAME'])


i = 1
# write data to csv file, which can be imported to Anytone
with open('out_data_{}.csv'.format(datetime.datetime.now().timestamp()), 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(
        ['No.', 'Radio ID', 'Callsign', 'Name', 'City', 'State', 'Country', 'Remarks', 'Call Type', 'Call Alert'])
    for r in data:
        writer.writerow(
            [i, r['RADIO_ID'], r['CALLSIGN'], r['FIRST_NAME'], r['CITY'], r['STATE'], r['COUNTRY'], '', 'Private Call',
             'None'])
        i += 1
