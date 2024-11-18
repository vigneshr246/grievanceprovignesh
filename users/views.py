from django.http import HttpResponse
from django.shortcuts import render
# Home Page View
def home_page(request):
    return render(request, 'users/home.html')

# Login Page View
def login_page(request):
    if request.method == "POST":
        # Retrieve input values
        email_input = request.POST.get('email')
        pass_value = request.POST.get('pass')
        checkbox_value = request.POST.get('checkbox')  # Will be None if unchecked
        
        # Example logic
        response = f"Text Input: {email_input}, Password: {pass_value}, Checkbox: {checkbox_value}"
        return HttpResponse(response)
    return render(request, 'users/home.html')

# Register Page View
def register_page(request):
    return render(request, 'home.html')

def forget_page(request):
    return render(request, 'home.html')

def user_dashboard(request):
    return render(request, 'users/user_dashboard.html')

# Complaint Form View
#def complaint_form(request):
    return render(request, 'complaint_form.html')
