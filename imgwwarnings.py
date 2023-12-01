#!/usr/bin/env python3
import os
import requests
# from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
# import xmltodict
import json
from enum import Enum
import locale
from unidecode import unidecode
from roman import toRoman


# Ostrzeżenia meteorologiczne:
# https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt?lc=

# Komunikaty meteorologiczne
# https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/komet-teryt?lc=

class E_Wojewodztwa(Enum):
    DS = "dolnośląskie"
    KP = "kujawsko-pomorskie"
    LB = "lubuskie"
    LD = "łódzkie"
    LU = "lubelskie"
    MA = "małopolskie"
    MZ = "mazowieckie"
    OP = "opolskie"
    PD = "podlaskie"
    PK = "podkarpackie"
    PM = "pomorskie"
    SK = "świętokrzyskie"
    SL = "śląskie"
    WM = "warmińsko-mazurskie"
    WP = "wielkopolskie"
    ZP = "zachodniopomorskie"


# Powiaty - to nie są wszystkie!!!
# TODO pozostałe powiaty zaimportować jakimś batchem z IMGW
# TERYT CODES
    # 0201: "BOLESŁAWIECKI",
    # 0202: "DZIERŻONIOWSKI",
    # 0203: "GŁOGOWSKI",
    # 0205: "JAWORSKI",
    # 0206: "KARKONOSKI",
    # 0207: "KAMIENNOGÓRSKI",
    # 0208: "KŁODZKI",
    # 0209: "LEGNICKI",
    # 0210: "LUBAŃSKI",
    # 0211: "LUBIŃSKI",
    # 0212: "LWÓWECKI",
    # 0215: "OŁAWSKI",
    # 0216: "POLKOWICKI",
    # 0217: "STRZELIŃSKI",
    # 0218: "ŚREDZKI (DOLNOŚLĄSKIE)",
    # 0219: "ŚWIDNICKI (DOLNOŚLĄSKIE)",
    # 0221: "WAŁBRZYSKI",
    # 0222: "WOŁOWSKI",
    # 0223: "WROCŁAWSKI",
    # 0224: "ZĄBKOWICKI",
    # 0225: "ZGORZELECKI",
    # 0226: "ZŁOTORYJSKI",
    # 0261: "JELENIA GÓRA",
    # 0262: "LEGNICA",
    # 0264: "WROCŁAW",
    # 0265: "WAŁBRZYCH",
    # 0601: "BIALSKI",
    # 0602: "BIŁGORAJSKI",
    # 0603: "CHEŁMSKI",
    # 0604: "HRUBIESZOWSKI",
    # 0605: "JANOWSKI",
    # 0606: "KRASNOSTAWSKI",
    # 0608: "LUBARTOWSKI",
    # 0609: "LUBELSKI",
    # 0610: "ŁĘCZYŃSKI",
    # 0613: "PARCZEWSKI",
    # 0615: "RADZYŃSKI",
    # 0617: "ŚWIDNICKI (LUBELSKIE)",
    # 0618: "TOMASZOWSKI (LUBELSKIE)",
    # 0619: "WŁODAWSKI",
    # 0620: "ZAMOJSKI",
    # 0661: "BIAŁA PODLASKA",
    # 0662: "CHEŁM",
    # 0663: "LUBLIN",
    # 0664: "ZAMOŚĆ",
    # 0804: "NOWOSOLSKI",
    # 0810: "ŻAGAŃSKI",
    # 0811: "ŻARSKI",
    # 1201: "BOCHEŃSKI",
    # 1202: "BRZESKI (MAŁOPOLSKIE)",
    # 1203: "CHRZANOWSKI",
    # 1205: "GORLICKI",
    # 1206: "KRAKOWSKI",
    # 1207: "LIMANOWSKI",
    # 1209: "MYŚLENICKI",
    # 1210: "NOWOSĄDECKI",
    # 1211: "NOWOTARSKI",
    # 1213: "OŚWIĘCIMSKI",
    # 1215: "SUSKI",
    # 1216: "TARNOWSKI",
    # 1217: "TATRZAŃSKI",
    # 1218: "WADOWICKI",
    # 1219: "WIELICKI",
    # 1261: "KRAKÓW",
    # 1262: "NOWY SĄCZ",
    # 1263: "TARNÓW",
    # 1401: "BIAŁOBRZESKI",
    # 1402: "CIECHANOWSKI",
    # 1403: "GARWOLIŃSKI",
    # 1404: "GOSTYNIŃSKI",
    # 1405: "GRODZISKI (MAZOWIECKIE)",
    # 1406: "GRÓJECKI",
    # 1407: "KOZIENICKI",
    # 1408: "LEGIONOWSKI",
    # 1409: "LIPSKI",
    # 1410: "ŁOSICKI",
    # 1411: "MAKOWSKI",
    # 1412: "MIŃSKI",
    # 1413: "MŁAWSKI",
    # 1414: "NOWODWORSKI (MAZOWIECKIE)",
    # 1415: "OSTROŁĘCKI",
    # 1416: "OSTROWSKI (MAZOWIECKIE)",
    # 1417: "OTWOCKI",
    # 1418: "PIASECZYŃSKI",
    # 1419: "PŁOCKI",
    # 1420: "PŁOŃSKI",
    # 1421: "PRUSZKOWSKI",
    # 1422: "PRZASNYSKI",
    # 1423: "PRZYSUSKI",
    # 1424: "PUŁTUSKI",
    # 1425: "RADOMSKI",
    # 1426: "SIEDLECKI",
    # 1427: "SIERPECKI",
    # 1428: "SOCHACZEWSKI",
    # 1429: "SOKOŁOWSKI",
    # 1430: "SZYDŁOWIECKI",
    # 1432: "WARSZAWSKI ZACHODNI",
    # 1433: "WĘGROWSKI",
    # 1434: "WOŁOMIŃSKI",
    # 1435: "WYSZKOWSKI",
    # 1436: "ZWOLEŃSKI",
    # 1437: "ŻUROMIŃSKI",
    # 1438: "ŻYRARDOWSKI",
    # 1461: "OSTROŁĘKA",
    # 1462: "PŁOCK",
    # 1463: "RADOM",
    # 1464: "SIEDLCE",
    # 1465: "WARSZAWA",
    # 1601: "BRZESKI (OPOLSKIE)",
    # 1602: "GŁUBCZYCKI",
    # 1603: "KĘDZIERZYŃSKO-KOZIELSKI",
    # 1605: "KRAPKOWICKI",
    # 1607: "NYSKI",
    # 1609: "OPOLSKI (OPOLSKIE)",
    # 1610: "PRUDNICKI",
    # 1611: "STRZELECKI",
    # 1661: "OPOLE",
    # 1801: "BIESZCZADZKI",
    # 1802: "BRZOZOWSKI",
    # 1803: "DĘBICKI",
    # 1804: "JAROSŁAWSKI",
    # 1805: "JASIELSKI",
    # 1806: "KOLBUSZOWSKI",
    # 1807: "KROŚNIEŃSKI (PODKARPACKIE)",
    # 1808: "LEŻAJSKI",
    # 1809: "LUBACZOWSKI",
    # 1810: "ŁAŃCUCKI",
    # 1811: "MIELECKI",
    # 1812: "NIŻAŃSKI",
    # 1813: "PRZEMYSKI",
    # 1814: "PRZEWORSKI",
    # 1815: "ROPCZYCKO-SĘDZISZOWSKI",
    # 1816: "RZESZOWSKI",
    # 1817: "SANOCKI",
    # 1819: "STRZYŻOWSKI",
    # 1821: "LESKI",
    # 1861: "KROSNO",
    # 1862: "PRZEMYŚL",
    # 1863: "RZESZÓW",
    # 2401: "BĘDZIŃSKI",
    # 2402: "BIELSKI (ŚLĄSKIE)",
    # 2403: "CIESZYŃSKI",
    # 2405: "GLIWICKI",
    # 2408: "MIKOŁOWSKI",
    # 2410: "PSZCZYŃSKI",
    # 2411: "RACIBORSKI",
    # 2412: "RYBNICKI",
    # 2413: "TARNOGÓRSKI",
    # 2414: "BIERUŃSKO-LĘDZIŃSKI",
    # 2415: "WODZISŁAWSKI",
    # 2417: "ŻYWIECKI",
    # 2461: "BIELSKO-BIAŁA",
    # 2462: "BYTOM",
    # 2463: "CHORZÓW",
    # 2465: "DĄBROWA GÓRNICZA",
    # 2466: "GLIWICE",
    # 2467: "JASTRZĘBIE-ZDRÓJ",
    # 2468: "JAWORZNO",
    # 2469: "KATOWICE",
    # 2470: "MYSŁOWICE",
    # 2471: "PIEKARY ŚLĄSKIE",
    # 2472: "RUDA ŚLĄSKA",
    # 2473: "RYBNIK",
    # 2474: "SIEMIANOWICE ŚLĄSKIE",
    # 2475: "SOSNOWIEC",
    # 2476: "ŚWIĘTOCHŁOWICE",
    # 2477: "TYCHY",
    # 2478: "ZABRZE",
    # 2479: "ŻORY",

