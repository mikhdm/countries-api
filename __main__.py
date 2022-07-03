import uvicorn

from app import application, settings


if __name__ == '__main__':
    params = {
        'host': settings('APP_HOST'),
        'port': settings('APP_PORT'),
        'log_level': 'warning',
    }
    print(params)
    uvicorn.run(application, **params)

 