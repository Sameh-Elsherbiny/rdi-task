FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --force-reinstall --exists-action w -r requirements.txt

RUN pip install uvicorn

RUN mkdir -p /app/logs \
    && chown -R www-data:www-data /app/logs \
    && chmod -R 755 /app/logs

EXPOSE 8000

CMD ["uvicorn", "project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
