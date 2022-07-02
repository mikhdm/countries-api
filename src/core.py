from application import app

from application.src.validators import CountriesResponseSchema, ErrorSchema
from application import META
from application.src import errors
from application.src.utils import prepare
from application.src.exception import AppException


def predict(raw_address):
    address = prepare(raw_address)
    X_address = META['vectorizer'].transform([address])
    values = META['estimator'].predict(X_address)
    return {
        'address': raw_address,
        'country': values[0],
    }


@app.get('/countries',
         response_model=CountriesResponseSchema,
         responses={
             404: ErrorSchema,
             422: ErrorSchema,
         })
def v_countries(address: str = None):
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