
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import secrets
import string
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "url-shortener-project-db")

client = None
collection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, collection
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db.urls
    await collection.create_index("short_code", unique=True)
    print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
    yield
    client.close()

app = FastAPI(title="URL Shortener API", lifespan=lifespan)

class URLRequest(BaseModel):
    long_url: str

def generate_short_code(length: int = 7):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.post("/shorten")
async def shorten_url(request: URLRequest):
    short_code = generate_short_code()
    while await collection.find_one({"short_code": short_code}):
        short_code = generate_short_code()

    await collection.insert_one({
        "short_code": short_code,
        "long_url": request.long_url,
        "clicks": 0
    })
    return {
        "short_url": f"https://your-domain.com/{short_code}",
        "short_code": short_code
    }

@app.get("/{short_code}")
async def redirect(short_code: str):
    url_doc = await collection.find_one({"short_code": short_code})
    if not url_doc:
        raise HTTPException(status_code=404, detail="Short URL not found")
    await collection.update_one({"short_code": short_code}, {"$inc": {"clicks": 1}})
    return RedirectResponse(url=url_doc["long_url"])

@app.get("/stats/{short_code}")
async def get_stats(short_code: str):
    url_doc = await collection.find_one({"short_code": short_code})
    if not url_doc:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return {
        "short_code": short_code,
        "long_url": url_doc["long_url"],
        "clicks": url_doc.get("clicks", 0)
    }

@app.get("/")
async def root():
    return {"message": "URL Shortener API is running!"}
