from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from django.contrib.sites.models import Site

from customers.models import Client
from accounts.models import Account, Profile

# Create your views here.


def index(request):
    print(request.tenant.schema_name)
    return HttpResponse("HELLO WORLD")

class CustomersView(View):
    
    def get(self, request):
        if not request.tenant.schema_name == 'public' or not request.user.is_authenticated():
            return redirect('account_logout')

        customers = Client.objects.all().exclude(schema_name='public')
        tab_list = [
            {'tab_name': 'Customer Management', 'url': 'customers'}
        ]
        return render(request, 'superadmin/customers.html', {"customers": customers, 'tab_list': tab_list})


class AddCustomerView(View):
    
    def get(self, request):
        tab_list = [
            {'tab_name': 'Customer Management', 'url': 'customers'}
        ]
        return render(request, 'superadmin/add_new_customer.html', {'tab_list': tab_list})

    def post(self, request):
        if not request.tenant.schema_name == 'public' or not request.user.is_authenticated():
            return redirect('account_logout')
        tenant = Client(
            domain_url = request.POST.get('domain_url'),
            schema_name = request.POST.get('schema_name'),
            name = request.POST.get('name'),
            paid_until = request.POST.get('paid_until'),
            on_trial = True if request.POST.get('on_trial', None) else False
        )
        tenant.save()
        messages.success(request, 'New Customer added successfully.')
        return redirect('customers')


class DeleteCustomerView(View):
    
    def post(self, request):
        if not request.tenant.schema_name == 'public' or not request.user.is_authenticated():
            return redirect('account_logout')

        customer_id = request.POST.get('customer_id', None)
        try:
            customer_id = int(customer_id)
            client = Client.objects.get(id=customer_id)
            site = Site.objects.filter(domain=client.domain_url).first()
            if site:
                site.delete()
            client.delete(force_drop=True)
            messages.success(request, "Company is deleted.")
            return redirect('customers')
        except:
            import sys
            print(sys.exc_info())
            messages.info(request, "Something went wrong. Please try again")
            return redirect('customers')


class AddEmployeeView(View):
    
    def get(self, request):
        tab_list = [
            {'tab_name': 'Employee Management', 'url': 'employees'}
        ]
        return render(request, 'admin/add_new_employee.html', {'tab_list': tab_list})

    def post(self, request):
        if not request.user.is_superuser:
            messages.warning(request, 'You are not authorised.')
            return redirect('employees')
        account = Account(
            email=request.POST.get('email')
        )
        account.set_password(request.POST.get('password'))
        account.save()
        # Invite mail logic here
        profile = Profile(
            user_id=account.id,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name', ''),
            role=request.POST.get('role')
        )
        profile.save()
        messages.success(request, 'New Employee added successfully.')
        return redirect('employees')


class EmployeesView(View):
    
    def get(self, request):
        if request.user.is_authenticated() and request.user.is_superuser:
            tab_list = [
            {'tab_name': 'Employee Management', 'url': 'employees'},
            # {'tab_name': 'Team Management', 'url': 'teams'}
        ]
            employees = Account.objects.filter(is_superuser=False)

            return render(request, 'admin/employees.html', {'employees': employees, 'tab_list': tab_list})
        if request.user.is_authenticated():
            return redirect('employee_detail')
        return redirect('account_logout')


class DeleteEmployeeView(View):
    
    def post(self, request):
        if not request.user.is_superuser:
            messages.warning(request, 'You are not authorised.')
            return redirect('employees')

        employee_id = request.POST.get('employee_id', None)
        try:
            employee = Account.objects.get(id=int(employee_id))
            employee.delete()
            messages.success(request, "Emplyee is deleted.")
            return redirect('employees')
        except:
            import sys
            print(sys.exc_info())
            messages.info(request, "Something went wrong. Please try again")
            return redirect('employees')


class GetEmployeeDetailView(View):
    
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('account_logout')
        if request.user.is_superuser:
            return redirect('employees')
        tab_list = [
            {'tab_name': 'My Profile', 'url': 'employee_detail'},
            # {'tab_name': 'Team Management', 'url': 'teams'}
        ]
        return render(request, 'employee/details.html', {'tab_list': tab_list})


class UpdateEmployeeView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('account_logout')
        if request.user.is_superuser:
            return redirect('employees')
        tab_list = [
            {'tab_name': 'My Profile', 'url': 'employee_detail'},
            # {'tab_name': 'Team Management', 'url': 'teams'}
        ]
        return render(request, 'employee/profile_update_form.html', {'tab_list': tab_list})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('account_logout')
        if request.user.is_superuser:
            return redirect('employees')
        tab_list = [
            {'tab_name': 'My Profile', 'url': 'employee_detail'},
            # {'tab_name': 'Team Management', 'url': 'teams'}
        ]
        print(request.POST)
        profile = request.user.profile
        profile.first_name = request.POST.get('first_name', profile.first_name)
        profile.last_name = request.POST.get('last_name', profile.last_name)
        profile.gender = request.POST.get('gender', profile.gender)
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('employee_detail')
