# Standard Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q

from apps.admin_panel.models import Event, Notification
from apps.farmers.models import Analysis, Case
from django.utils import timezone



# =============================================================================
# FARMER DASHBOARD VIEWS
# =============================================================================


@login_required
def farmer_dashboard(request):
    """Farmer dashboard with basic stats."""
    user = request.user

    # Get basic statistics from database
    total_analyses = Analysis.objects.filter(farmer=user).count()
    open_cases = Case.objects.filter(farmer=user, status='open').count()
    total_cases = Case.objects.filter(farmer=user).count()
    
    # Get event and notification stats
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).count()
    total_notifications = Notification.objects.filter(recipient=user).count()
    unread_notifications = Notification.objects.filter(recipient=user, is_read=False).count()
    
    stats = {
        "uploads": total_analyses,
        "open_cases": open_cases,
        "total_cases": total_cases,
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "total_notifications": total_notifications,
        "unread_notifications": unread_notifications
    }

    # Get recent analyses (last 3)
    recent_analyses = Analysis.objects.filter(farmer=user).order_by('-analysis_date')[:3]
    recent_detections = []
    
    for analysis in recent_analyses:
        recent_detections.append({
            "crop_name": analysis.crop_name,
            "disease_name": analysis.disease_name,
            "date": analysis.analysis_date.strftime('%Y-%m-%d')
        })

    return render(request, 'dashboard/farmer/dashboard.html', {
        "user": user,
        "stats": stats,
        "recent_detections": recent_detections
    })


@login_required
def farmer_profile(request):
    """Farmer profile page."""
    user = request.user
    farmer_profile = getattr(user, "farmer_profile", None)
    return render(request, "dashboard/farmer/profile.html", {
        "user": user,
        "farmer_profile": farmer_profile,
    })



@login_required
def farmer_events(request):
    """Display events to farmers."""
    events = Event.objects.all().order_by("-date")
    return render(request, "dashboard/farmer/farmer_events.html", {
        "user": request.user,
        "events": events,
    })

def farmer_notifications(request):
    """
    Display all notifications for the logged-in farmer.
    Unread notifications are highlighted.
    """
    notifications = request.user.notifications.all().order_by('-created_at')

    return render(request, "dashboard/farmer/farmer_notifications.html", {
        "notifications": notifications,
    })