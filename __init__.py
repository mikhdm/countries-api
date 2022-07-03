import pickle

import aiofiles
from envparse import env
from fastapi import FastAPI, Request, Response
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import URL

from app.src.exceptions import AppException
from app.src.utils import error_response

__all__ = (
    'application',
    'settings',
    'META',
)

env.read_envfile('.env')
settings = env

application = FastAPI(
    title='Countries API',
    docs_url='/',
    version=settings.str('APP_VERSION', default='0.0.0'),
    openapi_url='/openapi.json',
    openapi_tags=[{
        'name': 'countries',
        'description': 'Countries API',
    }])

META = {}


@application.on_event('startup')
async def startup():
    params = {
        'host': settings('DB_HOST'),
        'port': settings('DB_PORT', cast=int),
        'username': settings('DB_USER'),
        'password': settings('DB_PASS'),
        'database': settings('DB_NAME'),
    }
    url = URL.create('postgresql+asyncpg', **params)
    db = create_async_engine(url, echo=True)
    
    estimator, vectorizer = None, None
    try:
        async with aiofiles.open('./model/estimator.pkl', mode='rb') as ef:
            estimator = await ef.read()
    except FileNotFoundError:
        pass
    
    try:
        async with aiofiles.open('./model/vectorizer.pkl', mode='rb') as vf:
            vectorizer = await vf.read()
    except FileNotFoundError:
        pass

    META['engine'] = db 
    META['connection'] = await db.connect()
    
    if estimator and vectorizer:
        META['estimator'] = pickle.loads(estimator)
        META['vectorizer'] = pickle.loads(vectorizer)


@application.on_event('shutdown')
async def shutdown():
    if 'engine' in META:
        await META['engine'].dispose()
    if 'connection' in META:
        await META['connection'].close()
        

@application.exception_handler(AppException)
async def auth_exception_handler(rq: Request, exc: AppException) -> Response:
    return error_response(status_code=exc.status_code,
                          error_code=exc.error_code,
                          message=exc.message)
