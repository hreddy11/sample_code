from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch_week_info/', views.fetch_week_info, name='fetch_week_info'),
]
