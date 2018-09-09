from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages

from customers.models import Client

# Create your views here.


def index(request):
    print(request.tenant.schema_name)
    return HttpResponse("HELLO WORLD")

class CustomersView(View):
    
    def get(self, request):
        if not request.tenant.schema_name == 'public' and not request.user.is_authenticated():
            return redirect('account_logout')
        customers = Client.objects.all()
        return render(request, 'superadmin/customers.html', {"customers": customers})


class AddCustomerView(View):
    
    def get(self, request):
        return render(request, 'superadmin/add_new_customer.html')

    def post(self, request):
        print(request.POST)
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
