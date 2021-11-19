from contextlib import contextmanager

import psycopg2

from datapipelines.utils.sde_config import DBConnection


@contextmanager
def warehouse_connection(warehouse_conn: DBConnection):
    conn = psycopg2.connect(
        host=warehouse_conn.host,
        database=warehouse_conn.db,
        user=warehouse_conn.user,
        password=warehouse_conn.password,
    )
    conn.autocommit = True
    try:
        cur = conn.cursor()
        yield cur
    finally:
        cur.close()
        conn.close()
