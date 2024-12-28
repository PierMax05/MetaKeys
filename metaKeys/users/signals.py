import logging
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
from django.contrib.auth.signals import user_logged_in, user_logged_out

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.debug(f"Created Profile for user: {instance.username}")

@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    logger.info(f"User logged in: {user.username}")

@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    logger.info(f"User logged out: {user.username}")

