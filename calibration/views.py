from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import User, MedicalEquipment, Notification, CalibrationLog, CalibrationRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
import serial
import time
from datetime import datetime
from django.utils import timezone

# Create your views here.


# Home view
def home(request):
    return render(request, 'home.html')

# ---------------- USER VIEWS ----------------

# Data storage view
def storage(request):
    return render(request, 'Equipment tracking.html')

# Data storage view
def no(request):
    return render(request, 'Notifications and alerts.html')

def privacy(request):
    return render(request, 'privacy.html')

def log(request):
    return render(request, 'log.html')

def req(request):
    return render(request, 'req.html')


def user_list(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'users_list.html', {'users': users})  # Render users_list.html with users data


def notification_list(request):
    notifications = Notification.objects.all().order_by('-created_at')  # Get all notifications, newest first
    return render(request, 'notifications.html', {'notifications': notifications})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("calibration:login")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {"form": form })

def login_view(request): 
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user()) 
            return redirect("calibration:home")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'calibration/login.html', {"form": form})

@method_decorator(login_required, name='dispatch')
class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'user_list.html', {'users': users})





# List View
class MedicalEquipmentListView(LoginRequiredMixin, ListView):
    model = MedicalEquipment
    template_name = 'medicalequipment_list.html'
    context_object_name = 'equipments'

    def get_queryset(self):
        # Ensure no equipment without a valid id is passed
        return MedicalEquipment.objects.exclude(equipment_id__isnull=True)

# Create View 
class MedicalEquipmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MedicalEquipment
    fields = ['name', 'model_number', 'manufacturer', 'location', 'last_calibration_date', 'calibration_due_date', 'status', 'assigned_engineer']
    template_name = 'medicalequipment_form.html'
    success_url = reverse_lazy('calibration:medicalequipment_list')

    def test_func(self):
        return self.request.user.role in ['admin', 'engineer', 'technician']

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to create medical equipment.")
        return redirect('calibration:medicalequipment_list')  # Redirect them to the list view

# Update View
class MedicalEquipmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MedicalEquipment
    fields = ['location', 'last_calibration_date', 'calibration_due_date', 'status', 'assigned_engineer']
    template_name = 'medicalequipment_form.html'
    success_url = reverse_lazy('calibration:medicalequipment_list')

    def test_func(self):
        return self.request.user.role in ['admin', 'engineer', 'technician']
    def form_valid(self, form):
        # Set is_notified to False when equipment details are updated
        form.instance.Is_notified = False
        return super().form_valid(form)

# Delete View
class MedicalEquipmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MedicalEquipment
    template_name = 'medicalequipment_confirm_delete.html'
    success_url = reverse_lazy('calibration:medicalequipment_list')

    def test_func(self):
        return self.request.user.role == 'admin'
    

# List View
class CalibrationLogListView(LoginRequiredMixin, ListView):
    model = CalibrationLog
    template_name = 'calibrationlog_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return CalibrationLog.objects.select_related('equipment' ).order_by('calibration_date')

# Create View
class CalibrationLogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CalibrationLog
    fields = ['equipment', 'calibrated_by', 'comments']
    template_name = 'calibration_log_form.html'
    success_url = reverse_lazy('calibration:calibration_log_list')

    

    def test_func(self):
        return self.request.user.role in ['admin', 'engineer', 'technician']

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to add a calibration log.")
        return redirect('calibration:calibration_log_list')

# Update View
class CalibrationLogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CalibrationLog
    fields = ['equipment', 'comments']
    template_name = 'calibration_log_form.html'
    success_url = reverse_lazy('calibration:calibration_log_list')

    def test_func(self):
        return self.request.user.role in ['admin', 'engineer', 'technician']

# Delete View
class CalibrationLogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CalibrationLog
    template_name = 'calibration_log_confirm_delete.html'
    success_url = reverse_lazy('calibration:calibration_log_list')

    def test_func(self):
        return self.request.user.role == 'admin'


# List View
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


from .tasks import hello

def test_task(request):
    result = hello.delay()
    return JsonResponse({"task_id": result.id})


# List View for Calibration Logs




# List View - View all Calibration Requests
class CalibrationRequestListView(LoginRequiredMixin, ListView):
    model = CalibrationRequest
    template_name = 'calibrationrequest_list.html'
    context_object_name = 'calibration_requests'

    def get_queryset(self):
        return CalibrationRequest.objects.all().order_by('-request_date')

# Create View - Request Calibration for an Equipment
class CalibrationRequestCreateView(LoginRequiredMixin, CreateView):
    model = CalibrationRequest
    fields = ['equipment', 'requested_by', 'assigned_to', 'status', 'comments']
    template_name = 'calibrationrequest_form.html'
    success_url = reverse_lazy('calibration:calibrationrequest_list')

    def form_valid(self, form):
        form.instance.requested_by = self.request.user  # Set requested_by to the logged-in user
        messages.success(self.request, "Calibration request submitted successfully.")
        return super().form_valid(form)

# Update View - Approve/Reject Calibration Requests
class CalibrationRequestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CalibrationRequest
    fields = ['equipment', 'requested_by', 'assigned_to', 'status', 'comments']
    template_name = 'calibrationrequest_form.html'
    success_url = reverse_lazy('calibration:calibrationrequest_list')

    def test_func(self):
        return self.request.user.role in ['admin', 'engineer']

    def form_valid(self, form):
        messages.success(self.request, "Calibration request updated successfully.")
        return super().form_valid(form)

# Delete View - Delete a Calibration Request (Admins only)
class CalibrationRequestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CalibrationRequest
    template_name = 'calibrationrequest_confirm_delete.html'
    success_url = reverse_lazy('calibration:calibrationrequest_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Calibration request deleted successfully.")
        return super().delete(request, *args, **kwargs)




def arduino(request):
    data_lines = []
    ser = None  

    try:
        equipment_id = 3  # Replace with the actual equipment ID
        equipment = MedicalEquipment.objects.get(equipment_id=equipment_id)

        # Check if calibration is due
        current_time = timezone.now()
        if equipment.calibration_due_date <= current_time:
            data_lines.append("Calibration is due! Stopping the machine.")
            print("Calibration due, stopping the machine.")  # Debugging message
            
            # Open the serial connection to send the STOP command
            ser = serial.Serial("COM6", 9600, timeout=5)
            time.sleep(2)  # Allow Arduino to establish connection

            print("Sending STOP command to Arduino...")  
            ser.write(b"STOP\n")  # Send STOP command
            time.sleep(1)  # Give Arduino time to process the command
            print("STOP command sent.")  

            ser.close()  # Close the serial connection after sending STOP
            return render(request, "arduino.html", {"data_lines": data_lines})

        # If calibration is not due, continue with normal readings
        ser = serial.Serial("COM6", 9600, timeout=5)
        time.sleep(2)

        for _ in range(5):
            line = ser.readline().decode().strip()
            if line:
                data_lines.append(line)
                print(f"Received from Arduino: {line}")  

    except Exception as e:
        print(f"Error occurred: {e}")  
        data_lines.append(f"Error: {e}")

    finally:
        if ser:
            print("Closing serial connection.")  
            ser.close()

    return render(request, "arduino.html", {"data_lines": data_lines})

