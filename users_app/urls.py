from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index), #GET Renders our database
    path('process', views.process) #POST redirect to index
]