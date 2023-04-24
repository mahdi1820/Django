from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'


