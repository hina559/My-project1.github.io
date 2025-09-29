from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FarmerProfile, DoctorProfile

# Customize the CustomUser display in admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )

# Register all models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FarmerProfile)
admin.site.register(DoctorProfile)
