# Use an official PostgreSQL image as the base for the database
FROM postgres:15-alpine as postgres

# Environment variables for PostgreSQL
ENV POSTGRES_USER=db_user
ENV POSTGRES_PASSWORD=db_password
ENV POSTGRES_DB=dbt_database

# Use an official Python image to create a dbt service
FROM python:3.11-slim as python

# Install necessary Python packages
RUN pip install --no-cache-dir psycopg2-binary

# Set working directory for Python
WORKDIR /usr/app

# Copy the Python script and the SQL file into the container
# COPY import_db.py /usr/app/
COPY sqlite_upload.py /usr/app/
# COPY chinook.sql /usr/app/
COPY chinook.sqlite /usr/app/

# Define a custom entrypoint to execute the SQL file before dbt and Redash start
# ENTRYPOINT ["python", "/usr/app/import_db.py"]
ENTRYPOINT ["python", "/usr/app/sqlite_upload.py"]

# Use an official Redash image as the base
FROM redash/redash:latest as redash

# Expose the port for Redash
EXPOSE 5000

# Define a network to allow containers to communicate
FROM postgres as final

# Create a bridge network
FROM python as final

# Ensure dbt can connect to PostgreSQL
FROM redash as final