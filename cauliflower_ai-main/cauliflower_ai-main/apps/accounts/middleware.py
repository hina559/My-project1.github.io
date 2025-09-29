from django.shortcuts import redirect
from django.contrib import messages

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define protected routes that require authentication
        protected_routes = [
            '/dashboard/farmer/',
            '/dashboard/doctor/',
            '/dashboard/admin/',
        ]
        
        # Define auth routes that should redirect authenticated users
        auth_routes = [
            '/login/',
            '/register/farmer/',
            '/register/doctor/',
            '/accounts/login/',
            '/accounts/register/farmer/',
            '/accounts/register/doctor/',
        ]
        
        # Check if user is authenticated
        is_authenticated = request.user.is_authenticated
        
        # Get current path
        current_path = request.path
        

        

        
        # If user is not authenticated and trying to access protected routes
        if not is_authenticated and any(current_path.startswith(route) for route in protected_routes):
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        
        # If user is authenticated and trying to access auth routes, redirect to appropriate dashboard
        if is_authenticated and any(current_path.startswith(route) for route in auth_routes):
            if request.user.role == 'farmer':
                return redirect('farmer_dashboard')
            elif request.user.role == 'doctor':
                return redirect('doctor_dashboard')
            elif request.user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('landing')
        
        # Frontend-level role-based access control
        if is_authenticated:
            user_role = request.user.role
            
            # Prevent doctors from accessing farmer routes
            if user_role == 'doctor' and current_path.startswith('/dashboard/farmer/'):
                messages.error(request, 'Access denied. This area is for farmers only.')
                return redirect('doctor_dashboard')
            
            # Prevent farmers from accessing doctor routes
            if user_role == 'farmer' and current_path.startswith('/dashboard/doctor/'):
                messages.error(request, 'Access denied. This area is for doctors only.')
                return redirect('farmer_dashboard')
            
            # Prevent non-admin users from accessing admin routes
            if user_role != 'admin' and current_path.startswith('/dashboard/admin/'):
                messages.error(request, 'Access denied. This area is for administrators only.')
                if user_role == 'farmer':
                    return redirect('farmer_dashboard')
                elif user_role == 'doctor':
                    return redirect('doctor_dashboard')
                else:
                    return redirect('landing')
            
            # Prevent admin from accessing non-admin dashboard routes
            if user_role == 'admin' and (current_path.startswith('/dashboard/farmer/') or current_path.startswith('/dashboard/doctor/')):
                messages.error(request, 'Access denied. This area is not for administrators.')
                return redirect('admin_dashboard')
        
        response = self.get_response(request)
        return response 