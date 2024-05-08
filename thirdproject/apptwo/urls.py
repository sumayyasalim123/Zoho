from django.urls import path,include
from .import views
urlpatterns = [
    path('apptwohome',views.apptwohome,name='apptwohome'),
    path('login',views.login,name='login'),
     path('signup',views.signup,name='signup'),
      path('contact',views.contact,name='contact'),
]