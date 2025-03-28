from django.contrib import admin
from .models import User, MedicalEquipment, Notification, CalibrationLog, CalibrationRequest, Message

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'role', 'department', 'phone_number', 'created_at')

class MedicalEquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_id', 'name', 'model_number', 'manufacturer', 'location', 'last_calibration_date', 'calibration_due_date', 'Is_notified', 'status', 'assigned_engineer', 'created_at')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'equipment', 'message', 'status', 'created_at')
    
class CalibrationLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'equipment', 'calibrated_by', 'calibration_date', 'comments')

class CalibrationRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'equipment', 'requested_by', 'assigned_to', 'request_date', 'status', 'comments')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'score')


# Registering the models
admin.site.register(User, UserAdmin)
admin.site.register(MedicalEquipment, MedicalEquipmentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(CalibrationLog,CalibrationLogAdmin)
admin.site.register(CalibrationRequest, CalibrationRequestAdmin)
admin.site.register(Message, MessageAdmin)
