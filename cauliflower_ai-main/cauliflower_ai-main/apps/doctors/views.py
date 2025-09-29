from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import GeneralSuggestion
from apps.farmers.models import Case, CaseMessage  # adjust import if your Case model is elsewhere

# =============================================================================
# CASE MESSAGE FORM
# =============================================================================
class CaseMessageForm(forms.ModelForm):
    class Meta:
        model = CaseMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your message...'})
        }

# =============================================================================
# SUGGESTION CREATION VIEW
# =============================================================================
@login_required
def create_suggestion(request):
    if request.method == "POST":
        disease_type = request.POST.get("disease_type")
        title = request.POST.get("title")
        treatment = request.POST.get("treatment")
        prevention = request.POST.get("prevention")
        best_practices = request.POST.get("best_practices")
        priority = request.POST.get("priority")

        # Save suggestion
        GeneralSuggestion.objects.create(
            doctor=request.user,
            disease_type=disease_type,
            title=title,
            treatment=treatment,
            prevention=prevention,
            best_practices=best_practices,
            priority=priority,
        )
        return redirect("doctor_past_suggestions")  # after saving, go to list page

    return render(request, "dashboard/doctor/create_suggestion.html")

# =============================================================================
# DOCTOR CASE VIEWS
# =============================================================================
@login_required
def doctor_cases_list(request):
    """Display all cases assigned to the logged-in doctor"""
    cases = Case.objects.filter(
        assigned_doctor=request.user
    ).select_related('analysis', 'farmer').order_by('-created_at')
    
    return render(request, 'dashboard/doctor/cases_list.html', {
        'cases': cases,
        'cases_count': cases.count()
    })


@login_required
def doctor_case_detail(request, case_id):
    """Display case details and handle doctor chat messages"""
    case = get_object_or_404(
        Case.objects.select_related('analysis', 'farmer', 'assigned_doctor'),
        id=case_id,
        assigned_doctor=request.user
    )

    # Concatenate farmer and doctor names
    case.farmer_full_name = f"{case.farmer.first_name} {case.farmer.last_name}"
    case.doctor_full_name = f"{case.assigned_doctor.first_name} {case.assigned_doctor.last_name}" if case.assigned_doctor else None

    # Handle chat messages
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            CaseMessage.objects.create(
                case=case,
                sender=request.user,
                message=message_text
            )
            return redirect('doctor_case_detail', case_id=case.id)

    messages_qs = case.messages.select_related('sender').all()

    return render(request, 'dashboard/doctor/case_detail.html', {
        'case': case,
        'messages_qs': messages_qs
    })
