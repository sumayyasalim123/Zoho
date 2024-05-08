from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('welcome',views.welcome,name='welcome'),
    path('sumayya',views.sumayya,name='sumayya'),
    path('link',views.link,name='link'),
    path('styletag',views.styletag,name='styletag'),
    path('add_numbers',views.add_numbers, name='add_numbers'),
    path('',views.calculator,name='calculator'),
   
    
    path('calculate',views.calculate,name='calculate')

]


