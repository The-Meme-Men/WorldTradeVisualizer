import pymongo
from util.cred_handler import get_secret


def get_database():
    return pymongo.MongoClient(f"mongodb+srv://{get_secret('mongo_username')}"
                               f":{get_secret('mongo_password')}@{get_secret('mongo_host')}"
                               f"/admin?authSource=admin&replicaSet=db-mongodb-nyc3-59233&readPreference=primary"
                               f"&appname=MongoDB%20Compass&ssl=true&tlsCAFile=util/ca-certificate.crt"
                               ).cis492final