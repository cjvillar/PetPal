from fastapi import FastAPI
from backend.database import mongo_instance
from backend.routers import users

app = FastAPI(
    docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json"
)
app.include_router(users.router)


@app.on_event("startup")
async def startup_db_client():
    await mongo_instance.connect()


@app.on_event("shutdown")
async def shutdown_db_client():
    await mongo_instance.close()


@app.get("/")
async def read_root():
    return {"Hello": "PetPal"}
