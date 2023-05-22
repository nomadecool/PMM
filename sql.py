from odbc import some_database_operation, table_in, read_sql, hash
import os


def create_table():
    """
    Creates first time table.
    """
    create_table = """ PRAGMA foreign_keys = ON;
        
        CREATE TABLE IF NOT EXISTS type_move (
            id_type_move INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            sign INTEGER CHECK (sign = -1 OR sign = 1)
        );

        CREATE TABLE IF NOT EXISTS role (
            id_role INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            date_create TEXT,
            date_edit TEXT,
            is_admin INTEGER
        );

        CREATE TABLE IF NOT EXISTS account (
            id_account INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            user_name TEXT NOT NULL,
            user_mail TEXT,
            password TEXT,
            id_role INTEGER,
            language_code TEXT,
            FOREIGN KEY (id_role) REFERENCES role(id_role) ON DELETE RESTRICT,
            UNIQUE (id_account)
        );

        CREATE TABLE IF NOT EXISTS category (
            id_category INTEGER PRIMARY KEY AUTOINCREMENT,
            id_parent_category INTEGER,
            description TEXT NOT NULL,
            id_type_move INTEGER,
            is_active INTEGER,
            id_account INTEGER,
            FOREIGN KEY (id_parent_category) REFERENCES category(id_category) ON DELETE RESTRICT,
            FOREIGN KEY (id_type_move) REFERENCES type_move(id_type_move) ON DELETE RESTRICT,
            FOREIGN KEY (id_account) REFERENCES account(id_account) ON DELETE RESTRICT,
            UNIQUE (id_category)
        );

        CREATE TABLE IF NOT EXISTS moves (
            id_moves INTEGER PRIMARY KEY AUTOINCREMENT,
            id_account INTEGER,
            id_category INTEGER,
            amount NUMERIC NOT NULL,
            date_create TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
            date_edit TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
            id_type_move INTEGER,
            balance NUMERIC,
            attachment TEXT,
            FOREIGN KEY (id_account) REFERENCES account(id_account) ON DELETE RESTRICT,
            FOREIGN KEY (id_category) REFERENCES category(id_category) ON DELETE RESTRICT,
            FOREIGN KEY (id_type_move) REFERENCES type_move(id_type_move) ON DELETE RESTRICT,
            UNIQUE (id_moves)
        );

        CREATE TABLE IF NOT EXISTS table_info (
            id_table INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT,
            sql_in TEXT,
            sql_out TEXT,
            date_create TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
            UNIQUE (id_table, table_name) 
        );

        CREATE TABLE IF NOT EXISTS logs (
            id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            date_create TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
            data TEXT
        );
    """
    some_database_operation(create_table, is_script=True)




# para ser ejecutado por única vez
sql_statements = {
    'account': """INSERT INTO account (id_account, first_name, user_name, user_mail, password, id_role, language_code)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
    'table_info': """INSERT INTO table_info (table_name, sql_in, sql_out)
                     VALUES (?, ?, ?)""",
    'logs': """INSERT INTO logs (type, data)
               VALUES (?, ?)""",
    'type_move': """INSERT INTO type_move (description, sign)
                    VALUES (?, ?)""",
    'role': """INSERT INTO role (description, date_create, date_edit, is_admin)
               VALUES (?, ?, ?, ?)""",
    'category': """INSERT INTO category (id_parent_category, description, id_type_move, is_active, id_account)
                   VALUES (?, ?, ?, ?, ?)""",
    'moves': """INSERT INTO moves (id_account, id_category, amount, id_type_move, balance, attachment)
                VALUES (?, ?, ?, ?, ?, ?)"""
}






if __name__ == '__main__':
    create_table()

    for table_name, sql in sql_statements.items():
        some_database_operation('''INSERT INTO table_info (table_name, sql_in, sql_out)
                     VALUES (?, ?, ?)''', (table_name, sql, None))

    print(read_sql("select * from table_info"))

    values = (os.getenv('ID_USER'), os.getenv('FIRST_NAME'), os.getenv('USERNAME'), os.getenv('USER_MAIL'), hash(os.getenv('PASSWORD')), '1', 'es')
    some_database_operation(table_in('account'), values)

