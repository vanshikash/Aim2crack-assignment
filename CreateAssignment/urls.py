from os import link
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.linkcreate,name='CreateAssignment-home'),
    
    path('<slug:link>/instructions/',views.instructions,name='CreateAssignment-instructions'),

    path('<slug:link>/', views.summary,name='CreateAssignment-summary'),

    path('<slug:link>/instructions/edit',views.edit ,name='CreateAssignment-edit'),


]