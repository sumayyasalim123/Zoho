from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('thiruvanathapuram',views.thiruvananthapuram,name='thiruvanathapuram'),
    path('ernakulam',views.ernakulam,name='ernakulam'),
    path('palakkad',views.palakkad,name='palakkad'),
   ]