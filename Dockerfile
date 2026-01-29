FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# copy only requirements first for caching
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=config.settings

EXPOSE $PORT

CMD ["/app/entrypoint.sh"]
