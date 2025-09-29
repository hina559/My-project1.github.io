from django.urls import path
from .views import (
    detect_disease_view, 
    open_case_view,
    farmer_cases_list,
    farmer_case_detail
)

urlpatterns = [
    path("detect/", detect_disease_view, name="farmer_detect_disease"),
    path("open-case/", open_case_view, name="farmer_open_case"),
     
    # Case management URLs
    path("cases/", farmer_cases_list, name="farmer_cases_list"),
    path("cases/<int:case_id>/", farmer_case_detail, name="farmer_case_detail"),
]