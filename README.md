### Countries API

#### Description
Countries API uses linear support vector classification model to make predictions.
Achieved accuracy on a validation set is around 0.87.
Every address provided in the dataset transformed into vector of features where every feature is
tf-idf measure of a term from vocabulary built from all tokens in addresses.
During preparation of vocabulary numbers of streets and postcodes was removed to reduce size of vocabulary and concentrate model on a more meaningful information such as cities, countries and street names.

#### API:

`GET /countries?address=<address>`

response: 
```
{
    "data": {
        "country": <string>
    }
}
```

error:
```
{
    "error": {
        "message": <string>,
        "code": <int>
    }
}
```
