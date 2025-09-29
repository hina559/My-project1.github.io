from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Value
from django.db.models.functions import Concat

from apps.accounts.models import CustomUser
from .models import Event, Notification



# -----------------------------------------------------------------------------
# EVENTS MANAGEMENT
# -----------------------------------------------------------------------------
@csrf_exempt
def add_event(request):
    """Render form on GET, create event on POST."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        date_str = request.POST.get('date', '').strip()
        venue = request.POST.get('venue', '').strip()
        description = request.POST.get('description', '').strip()

        if not all([title, date_str, venue, description]):
            messages.error(request, 'All fields are required.')
            return redirect('admin_create_event')

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Use YYYY-MM-DD.')
            return redirect('admin_create_event')

        Event.objects.create(title=title, date=date, venue=venue, description=description)
        messages.success(request, f'Event "{title}" created successfully.')
        

    return render(request, 'dashboard/admin/add_event.html')


@csrf_exempt
def delete_event(request, event_id):
    """Delete an event via AJAX, no redirect."""
    if request.method == 'POST':
        try:
            event = get_object_or_404(Event, id=event_id)
            event_title = event.title
            event.delete()
            # Return JSON only; frontend shows toast
            return JsonResponse({
                'success': True,
                'message': f'Event "{event_title}" deleted successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error deleting event: {str(e)}'
            })

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# -----------------------------------------------------------------------------
# DOCTOR MANAGEMENT
# -----------------------------------------------------------------------------
@csrf_exempt
def approve_doctor(request, doctor_id):
    """Approve a doctor account."""
    if request.method == 'POST':
        try:
            doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')
            doctor.doctor_profile.is_approved = True
            doctor.doctor_profile.save()
            doctor_name = f"{doctor.first_name} {doctor.last_name}".strip() or doctor.username
            messages.success(request, f'Doctor "{doctor_name}" approved successfully.')
            return JsonResponse({'success': True, 'message': f'Doctor "{doctor_name}" approved successfully.'})
        except Exception as e:
            messages.error(request, f'Error approving doctor: {str(e)}')
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def delete_doctor(request, doctor_id):
    """Delete a doctor account."""
    if request.method == 'POST':
        try:
            doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')
            doctor_name = f"{doctor.first_name} {doctor.last_name}".strip() or doctor.username
            doctor.delete()
            messages.success(request, f'Doctor "{doctor_name}" deleted successfully.')
            return JsonResponse({'success': True, 'message': f'Doctor "{doctor_name}" deleted successfully.'})
        except Exception as e:
            messages.error(request, f'Error deleting doctor: {str(e)}')
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# -----------------------------------------------------------------------------
# FARMER MANAGEMENT
# -----------------------------------------------------------------------------
@csrf_exempt
def delete_farmer(request, farmer_id):
    """Delete a farmer account."""
    if request.method == 'POST':
        try:
            farmer = get_object_or_404(CustomUser, id=farmer_id, role='farmer')
            farmer_name = f"{farmer.first_name} {farmer.last_name}".strip() or farmer.username
            farmer.delete()
            messages.success(request, f'Farmer "{farmer_name}" deleted successfully.')
            return JsonResponse({'success': True, 'message': f'Farmer "{farmer_name}" deleted successfully.'})
        except Exception as e:
            messages.error(request, f'Error deleting farmer: {str(e)}')
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# -----------------------------------------------------------------------------
# ADMIN PROFILE
# -----------------------------------------------------------------------------
@csrf_exempt
def update_admin_profile(request):
    """Update admin profile information."""
    if request.method == 'POST':
        try:
            admin = request.user
            # Update basic info
            admin.first_name = request.POST.get('first_name', '').strip() or admin.first_name
            admin.last_name = request.POST.get('last_name', '').strip() or admin.last_name
            admin.email = request.POST.get('email', '').strip() or admin.email

            # Update password
            new_password = request.POST.get('new_password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()
            if new_password and new_password == confirm_password:
                if len(new_password) >= 6:
                    admin.set_password(new_password)
                    admin.plain_password = new_password
                    messages.success(request, 'Password updated successfully.')
                else:
                    return JsonResponse({'success': False, 'message': 'Password must be at least 6 characters long.'})
            elif new_password != confirm_password:
                return JsonResponse({'success': False, 'message': 'Passwords do not match.'})

            admin.save()
            messages.success(request, 'Admin profile updated successfully.')
            return JsonResponse({'success': True, 'message': 'Admin profile updated successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# -----------------------------------------------------------------------------
# NOTIFICATIONS
# -----------------------------------------------------------------------------
@csrf_exempt
def add_notification(request):
    """
    Admin creates a notification for a specific user (doctor or farmer).
    """
    recipients = (
        CustomUser.objects
        .exclude(role="admin")
        .annotate(full_name=Concat(F("first_name"), Value(" "), F("last_name")))
    )

    if request.method == "POST":
        recipient_id = request.POST.get("recipient_id")
        title = request.POST.get("title", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not all([recipient_id, title, message_text]):
            messages.error(request, "All fields are required.")
            return redirect("admin_add_notification")

        try:
            recipient = CustomUser.objects.get(id=recipient_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "Selected user does not exist.")
            return redirect("admin_add_notification")

        Notification.objects.create(
            recipient=recipient,
            title=title,
            message=message_text,
        )
        messages.success(
            request,
            f'Notification "{title}" sent to {recipient.get_full_name() or recipient.username}.'
        )
        return redirect("admin_add_notification")

    return render(
        request,
        "dashboard/admin/add_notification.html",
        {"recipients": recipients},
    )


@csrf_exempt  # CSRF is handled via fetch headers
def delete_notification(request, note_id):
    """Delete a notification via AJAX."""
    if request.method == "POST":
        try:
            note = Notification.objects.get(id=note_id)
            note.delete()
            return JsonResponse({"success": True, "message": "Notification deleted successfully."})
        except Notification.DoesNotExist:
            return JsonResponse({"success": False, "message": "Notification not found."})
    return JsonResponse({"success": False, "message": "Invalid request method."})
