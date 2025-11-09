# Deployment Guide

This guide covers the steps needed to deploy the Property Listings API to production.

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Redis server (for caching and Celery)
- Environment variables configured

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-server-domain.com,your-app.herokuapp.com,localhost,127.0.0.1

# Database Configuration
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@example.com
```

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations

```bash
python manage.py migrate
```

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Running the Application

### Development Mode

```bash
# Start Django development server
python manage.py runserver

# Start Celery worker (in a separate terminal)
celery -A alx_backend_caching_property_listings worker --loglevel=info
```

### Production Mode

#### Using Gunicorn

```bash
# Start web server
gunicorn alx_backend_caching_property_listings.wsgi --bind 0.0.0.0:8000

# Start Celery worker
celery -A alx_backend_caching_property_listings worker --loglevel=info
```

#### Using Procfile (Heroku/Render)

The `Procfile` is already configured. Deploy to your platform and it will automatically:
- Start the web server using Gunicorn
- Start the Celery worker

## Accessing API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://your-domain/swagger/`
- **ReDoc**: `http://your-domain/redoc/`
- **OpenAPI JSON**: `http://your-domain/swagger.json/`
- **OpenAPI YAML**: `http://your-domain/swagger.yaml/`

## Testing Celery Tasks

### Test Email Task

You can test the Celery email task from Django shell:

```python
from properties.tasks import send_welcome_email

# Send email asynchronously
result = send_welcome_email.delay('user@example.com', 'Welcome!', 'Thanks for signing up!')
print(result.get())  # Wait for result
```

### Test Property Processing Task

```python
from properties.tasks import process_property_listing

# Process property asynchronously
result = process_property_listing.delay(1)
print(result.get())  # Wait for result
```

## Platform-Specific Deployment

### Heroku

1. Set environment variables in Heroku dashboard
2. Deploy using Git:
   ```bash
   git push heroku main
   ```
3. Run migrations:
   ```bash
   heroku run python manage.py migrate
   ```
4. Collect static files:
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

### Render

1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Render will automatically use the `Procfile` to start services

### PythonAnywhere

1. Upload your project files
2. Set up a virtual environment
3. Install dependencies
4. Configure WSGI file
5. Set up scheduled tasks for Celery worker

## Troubleshooting

### Celery Worker Not Starting

- Ensure Redis is running: `redis-cli ping` (should return `PONG`)
- Check `CELERY_BROKER_URL` in your `.env` file
- Verify Redis connection: `redis-cli -h your-redis-host -p 6379`

### Static Files Not Loading

- Run `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` setting in `settings.py`
- Ensure your web server is configured to serve static files

### Database Connection Issues

- Verify database credentials in `.env`
- Ensure database server is running
- Check network connectivity to database host

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` is set and secure
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] Database credentials are secure
- [ ] Static files are served correctly
- [ ] HTTPS is enabled
- [ ] Environment variables are not committed to Git

