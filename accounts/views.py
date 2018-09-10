from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as d_logout
from django.http import HttpResponse
from django.views import View
from django.contrib import messages

# Create your views here.

def index(request):
    print(request.tenant.schema_name)
    return HttpResponse("HELLO WORLD")


class LoginView(View):
    
    def get(self, request):
        if not request.user or request.user.is_anonymous or not request.user.superuser:
            return render(request, 'common/login.html')
        return redirect('customers')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            return redirect('account_logout')
        login(request, user)
        messages.success(request, 'You are logged out successfully.')
        if request.tenant.schema_name == 'public':
            return redirect('customers')
        if user.is_superuser:
            return redirect('employees')
        return redirect('index')


def logout(request):
    print("AM IIII")
    d_logout(request)
    messages.success(request, 'You are logged out successfully.')
    return redirect('account_login')
