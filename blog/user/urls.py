from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.users),
    url(r"^/(?P<username>)[\w]+", views.users),
]