# Klasa Imgw przestarzała
# class Imgw:
#     def __init__(self, woj):
#         self.woj = woj
#         self.url = 'https://danepubliczne.imgw.pl/datastore'
#         self.litags = None
#         self.getData()
#
#     def getData(self):
#         """
#         Get a list of files available for download
#         """
#         r = requests.post(
#             url='{}/getFilesList'.format(self.url),
#             data={"productType": "oper", "path": "/Oper/ost_meteo/wojew"}
#         )
#         d = r.text
#         soup = BeautifulSoup(d, "lxml")     # Parse the html content
#         self.litags = soup.find_all("a")          # Find all li tag
#
#     def getXmlFile(self, url):
#         r = requests.get(url='https://danepubliczne.imgw.pl/datastore/getfiledown/Oper/ost_meteo/wojew/{}'.format(url))
#         d = r.text
#         d = xmltodict.parse(d)
#         teryt = []
#         if type(d['Forecast']['WARNINGS']['WARNING']) == list:
#             for r in d['Forecast']['WARNINGS']['WARNING']:
#                 if 'Object' in r:
#                     for x in r['Object']['Counties']['County']:
#                         teryt.append({'cn': x['CountyName'].upper(), 'cc': x['CountyTerytCode']})
#         elif type(d['Forecast']['WARNINGS']['WARNING']) == dict:
#             for x in d['Forecast']['WARNINGS']['WARNING']['Object']['Counties']['County']:
#                 teryt.append({'cn': x['CountyName'].upper(), 'cc': x['CountyTerytCode']})
#         return teryt
#
#     def stan(self):
#         """
#         Ostrzeżenia meteorologiczne zbiorczo dla województwa
#         Nie rozwijałem tego pliku XML, może są tam ciekawe dane do obrobienia
#         Póki co drukuje listę TerytCodes dla ostrzerzeń w danym województwie
#         """
#         try:
#             teryt = []
#             for data in self.litags:
#                 # Get text from each tag
#                 fn = data.text[1:]
#                 if fn[:8] == '{}W_STAN'.format(self.woj) and 'xml' in fn:
#                     t = self.getXmlFile(fn)
#                     for r in t:
#                         write = True
#                         for x in teryt:
#                             if r['cc'] == x['cc']:
#                                 write = False
#                                 break
#                         if write:
#                             teryt.append(r)
#         except Exception as e:
#             print('Error: {}'.format(e))
#         finally:
#             teryt.sort(key=self.mySort)
#             for x in teryt:
#                 print('{}: "{}",'.format(x['cc'], x['cn']))
#
#     def mySort(self, e):
#         return e['cc']
#
#     def getXmlWarning(self, url):
#         """
#         Parse the Xml warning document from the given url
#         :param url: url of warning xml file
#         :return: Dictionary with warning data
#         """
#         data = None
#         r = requests.get(url='https://danepubliczne.imgw.pl/datastore/getfiledown/Oper/ost_meteo/wojew/{}'.format(url))
#         d = r.text
#         d = xmltodict.parse(d)
#         if 'WARNING' in d['Forecast']:
#             format = '%Y-%m-%d %H:%M:%S'
#             if datetime.strptime(d['Forecast']['WARNING']['Object']['ValidTo'][:19], format) > datetime.now():
#                 data = {
#                     'Type': d['Forecast']['WARNING']['Object']['Type'],
#                     'PhenomenonCode': d['Forecast']['WARNING']['Object']['PhenomenonCode'],
#                     'Level': d['Forecast']['WARNING']['Object']['Level'],
#                     'Probability': d['Forecast']['WARNING']['Object']['Probability'],
#                     'WarningNumber': d['Forecast']['WARNING']['Object']['WarningNumber'],
#                     'ReleaseDateTime': d['Forecast']['WARNING']['Object']['ReleaseDateTime'],
#                     'ValidFrom': d['Forecast']['WARNING']['Object']['ValidFrom'],
#                     'ValidTo': d['Forecast']['WARNING']['Object']['ValidTo'],
#                     'Polish': d['Forecast']['WARNING']['Object']['Polish'],
#                 }
#             return data
#
#     def wrn(self, TerytCode):
#         """
#         Meteorological warnings for the district.
#         Method downloads meteorological warnings from the IMGW public website
#         and saves data to the meteowarnings.json file
#         :param TerytCode: County Code, ex. for "grodziski" 1405, look in TERYT CODES comment
#         """
#         # Read current json file
#         with open('meteowarnings.json', 'r', encoding='utf-8') as openfile:
#             json_object = json.load(openfile)
#             json_object['warnings'].clear()
#
#         # Read xml warnings from IMGW public server
#         for data in self.litags:
#             fn = data.text[1:]
#             if fn[:8] == '{}W_{}'.format(self.woj, TerytCode) and 'xml' in fn:
#                 w = self.getXmlWarning(fn)
#                 if w is not None:
#                     json_object['warnings'].append(w)
#
#         # Remove expired warnings
#         format = '%Y-%m-%d %H:%M:%S'
#         for r in json_object['warnings'][:]:
#             if datetime.strptime(r['ValidTo'], format) < datetime.now():
#                 json_object['warnings'].remove(r)
#
#         # Save result json file
#         with open("meteowarnings.json", "w", encoding='utf-8') as outfile:
#             json.dump(json_object, outfile, indent=4, ensure_ascii=False)
#
#         # Return data
#         return json_object


