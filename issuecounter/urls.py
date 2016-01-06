from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^fetch-info/$',views.fetch_info,name="fetch_info"),
]