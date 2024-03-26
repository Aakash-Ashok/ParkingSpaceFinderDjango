from django import forms
from django.core.validators import RegexValidator
from app.models import *
from django.forms import DateTimeInput

from django import forms
from django.utils.translation import gettext_lazy as _

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = User
        fields = ["name", "email", "username", "password","confirm_password", "dob", "gender", "address", "phone_number", "profile_image"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_staff = True
        instance.set_password(self.cleaned_data["password"])  
        if commit:
            instance.save()
        return instance

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))   

    class Meta:
        model = User
        fields = ["name", "email", "username", "password", "confirm_password", "dob", "gender", "address", "phone_number", "profile_image"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'password' in self.cleaned_data:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")
        return cleaned_data
    
class ParkZoneForm(forms.ModelForm):
    VEHICLE_CHOICES = (
        ('bike', 'Bike'),
        ('car', 'Car'),
        ('heavy', 'Heavy Vehicle')
    )

    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="Select State")
    district = forms.ModelChoiceField(queryset=District.objects.all(), empty_label="Select District")
    location = forms.ModelChoiceField(queryset=Location.objects.all(),empty_label="Select location")
    vehicle_type = forms.ChoiceField(choices=VEHICLE_CHOICES)

    class Meta:
        model = ParkZone
        exclude = ["owner"]



class ReservationForm(forms.ModelForm):
    VEHICLE_CHOICES = (
        ('bike', 'Bike'),
        ('car', 'Car'),
        ('heavy', 'Heavy Vehicle')
    )

    vehicle_type = forms.ChoiceField(choices=VEHICLE_CHOICES)
    start_time = forms.DateTimeField(label='Start Time', widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    finish_time = forms.DateTimeField(label='Finish Time', widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    plate_number = forms.CharField(validators=[RegexValidator(
        regex=r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$', 
        message='Plate number must be in the format KXX123X',
        code='invalid_plate_number'
    )])
    phone_number = forms.CharField(validators=[RegexValidator(
        regex=r'^[0-9]+$',
        message='Phone number must contain only digits',
        code='invalid_phone_number'
    )])

    class Meta:
        model = Reservation
        exclude = ['ticket_code', 'customer', 'checked_out', 'parking_zone',"total_price"]

class ParkZoneSearchForm(forms.ModelForm):
    class Meta:
        model = ParkZone
        fields = ['location']
        labels = {
            'location': _('Location')
        }

class UserUpdateForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))   

    class Meta:
        model = User
        fields = ["name", "email", "dob", "gender", "address", "phone_number", "profile_image"]


class AdminUpdateForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = User
        fields = ["name", "email", "dob", "gender", "address", "phone_number", "profile_image"]



