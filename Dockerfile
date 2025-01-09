FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --force-reinstall --exists-action w -r requirements.txt

RUN pip install uvicorn
# RUN pip install django-ckeditor-5
# Copy the rest of the application code#
#COPY . .

RUN mkdir -p /app/logs \
    && chown -R www-data:www-data /app/logs \
    && chmod -R 755 /app/logs
# Expose the port that Uvicorn will run on
EXPOSE 8000
#RUN pwd && ls
### Command to run the application using Uvicorn
CMD ["uvicorn", "project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]