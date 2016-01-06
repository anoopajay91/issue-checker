from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^fetch-info/$',views.fetch_info,name="fetch_info"),
    url(r'^yesterday/$',views.last_24),
    url(r'^7-days-back/$',views.before_24_less_than_7),

]