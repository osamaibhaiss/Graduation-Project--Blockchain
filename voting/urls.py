from django.contrib import admin
from django.urls import path
from . import  views


app_name = 'voting'  # Define the namespace here

urlpatterns = [
    path('home', views.home1, name='home1'),
    path('elections/', views.elections, name='elections'),
    path('vote/<int:election_id>/', views.vote, name='vote'),  # Keep only one definition of this URL
    path('results/<int:election_id>/', views.results, name='results'),
    
]


   #path('', views.home1, name='home1'),
   
   
  

