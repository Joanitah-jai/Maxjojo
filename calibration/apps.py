import os
import threading
import time
from django.apps import AppConfig


class CalibrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calibration'

    # def ready(self):
    #     """Start Celery worker and Celery Beat when Django starts."""
    #     if os.environ.get('RUN_MAIN') == 'true':  # Prevent double execution in development
    #         # Start Celery worker in a separate thread
    #         def start_celery_worker():
    #             os.system('celery -A calibration_management_system worker --loglevel=info --concurrency=2')

    #         worker_thread = threading.Thread(target=start_celery_worker, daemon=True)
    #         worker_thread.start()

    #         # Start Celery Beat in a separate thread
    #         def start_celery_beat():
    #             os.system('celery -A calibration_management_system beat --loglevel=info')

    #         beat_thread = threading.Thread(target=start_celery_beat, daemon=True)
    #         beat_thread.start()