# Countries API

## Quick start

To quickly try and run a service, the host OS should have `docker` installed (on Linux) or Docker Desktop (on macOS).
`make` utility must be present as well.

If both of the tools are installed, open a Terminal and, staying inside the root of the project, run:
`make up` and then locate to `http://localhost:8090/`, you will see the Swagger docs.\
You can try querying right away from the Swagger interactive docs. To stop containers from running, run `make down`.
To run tests, just run `make test`. To run training of new estimator view [description](#test--run) of `make train` command in **Test & run** section.

## Description

This project illustrates a possible approach to deploying a machine learning model as a FastAPI microservice.

API provides the only endpoint `GET /countries` that receives an address as a query parameter and returns the country code it was able to derive.\
API uses a linear support vector classification model to make predictions.\
Every address provided in the dataset was transformed into a vector of features, where every feature is a tf-idf measure of a term from a vocabulary built from all tokens in addresses.\
During preparation of a vocabulary, several streets and postcodes were removed (if a number, or street number was considered as a token)\
to reduce the size of the vocabulary and concentrate the model on more meaningful information, such as cities, countries, and street names.


## API:

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

## Test & Run

Available tests test only the basic logic of a query. For production, tests must be moved into a separate DB and app context\
and run independently of the main application.
Some stress testing should also be applied with the locust library, for example.\
Tests here as a demo of basic working features only.

Application is controlled through Makefile and Docker.

`make build` - build an application image.

`make up` - run application and db containers.

`make down` - stop application and DB containers.

`make test` - run tests.

`make train` - Apply training of a new estimator. This action replaces the available pretrained model and vectorizer.\
Train and test data must be provided via `TRAIN_PATH` and `TEST_PATH` variables, e.g..
```
    $ TRAIN_PATH=/app/dataset/addresses.jsonl TEST_PATH=/app/dataset/cities.test.jsonl make train
```

- File format should be `jsonl` with at least `address` and `country` keys;
- File path should be a **path to a file inside a container** (`dataset` folder should be used for this purpose). It is shared with the running container.

This command could be used for updating a pretrained model with new data: you need to update existing addresses.jsonl\
with the extended version and then provide updated files for training and validation (into `dataset` folder).\
The `dataset` folder is shared with the running app container to provide any data for training and validation. The newly trained model will appear\
In the `model` folder, it is also shared with the running app container to preserve the pickled model somewhere else.

`make load` - run loading data into DB. (very long operation (40m - 1h) depending on the size of the file).\
File to load data must be provided via `LOAD_PATH` env variable, e.g..
```
    $ LOAD_PATH=/app/dataset/addresses.jsonl make load
```

- File format must be `jsonl` with at least `address` and `country` keys;
- File path should be a **path to a file inside a container** (`dataset` and `model` folders are shared with running container).
This command is assumed to be useful for production to quickly load address and country data into the database.
