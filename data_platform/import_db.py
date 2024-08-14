import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'dbname': 'postgres',  # Use 'postgres' or any other database to connect initially
    'user': 'db_user',
    'password': 'db_password',
    'host': 'postgres',   # or your PostgreSQL server's address
    'port': '5432',        # default PostgreSQL port
}

# Path to the SQL file
sql_file_path = '/usr/app/chinook.sql'

def execute_sql_file(connection, file_path):
    with open(file_path, 'r') as file:
        sql_commands = file.read()
    
    with connection.cursor() as cursor:
        # Split commands by semicolons
        commands = sql_commands.split(';')
        for command in commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                except psycopg2.Error as e:
                    print(f"Error executing command: {command}")
                    print(e)

def main():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True  # Enable autocommit for database creation

        # Execute SQL file
        execute_sql_file(conn, sql_file_path)
        
    except psycopg2.Error as e:
        print("Database connection error:", e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()

