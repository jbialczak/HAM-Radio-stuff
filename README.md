# HAM-Radio-stuff
My stuff for HAM Radio

### AT878_make_contact_list.py:
Script download current all DMR users list from radioId.net and make csv file for import to
Anytone AT-D878 ContactList_

### UKE_check_license_for_callsign.py:
For polish users only.
Zdarzyło mi się nawiązać łączności z nielicencjonowanymi krótkofalowcami, postanowiłem zrobić skrypt, który szybko sprawdzi ważność licencji. 
Skrypt sprawdza czy znak wywołąwczy znajduje się w udzielonych przez UKE licencjach.

### pota.py:
Download POTA reference list from POTA website and return list of python dictionary.
Pandas library required.

### wiresx_active_nodes.py:
Download active nodes list from YAESU website. Print list of dictionary for polish nodes.
Pandas library required.

### imgwwarnings.py:
For polish users only.
Skrypt zwraca status APRS dotyczący ostrzerzeń pogodowych IMGW w danym regionie.
Status można wykorzystać do wysłania beacon'a do sieci APRS.
Korzysta z danych XML dostępnych publicznie w serwisie https://danepubliczne.imgw.pl/datastore.
Jest to wersja beta do testowania.