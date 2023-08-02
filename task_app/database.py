import pymongo
from common_layer import constants
from pymongo import MongoClient
from sqlalchemy import create_engine
from common_layer import constants

# MongoDB Configuration
mongodb_uri = f"{constants.MONGODB_URL}"
client = MongoClient(mongodb_uri)
db_name = pymongo.uri_parser.parse_uri(mongodb_uri)["database"]
db = client[f"{db_name}"]


# Postgres Configuration
POSTGRES_DATABASE_URL = f"postgresql+psycopg2://{constants.POSTGRES_USERNAME}:{constants.POSTGRES_PASSWORD}@{constants.POSTGRES_HOST}:{constants.POSTGRES_PORT}/{constants.POSTGRES_DATABASE_NAME}"
engine = create_engine(POSTGRES_DATABASE_URL, echo=True)