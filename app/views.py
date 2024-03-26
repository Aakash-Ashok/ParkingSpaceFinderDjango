from django.shortcuts import render,redirect
from django.views.generic import *
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy ,reverse
import random
import string
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404
from datetime import time
from datetime import datetime, time
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.


class HomeView(TemplateView):
    template_name="home.html"

class AdminHomeView(TemplateView):
    template_name="admin_home.html"

class UserHomeView(TemplateView):
    template_name="user_home.html"

class UserRegistration(CreateView):
    form_class = UserForm
    template_name = 'user_registration.html'
    success_url = reverse_lazy('login')

class AdminRegistration(CreateView):
    form_class = AdminForm
    template_name = 'admin_registration.html'
    success_url = reverse_lazy('login')
    
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
                login(self.request, user)
                if user.is_staff:
                    return redirect('admin-home')
                else:
                    return redirect('user-home')
        return super().form_invalid(form)
    
def logout_view(request):
    logout(request)
    return redirect('home')

class UpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('profile')  # Redirect to the profile page
    pk_url_kwarg = 'pk'  

class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
    
class ParkZoneCreateView(CreateView):
    model = ParkZone
    form_class = ParkZoneForm
    template_name = 'parkzone_create.html'
    success_url = reverse_lazy('admin-home')  # Redirect to the homepage after creation

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class ParkZoneListView(ListView):
    model = ParkZone
    template_name = 'parkzone_list.html'
    context_object_name = 'parkzones'

    def get_queryset(self):
        return ParkZone.objects.filter(owner=self.request.user)
    

class ParkZoneUpdateView(UpdateView):
    model = ParkZone
    form_class = ParkZoneForm
    template_name = 'parkzone_update.html'
    success_url = reverse_lazy('parkzone_list')

    def get_queryset(self):
        return ParkZone.objects.filter(owner=self.request.user)


def create_ticket_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


class ReservationCreateView(FormView):
    form_class = ReservationForm
    template_name = 'reservation_create.html'
    success_url = 'user-home'

    def form_valid(self, form):
        start_time = form.cleaned_data['start_time']
        finish_time = form.cleaned_data['finish_time']
        vehicle_type = form.cleaned_data['vehicle_type']

        current_datetime = timezone.now()

        if start_time < current_datetime or finish_time < current_datetime:
            return self.form_invalid(form, message='Reservation time must be in the future')

        if start_time >= finish_time:
            return self.form_invalid(form, message='End time must be after start time')

        parking_zone_id = self.kwargs.get("pk")
        parking_zone = get_object_or_404(ParkZone, id=parking_zone_id)
        if parking_zone.vacant_slots == 0:
            return self.form_invalid(form, message='Parking Zone Full!')

        # Check if the parking zone is for the correct vehicle type
        if vehicle_type != parking_zone.vehicle_type:
            return self.form_invalid(form, message='Invalid vehicle type for this parking zone')

        # Check if the user has an active reservation
        active_reservation = Reservation.objects.filter(customer=self.request.user, checked_out=False).first()
        if active_reservation:
            return self.form_invalid(form, message='You already have an active reservation')

        ticket_code = create_ticket_code()
        while Reservation.objects.filter(ticket_code=ticket_code).exists():
            ticket_code = create_ticket_code()

        total_hours = (finish_time.hour - start_time.hour) + (finish_time.minute - start_time.minute) / 60
        total_price = total_hours * float(parking_zone.price)

        with transaction.atomic():
            reservation = Reservation.objects.create(
                customer=self.request.user,
                parking_zone=parking_zone,
                ticket_code=ticket_code,
                total_price=total_price,
                start_time=start_time,
                finish_time=finish_time,
                plate_number=form.cleaned_data['plate_number'],
                vehicle_type=vehicle_type,
                phone_number=form.cleaned_data['phone_number']
            )
            parking_zone.occupied_slots += 1
            parking_zone.vacant_slots = parking_zone.total_slots - parking_zone.occupied_slots
            parking_zone.save()

        return super().form_valid(form)

    def form_invalid(self, form, message=None):
        if message:
            form.add_error(None, message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse(self.success_url)


def delete_reservation(self, request, pk, *args, **kwargs):
    try:
        user_reservation = self.model.objects.get(customer=request.user, pk=pk)
        if user_reservation.checked_out:
            messages.error(request, 'Reservation has already been checked out')
            return redirect('reservation-list')
        parking_zone = user_reservation.parking_zone
        with transaction.atomic():
            parking_zone.occupied_slots -= 1
            parking_zone.vacant_slots += 1
            parking_zone.save()
            user_reservation.delete()
        messages.success(request, 'Reservation deleted successfully')
        return redirect('reservation-list')
    except self.model.DoesNotExist:
        messages.error(request, 'Reservation not found')
        return redirect('reservation-list')
    






class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservation_user_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(customer=self.request.user)


def check_out_reservation(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    parking_zone = reservation.parking_zone
    if reservation.checked_out:
        messages.error(request, 'Reservation has already been checked out')
    else:
        with transaction.atomic():
            reservation.checked_out = True
            reservation.save()
            parking_zone.occupied_slots -= 1
            parking_zone.vacant_slots += 1
            parking_zone.save()
        messages.success(request, 'Reservation checked out successfully')
    return redirect('reservation-list')


class ReservationAdminListView(ListView):
    model = Reservation
    template_name = 'reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        # Get the parking zone ID from the URL
        pk = self.kwargs.get('pk')
        # Get the current user's parking zone and filter reservations by that parking zone
        parking_zone = ParkZone.objects.get(pk=pk, owner=self.request.user)
        return Reservation.objects.filter(parking_zone=parking_zone)


def parking_zone_search(request):
    park_zones = ParkZone.objects.all()
    form = ParkZoneSearchForm(request.GET)
    
    if form.is_valid():
        loc_id = form.cleaned_data.get('location')
        park_zones = ParkZone.objects.filter(location_id=loc_id)
    
    return render(request, 'search_results.html', {'form': form, 'park_zones': park_zones})





class UpdatePasswordView(FormView):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('user-home')

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['new_password1'])
        user.save()
        update_session_auth_hash(self.request, user)  # Important!
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
