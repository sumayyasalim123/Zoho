from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('welcome',views.welcome,name='welcome'),
]