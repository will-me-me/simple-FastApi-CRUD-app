from http.client import HTTPException
from typing import Optional, List
from uuid import UUID, uuid4
from click import option
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import Gender, Role, User, UserUpdateRequest


app = FastAPI()
db: List[User]=[
    User(
    id=UUID("75ec0e5f-6d78-4d9d-b4e3-b47088030550"), 
    first_name='willy',
    last_name='bill',
    gender=Gender.female,
    roles=[Role.student]
    ),

     User(
    id=UUID("c6d18233-deaa-4796-85ac-98181d61f54f"), 
    first_name='Leo',
    last_name='messi',
    gender=Gender.male,
    roles=[Role.admin, Role.user]
    )
]




@app.get('/')
def read_root():
    return {'hello':'world'}

@app.get('/api/v1/users')
async def get_all_users():
    return db;

@app.post('/api/v1/users')
async def add_user(user:User):
    db.append(user)
    return {"id": user.id}
    
@app.delete('/api/v1/users/{user_id}')
async def delete_user(user_id:UUID):
    for user in db:
        if user.id==user_id:
            db.remove(user)
            return {'message':'user Delted'}
    raise HTTPException(
        status_code=404,
        detail=f'user with id: {user_id} does not exists'
        )
@app.put('/api/v1/users/{user_id}')
async def update_user(updated_user: UserUpdateRequest, user_id:UUID):
    for user in db:
        if user.id==user_id:
            if updated_user.first_name is not None:
                user.first_name=updated_user.first_name
            if updated_user.last_name is not None:
                user.last_name=updated_user.last_name
            if updated_user.middle_name is not None:
                user.middle_name=updated_user.middle_name
            if updated_user.roles is not None:
                user.roles=updated_user.roles
            return{'message':'User Updated Succesfully'}
    raise HTTPException(
        status_code=404,
        detail=f'user with id: {user_id} does not exists'
    )


