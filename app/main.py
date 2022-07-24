from typing import Union, List

import pyodbc
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel


class Item(BaseModel):
    name: str = "desk"
    description: Union[str, None] = None
    price: float = 10.1
    tax: Union[float, None] = None


app = FastAPI()


@app.post('/items/{item_id}')
async def create_item(
    item: Item,
    item_id: int = Path(
        description='some description'),

    q: List[str] = Query(
        default=['a', 'b'],
        title='title',
        description='description')
):
    result = {'id': item_id, **item.dict()}
    if q:
        result.update({'q': q})
    return result


def connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=LWO1-LHP-A00359;DATABASE=db;UID=admin;PWD=12345'
    )
    return conn


@app.get('/user/{user_id}')
async def get_users(user_id: int):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM Users where id={user_id}')
    user = cursor.fetchone()
    return {'user_id': user[0], 'user_name': user[1]}
