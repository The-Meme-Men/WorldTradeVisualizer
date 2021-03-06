import time
import pandas as pd
from db.database_connection import initialize, create_session
from db.models import MOTCode
from db.db_utils import get_or_create
from alive_progress import alive_bar


def get_mot_codes():
    print('Getting MOT Codes')
    file = pd.read_excel('ComtradeStats.xlsx', sheet_name='REF MOT')
    df = pd.DataFrame(file)
    session = create_session()

    with alive_bar(total=len(df)) as bar:
        for indexx, row in df.iterrows():
            get_or_create(session, MOTCode, code=row['motCode'], description=row['motName'])
            bar()
    session.commit()
    session.close()
