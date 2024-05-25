import uvicorn
from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Query, Path


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


class ResponseData(BaseModel):
    q: str
    item: Item
    item_id: int


@app.post('/items/{item_id}')
async def items(item_id: Annotated[int, Path(ge=1, le=100)],
                q: Annotated[str | None, Query(title='wowwow', description='it is description', min_length=10)],
                item: Item) -> ResponseData:
    print(q)
    return ResponseData(q=q, item=item, item_id=item_id)


if __name__ == '__main__':
    uvicorn.run(app=app, port=8011)
