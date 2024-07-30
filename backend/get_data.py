"""
Quick Test MongoDB connection and data
python get_data.py 

"""

import asyncio
from database import mongo_instance, get_users_collection

async def fetch_data():
    try:
        # database connect
        await mongo_instance.connect()
        
        # users collection
        users_collection = await get_users_collection()

        # find all  users
        users_cursor = users_collection.find()
        users = await users_cursor.to_list(length=None)
        print(f"User Count: {len(users)}")
        print(f"Data: {users}")
        print(f"Using database: {mongo_instance.db.name}")
        print(f"Using collection: {users_collection.name}")

    except Exception as e:
        print(f"Error retrieving data: {e}")
    finally:
        # close db connection
        await mongo_instance.close()

if __name__ == "__main__":
    asyncio.run(fetch_data())

