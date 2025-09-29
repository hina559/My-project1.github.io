from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Case, Analysis,CaseMessage
import random
from apps.doctors.models import GeneralSuggestion  # Make sure this import is correct
from django import forms
from apps.accounts.models import CustomUser 

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
# GLOBAL DISEASE DATA
# =============================================================================
DISEASE_GLOBAL_DATA = {
    "alternaria_leaf_spot": {
        "prevention": [
            "Seedling Stage: Use certified disease-free seeds",
            "Avoid overhead watering",
            "Vegetative Stage: Rotate crops annually",
            "Remove and destroy infected leaves",
            "Flowering Stage: Ensure proper spacing for airflow",
            "Fruiting Stage: Apply protective mulch",
        ],
        "treatment": [
            "Seedling Stage: Spray copper-based fungicide if spots appear",
            "Vegetative Stage: Apply chlorothalonil or mancozeb fungicides",
            "Flowering Stage: Repeat fungicide sprays at 7–10 day intervals",
            "Fruiting Stage: Remove and destroy infected fruits",
        ],
        "best_practices": [
            "Sanitize garden tools",
            "Avoid working with wet plants",
            "Practice strict crop rotation",
        ],
    },
    "club_root": {
        "prevention": [
            "Seedling Stage: Use resistant varieties",
            "Test soil pH and maintain above 7.2",
            "Vegetative Stage: Apply lime to acidic soils",
            "Avoid waterlogging",
        ],
        "treatment": [
            "Currently no effective chemical treatment",
            "Uproot and destroy infected plants",
            "Improve soil drainage",
        ],
        "best_practices": [
            "Rotate crops with non-crucifers",
            "Keep field records of outbreaks",
            "Ensure tools are sanitized",
        ],
    },
    "downy_mildew": {  # already had data, kept same
        "prevention": [
            "Seedling Stage: Plant in sunny, ventilated areas",
            "Avoid water on leaves",
            "Vegetative Stage: Avoid dense planting",
            "Do not irrigate at night",
            "Flowering Stage: Keep humidity below 70%",
            "Remove affected leaves",
            "Fruiting Stage: Use drip irrigation",
            "Harvest promptly",
        ],
        "treatment": [
            "Seedling Stage: Spray neem oil if yellowing detected",
            "Vegetative Stage: Apply fungicide weekly",
            "Flowering Stage: Targeted fungicide early morning/evening",
            "Fruiting Stage: Remove infected fruits",
            "Apply protective fungicide",
        ],
        "best_practices": [
            "Inspect plants twice a week",
            "Ensure soil drains well",
            "Maintain proper crop rotation",
        ],
    },
    "cabbage_aphid_colony": {
        "prevention": [
            "Seedling Stage: Inspect seedlings for aphids before planting",
            "Encourage natural predators (lady beetles, lacewings)",
            "Vegetative Stage: Avoid over-fertilizing with nitrogen",
            "Remove weeds around fields",
        ],
        "treatment": [
            "Apply insecticidal soap or neem oil",
            "Use systemic insecticides if infestation is severe",
            "Spray early morning or evening to protect pollinators",
        ],
        "best_practices": [
            "Scout fields weekly",
            "Rotate crops",
            "Maintain biodiversity to support natural predators",
        ],
    },
    "ring_spot": {
        "prevention": [
            "Seedling Stage: Use certified seeds",
            "Avoid planting in infected soil",
            "Vegetative Stage: Remove infected leaves",
            "Flowering Stage: Maintain good airflow",
            "Fruiting Stage: Apply protective mulch",
        ],
        "treatment": [
            "Apply fungicides such as chlorothalonil",
            "Remove and destroy infected plant debris",
        ],
        "best_practices": [
            "Sanitize tools regularly",
            "Avoid overhead irrigation",
            "Rotate with non-host crops",
        ],
    },
    "black_rot": {  # already had data, kept same
        "prevention": [
            "Seedling Stage: Sterilize trays and pots",
            "Ensure seedlings are disease-free",
            "Maintain proper spacing",
            "Vegetative Stage: Prune affected leaves",
            "Avoid shaded or damp areas",
            "Use mulch",
            "Flowering Stage: Avoid overhead watering",
            "Monitor humidity",
            "Ventilate greenhouse",
            "Fruiting Stage: Remove infected fruits",
            "Rotate crops",
        ],
        "treatment": [
            "Seedling Stage: Spray copper-based fungicide weekly if infection detected",
            "Remove infected seedlings",
            "Vegetative Stage: Apply fungicide to affected areas",
            "Prune infected leaves",
            "Flowering Stage: Spray fungicide early morning or evening",
            "Remove infected flowers",
            "Fruiting Stage: Systemic fungicide",
            "Monitor fruits daily",
        ],
        "best_practices": [
            "Inspect plants daily",
            "Maintain clean tools",
            "Record outbreaks for future management",
        ],
    },
    "bacterial_spot_rot": {  # already had data, kept same
        "prevention": [
            "Seedling Stage: Use certified disease-free seeds",
            "Sanitize trays and tools",
            "Vegetative Stage: Avoid overhead irrigation",
            "Remove infected leaves",
            "Flowering Stage: Avoid working when leaves are wet",
            "Fruiting Stage: Rotate crops",
            "Disinfect harvesting tools",
        ],
        "treatment": [
            "Seedling Stage: Apply copper-based bactericide weekly",
            "Vegetative Stage: Spot spray infected leaves",
            "Flowering Stage: Spray bactericide early morning/evening",
            "Fruiting Stage: Remove infected fruits",
            "Apply systemic bactericide",
        ],
        "best_practices": [
            "Keep greenhouse ventilated",
            "Monitor humidity",
            "Maintain detailed records of outbreaks",
        ],
    },
    "no_disease": {
        "prevention": [],
        "treatment": [],
        "best_practices": [
            "Maintain healthy soil",
            "Water appropriately",
            "Regular crop inspection",
        ],
    },
}


