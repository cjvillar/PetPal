from typing import Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from bson import Binary
from .database import users_collection 

app = FastAPI(docs_url="/api/docs",redoc_url="/api/redoc", openapi_url="/api/openapi.json")

# Pydantic models for data validation
class User(BaseModel):
    user_id: UUID
    user: str
    email: str

class UserCreate(BaseModel):
    user: str
    email: str

@app.get("/")
async def read_root():
    return {"Hello": "PetPal"}

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    try:
        user_id = uuid4()  # auto generate UUID
        new_user = {
            "_id": Binary.from_uuid(user_id),  # convert UUID to BSON Binary
            "user": user.user,
            "email": user.email
        }
        result = await users_collection.insert_one(new_user)
        if result.inserted_id:
            return {"user_id": user_id, "user": user.user, "email": user.email}
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, user: User):
    try:
        # check user exists
        existing_user = await users_collection.find_one({"_id": user_id})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        #  user_id in the request must match user_id in the URL
        if user.user_id != user_id:
            raise HTTPException(status_code=400, detail="User ID mismatch")

        # update user data
        update_result = await users_collection.update_one(
            {"_id": user_id},
            {"$set": {"user": user.user, "email": user.email}}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        updated_user = await users_collection.find_one({"_id": user_id})
        return updated_user
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/users", response_model=List[User])
async def get_users():
    try:
        users_cursor = users_collection.find()
        users = await users_cursor.to_list(length=None)

        # convert BSON Binary to UUID and map _id to user_id
        for user in users:
            user['user_id'] = UUID(bytes=user['_id'])
            user.pop('_id')

        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
