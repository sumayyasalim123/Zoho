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
    path('worker_signup',views.worker_signup,name="worker_signup"),
    path('workercreate/', views.workercreate, name="workercreate"),
    path('works_in_category/<str:category_name>/', views.works_in_category, name='works_in_category'),
   
    path('edit_user_profile/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
    path('reset_user_password/', views.reset_user_password, name='reset_user_password'),
    path('workers/', views. worker_list, name='worker_list'),
    path('workers_details/<int:worker_id>/',views.worker_details, name='worker_details'),
    path('worker_approval_table/',views.worker_approval_table, name='worker_approval_table'),
    path('approve_worker/<int:worker_id>/', views.approve_worker, name='approve_worker'),
    path('disapprove_worker/<int:worker_id>/', views.disapprove_worker, name='disapprove_worker'),
    path('admin_add_categories',views.admin_add_categories,name="admin_add_categories"),
    path('add_catogoriesdb',views.add_catogoriesdb,name="add_catogoriesdb"),
    path('categories_approval/', views.categories_approval, name='categories_approval'),
    path('approve-category/<int:category_id>/', views.approve_category, name='approve_category'),
    path('notifications_redirect/', views.notifications_redirect, name='notifications_redirect'),
    
    path('user_profile/<str:username>/',views.user_profile, name='user_profile'),
    path('edit-user_profile/', views. edit_user_profile, name='edit_user_profile'),
    path('worker_profile/<str:username>/',views.worker_profile, name='worker_profile'),
    path('edit-worker_profile/<int:user_id>/', views.edit_worker_profile, name='edit_worker_profile'),
    path('reset_worker_password/<str:username>/',views.reset_worker_password, name='reset_worker_password'),
    path('add_service/',views.add_service, name='add_service'),
    path('myservice/', views.myservice, name='myservice'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('works_in_category/<str:category_name>/', views.works_in_category, name='works_in_category'),
    path('services_in_category/', views.services_in_category, name='services_in_category'),

    path('all_bookings/', views.all_bookings, name='all_bookings'),
    path('book_service/<int:service_id>/', views.book_service, name='book_service'),
    path('booking_approval/', views.booking_approval, name='booking_approval'),
    path('approve-booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('admin_home-status/',views.admin_home, name='admin_home'),
    path('approve-booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('disapprove-booking/<int:booking_id>/', views.disapprove_booking, name='disapprove_booking'),
    path('admin_worker_list/<str:username>/', views. admin_worker_list, name='admin_worker_list'),
    path('delete_worker/<int:worker_id>/', views.delete_worker, name='delete_worker'),
    
    path('admin_customer_list/', views.admin_customer_list, name='admin_customer_list'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name="delete_customer"),
    path('booking_approval_table/', views.booking_approval_table, name='booking_approval_table'),
    path('mark_compleated/<int:booking_id>/', views.mark_compleated, name='mark_compleated'),

    path('my_orders/', views.my_orders, name='my_orders'),
    path('my_orders_updations/', views.my_orders_updations, name='my_orders_updations'),
    path('review_form/<int:booking_id>/', views.review_form, name='review_form'),
    path('review_list/', views.review_list, name='review_list'),
    path('search/', views.worker_search, name='worker_search'),
    path('worker_services/<int:worker_id>/', views.worker_services, name='worker_services'),
    path('admin_service_serch/', views.admin_service_serch, name='admin_service_serch'),
    path('service_reviews/<int:service_id>/', views.service_reviews, name='service_reviews'),
    path('admin_category_list/',views. admin_category_list, name='admin_category_list'),
    path('admin_logout/',views.admin_logout, name='admin_logout'),
    path('user_logout/',views.user_logout, name='user_logout'),
    path('worker_logout/',views.worker_logout, name='worker_logout'),
    
   ]
    
   