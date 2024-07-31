"""
Quick Test MongoDB connection and data
python get_data.py 

"""

import asyncio
from database import mongo_instance, get_users_collection, get_pets_collection


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
        print("##########################################\n")

        # find pets
        pets_collection = await get_pets_collection()
        pets_cursor = pets_collection.find()
        pets = await pets_cursor.to_list(length=None)
        print("##########################################")
        print(f"Pet Count: {len(pets)}")
        print(f"Data: {pets}")
        print(f"Using database: {mongo_instance.db.name}")
        print(f"Using collection: {pets_collection.name}")

    except Exception as e:
        print(f"Error retrieving data: {e}")
    finally:
        # close db connection
        await mongo_instance.close()


if __name__ == "__main__":
    asyncio.run(fetch_data())
