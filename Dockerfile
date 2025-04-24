# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CSRF_TRUSTED_ORIGINS="https://your.domain.com"
ENV DJANGO_SUPERUSER_USERNAME="admin"
ENV DJANGO_SUPERUSER_EMAIL="admin@admin.com"
ENV DJANGO_SUPERUSER_PASSWORD="admin"

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script and set permissions
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Copy project files
COPY . /app/

# Create necessary directories and set permissions
RUN mkdir -p /app/database /app/media /app/staticfiles \
    && chmod -R 777 /app/database /app/media /app/staticfiles \
    && chmod -R 755 /app/docker-entrypoint.sh

# # Create migrations and compile messages during build
# RUN python manage.py makemigrations \
#     && python manage.py migrate \
#     && python manage.py compilemessages

# Create a non-root user and switch to it
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 