warning_levels = [
    "BRAK OSTRZEZEN",
    "ZOLTY ALARM",
    "POMARANCZOWY ALARM",
    'CZERWONY ALARM'
]


def take_data_for_terytCode(terytCode: str):
    """
    Metoda pobiera dane dotyczące ostrzeżeń i komunikatów meteo
    z serwera IMGW i generuje słownik z danymi, które zapisuje do pliku meteowarnings.json
    :param terytCode: Kod terytorium
    :return: dict
    """
    format = '%Y-%m-%d %H:%M'
    # Read current json file
    with open('meteowarnings.json', 'r', encoding='utf-8') as openfile:
        json_object = json.load(openfile)
        json_object['warnings'].clear()
        json_object['komets'].clear()
    i = 0

    # Ostrzeżenia meteorologiczne
    r = requests.get(url='https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt?lc=')
    d = r.json()
    osmet_list = None
    if terytCode in d['teryt'] and 'warnings' in d:
        osmet_list = d['teryt'][terytCode]
    if osmet_list is not None:
        if type(osmet_list) == list:
            for r in osmet_list:
                if r in d['warnings']:
                    d['warnings'][r]['type'] = 'WARNING'
                    d['warnings'][r]['WarningNumber'] = r
                    d['warnings'][r]['index'] = i
                    i += 1
                    json_object['warnings'].append(d['warnings'][r])

        # Remove expired warnings
        for r in json_object['warnings'][:]:
            if datetime.strptime(r['ValidTo'], format) < datetime.now():
                json_object['warnings'].remove(r)

    # Komunikaty meteorologiczne
    r = requests.get(url='https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/komet-teryt?lc=')
    d = r.json()
    komet_list = None
    if terytCode in d['teryt'] and 'komets' in d:
        komet_list = d['teryt'][terytCode]
    if komet_list is not None:
        if type(komet_list) == list:
            for r in komet_list:
                if r in d['komets']:
                    d['komets'][r]['type'] = 'KOMUNIKAT'
                    d['komets'][r]['PhenomenonName'] = d['komets'][r]['Phenomenon'][0]['Name']
                    d['komets'][r]['WarningNumber'] = r
                    d['komets'][r]['index'] = i
                    i += 1
                    json_object['warnings'].append(d['komets'][r])

        # Remove expired warnings
        for r in json_object['komets'][:]:
            if datetime.strptime(r['ValidTo'], format) < datetime.now():
                json_object['komets'].remove(r)

    # Save result json file
    with open("meteowarnings.json", "w", encoding='utf-8') as outfile:
        json.dump(json_object, outfile, indent=4, ensure_ascii=False)

    # Return data
    return json_object


