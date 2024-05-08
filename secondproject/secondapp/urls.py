from django.urls import path,include
from .import views
from django.urls import path


from django.contrib import admin
urlpatterns = [
    path('',views.index,name='index'),
    path('kannur',views.kannur,name='kannur'),
    path('ernakulam',views.ernakulam,name='ernakulam'),
    path('palakkad',views.palakkad,name='palakkad'),
    path('sum',views.sum,name='sum'),
    path('result',views.result,name='result'),
    
    ]
    