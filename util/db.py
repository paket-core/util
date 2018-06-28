"""Database utils."""
import contextlib
import functools

import mysql.connector


@contextlib.contextmanager
def sql_connection(db_name=None, host=None, port=3306, user=None, password=None):
    """Context manager for querying the database."""
    try:
        connection = mysql.connector.connect(host=host, port=port, user=user, passwd=password, database=db_name)
        yield connection.cursor(dictionary=True)
        connection.commit()
    except mysql.connector.Error as db_exception:
        raise db_exception
    finally:
        if 'connection' in locals():
            # noinspection PyUnboundLocalVariable
            connection.close()


def custom_sql_connection(host=None, port=3306, user=None, password=None, db_name=None):
    """Return a customized sql_connection context manager."""
    return functools.partial(sql_connection, db_name, host, port, user, password)


def clear_tables(active_sql_connection, db_name):
    """Clear all tables in the database."""
    with active_sql_connection() as sql:
        sql.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = %s", (db_name,))
        for table_name in [row['TABLE_NAME'] for row in sql.fetchall()]:
            sql.execute("DELETE from {}".format(table_name))
