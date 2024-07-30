from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID, uuid4
from bson import Binary
from pydantic import BaseModel
from backend.database import get_users_collection

router = APIRouter()

# Pydantic models for data validation
class User(BaseModel):
    user_id: UUID
    user: str
    email: str


class UserCreate(BaseModel):
    user: str
    email: str

#create user
@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, users_collection=Depends(get_users_collection)):
    try:
        user_id = uuid4()  # auto generate UUID
        new_user = {
            "_id": Binary.from_uuid(user_id),  # convert UUID to BSON Binary
            "user": user.user,
            "email": user.email,
        }
        result = await users_collection.insert_one(new_user)
        if result.inserted_id:
            return {"user_id": user_id, "user": user.user, "email": user.email}
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


#update user
@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: UUID, user: User, users_collection=Depends(get_users_collection)
):
    try:
        # check user exists
        existing_user = await users_collection.find_one(
            {"_id": Binary.from_uuid(user_id)}
        )
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # user ID in the request must match user ID in the URL
        if user.user_id != user_id:
            raise HTTPException(status_code=400, detail="User ID mismatch")

        # update user data
        update_result = await users_collection.update_one(
            {"_id": Binary.from_uuid(user_id)},
            {"$set": {"user": user.user, "email": user.email}},
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        updated_user = await users_collection.find_one(
            {"_id": Binary.from_uuid(user_id)}
        )
        return updated_user
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

#get users
@router.get("/users", response_model=List[User])
async def get_users(users_collection=Depends(get_users_collection)):
    try:
        users_cursor = users_collection.find()
        users = await users_cursor.to_list(length=None)

        # list all users
        for user in users:
            user["user_id"] = UUID(bytes=user["_id"])
            user.pop("_id")

        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#delete users
@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: UUID, users_collection=Depends(get_users_collection)):
    try:
        # convert UUID to BSON Binary
        user_id_bson = Binary.from_uuid(user_id)
        
        # check for user in db
        existing_user = await users_collection.find_one({"_id": user_id_bson})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # delete user
        delete_result = await users_collection.delete_one({"_id": user_id_bson})
        if delete_result.deleted_count == 1:
            return {"status": "success", "message": f"User with id {user_id} deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete user")
    except Exception as e:
        print(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
