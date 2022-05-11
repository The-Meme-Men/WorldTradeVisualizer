import requests
import json
from db.database_connection import initialize, create_session
from db.models import Country
from db.db_utils import get_or_create


def get_countries():
    print('Getting Countries')
    # Get reporter countries
    nested = requests.get('https://comtrade.un.org/Data/cache/reporterAreas.json')
    nested.encoding = 'utf-8-sig'
    nested = json.loads(nested.text)['results']
    flattened = [{'id': el['id'], 'text': el['text']} for el in nested]
    print('Got Reporters from API')

    session = create_session()
    for result in flattened:
        country, created = get_or_create(session, Country, country_id=result['id'], name=result['text'], reporter=True)
    session.commit()

    print('Created reporter objects')

    # Get partner countries
    nested = requests.get('https://comtrade.un.org/Data/cache/partnerAreas.json')
    nested.encoding = 'utf-8-sig'
    nested = json.loads(nested.text)['results']
    flattened = [{'id': el['id'], 'text': el['text']} for el in nested]
    print('Got partners from API')

    for result in flattened:
        country, created = get_or_create(session, Country, country_id=result['id'], name=result['text'])
        country.partner = True
    print('Got all')
    session.commit()
    session.close()
