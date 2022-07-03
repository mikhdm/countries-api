### Countries API

#### Description
Countries API uses linear support vector classification model to make predictions.\
Achieved accuracy on a validation set is around `0.82`.\
To achieve better results one could use [huggingface transformers library](https://huggingface.co/docs/transformers/tasks/sequence_classification),
or [ArcGIS pro API](https://developers.arcgis.com/python/samples/identifying-country-names-from-incomplete-house-addresses/) which
shows great results on text classification tasks.\
Every address provided in the dataset was transformed into vector of features where every feature is tf-idf measure of a term from vocabulary built from all tokens in addresses.\
During preparation of a vocabulary numbers of streets and postcodes was removed (if a number, or street numer was considered as a token)\
to reduce size of vocabulary and concentrate model on a more meaningful information such as cities, countries and street names.


#### API:

`GET /countries?address=<address>`

`response`: 
```
{
    "data": {
        "country": <string>
    }
}
```

`error`:
```
{
    "error": {
        "message": <string>,
        "code": <int>
    }
}
```

#### Test & Run
Available tests test only basic logic of a query. It would be better to separate test context to separated DB and app\
which should be run independently of main application.\
Tests here run as a demonstration of basic features only.

All aplication is controlled throuh Makefile.

`make build` - build an application image.\

`make up` - run application and db containers.\

`make down` - stop application and db containers.\

`make test` - run tests.\

`make train` - apply training of estimator.\
Train and test data must be provided via `TRAIN_PATH` and `TEST_PATH` variables, e. g.
```
    $ TRAIN_PATH=/app/dataset/addresses.jsonl TEST_PATH=/app/dataset/cities.test.jsonl make train
```
file format should be `jsonl` with at least `address` and `country` keys.

`make load` - run populating of DB with a data. (very long operation depending on size of a file).\
File to load data should be provided via LOAD_PATH env variable, e. g.\
```
    $ LOAD_PATH=/app/dataset/addresses.jsonl make load
```
File format should be `jsonl` with at least `address` and `country` keys.
