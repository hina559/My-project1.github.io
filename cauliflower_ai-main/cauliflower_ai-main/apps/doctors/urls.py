from django.urls import path
from . import views

urlpatterns = [
    # Doctor suggestions
    path("suggestions/create/", views.create_suggestion, name="doctor_create_suggestion"),

    # Doctor cases
    path("cases/", views.doctor_cases_list, name="doctor_cases_list"),
    path("cases/<int:case_id>/", views.doctor_case_detail, name="doctor_case_detail"),
]
