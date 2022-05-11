import pandas as pd
from db.database_connection import initialize, create_session
from db.models import MOTCode
from db.db_utils import get_or_create


def get_mot_codes():
    file = pd.read_excel('ComtradeStats.xlsx', sheet_name='REF MOT')
    df = pd.DataFrame(file)
    session = create_session()

    for index, row in df.iterrows():
        get_or_create(session, MOTCode, code=row['motCode'], description=row['motName'])
        # country = Country(country_id=row['geoAreaCode'], name=row['geoAreaDescription'])
        # session.add(country)
    session.commit()
    session.close()