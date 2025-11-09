from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_welcome_email(user_email, subject='Welcome!', message='Thanks for signing up!'):
    """
    Background task to send welcome email to a user.
    
    Args:
        user_email: Email address of the user
        subject: Email subject (default: 'Welcome!')
        message: Email message (default: 'Thanks for signing up!')
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
            [user_email],
            fail_silently=False,
        )
        return f"Email sent successfully to {user_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@shared_task
def process_property_listing(property_id):
    """
    Example background task for processing property listings.
    This can be used for tasks like generating thumbnails, 
    sending notifications, or updating search indices.
    
    Args:
        property_id: ID of the property to process
    """
    # Add your property processing logic here
    return f"Property {property_id} processed successfully"

