'''
Test MongoDB connection and data
python get_data.py 

'''

import asyncio
from database import db,users_collection

async def fetch_data():
    try:
        # find all documents from the collection
        users_cursor = users_collection.find()
        users = await users_cursor.to_list(length=None)
        
        print(f"Data: {users}")
        print(f"Using database: {db.name}")
        print(f"Using collection: {users_collection.name}") 
    
    except Exception as e:
        print(f"Error retrieving data: {e}")

# run the async function
if __name__ == "__main__":
    asyncio.run(fetch_data())