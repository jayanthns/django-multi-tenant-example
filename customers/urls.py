from django.conf.urls import url

from customers.views import index, CustomersView, AddCustomerView

urlpatterns = [
    url(r'^index/', view=index),
    url(r'^add-customer', view=AddCustomerView.as_view(), name='add_customer'),
    url(r'^', view=CustomersView.as_view(), name='customers'),
]
