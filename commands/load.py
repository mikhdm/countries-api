#!/usr/bin/python

import click
import json
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy import select

from app.src.db import country, address
from app import settings

params = {
    'host': settings('DB_HOST'),
    'port': settings('DB_PORT'),
    'username': settings('DB_USER'),
    'password': settings('DB_PASS'),
    'database': settings('DB_NAME'),
}


@click.command()
@click.option('--addresses', help='Addresses file path (JSONL format).')
def load(addresses):
    
    url = URL.create('postgresql', **params)
    engine = create_engine(url)
    
    with open(addresses, 'r') as af:
        addrs = [json.loads(a) for a in af.readlines()]

    codes = filter(lambda v: v, {addr['country'] for addr in addrs})
    with engine.connect() as conn:
        click.echo('Inserting new countries...')
        for code in codes:
            r = conn.execute(select([country]).where(country.c.label == code))
            item = r.fetchone()
            if not item:
                conn.execute(country.insert().values(label=code.strip()))
        click.echo('Inserting new addresses...')
        for addr in addrs:
            r = conn.execute(select([country])
                             .where(country.c.label == addr['country']))
            id_ = r.fetchone()[0]
            conn.execute(address.insert()
                                .values(raw=addr['address'],
                                        country_id=id_,
                                        manual=True))
    click.echo('OK')
            
            
if __name__ == '__main__':
    load()
    