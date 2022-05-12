import time
import pandas as pd
from db.database_connection import initialize, create_session
from db.models import QuantityCode
from db.db_utils import get_or_create
from alive_progress import alive_bar


def get_quantities():
    print('Getting Quantities')
    file = pd.read_excel('ComtradeStats.xlsx', sheet_name='REF QTY')
    df = pd.DataFrame(file)
    session = create_session()

    with alive_bar(total=len(df)) as bar:
        for index, row in df.iterrows():
            get_or_create(session, QuantityCode, code=row['qtyCode'], description=row['qtyDescription'])
            bar()
    session.commit()
    session.close()
