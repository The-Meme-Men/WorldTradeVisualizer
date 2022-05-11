import requests
import json

parameters = {
    'token': 'fg4ZoP1LWsiW5d9GC32PUdZZ+/KtvFO16YqXyWnUQd6OLzkQqq64CzBwlCK8JP25j7Nyx6cH4K3nKcZVewvs7IgG2DbNB3ffCsvHZajefKa1CzaWYFQjfYxHOceLrpJPqKlbvzPT+2Ilw0npZvvZh+spjOlAX9w2xXjnh2xiztQ=',
    'max': 502,
    'type': 'S',
    'freq': 'A',
    'px': 'EB02',
    'ps': 2019,
    'r': 'all',
    'p': 0,
    'rg': 'all',
    'cc': 205
}

result = requests.get('https://comtrade.un.org/api/get/plus', params=parameters)
print(json.dumps(result.json(), indent=2))
