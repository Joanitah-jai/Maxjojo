from django.urls import path
from . import views

app_name = 'calibration'  # This registers the namespace

urlpatterns = [
    # User Views
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('test-task/', views.test_task, name='test_task'),
    path('arduino/', views.arduino, name='arduino'),


    # Calibration Log Views
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('log', views.log, name='log'),
    path('req', views.req, name='req'),
    path('privacy', views.privacy, name='privacy'),
    path('no', views.no, name='no'),
    path('home/', views.home, name='home'),  # Home view
    path('storage/', views.storage, name='storage'),  # Home view
    path('users/', views.user_list, name='user_list'),
    path('notifications/', views.notification_list, name='notification_list'),



    # MedicalEquipment URLs
    path('equipments/', views.MedicalEquipmentListView.as_view(), name='medicalequipment_list'),
    path('equipments/create/', views.MedicalEquipmentCreateView.as_view(), name='medicalequipment_create'),
    path('equipment/<int:pk>/update/', views.MedicalEquipmentUpdateView.as_view(), name='medicalequipment_update'),
    path('equipment/<int:pk>/delete/', views.MedicalEquipmentDeleteView.as_view(), name='medicalequipment_delete'),

    path('calibration_logs/', views.CalibrationLogListView.as_view(), name='calibration_log_list'),
    
    # Calibration Log Create
    path('calibration_log/create/', views.CalibrationLogCreateView.as_view(), name='calibration_log_create'),
    
    # Calibration Log Edit
    path('calibration_log/<int:pk>/edit/', views.CalibrationLogUpdateView.as_view(), name='calibration_log_edit'),
    
    # Calibration Log Delete
    path('calibration_log/<int:pk>/delete/', views.CalibrationLogDeleteView.as_view(), name='calibration_log_delete'),
 
    # Notification URLs
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
   
   
    # Calibration Request URLs
    path('calibration-requests/', views.CalibrationRequestListView.as_view(), name='calibrationrequest_list'),
    path('calibration-requests/new/', views.CalibrationRequestCreateView.as_view(), name='calibrationrequest_create'),
    path('calibration-requests/<int:pk>/edit/', views.CalibrationRequestUpdateView.as_view(), name='calibrationrequest_update'),
    path('calibration-requests/<int:pk>/delete/', views.CalibrationRequestDeleteView.as_view(), name='calibrationrequest_delete'),

]
