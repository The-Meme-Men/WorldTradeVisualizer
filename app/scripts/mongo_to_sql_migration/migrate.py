from db.database_connection import initialize, create_session
from db.db_utils import get_or_create
from db.models import TradeStat, Country, Commodity, RGCode, QuantityCode
from db.mongo.database_connection import get_database

countries = {}
commodities = {}


def run_migration():
    db = get_database()
    initialize()
    session = create_session()

    stats = db.trade_stats.find({'rt3ISO': 'ARM', 'yr': 2020})

    for stat in stats:
        # Get reporter country
        if stat['rtTitle'] not in countries.keys():
            reporter_object, created = get_or_create(session, Country, country_id=stat['rtCode'], name=stat['rtTitle'],
                                                     iso=stat['rt3ISO'])
            if created:
                session.commit()
            countries[stat['rtTitle']] = reporter_object
        reporter_object = countries[stat['rtTitle']]

        # Get partner country
        if stat['ptTitle'] not in countries.keys():
            partner_object, created = get_or_create(session, Country, country_id=stat['ptCode'],
                                                    name=stat['ptTitle'], iso=stat['pt3ISO'])
            if created:
                session.commit()
            countries[stat['ptTitle']] = partner_object
        partner_object = countries[stat['ptTitle']]

        # Get second partner (if exists)
        if not stat['ptCode2'] is None:
            if stat['ptTitle2'] not in countries.keys():
                second_partner_object, created = get_or_create(session, Country, country_id=stat['ptCode2'],
                                                        name=stat['ptTitle2'], iso=stat['pt3ISO2'])
                if created:
                    session.commit()
                countries[stat['ptTitle2']] = second_partner_object
            second_partner_object = countries[stat['ptTitle2']]
        else:
            second_partner_object = None

        # Get commodity
        if stat['cmdCode'] not in commodities.keys():
            commodity_object, created = get_or_create(session, Commodity, description=stat['cmdDescE'],
                                                      comtrade_code=stat['cmdCode'])
            if created:
                session.commit()
            commodities[stat['cmdCode']] = commodity_object
        commodity_object = commodities[stat['cmdCode']]

    session.close()
