import requests
import json
#
# parameters = {
#     'token': 'fg4ZoP1LWsiW5d9GC32PUdZZ+/KtvFO16YqXyWnUQd6OLzkQqq64CzBwlCK8JP25j7Nyx6cH4K3nKcZVewvs7IgG2DbNB3ffCsvHZajefKa1CzaWYFQjfYxHOceLrpJPqKlbvzPT+2Ilw0npZvvZh+spjOlAX9w2xXjnh2xiztQ=',
#     'max': 502,
#     'type': 'C',
#     'freq': 'A',
#     'px': 'EB02',
#     'ps': 2019,
#     'r': 'all',
#     'p': 0,
#     'rg': 'all',
#     'cc': 1
# }
#
# result = requests.get('https://comtrade.un.org/api/get/plus', params=parameters)
# print(json.dumps(result.json(), indent=2))
from db.database_connection import initialize, create_session
from db.models import Country
from db.db_utils import get_or_create

nested = requests.get('https://comtrade.un.org/Data/cache/partnerAreas.json')
nested.encoding = 'utf-8-sig'
nested = json.loads(nested.text)['results']
flattened = [{'id':el['id'], 'text': el['text']} for el in nested]
print(flattened)
initialize()
session = create_session()
for result in flattened:
    country, created = get_or_create(session, Country, country_id=result['id'], name=result['text'])
    country.partner = True
session.commit()
session.close()
