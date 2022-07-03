import re
import sys
import time
from typing import List, Dict

from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

RE_DIGIT = re.compile(r'\d+[a-z-\\/]+\d*', re.UNICODE)


def runtime(func):
    def wrapper(*args, **kwargs):
        s = time.time()
        result = func(*args, **kwargs)
        e = time.time()
        sys.stdout.write("running time: {:.10f} sec".format(e - s))
        return result
    return wrapper


def filtertokenize(address: str) -> List[str]:
    tokens = map(str.lower, re.split(r'[, ]+', address))
    cond = (lambda t:
            t != '-'
            and t != '.'
            and t != ','
            and not t.isdigit()
            and not RE_DIGIT.match(t))
    return list(filter(cond, tokens))
    
    
def prepared(data: List[Dict]) -> List[Dict]:
    for item in data:
        yield {
            'address': item['address'],
            'tokens': filtertokenize(item['address']),
            'country': item['country'],
        }


def error_response(status_code: int, error_code: int, message: str) -> Response:
    data = {
        'error': {
            'message': message,
            'code': error_code,
        }
    }
    return JSONResponse(status_code=status_code, content=jsonable_encoder(data))