def makeAPRSStatus(warnings):
    """
    Metoda wystawia dane do wysłania statusu APRS
    :param warnings: Słownik z danymi o ostrzeżeniach
    """
    msg = None
    format = '%Y-%m-%d %H:%M'
    lastalarm = warnings['LastAlarm'] if warnings['LastAlarm'] is not None else -1
    locale.setlocale(locale.LC_ALL, '')
    if len(warnings['warnings']) > 0:
        for r in warnings['warnings']:
            dt = datetime.strptime(r['ValidTo'], format)
            dt_from = datetime.strptime(r['ValidFrom'], format)
            if dt.day == dt_from.day and dt.month == dt_from.month:
                okres = '{}.{} {}:{}-{}:{}'.format(dt_from.day, toRoman(dt_from.month), dt_from.hour, dt_from.strftime("%M"), dt.hour, dt.strftime("%M"))
            else:
                okres = '{}.{} {}:{} - {}.{} {}:{}'.format(dt_from.day, toRoman(dt_from.month), dt_from.hour, dt_from.strftime("%M"), dt.day, toRoman(dt.month), dt.hour, dt.strftime("%M"))
            if len(warnings['warnings']) > 1:
                if (r['index'] > int(lastalarm) or lastalarm is None) and dt > datetime.now() > dt_from - timedelta(hours=2):
                    msg = '{} {}'.format(r['PhenomenonName'], okres)
                    if r['type'] == 'WARNING':
                        msg = '>{} {}'.format(warning_levels[int(r['Level'])], msg)
                    elif r['type'] == 'KOMUNIKAT':
                        msg = '>KOMUNIKAT METEO: {}'.format(msg)
                    lastalarm = r['index']
                    break
            else:
                if dt > datetime.now() > dt_from - timedelta(hours=2):
                    msg = '{} {}'.format(r['PhenomenonName'], okres)
                    msg = '>{} {}'.format(warning_levels[int(r['Level'])], msg)
                    lastalarm = r['index']
                    break
        warnings['LastAlarm'] = lastalarm if len(warnings) - 1 >= lastalarm else None
    elif lastalarm >= 0:
        msg = '>'
        warnings['LastAlarm'] = None
    with open("meteowarnings.json", "w", encoding='utf-8') as outfile:
        json.dump(warnings, outfile, indent=4, ensure_ascii=False)
    if msg is not None:
        print(unidecode(msg))
    else:
        exit()


if not os.path.exists("meteowarnings.json"):
    with open("meteowarnings.json", "w", encoding='utf-8') as outfile:
        json.dump({'LastAlarm': None, 'warnings': [], 'komets': []}, outfile, indent=4, ensure_ascii=False)


# Stara metoda pobierania ostrzeżeń meteorologicznych        
# Odkomentuj to co poniżej, i skonfiguruj odpowiednie województwo i TerytCode
# api = Imgw(E_Wojewodztwa.MZ.name)   # Kod województwa (z Enum lub po prostu 'MZ' dla mazowieckiego)
# data = api.wrn('1405')              # Kod powiatu (kod powiatu musi przynależeć do podanego województwa)
# makeAPRSStatus(data)


# Nowa metoda pobierania ostrzeżeń meteorologicznych
data = take_data_for_terytCode('1405')  # Podaj terytCode dla Twojej lokalizacji (np. 1405 = powiat grodziski)
makeAPRSStatus(data)
