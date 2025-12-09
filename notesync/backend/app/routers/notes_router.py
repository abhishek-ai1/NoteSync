from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas import NoteCreate, NoteUpdate, NoteOut
from ..auth import get_current_user
from .. import crud
from bson import ObjectId

router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.post("/", response_model=NoteOut)
async def create_note(payload: NoteCreate, user=Depends(get_current_user)):
    n = await crud.create_note(user_id := str(user["_id"]), payload.title, payload.content)
    n["_id"] = str(n["_id"])
    n["owner_id"] = str(n["owner_id"])
    n["collaborators"] = [str(x) for x in n.get("collaborators", [])]
    return n

@router.get("/", response_model=List[NoteOut])
async def list_notes(user=Depends(get_current_user)):
    notes = await crud.list_notes_for_user(str(user["_id"]))
    out = []
    for n in notes:
        n["_id"] = str(n["_id"])
        n["owner_id"] = str(n["owner_id"])
        n["collaborators"] = [str(x) for x in n.get("collaborators", [])]
        out.append(n)
    return out

@router.get("/{note_id}", response_model=NoteOut)
async def get_note(note_id: str, user=Depends(get_current_user)):
    note = await crud.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note["_id"] = str(note["_id"])
    note["owner_id"] = str(note["owner_id"])
    note["collaborators"] = [str(x) for x in note.get("collaborators", [])]
    return note

@router.patch("/{note_id}", response_model=NoteOut)
async def update_note(note_id: str, payload: NoteUpdate, user=Depends(get_current_user)):
    note = await crud.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    # permission check: owner or collaborator
    uid = str(user["_id"])
    if str(note["owner_id"]) != uid and ObjectId(uid) not in note.get("collaborators", []):
        raise HTTPException(status_code=403, detail="Forbidden")

    upd = {k:v for k,v in payload.dict(exclude_unset=True).items()}
    updated = await crud.update_note(note_id, upd)
    updated["_id"] = str(updated["_id"])
    updated["owner_id"] = str(updated["owner_id"])
    updated["collaborators"] = [str(x) for x in updated.get("collaborators", [])]
    return updated

@router.delete("/{note_id}")
async def delete_note(note_id: str, user=Depends(get_current_user)):
    note = await crud.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    uid = str(user["_id"])
    if str(note["owner_id"]) != uid:
        raise HTTPException(status_code=403, detail="Only owner can delete")
    await crud.delete_note(note_id)
    return {"ok": True}
