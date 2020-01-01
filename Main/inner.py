# from books import admin
from django.conf.urls import url, include
from Main import views

urlpatterns = [
    url(r'^time/$', views.current_datetime),
    # url(r'^hello/$', views.current_url_view_good),
]