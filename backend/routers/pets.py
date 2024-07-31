from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID, uuid4
from bson import Binary
from pydantic import BaseModel
from backend.database import get_users_collection, get_pets_collection

router = APIRouter()

# Pydantic models for data validation
class Pet(BaseModel):
    pet: str
    user: UUID


class PetCreate(BaseModel):
    pet: str
    user: UUID


# POST  add a pet
@router.post(
    "/pets/",
    response_model=Pet,
    tags=["Pet Operations"],
    summary="Create a new pet for a user",
    description="This endpoint creates a new pet for a user in the system.",
)
async def create_pet(pet: PetCreate):
    try:
        # Check if the user exists
        user = await get_users_collection.find_one(
            {"_id": Binary.from_uuid(pet.user_id)}
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Create new pet
        new_pet = {
            "pet": pet.pet,
            "user_id": Binary.from_uuid(pet.user_id),  # Store user_id as BSON Binary
        }
        result = await get_pets_collection.insert_one(new_pet)
        if result.inserted_id:
            return Pet(pet=pet.pet, user_id=pet.user_id)
        else:
            raise HTTPException(status_code=500, detail="Failed to create pet")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# GET retrieve all pets for a specific user
@router.get(
    "/pets/{user_id}",
    response_model=List[Pet],
    tags=["Pet Operations"],
    summary="List Pets in the system",
    description="This endpoint list pets for a user in the system.",
)
async def get_pets(user_id: UUID):
    try:
        pets_cursor = get_pets_collection.find({"user_id": Binary.from_uuid(user_id)})
        pets = await pets_cursor.to_list(length=None)

        if not pets:
            raise HTTPException(status_code=404, detail="No pets found for this user")

        return [
            Pet(
                pet=p["pet"],
                user_id=UUID(
                    bytes=p["user_id"].as_uuid()
                ),  # Convert BSON Binary to UUID
            )
            for p in pets
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# DELETE to remove a pet
@router.delete(
    "/pets/{pet_id}",
    response_model=dict,
    tags=["Pet Operations"],
    summary="Delete a pet for a user ( Oh no! what happened to them ... sad)",
    description="This endpoint deletes pet for a user in the system.",
)
async def delete_pet(pet_id: UUID):
    try:
        result = await get_pets_collection.delete_one({"_id": Binary.from_uuid(pet_id)})
        if result.deleted_count == 1:
            return {
                "status": "success",
                "message": f"Pet with id {pet_id} deleted successfully",
            }
        else:
            raise HTTPException(status_code=404, detail="Pet not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
