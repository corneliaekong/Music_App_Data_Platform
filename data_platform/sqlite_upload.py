import sqlite3
import psycopg2
from psycopg2 import sql

# Connect to SQLite database
sqlite_conn = sqlite3.connect('/usr/app/chinook.sqlite')
sqlite_cursor = sqlite_conn.cursor()

# Connect to PostgreSQL database
pg_conn = psycopg2.connect(
    dbname='dbt_database',
    user='db_user',
    password='db_password',
    host='postgres',
    port='5432'
)
pg_cursor = pg_conn.cursor()

# Retrieve the list of tables from SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

for table_name in tables:
    table_name = table_name[0].lower()  # Convert the table name to lowercase
    print(f"Processing table: {table_name}")

    # Fetch the table schema from SQLite
    sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
    columns = sqlite_cursor.fetchall()
    column_names = [column[1].lower() for column in columns]  # Convert column names to lowercase

    # Create a table in PostgreSQL
    try:
        create_table_query = f"CREATE TABLE IF NOT EXISTS public.{table_name} ("
        for column in columns:
            col_name = column[1].lower()  # Convert column names to lowercase
            col_type = column[2]
            if "INT" in col_type.upper():
                col_type = "INTEGER"
            elif "TEXT" in col_type.upper() or "VARCHAR" in col_type.upper() or "NVARCHAR" in col_type.upper():
                col_type = "VARCHAR(255)"  # Replace NVARCHAR with VARCHAR
            elif "REAL" in col_type.upper():
                col_type = "FLOAT"
            elif "BLOB" in col_type.upper():
                col_type = "BYTEA"
            elif "DATETIME" in col_type.upper():  # Replace DATETIME with TIMESTAMP
                col_type = "TIMESTAMP"
            create_table_query += f"{col_name} {col_type},"
        create_table_query = create_table_query.rstrip(",") + ");"
        
        # Print the CREATE TABLE query for debugging
        print(f"CREATE TABLE QUERY: {create_table_query}")
        
        pg_cursor.execute(create_table_query)
        pg_conn.commit()  # Ensure the table creation is committed before proceeding
        print(f"Table {table_name} created successfully.")
    except Exception as e:
        print(f"Error creating table {table_name}: {e}")
        continue

    # Fetch data from the SQLite table
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()

    # Insert data into PostgreSQL table
    try:
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier('public', table_name),  # Use lowercase table name
            sql.SQL(', ').join(map(sql.Identifier, column_names)),  # Use lowercase column names
            sql.SQL(', ').join(sql.Placeholder() * len(column_names))
        )

        for row in rows:
            pg_cursor.execute(insert_query, row)

        pg_conn.commit()
        print(f"Data inserted into table {table_name} successfully.")
    except Exception as e:
        print(f"Error inserting data into table {table_name}: {e}")
        continue

# Close connections
sqlite_conn.close()
pg_conn.close()