import requests
import pandas as pd


r = requests.get(url='http://www.yaesu.com/jp/en/wires-x/id/active_node.php')
nodes = []

for r in r.text.splitlines():
    if r[:8] == 'dataList':
        line = r[r.find('{'):r.find('}') + 1]
        id = line[line.find('id:') + 4:line.find('dtmf_id:') - 3]
        dtmf_id = line[line.find('dtmf_id:') + 9:line.find('call_sign:') - 3]
        call_sign = line[line.find('call_sign:') + 11:line.find('ana_dig:') - 3]
        ana_dig = line[line.find('ana_dig:') + 9:line.find('city:') - 3]
        city = line[line.find('city:') + 6:line.find('state:') - 3]
        state = line[line.find('state:') + 7:line.find('country:') - 3]
        country = line[line.find('country:') + 9:line.find('freq:') - 3]
        freq = line[line.find('freq:') + 6:line.find('sql:') - 3]
        sql = line[line.find('sql:') + 5:line.find('lat:') - 3]
        lat = line[line.find('lat:') + 5:line.find('lon:') - 3].replace('&quot', '"')
        lon = line[line.find('lon:') + 5:line.find('comment:') - 3].replace('&quot', '"')
        comment = line[line.find('comment:') + 9:line.find('"}')]
        data = {'id': id, 'dtmf_id': dtmf_id, 'call_sign': call_sign, 'ana_dig': ana_dig, 'city': city, 'state': state,
                'country': country, 'freq': freq, 'sql': sql, 'lat': lat, 'lon': lon, 'comment': comment}
        nodes.append(data)


# Show polish-only nodes
plnodes = []
for r in nodes:
    if r['country'] == 'Poland':
        plnodes.append(r)

print(plnodes)
