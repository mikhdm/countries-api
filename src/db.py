from sqlalchemy import MetaData
from sqlalchemy import Table, Column, ForeignKey, Index
from sqlalchemy import Integer, String, Boolean

convention = {
    'column_name': (lambda constraint, _:
                    '_'.join([c.name for c in constraint.columns.values()])),
    'ix': 'ix__%(table_name)s__%(column_name)s',
    'uq': 'uq__%(table_name)s__%(column_name)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(column_name)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s',
}

metadata = MetaData(naming_convention=convention)


country = Table('country', metadata,
                Column('id',
                       Integer, primary_key=True),
                Column('label', String, unique=True),
                Index('ix_country_label', 'label', postgresql_using='hash'))


address = Table('address', metadata,
                Column('id',
                       Integer, primary_key=True),
                Column('raw', String),
                Column('country_id',
                       Integer,
                       ForeignKey("country.id", ondelete="SET NULL"),
                       nullable=True),
                Column('manual', Boolean, default=False))
