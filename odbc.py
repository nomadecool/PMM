import sqlite3
import re
import os
from dotenv import load_dotenv
from hash import hash
load_dotenv()

DB_NAME = os.getenv('DB_NAME')


def get_database_connection():
    conn = sqlite3.connect(DB_NAME)
    print(f"Opened a new database connection with id {id(conn)}")
    return conn


def some_database_operation(sql, values=None, is_script=False):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        if is_script:
            cursor.executescript(sql)
        else:
            # Comprobar si tenemos valores para incluir en la consulta
            if values:
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)
        conn.commit()
    print(f"Closed database connection with id {id(conn)}")





def write_log(sql, error):
    table_name = extract_table_name(sql)
    error_message = str(error)
    sql_log = """INSERT INTO logs (id_table, data) VALUES (?, ?)"""
    values_log = (table_name, error_message)
    try:
        some_database_operation(sql_log, values_log)
    except Exception as e:
        print(f"An error occurred when logging the error: {e}")
    finally:
        print("write_log ended")


def extract_table_name(sql):
    match = re.search('INSERT INTO (\w+)', sql)
    if match:
        return match.group(1)


def write_data(sql, values):
    try:
        some_database_operation(sql, values)
    except sqlite3.IntegrityError as e:
        table_name = extract_table_name(sql)
        write_log(table_name, e)
        print(f"An error occurred: {e}")
    finally:
        print("write_data ended")



def read_sql(sql):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows

def one_sql(sql):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()  # this will return a tuple
    return row[0] if row else None  # return the first item in the tuple, or None if no result



def table_in(table):
    sql = one_sql(f"select sql_in from table_info where table_name='{table}'")
    return sql


if __name__ == '__main__':

    print(read_sql(f"select password from account where id_account={os.getenv('ID_USER')}"))
    if '777524f0cf9c792596eb2b3c57801dbd37b6999910d7e693922ab25c9193faa9' == one_sql(f"select password from account where id_account={os.getenv('ID_USER')}"):
        print('OKEY!!!')
    print(read_sql("select * from logs"))