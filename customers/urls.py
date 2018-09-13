from django.conf.urls import url

from customers.views import index, CustomersView, AddCustomerView, DeleteCustomerView, EmployeesView, DeleteEmployeeView, AddEmployeeView,GetEmployeeDetailView, UpdateEmployeeView

urlpatterns = [
    
    url(r'^add-customer/?', view=AddCustomerView.as_view(), name='add_customer'),
    url(r'^delete-customer/?', view=DeleteCustomerView.as_view(), name='delete_customer'),
    url(r'^customers/?', view=CustomersView.as_view(), name='customers'),
    url(r'^add-employee/?', view=AddEmployeeView.as_view(), name='add_employee'),
    url(r'^employees/?', view=EmployeesView.as_view(), name='employees'),
    url(r'^employee-detail/?', view=GetEmployeeDetailView.as_view(), name='employee_detail'),
    url(r'^update-profile/?', view=UpdateEmployeeView.as_view(), name='update_profile'),
    url(r'^delete-employee/?', view=DeleteEmployeeView.as_view(), name='delete_employee'),
    url(r'^', view=EmployeesView.as_view()),
]
