from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [

    #User
    path('user/registration/', UserRegistration.as_view(), name='user_registration'),
    path('user/home/',UserHomeView.as_view(),name="user-home"),
    path('reservation/<int:pk>',ReservationCreateView.as_view(), name='create_reservation'),
    path('parkzones/', parking_zone_search, name='parkzone_user_list'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('reservation/<int:pk>/delete/', delete_reservation, name='delete-reservation'),
    path('checkedout/<int:pk>',check_out_reservation,name="checkout"),
   

   



    #admin

    path('registration/admin/', AdminRegistration.as_view(), name='admin_registration'),
    path('home/admin/',AdminHomeView.as_view(),name="admin-home"),
    path('parkzone/create/', ParkZoneCreateView.as_view(), name='create_parkzone'),
    path('parkzone/list/', ParkZoneListView.as_view(), name='parkzone_list'),
    path('parkzone/update/<int:pk>/', ParkZoneUpdateView.as_view(), name='update_parkzone'),
    path('parking_zone/<int:pk>/reservations/', ReservationAdminListView.as_view(), name='admin-reservation-list'),




    #Comman URl

    path('',HomeView.as_view(),name="home"),
    path("login",LoginView.as_view(),name="login"),
    path('update_password/<int:pk>', UpdatePasswordView.as_view(), name='update-password'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update/<int:pk>/', UpdateView.as_view(), name='update_profile'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
