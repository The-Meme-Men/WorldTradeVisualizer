import requests
import json
from datetime import datetime
from db.database_connection import initialize, create_session
from db.models import AvailabilityRecord
from db.db_utils import get_or_create
from util.cred_handler import get_secret

def get_availability():
    print('Fetching Availability Records From API')
    all_avail_records = requests.get("https://comtrade.un.org/api/refs/da/view", {"token": get_secret("comtrade_api_key")}).json()
    initialize()
    session = create_session()
    created_recs = 0
    updated_recs = 0
    total_recs = 0
    for record in all_avail_records:
        avail_record, created = get_or_create(session, AvailabilityRecord, 
            frequency=record['freq'], 
            com_class_code=record['px'], 
            reporter=record['r'], 
            period=record['ps'],
            is_original=record['isOriginal']
        )
        if created:
            created_recs += 1
            avail_record.total_records = record['TotalRecords']
            avail_record.publication_date = datetime.strptime(record['publicationDate'], '%Y-%m-%dT%H-%M-%S')
            avail_record.is_partner_detail = record['isPartnerDetail']
            avail_record.inserted = False
        else:
            new_rec_time = datetime.strptime(record['publicationDate'], '%Y-%m-%dT%H-%M-%S')
            if new_rec_time > avail_record.publication_date:
                avail_record.total_records = record['TotalRecords']
                avail_record.publication_date = new_rec_time
                avail_record.is_partner_detail = record['isPartnerDetail']
                avail_record.inserted = False
                updated_recs += 1
        total_recs += 1
    session.commit()
    session.close()
    print(f'{total_recs} records retrieved ({created_recs} created, {updated_recs} updated)')
