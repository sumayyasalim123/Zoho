from django.urls import path,include
from .import views


urlpatterns = [
    path('',views.index,name="index"),
    path('usersignup',views.usersignup,name="usersignup"),
    path('usercreate',views.usercreate,name="usercreate"),
    path('loginpage',views.loginpage,name="loginpage"),
    path('user_login',views.user_login,name="user_login"),
    path('user_home/',views.user_home,name="user_home"),
    path('admin_home',views.admin_home,name="admin_home"),
    path('worker_home',views.worker_home,name="worker_home"),
    path('workersignup',views.workersignup,name="workersignup"),
    path('workercreate/', views.workercreate, name="workercreate"),
    path('works_in_category/<str:category_name>/', views.works_in_category, name='works_in_category'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('edit_user_profile/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
    path('reset_user_password/', views.reset_user_password, name='reset_user_password'),
    path('workers/', views. worker_list, name='worker_list'),
    path('workers_details/<int:worker_id>/',views.worker_details, name='worker_details'),
    path('worker_approval_table/',views.worker_approval_table, name='worker_approval_table'),
    path('approve_worker/<int:pk>/',views. approve_worker, name='approve_worker'),
   
   
   
]
   