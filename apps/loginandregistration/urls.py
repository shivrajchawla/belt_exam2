from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^register$',views.register),
    url(r'^show$',views.success),
    url(r'^logout$',views.logout),
    url(r'^login$',views.login),
    url(r'^$',views.index)
]