from django.apps import AppConfig
from django.core.signals import request_started
from django.dispatch import receiver
import os

class StudioMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'studio_main'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from utils.file_cleaner import clean_duplicates
            cleaned = clean_duplicates()
            print(f"Cleaned {cleaned} duplicate files on startup")
