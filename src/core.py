from app import application
from app import META


def predict(address):
    X_address = META['vectorizer'].transform([address])
    values = META['estimator'].predict(X_address)
    return {
        'address': address,
        'country': values[0],
    }

