FROM python:3.11-slim

WORKDIR /app

# install system deps
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# make sure some packages are installed
RUN pip install psycopg2-binary
RUN pip install ultralytics==8.3.228

COPY . .

EXPOSE 8000

# run migrations and start the app
CMD ["sh", "-c", "alembic -c backend/alembic.ini upgrade head && python -m backend.app"]
