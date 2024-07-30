# database.py
import os
from dotenv import load_dotenv
import motor.motor_asyncio

# load vars from .env
load_dotenv()

# MongoDB credentials from .env
mongo_user = os.getenv("MONGO_USER")
mongo_pw = os.getenv("MONGO_PW")
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_db = os.getenv("MONGO_DB")

# MongoDB URL
mongodb_url = f"mongodb://{mongo_user}:{mongo_pw}@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"

# MongoDB client 
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
db = client.get_database(mongo_db)

#user collection
users_collection = db.get_collection("users")



