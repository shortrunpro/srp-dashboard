from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('', views.index),
    path('week', views.index),
    path('month', views.month)
]