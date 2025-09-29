from django.contrib import admin
from .models import GeneralSuggestion

class GeneralSuggestionAdmin(admin.ModelAdmin):
    model = GeneralSuggestion
    list_display = ("title", "disease_type", "priority", "doctor", "created_at")
    list_filter = ("disease_type", "priority", "created_at")
    search_fields = ("title", "treatment", "prevention", "best_practices")
    ordering = ("-created_at",)

# Register the model
admin.site.register(GeneralSuggestion, GeneralSuggestionAdmin)
