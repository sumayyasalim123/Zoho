from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('about',views.about,name='about'),
    path('usercreate',views.usercreate,name='usercreate'),
    path('login1',views.login1,name='login1'),
    path('logout',views.logout,name='logout')
    
    ]