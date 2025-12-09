from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import crud
from ..auth import create_access_token
from ..schemas import UserCreate, UserOut, Token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate):
    existing = await crud.get_user_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = await crud.create_user(payload.username, payload.email, payload.password)
    return {"id": str(user["_id"]), "username": user["username"], "email": user.get("email"), "created_at": user["created_at"]}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}
