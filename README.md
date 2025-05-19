# FastAPI Todo List - Test Assignment

This repository is a test assignment implementing a Todo List API using FastAPI.

## Installation in virtual environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mrslimek/fastapitodolist.git
   ```
2. **Change directory:**
   ```bash
   cd fastapitodolist
   ```
3. **Create, activate virtual environment and install dependencies using the uv package manager:**
   ```bash
   uv sync
   ```
4. **Create `.env` file in the root directory and add the following environment variables:**
   ```dotenv
   PG_USER = your_pg_user
   PG_PASSWORD = your_pg_password
   PG_DB = your_pg_db
   PG_HOST = your_pg_host
   PG_PORT = your_pg_port
   ```
5. **Create a directory named `certs` in the root directory.**
	```
	mkdir certs
	```
6. **Change directory:**
	```bash
	cd certs
	```
7. **Generate the JWT RSA keys inside the `certs` directory using the following commands:**
   ```bash
   openssl genrsa -out jwt-private.pem 2048
   openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
   ```
8. **Make migrations with the following command:**
	```bash
	uv run alembic revision --autogenerate -m "init migration"
	uv run alembic upgrade head
	```

## Running the Application

Start the application with:
```bash
uv run uvicorn app.main:app --reload
```

## API Documentation

After starting the server, access the interactive API documentation at:
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`


## Running the Application

Start the application with:
```bash
uv run uvicorn app.main:app --reload
```

## API Documentation

After starting the server, access the interactive API documentation at:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Running the Application in Docker

To run the application inside a container:

1. **Ensure Docker and Docker Compose are installed.**
2. **Create the `.env` file in the root directory:**
   ```dotenv
   PG_USER=your_pg_user
   PG_PASSWORD=your_pg_password
   PG_DB=your_pg_db
   PG_HOST=db
   PG_PORT=5432
   ```
3. **Create a directory named `certs` in the root directory and generate RSA keys:**
   ```bash
   mkdir certs
   cd certs
   openssl genrsa -out jwt-private.pem 2048
   openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
   ```
4. **Build and start the Docker containers:**
   ```bash
   docker compose up --build
   ```

## API Documentation

After starting the server, access the interactive API documentation at:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`
```
