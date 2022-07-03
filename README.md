### Countries API

#### Description
Countries API uses linear support vector classification model to make predictions.\
Achieved accuracy on a validation set is around `0.82`.\
To achieve better results one could use [huggingface transformers library](https://huggingface.co/docs/transformers/tasks/sequence_classification),
or [ArcGIS pro API](https://developers.arcgis.com/python/samples/identifying-country-names-from-incomplete-house-addresses/) which
show great results on text classification tasks.\
Every address provided in the dataset was transformed into vector of features where every feature is tf-idf measure of a term from vocabulary built from all tokens in addresses.\
During preparation of a vocabulary numbers of streets and postcodes was removed (if a number, or street number was considered as a token)\
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
Available tests test only basic logic of a query. For production tests must be moved into separated DB and app context\
and run independently of main application.
Some stress testing should be applied also with locust library for example.\
Tests here as a demo of basic working features only.

Application is controlled through Makefile and docker.

`make build` - build an application image.

`make up` - run application and db containers.

`make down` - stop application and db containers.

`make test` - run tests.

`make train` - Apply training of a new estimator. This action replaces available pretrained model and vectorizer.\
Train and test data must be provided via `TRAIN_PATH` and `TEST_PATH` variables, e. g.
```
    $ TRAIN_PATH=/app/dataset/addresses.jsonl TEST_PATH=/app/dataset/cities.test.jsonl make train
```
file format should be `jsonl` with at least `address` and `country` keys.\
This command could be used for updating of pretrained model with new data, you need to update existing addresses.jsonl data\
with extended version and then provide file for training and validation. News files should be put into `dataset` folder.\
This folder is shared with running app container to provide any data for training and validation. Newly trained model will appear\
at `model` folder, it is shared with running app container to preserve any model somewhere else or put it to work with instead of default.

`make load` - run populating of DB with a data. (very long operation depending on a size of a file).\
File to load data must be provided via `LOAD_PATH` env variable, e. g.
```
    $ LOAD_PATH=/app/dataset/addresses.jsonl make load
```
File format must be `jsonl` with at least `address` and `country` keys. This command assumes to be useful for production
to quickly load address and country data into database.
This application runs with uvicorn as a main server by default, but for production\
it s be put under some kind of a reverse proxy like nginx, traefik (which feels much better) or envoy and multiplied on a several process instances.
Blue-green deployment to seamless reload should be applied as well.
