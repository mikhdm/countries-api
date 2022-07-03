#!/usr/bin/python

import os
import json
import pickle
from typing import List, Dict, Generator, Tuple

import click
import numpy as np
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer

from app.commands import cli, DB
from app.src.utils import filtertokenize


def prepared(data: List[Dict]) -> Generator[Dict, None, None]:
    for item in data:
        yield {
            'address': item['address'],
            'tokens': filtertokenize(item['address']),
            'country': item['country'],
        }


def vocabulary(addrs: List[Dict]) -> set:
    voc = set()
    for item in prepared(addrs):
        for t in item['tokens']:
            if t:
                voc.add(t)
    return voc


def vectorize(vectorizer: TfidfVectorizer,
              train: List[Dict],
              test: List[Dict]) -> Tuple:
    X_train = vectorizer.fit_transform(item['address'] for item in train)
    X_test = vectorizer.transform(item['address'] for item in test)
    Y_train = np.array([item['country'] for item in train])
    Y_test = np.array([item['country'] for item in test])
    return X_train, X_test, Y_train, Y_test


def _read_file(filename: str) -> Generator[Dict, None, None]:
    with open(filename, mode='r') as f:
        for line in f.readlines():
            yield json.loads(line)


@cli.command()
@click.argument('train', type=click.Path(exists=True))
@click.argument('test', type=click.Path(exists=True))
@click.pass_context
def train(ctx, train, test):
    click.echo('Contents of /app/model path: ')
    click.echo('-----')
    for f in os.listdir('/app/model'):
        click.echo(f)
    click.echo('-----')
    
    click.echo('Reading data...')
    train_data = list(_read_file(train))
    test_data = list(_read_file(test))
    
    click.echo('Building vocabulary...')
    voc = vocabulary(train_data)
    if not voc:
        raise click.ClickException('File is empty')

    vec = TfidfVectorizer(vocabulary=voc)
    X_train, X_test, Y_train, Y_test = vectorize(vec, train_data, test_data)
    model = svm.LinearSVC()
    click.echo('Fitting...')
    model.fit(X_train, Y_train)
    click.echo('Validating...')
    Y_predict = model.predict(X_test)
    accuracy = np.mean(Y_predict == Y_test)
    click.echo(f'Accuracy: {accuracy:.2f}')
    
    click.echo('Saving estimator...')
    with open('/app/model/estimator.pkl', mode='wb+') as ef:
        pickle.dump(model, ef)
    click.echo('Saving vectorizer...')
    with open('/app/model/vectorizer.pkl', mode='wb+') as vf:
        pickle.dump(vec, vf)


if __name__ == '__main__':
    train()
