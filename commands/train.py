#!/usr/bin/python

import re
from typing import List, Dict

import click
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from app.src.db import country, address
from app import settings
from app.commands import cli, DB 
from app.commands.load import load


@cli.command()
@click.argument('filename', required=False, type=click.Path(exists=True))
@click.pass_context
def train(ctx, filename):
    if filename:
        ctx.forward(load)

    url = URL.create('postgresql', **DB)
    engine = create_engine(url)

    click.echo('Running training of the estimator...')

if __name__ == '__main__':
    train()


