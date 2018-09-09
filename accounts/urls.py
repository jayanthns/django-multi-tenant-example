from django.conf.urls import url

from accounts.views import index, LoginView, logout

urlpatterns = [
    url(r'^index/', view=index, name='index'),
    url(r'^login/', view=LoginView.as_view(), name='account_login'),
]
