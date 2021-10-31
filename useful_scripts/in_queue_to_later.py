from src.db.mongo_parser.collections_schemas import Video
from src.db.mongo_parser.mongo_parser import MongoParser
from src.config import *
parser = MongoParser(atlas=True, username=mongo_username, password=mongo_password)