from django.conf.urls import url

from customers.views import index, CustomersView, AddCustomerView, DeleteCustomerView, EmployeesView, DeleteEmployeeView, AddEmployeeView

urlpatterns = [
    url(r'^index/', view=index),
    url(r'^add-customer/?', view=AddCustomerView.as_view(), name='add_customer'),
    url(r'^delete-customer/?', view=DeleteCustomerView.as_view(), name='delete_customer'),
    url(r'^customers/?', view=CustomersView.as_view(), name='customers'),
    url(r'^add-employee/?', view=AddEmployeeView.as_view(), name='add_employee'),
    url(r'^employees/?', view=EmployeesView.as_view(), name='employees'),
    url(r'^delete-employee/?', view=DeleteEmployeeView.as_view(), name='delete_employee'),
]
