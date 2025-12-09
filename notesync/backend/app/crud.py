from bson import ObjectId
from datetime import datetime
from .db import users_coll, notes_coll
from .auth import get_password_hash, verify_password
from typing import Optional

# Users
async def create_user(username: str, email: Optional[str], password: str):
    hashed = get_password_hash(password)
    doc = {"username": username, "email": email, "hashed_password": hashed, "created_at": datetime.utcnow()}
    res = await users_coll.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc

async def get_user_by_username(username: str):
    return await users_coll.find_one({"username": username})

async def get_user_by_id(user_id: str):
    return await users_coll.find_one({"_id": ObjectId(user_id)})

async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    user["_id"] = str(user["_id"])
    return user

# Notes
async def create_note(owner_id: str, title: str, content: str = ""):
    doc = {
        "owner_id": ObjectId(owner_id),
        "collaborators": [],
        "title": title,
        "content": content,
        "pinned": False,
        "archived": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    res = await notes_coll.insert_one(doc)
    return await notes_coll.find_one({"_id": res.inserted_id})

async def get_note(note_id: str):
    return await notes_coll.find_one({"_id": ObjectId(note_id)})

async def list_notes_for_user(user_id: str, limit: int = 100):
    cursor = notes_coll.find({"$or": [{"owner_id": ObjectId(user_id)}, {"collaborators": ObjectId(user_id)}]}).sort("updated_at", -1).limit(limit)
    return await cursor.to_list(length=limit)

async def update_note(note_id: str, data: dict):
    data["updated_at"] = datetime.utcnow()
    await notes_coll.update_one({"_id": ObjectId(note_id)}, {"$set": data})
    return await get_note(note_id)

async def delete_note(note_id: str):
    await notes_coll.delete_one({"_id": ObjectId(note_id)})
    return True
