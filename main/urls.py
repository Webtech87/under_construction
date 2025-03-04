from django.urls import path
from . import views

app_name='main'

urlpatterns = [
    path('', views.site_under_construction, name="site_under_construction"),
]