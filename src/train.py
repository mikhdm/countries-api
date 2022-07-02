import re
from typing import List, Dict


RE_DIGIT = re.compile(r'\d+[a-z-\\/]+\d*', re.UNICODE)


def prepared(data: List[Dict]) -> List[Dict]:
    for item in data:
        tokens = map(str.lower, re.split(r'[, ]+', item['address']))
        tokens = filter(lambda t: (t != '-'
                                   and t != '.'
                                   and t != ','
                                   and not t.isdigit()
                                   and not RE_DIGIT.match(t)), tokens)
        yield {
            'address': item['address'],
            'tokens': list(tokens),
            'country': item['country'],
        }
