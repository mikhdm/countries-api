from fastapi.testclient import TestClient 
from fastapi import status 

from app.src import errors
from app import __main__ as main


def test_get_countries_empty():
    with TestClient(main.application) as client:
        response = client.get('/countries')
    rmock = {
        'error': {
            'message': 'Empty address',
            'code': errors.ERR_EMPTYADDR, 
        }
    }
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == rmock


def test_get_countries_usual():
    address = 'Nieuwendammerkade 26A-5, Amsterdam'
    with TestClient(main.application) as client:
        response = client.get('/countries', params={'address': address})
    rmock = {
        'data': {
            'country': 'NL',
        }
    }
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == rmock
