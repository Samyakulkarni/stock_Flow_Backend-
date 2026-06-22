FROM python:3.12-slim

WORKDIR /app

ENV DATABASE_URL=mysql+pymysql://root:root@host.docker.internal:3306/stockflow_db

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
