from enum import Enum
from fastapi import FastAPI


app = FastAPI()


class ChoiseName(str, Enum):
    lol1 = 'lol1'
    lol2 = 'lol2'
    lol3 = 'lol3'


@app.get('/users/{user}')
async def get(user: ChoiseName) -> dict[str, str]:
    return {'name': user}
