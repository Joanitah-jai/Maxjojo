from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-control'}),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-control'}),
    )
    role = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your role', 'class': 'form-control'}),
    )
    department = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your department', 'class': 'form-control'}),
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'role', 'department',
            'phone_number', 'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None  # Remove help text
            field.error_messages = {
                'required': 'This field is required.',
                'invalid': 'Enter a valid value.',
            }


# Login form (using AuthenticationForm)
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'})
    )



