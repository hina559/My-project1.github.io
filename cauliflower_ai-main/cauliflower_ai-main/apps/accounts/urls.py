from django.urls import path
from . import views

urlpatterns = [
    path('register/farmer/', views.register_farmer, name='register_farmer'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/edit/', views.edit_farmer_profile, name='edit_farmer_profile'),
    path('doctor/profile/edit/', views.edit_doctor_profile, name='edit_doctor_profile'),
]
