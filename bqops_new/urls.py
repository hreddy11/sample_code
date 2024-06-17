from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.index, name='index'),
    path('new/fetch_week_info/', views.fetch_week_info, name='fetch_week_info'),
]
