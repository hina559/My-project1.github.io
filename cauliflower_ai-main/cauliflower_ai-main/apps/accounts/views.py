# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FarmerProfile, DoctorProfile 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password


User = get_user_model()

def register_farmer(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        farm_size = request.POST.get('farm_size')
        years_farming = request.POST.get('years_farming')
        main_crops = request.POST.get('main_crops').strip()
        irrigation_method = request.POST.get('irrigation_method').strip()

        # Basic checks
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_farmer')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register_farmer')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='farmer'
        )
        
        # Store plain password for display
        user.plain_password = password
        user.save()

        # Create farmer profile
        FarmerProfile.objects.create(
            user=user,
            farm_size=farm_size,
            years_farming=years_farming,
            main_crops=main_crops,
            irrigation_method=irrigation_method
        )

        messages.success(request, 'Farmer registration successful! Please log in.')
        return redirect('login')  # Redirect to login page after success

    return render(request, 'auth/register/register_farmer.html')

def register_doctor(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        specialization = request.POST.get('specialization').strip()

        # Basic checks
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_doctor')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register_doctor')

        # Create doctor user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='doctor',
        )
        
        # Store plain password for display
        user.plain_password = password
        user.save()

        # Create doctor profile
        DoctorProfile.objects.create(
            user=user,
            specialization=specialization,
            is_approved=False
        )

        messages.success(request, 'Doctor account created successfully! Please wait for admin approval before you can access all features.')
        return redirect('login')  # Go to login page after registration

    return render(request, 'auth/register/register_doctor.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.role == 'farmer':
                return redirect('/dashboard/farmer/')
            elif user.role == 'doctor':
                return redirect('/dashboard/doctor/')
            elif user.role == 'admin':
                return redirect('/dashboard/admin/')
            else:
                return redirect('/')  # default fallback
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/login.html')


@login_required
def edit_farmer_profile(request):
    user = request.user
    farmer_profile = getattr(user, 'farmer_profile', None)
    
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        
        # Handle password change
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if new_password and confirm_password:
            # Check if new passwords match
            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return redirect('farmer_profile')
            
            # Check if new password is not empty
            if len(new_password) < 6:
                messages.error(request, 'New password must be at least 6 characters long.')
                return redirect('farmer_profile')
            
            # Set new password
            user.set_password(new_password)
            # Store plain password for display
            user.plain_password = new_password
            messages.success(request, 'Password changed successfully!')
        
        user.save()
        
        # Update farmer profile fields
        if farmer_profile:
            farmer_profile.farm_size = request.POST.get('farm_size', 0)
            farmer_profile.years_farming = request.POST.get('years_farming', 0)
            farmer_profile.main_crops = request.POST.get('main_crops', '').strip()
            farmer_profile.irrigation_method = request.POST.get('irrigation_method', '').strip()
            farmer_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('farmer_profile')  # Redirect back to profile page
    
    return redirect('farmer_profile')  # If not POST, redirect to profile page


@login_required
def edit_doctor_profile(request):
    user = request.user
    doctor_profile = getattr(user, 'doctor_profile', None)
    
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        
        # Handle password change
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if new_password and confirm_password:
            # Check if new passwords match
            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return redirect('doctor_profile')
            
            # Check if new password is not empty
            if len(new_password) < 6:
                messages.error(request, 'New password must be at least 6 characters long.')
                return redirect('doctor_profile')
            
            # Set new password
            user.set_password(new_password)
            # Store plain password for display
            user.plain_password = new_password
            messages.success(request, 'Password changed successfully!')
        
        user.save()
        
        # Update doctor profile fields
        if doctor_profile:
            doctor_profile.specialization = request.POST.get('specialization', '').strip()
            doctor_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('doctor_profile')  # Redirect back to profile page
    
    return redirect('doctor_profile')  # If not POST, redirect to profile page

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')
