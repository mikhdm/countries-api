import click

from app import settings

cli = click.Group()

DB = {
    'host': settings('DB_HOST'),
    'port': settings('DB_PORT', cast=int),
    'username': settings('DB_USER'),
    'password': settings('DB_PASS'),
    'database': settings('DB_NAME'),
}
