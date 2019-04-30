from sqlalchemy import (
    create_engine, MetaData, Table,
    Column, String, Integer,
    Float)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
pg_engine = create_engine('postgresql+pg8000://postgres:postgres@localhost:5432')
ModelBase = declarative_base(bind=pg_engine)

from random import randint
import time


class PostViewsModel(ModelBase):
    __tablename__ = 'post_views'

    id = Column(
        Integer,
        nullable=False,
        primary_key=True,
    )

    content_id = Column(
        String,
        nullable=False,
        index=True
    )

    timestamp = Column(
        Float,
        nullable=False,
        index=True,
    )

    views_count = Column(
        Integer,
        nullable=False,
    )


def create_database(row_count: int, pg_session) -> None:
    ModelBase.metadata.create_all()

    rows = []
    for i in range(row_count):
        timestamp = i*5/7
        row = PostViewsModel(content_id=str(randint(1, 10**4)),
                             timestamp=timestamp,
                             views_count=randint(0, 10**4))
        rows.append(row)
    pg_session.add_all(rows)

    start = time.time()
    pg_session.commit()
    print(f'write {row_count} rows: {time.time()-start:.3f}')


def get_values(pg_session, begin: float, end: float, content_id: str) -> tuple:
    start = time.time()
    query = (pg_session
              .query(PostViewsModel)
              .filter(PostViewsModel.content_id == str(content_id),
                      begin <= PostViewsModel.timestamp,
                      end >= PostViewsModel.timestamp)
              )
    values = query.all()
    stop = time.time()-start
    print(query)
    print(f'read {len(values)} rows: {stop:.3f}')
    return tuple(values)


if __name__ == '__main__':
    Session = sessionmaker(bind=pg_engine)
    pg_session = Session()

    all_rows = get_values(pg_session, 11_108.571, 1_000_000_000, '7999')
