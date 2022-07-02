import uvicorn

from application import app, settings

if __name__ == '__main__':
    params = {
        'host': settings('APP_HOST'),
        'port': settings('APP_PORT'),
        'log_level': 'warn',
    }
    uvicorn.run(app, **params)
    