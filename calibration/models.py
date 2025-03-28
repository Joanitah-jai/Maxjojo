from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import os
from twilio.rest import Client
from django.conf import settings



#lass ScheduledTask(models.Model):
    #TASK_STATUS_CHOICES = [
        #('pending', 'Pending'),
        #('in_progress', 'In Progress'),
        #('completed', 'Completed'),
    #]

    #task_name = models.CharField(max_length=255)
    #description = models.TextField(blank=True, null=True)
    #assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Links to technician/engineer
    #start_date = models.DateTimeField()
    #end_date = models.DateTimeField()
    #status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='pending')
    #reminder = models.BooleanField(default=True)  # To send notifications
    #phone_number = models.CharField(max_length=15, blank=True, null=True)  # Add this field for SMS

    #def __str__(self):
        #return self.task_name

    #def __str__(self):
        #return self.task_name

class Message(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Fetching the credentials from settings
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        # Message logic based on score
        if self.score >= 70:
            body = 'heyy how are u this is jojo'
        else:
            body = 'heyy how are u this is jojo, second chance lala'

        message = client.messages.create(
            body=body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to='+256754455044',  # Ensure this number is valid and verified
        )
        print(message.sid)
        return super().save(*args, **kwargs)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Admin'),
        ('engineer', 'Engineer'),
        ('technician', 'Technician'),
        ('manager', 'Manager'),
        ('nurse', 'Nurse'),
        ('doctor', 'Doctor'),
        ('logistics', 'Logistics Staff'),
        ('auditor', 'Auditor'),
        ('trainee', 'Trainee'),
        ('external', 'External Contractor'),
    )
    
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLES)
    department = models.CharField(max_length=100, null=True, blank=True)  # Optional
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Required fields for AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Ensure a user manager is defined
    objects = CustomUserManager()

    # Use email as the username field
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

class MedicalEquipment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
    )
    equipment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    last_calibration_date = models.DateTimeField()
    calibration_due_date = models.DateTimeField()
    Is_notified = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    assigned_engineer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_equipments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    STATUS_CHOICES = (
        ('unread', 'Unread'),
        ('read', 'Read'),
    )
    notification_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(MedicalEquipment, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.notification_id} for {self.equipment}"

class CalibrationLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(MedicalEquipment, on_delete=models.CASCADE)
    calibrated_by = models.TextField()
    calibration_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()

    def __str__(self):
        return f"Log {self.log_id} for {self.equipment.name}"

class CalibrationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    request_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(MedicalEquipment, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="requested_calibrations")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_requests")
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.request_id} for {self.equipment.name}"