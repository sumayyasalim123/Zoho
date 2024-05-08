from django.urls import path,include
from .import views
urlpatterns = [
    path('appthreehome',views.appthreehome,name='appthreehome'),
    path('detail',views.detail,name='detail'),
    path('register',views.register,name='register'),
]