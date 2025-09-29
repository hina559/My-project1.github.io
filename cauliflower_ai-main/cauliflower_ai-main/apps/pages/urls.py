from django.urls import path
from .views import (
    landing_page,
    login_page,
    register_farmer_page,
    register_doctor_page,
    mark_notification_read,  # <-- shared view
)
from .farmer_views import (
    farmer_dashboard,
    farmer_profile,
    farmer_events,
    farmer_notifications,
)
from .doctor_views import (
    doctor_dashboard,
    doctor_profile,
    doctor_suggest,
    doctor_past_suggestions,
    doctor_events,
    doctor_notifications,
)
from .admin_views import (
    admin_dashboard,
    manage_events,
    manage_farmers,
    manage_doctors,
    admin_profile,
    display_admin_notifications,
)

urlpatterns = [
    # Landing & Authentication
    path('', landing_page, name='landing'),
    path('login/', login_page, name='login'),
    path('register/farmer/', register_farmer_page, name='register_farmer'),
    path('register/doctor/', register_doctor_page, name='register_doctor'),

    # Farmer Dashboard
    path('dashboard/farmer/', farmer_dashboard, name='farmer_dashboard'),
    path('dashboard/farmer/profile/', farmer_profile, name='farmer_profile'),
    path('dashboard/farmer/events/', farmer_events, name='farmer_events'),
    path('dashboard/farmer/notifications/', farmer_notifications, name='farmer_notifications'),

    # Doctor Dashboard
    path('dashboard/doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/doctor/profile/', doctor_profile, name='doctor_profile'),
    path('dashboard/doctor/suggest/', doctor_suggest, name='doctor_suggest'),
    path('dashboard/doctor/view_suggestions/', doctor_past_suggestions, name='doctor_past_suggestions'),
    path('dashboard/doctor/events/', doctor_events, name='doctor_events'),
    path('dashboard/doctor/notifications/', doctor_notifications, name='doctor_notifications'),

    # Shared Notification Marking
    path('notifications/mark-read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),

    # Admin Dashboard
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/events/', manage_events, name='admin_manage_events'),
    path('dashboard/admin/farmers/', manage_farmers, name='manage_farmers'),
    path('dashboard/admin/doctors/', manage_doctors, name='manage_doctors'),
    path('dashboard/admin/profile/', admin_profile, name='admin_profile'),
    path('dashboard/admin/notifications/', display_admin_notifications, name='admin_manage_notifications'),
]
