from django.urls import path
from . import views

urlpatterns = [
    # Event management
    path('events/add/', views.add_event, name='admin_create_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='admin_delete_event'),
    
    # Notification management
    path('notifications/add/', views.add_notification, name='admin_add_notification'),
    path('notifications/delete/<int:note_id>/', views.delete_notification, name='admin_delete_notification'),

    # Delete functionality
    path('delete/doctor/<int:doctor_id>/', views.delete_doctor, name='admin_panel_delete_doctor'),
    path('delete/farmer/<int:farmer_id>/', views.delete_farmer, name='admin_panel_delete_farmer'),
    
    # Approve doctors
    path('approve/doctor/<int:doctor_id>/', views.approve_doctor, name='admin_panel_approve_doctor'),
    
    # Update admin profile
    path('update-profile/', views.update_admin_profile, name='admin_panel_update_profile'),
]
