from db.database_connection import initialize, create_session
from db.mongo.database_connection import get_database

initialize()
session = create_session()

mongo_db = get_database()
thingies = mongo_db.trade_stats.find({'pt3ISO': 'ARM'})[0]
print(thingies)

session.close()
