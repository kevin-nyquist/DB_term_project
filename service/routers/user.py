from fastapi import FastAPI, APIRouter, HTTPException, Depends
from typing import List

from app.models.user import User, UserCreate, UserUpdate
from app.dependencies.database import get_database, Database

app = FastAPI()
router = APIRouter()


@app.post("/users/", response_model=User)
async def create_user(user_data: UserCreate, db: Database = Depends(get_database)):
    user = await db.add_user(user_data)
    return user


@router.get("/users/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 10, db: Database = Depends(get_database)):
    users = await db.get_users(skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: Database = Depends(get_database)):
    user = await db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, db: Database = Depends(get_database)):
    user = await db.update_user(user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", response_model=None)
async def delete_user(user_id: int, db: Database = Depends(get_database)):
    result = await db.delete_user(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return None

app.include_router(router)