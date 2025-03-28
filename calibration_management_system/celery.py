import os
from celery import Celery
from django.conf import settings

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calibration_management_system.settings')

# Create Celery app
app = Celery('calibration_management_system')

# Configure Celery using Django settings
app.config_from_object(settings, namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Optional: Add any global Celery configurations
app.conf.update(
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    broker_transport_options={'visibility_timeout': 3600},
broker_connection_retry_on_startup = True  
)