# =============================================================================
# CASE MANAGEMENT VIEWS
# =============================================================================

@login_required
def farmer_cases_list(request):
    """Display all cases opened by the farmer in a table"""
    cases = Case.objects.filter(farmer=request.user).select_related('analysis').order_by('-created_at')
    
    # Handle case closure from list view
    if request.method == 'POST' and 'close_case' in request.POST:
        case_id = request.POST.get('case_id')
        try:
            case = Case.objects.get(id=case_id, farmer=request.user)
            if case.status != 'resolved':
                case.status = 'resolved'
                case.save()
                messages.success(request, f'Case #{case.id} has been closed successfully.')
            else:
                messages.info(request, f'Case #{case.id} is already closed.')
        except Case.DoesNotExist:
            messages.error(request, 'Case not found or you do not have permission to close it.')
        return redirect('farmer_cases_list')
    
    return render(request, 'dashboard/farmer/cases_list.html', {
        'cases': cases,
        'cases_count': cases.count()
    })



@login_required
def farmer_case_detail(request, case_id):
    """Display case details and handle farmer chat messages"""
    case = get_object_or_404(
        Case.objects.select_related('analysis', 'assigned_doctor'),
        id=case_id,
        farmer=request.user
    )

    # Add concatenated doctor name
    if case.assigned_doctor:
        case.assigned_doctor_full_name = f"{case.assigned_doctor.first_name} {case.assigned_doctor.last_name}"
    else:
        case.assigned_doctor_full_name = None

    # Chat form
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            CaseMessage.objects.create(
                case=case,
                sender=request.user,
                message=message_text
            )
            return redirect('farmer_case_detail', case_id=case.id)
        elif 'close_case' in request.POST and case.status != 'resolved':
            case.status = 'resolved'
            case.save()
            messages.success(request, f"Case #{case.id} marked as resolved.")
            return redirect('farmer_case_detail', case_id=case.id)

    messages_qs = case.messages.select_related('sender').all()

    return render(request, 'dashboard/farmer/case_detail.html', {
        'case': case,
        'messages_qs': messages_qs
    })

# =============================================================================
# DISEASE DETECTION & CASE CREATION VIEWS
# =============================================================================

@login_required
def detect_disease_view(request):
    """Detect disease from uploaded plant image"""
    result = None
    doctor_list = []
    if request.method == "POST" and request.FILES.get("plant_image"):
        image = request.FILES["plant_image"]

        # Fake AI Logic (random disease choice)
        DISEASES = {
            "black_rot": "Black Rot",
            "downy_mildew": "Downy Mildew",
            "bacterial_spot_rot": "Bacterial Spot Rot",
        }
        disease_key = random.choice(list(DISEASES.keys()))
        disease_name = DISEASES[disease_key]

        # Fetch related suggestions
        suggestions_qs = GeneralSuggestion.objects.filter(
            disease_type=disease_key
        ).select_related("doctor")

        suggestions = []
        for s in suggestions_qs:
            doctor = s.doctor
            doctor_name = f"{doctor.first_name} {doctor.last_name}".strip()
            doctor_list.append({
                "id": doctor.id,
                "name": doctor_name,
            })
            if not doctor_name:
                doctor_name = doctor.username

            suggestions.append({
                "title": s.title,
                "treatment": s.treatment,
                "prevention": s.prevention,
                "best_practices": s.best_practices,
                "priority": s.priority,
                "suggested_by": doctor_name,
            })

        # Build result object
        result = {
            "disease_name": disease_name,
            "analysis_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "suggestions": suggestions,
            "disease_key": disease_key,
            "general_info": DISEASE_GLOBAL_DATA.get(disease_key, {})
        }

    return render(request, "dashboard/farmer/image_upload.html", {"result": result, "doctor_list": doctor_list})


@login_required
def open_case_view(request):
    """Open a new case based on analysis results and assign a doctor"""
    if request.method == "POST":
        disease_name = request.POST.get("disease_name")
        crop_name = request.POST.get("crop_name")
        case_notes = request.POST.get("case_notes")
        doctor_id = request.POST.get("doctor_id")  # Selected doctor

        # Validate required fields
        if not disease_name or not doctor_id:
            messages.error(request, 'Please select a doctor and fill all required fields.')
            return redirect('farmer_detect_disease')
        
        # Create analysis record
        analysis = Analysis.objects.create(
            farmer=request.user,
            crop_name="Cauliflowerb",
            disease_name=disease_name,
        )
        # Fetch selected doctor if provided
        assigned_doctor = None
        if doctor_id:
            try:
                assigned_doctor = CustomUser.objects.get(id=doctor_id, role='doctor')
            except CustomUser.DoesNotExist:
                messages.warning(request, 'Selected doctor not found. Case will be unassigned.')

        # Create case with fixed priority
        case = Case.objects.create(
            farmer=request.user,
            analysis=analysis,
            title=f"Case for {crop_name} - {disease_name}",
            description=case_notes or f"Need help with {disease_name} on {crop_name}",
            priority='medium',  # FIXED
            status='open',
            assigned_doctor=assigned_doctor  # Make sure Case model has this field
        )

        messages.success(
            request,
            f"Case #{case.id} opened successfully! Dr. {assigned_doctor.first_name} will review your {crop_name} case with {disease_name}."
        )
        return redirect('farmer_case_detail', case_id=case.id)
    
    return redirect('farmer_detect_disease')