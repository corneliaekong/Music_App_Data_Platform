To access and connect to a PostgreSQL instance running inside a Docker container, follow these steps:

### 1. **Access the PostgreSQL Container**

You can access the PostgreSQL container using the `docker exec` command to open a shell inside the container. From there, you can use the `psql` command-line tool to interact with the database.

1. **Find the Container ID or Name**:
   First, list all running containers to get the container ID or name of your PostgreSQL container.
   ```bash
   docker ps
   ```

   Look for the container running the PostgreSQL image (`postgres:15-alpine`), and note the `CONTAINER ID` or `NAMES`.

2. **Open a Shell Inside the Container**:
   Use the `docker exec` command to start a shell session inside the PostgreSQL container.
   ```bash
   docker exec -it <container_id_or_name> sh
   ```

   If you are using the default `postgres` image, it might be better to use `bash` instead of `sh` (if `bash` is available in the container):
   ```bash
   docker exec -it <container_id_or_name> bash
   ```

### 2. **Connect to PostgreSQL Using `psql`**

Once inside the container, you can use the `psql` command-line tool to connect to the PostgreSQL instance.

```bash
psql -U <postgres_user> -d <database_name>
```

Replace `<postgres_user>` with the PostgreSQL user (e.g., `db_user`), and `<database_name>` with the name of the database (e.g., `dbt_database`).

#### **Example**:
If your environment variables are set as follows:
```env
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_DB=dbt_database
```

You would run:
```bash
psql -U db_user -d dbt_database
```

If you want to connect from outside the container, you can do so using the host machine’s IP address and the port mapped to the PostgreSQL container. Here’s how:

### 3. **Connect from Outside the Container**

To connect to the PostgreSQL instance from your local machine or another application outside of Docker:

1. **Get the Host Machine’s IP Address**: The default Docker network setup binds the container’s port to the host machine's IP address. By default, Docker Compose maps the PostgreSQL container’s port to `5432`.

2. **Connect Using `psql` from Your Local Machine**:
   ```bash
   psql -h localhost -p 5432 -U <postgres_user> -d <database_name>
   ```

   Here:
   - `-h localhost`: Specifies the host machine (if using Docker Desktop or Docker Toolbox, you might need to use the host IP or `localhost`).
   - `-p 5432`: The port on which PostgreSQL is exposed (adjust if you’ve mapped to a different port).
   - `-U <postgres_user>`: PostgreSQL user (e.g., `db_user`).
   - `-d <database_name>`: The name of the database (e.g., `dbt_database`).

### Example Command:
If you have mapped the PostgreSQL port to `5432` on the host machine:
```bash
psql -h localhost -p 5432 -U db_user -d dbt_database
```

### Summary

- **Inside Docker**: Use `docker exec` to get a shell inside the container and then use `psql` to connect to the PostgreSQL database.
- **Outside Docker**: Connect using `psql` with the host IP and port mapped to the PostgreSQL container.

Ensure you replace placeholders with your actual PostgreSQL credentials and settings.