from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('mural', views.mural, name='murali')
]