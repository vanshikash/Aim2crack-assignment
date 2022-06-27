from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.linkcreate,name='CreateAssignment-home'),
    
    path('instructions/',views.instructions,name='CreateAssignment-instructions'),
]