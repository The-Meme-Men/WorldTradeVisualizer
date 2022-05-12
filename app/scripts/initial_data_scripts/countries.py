import requests
import json
import time
from db.database_connection import initialize, create_session
from db.models import Country
from db.db_utils import get_or_create

from alive_progress import alive_bar


def get_countries():
    print('Getting Countries')
    # Get reporter countries
    nested = requests.get('https://comtrade.un.org/Data/cache/reporterAreas.json')
    nested.encoding = 'utf-8-sig'
    nested = json.loads(nested.text)['results']
    flattened = [{'id': el['id'], 'text': el['text']} for el in nested]
    print('Got Reporters from API')

    session = create_session()
    with alive_bar(total=len(flattened)) as bar:
        for result in flattened:
            country, created = get_or_create(session, Country, country_id=result['id'], name=result['text'], reporter=True)
            bar()
    session.commit()

    print('Created reporter objects')

    # Get partner countries
    nested = requests.get('https://comtrade.un.org/Data/cache/partnerAreas.json')
    nested.encoding = 'utf-8-sig'
    nested = json.loads(nested.text)['results']
    flattened = [{'id': el['id'], 'text': el['text']} for el in nested]
    print('Got partners from API')

    with alive_bar(total=len(flattened)) as bar:
        for result in flattened:
            country, created = get_or_create(session, Country, country_id=result['id'], name=result['text'])
            country.partner = True
            bar()
    print('Got all')
    session.commit()
    session.close()
