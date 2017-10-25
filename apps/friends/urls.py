from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^user/(?P<friend_id>\d+)$', views.user),
    url(r'^add_friend/(?P<friend_id>\d+)$', views.add_friend),
    url(r'^remove_friend/(?P<friend_id>\d+)$', views.remove_friend),
    url(r'^$',views.index)
]