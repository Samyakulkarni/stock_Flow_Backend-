# StockFlow Backend

FastAPI backend for the StockFlow Product Management System.

## Features

- Health check endpoint
- Product CRUD APIs
- Product search by name
- Dashboard summary endpoint
- MySQL integration with SQLAlchemy ORM
- Layered architecture: controller, service, repository, database

## Setup

1. Create the MySQL database:

   ```sql
   CREATE DATABASE stockflow_db;
   ```

2. Create your environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

3. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

4. Activate the virtual environment:

   ```powershell
   venv\Scripts\activate
   ```

5. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

6. Run the server:

   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment

Create `.env` from `.env.example` and set:

```env
DATABASE_URL=mysql+pymysql://root:root@host.docker.internal:3306/stockflow_db
```

For Docker on Windows, `host.docker.internal` lets the FastAPI container connect to MySQL running on the host machine.

## Docker

Build the image:

```powershell
docker build -t stockflow-backend .
```

Run the container:

```powershell
docker run --name stockflow-backend -p 8000:8000 -e DATABASE_URL="mysql+pymysql://root:root@host.docker.internal:3306/stockflow_db" stockflow-backend
```

## API URLs

- Swagger docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Products list: `http://localhost:8000/api/products`
- Search products: `http://localhost:8000/api/products/search?name=laptop`
- Dashboard summary: `http://localhost:8000/api/products/dashboard/summary`

## Notes

- This repository contains backend code only.
- The frontend app should be hosted separately and allowed through CORS at `http://localhost:5173`.
- `.env` is intentionally not committed. Use `.env.example` as the starter file.
