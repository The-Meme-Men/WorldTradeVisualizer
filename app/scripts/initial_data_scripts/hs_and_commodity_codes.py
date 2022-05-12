import requests
import json
import time
from db.database_connection import initialize, create_session
from db.models import Country, CommClassCode, Commodity
from db.db_utils import get_or_create

from alive_progress import alive_bar

hs_codes = ['HS', 'H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'ST', 'S1', 'S2', 'S3', 'S4', 'ST', 'BEC', 'EB02']

def get_hs_and_comm_codes():

    session = create_session()

    for hs_code in hs_codes:
        url = f'https://comtrade.un.org/Data/cache/classification{hs_code}.json'
        result = requests.get(url)
        print(f'Got results for {hs_code}')
        result.encoding = 'utf-8-sig'
        result = json.loads(result.text)
        comm_code_class, created = get_or_create(session, CommClassCode, code_class=result['classCode'], class_name=result['className'])
        session.commit()
        print(f'Creating commodities for {hs_code}')
        with alive_bar(total=len(result['results'])) as bar:
            for num, value in enumerate(result['results']):
                commodity, created = get_or_create(session, Commodity, comm_class_code=comm_code_class, description=value['text'], comtrade_code=value['id'])
                bar()
        session.commit()
    session.close()
