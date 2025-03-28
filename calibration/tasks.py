from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from .helpers.sms import send_sms
from .models import MedicalEquipment, Notification

logger = get_task_logger(__name__)

def generate_safe_message(equipment):

    return (
        f"Calibration Alert for {equipment.name}\n"
        f"Model: {equipment.model_number}\n"
        f"Location: {equipment.location}\n"
        f"Calibration Due Date: {equipment.calibration_due_date.strftime('%Y-%m-%d %H:%M')}"
    )

def generate_role_specific_message(equipment, role):

    base_message = (
        f"Calibration Alert for {equipment.name}\n"
        f"Model: {equipment.model_number}\n"
        f"Location: {equipment.location}\n"
        f"Calibration Due Date: {equipment.calibration_due_date.strftime('%Y-%m-%d %H:%M')}\n"
    )
    
    role_specific_instructions = {
        'admin': (
            f"{base_message}"
            f"Admin Action Required:\n"
            f"- Review and approve calibration schedule\n"
            f"- Ensure compliance with regulatory standards\n"
            f"- Coordinate resources for calibration process"
        ),
        'engineer': (
            f"{base_message}"
            f"Engineer Action Required:\n"
            f"- Conduct comprehensive technical assessment\n"
            f"- Verify equipment specifications and performance metrics\n"
            f"- Prepare detailed calibration technical report"
        ),
        'technician': (
            f"{base_message}"
            f"Technician Action Required:\n"
            f"- Prepare calibration tools and equipment\n"
            f"- Execute precise calibration procedure\n"
            f"- Document all calibration steps and measurements\n"
            f"- Update equipment maintenance log"
        )
    }
    
    return role_specific_instructions.get(role, base_message)

@shared_task(
    name='calibration.tasks.check_calibration_and_notify',
    bind=True,
    ignore_result=False,
    acks_late=True,
    track_started=True,
    max_retries=3,
    default_retry_delay=60  # 1 minutes
)
def check_calibration_and_notify(self):

    logger.info("Starting calibration check task")

    try:
        current_time = now()
        time_threshold = current_time + timedelta(hours=24)

        logger.debug(f"Checking equipment due before: {time_threshold}")

        due_equipments = MedicalEquipment.objects.filter(
            calibration_due_date__lte=time_threshold,
            calibration_due_date__gt=current_time,
            Is_notified=False 
        ).select_related()

        if not due_equipments.exists():
            logger.info("No unnotified equipment due for calibration within 24 hours")
            return {
                'status': 'success',
                'message': 'No equipment due for calibration',
                'count': 0
            }

        User = get_user_model()
        notification_users = User.objects.filter(
            role__in=['admin', 'engineer', 'technician'],
            is_active=True
        )

        if not notification_users.exists():
            logger.warning("No active users found for notification")
            return {
                'status': 'warning',
                'message': 'No valid phone numbers for notification',
                'count': due_equipments.count()
            }

        notification_count = 0
        for equipment in due_equipments:
            try:
                base_message = generate_safe_message(equipment)

                Notification.objects.create(
                    equipment=equipment,
                    message=base_message,
                    status='unread'
                )
  
                users_by_role = {}
                for user in notification_users:
                    if user.phone_number:
                        users_by_role.setdefault(user.role, []).append(user)

                for role, users in users_by_role.items():
    
                    role_message = generate_role_specific_message(equipment, role)
                    recipient_numbers = [user.phone_number for user in users]
                    if recipient_numbers:
                        send_sms(role_message, recipient_numbers)

                equipment.Is_notified = True
                equipment.save()

                notification_count += 1
                logger.info(f"Notifications sent for equipment: {equipment.name}")

            except Exception as e:
                logger.error(f"Failed to process notification for {equipment.name}: {str(e)}")
                continue

        return {
            'status': 'success',
            'message': 'Calibration check complete',
            'notifications_sent': notification_count,
            'total_due': due_equipments.count()
        }

    except Exception as e:
        logger.error(f"Task failed: {str(e)}", exc_info=True)
        self.retry(exc=e)

@shared_task(name='calibration.tasks.hello')
def hello():
    return "Hello from Celery!"