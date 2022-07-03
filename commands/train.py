#!/usr/bin/python

import re
import json
import pickle
from typing import List, Dict, Generator, Tuple

import click
import numpy as np
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from app import settings
from app.commands import cli, DB 
from app.commands.load import load
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
            voc.add(t)
    return voc


def vectorize(vectorizer: TfidfVectorizer,
              addrs: List[Dict],
              ) -> Tuple:
    corpus = [item['address'] for item in addrs]
    y = [item['country'] for item in addrs]
    x_train, x_test, y_train, y_test = \
        train_test_split(corpus, y, random_state=0, train_size=.7)
    X_train = vectorizer.fit_transform(x_train)
    X_test = vectorizer.transform(x_test)
    return X_train, X_test, np.array(y_train), np.array(y_test)


def _from_file(filename: str) -> Generator[Dict, None, None]:
    with open(filename, mode='r') as f:
        for line in f.readlines():
            yield json.loads(line)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--load', default=False, help='Load data into DB (JSONL file format).') 
@click.pass_context
def train(ctx, filename, load):
    if load:
        ctx.forward(load)
    
    click.echo('Reading data...')
    addrs_generator = _from_file(filename)
    click.echo('Building vocabulary...')
    addresses = list(addrs_generator)
    voc = vocabulary(addresses)
    if not voc:
        raise click.ClickException('File is empty')

    vec = TfidfVectorizer(vocabulary=voc)
    X_train, X_test, Y_train, Y_test = vectorize(vec, addresses)
    model = svm.LinearSVC()
    click.echo('Fitting...')
    model.fit(X_train, Y_train)
    click.echo('Validating...')
    Y_predict = model.predict(X_test)
    accuracy = np.mean(Y_predict == Y_test)
    click.echo(f'Accuracy: {accuracy}')
    
    click.echo('Saving estimator...')
    with open('../model/estimator.test.pkl', mode='wb') as ef:
        pickle.dump(model, ef)
    click.echo('Saving vectorizer...')
    with open('../model/vectorizer.test.pkl', mode='wb') as vf:
        pickle.dump(vec, vf)


if __name__ == '__main__':
    train()
