import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        import users.signals
        logger.info("UsersConfig ready: signals registered")
