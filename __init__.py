import pickle

import aiofiles
from envparse import env
from fastapi import FastAPI, Request, Response
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import URL

from application.src.exceptions import AppException
from application.src.utils import error_response

__all__ = (
    'app',
    'settings',
)

env.read_envfile('.env')
settings = env

app = FastAPI(
    title='Address resolver API',
    docs_url='/',
    version=settings('APP_VERSION', '0.0.0'),
    openapi_url='/openapi.json',
    openapi_tags=[{
        'name': 'resolver',
        'description': 'Address resolver API',
    }])

META = {}


@app.on_event('startup')
async def startup():
    params = {
        'host': settings('DB_HOST'),
        'port': settings('DB_PORT'),
        'username': settings('DB_USER'),
        'password': settings('DB_PASS'),
        'database': settings('DB_NAME'),
    }
    url = URL.create('postgres+asyncpg', **params)
    db = create_async_engine(url, echo=True)
    
    async with aiofiles.open('estimator.pkl', mode='rb') as ef:
        estimator = await ef.read()
    async with aiofiles.open('vectorizer.pkl', mode='rb') as vf:
        vectorizer = await vf.read()
        
    META['connection'] = await db.connect()
    META['estimator'] = pickle.loads(estimator)
    META['vectorizer'] = pickle.loads(vectorizer)


@app.on_event('shutdown')
async def shutdown():
    if 'connection' in META:
        await META['connection'].dispose()
        


@app.exception_handler(AppException)
async def auth_exception_handler(rq: Request, exc: AppException) -> Response:
    return error_response(status_code=exc.status_code,
                          error_code=exc.error_code,
                          message=exc.message)
