import time
import pandas as pd
from db.database_connection import initialize, create_session
from db.models import CSTCode
from db.db_utils import get_or_create
from alive_progress import alive_bar


def get_customs_codes():
    print('Getting Custom Codes')
    file = pd.read_excel('ComtradeStats.xlsx', sheet_name='REF CUSTOMS')
    df = pd.DataFrame(file)
    session = create_session()

    with alive_bar(total=len(df)) as bar:
        for index, row in df.iterrows():
            get_or_create(session, CSTCode, code=str(row['cstCode']), description=row['cstDescription'])
            bar()
    session.commit()
    session.close()
