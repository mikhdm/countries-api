import uvicorn

from app import application, settings
from app.src import errors
from app.src.exceptions import AppException
from app.src.validators import CountriesResponseSchema, ErrorSchema
from app.src.core import predict


@application.get('/countries',
         response_model=CountriesResponseSchema,
         responses={
             404: {'model': ErrorSchema},
             422: {'model': ErrorSchema},
         })
async def v_countries(address: str = None):
    if not address or address is None:
        raise AppException(status_code=422,
                           error_code=errors.ERR_EMPTYADDR,
                           message="Empty address")
    data = predict(address)
    return {
        'data': {
            'country': data['country'],
        }
    }


if __name__ == '__main__':
    params = {
        'host': settings('APP_HOST'),
        'port': settings('APP_PORT', cast=int),
        'log_level': 'info',
    }
    uvicorn.run(application, **params)
