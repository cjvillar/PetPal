import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# env variables from .env
load_dotenv()

# MongoDB credentials from .env
mongo_user = os.getenv("MONGO_USER")
mongo_pw = os.getenv("MONGO_PW")
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_db = os.getenv("MONGO_DB")

# MongoDB URL
mongodb_url = f"mongodb://{mongo_user}:{mongo_pw}@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._db_name = db_name
        self.client = None
        self.db = None
        self.users_collection = None

    async def connect(self):
        self.client = AsyncIOMotorClient(self._uri)
        self.db = self.client[self._db_name]
        self.users_collection = self.db.get_collection("users")
        print("Connected to MongoDB")

    async def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")


# create Mongo instance
mongo_instance = MongoDB(mongodb_url, mongo_db)

#dependencies
async def get_users_collection():
    if not mongo_instance.client:
        await mongo_instance.connect()
    return mongo_instance.users_collection
