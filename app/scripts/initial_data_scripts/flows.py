import time
import pandas as pd
from db.database_connection import initialize, create_session
from db.models import FlowCode
from db.db_utils import get_or_create
from alive_progress import alive_bar


def get_flows():
    print('Getting Flows')
    file = pd.read_excel('ComtradeStats.xlsx', sheet_name='REF FLOWS')
    df = pd.DataFrame(file)
    session = create_session()

    with alive_bar(total=len(df)) as bar:
        for index, row in df.iterrows():
            get_or_create(session, FlowCode, code=str(row['flwCode']), description=row['flwDescription'], category=str(row['flwCategory']) if not str(row['flwCategory']).lower() == 'NaN' else None)
            bar()
    session.commit()
    session.close()
