from django.urls import path,include
from .import views
from .views import my_form_view
urlpatterns = [
    path('',views.index,name="index"),
    path('user_signup',views.user_signup,name="user_signup"),
    path('usercreate',views.usercreate,name="usercreate"),
    path('user_home',views.user_home,name="user_home"),
    path('loginpage',views.loginpage,name="loginpage"),
    path('admin_login',views.admin_login,name="admin_login"),
    path('admin_home',views.admin_home,name="admin_home"),
    path('add_catogories',views.add_catogories,name="add_catogories"),
    path('add_catogoriesdb',views.add_catogoriesdb,name="add_catogoriesdb"),
    path('add_products',views.add_products,name="add_products"),
    path('add_productdb',views.add_productdb,name="add_productdb"),
    path('show_products',views.show_products,name="show_products"),
    path('delete/<int:pk>',views.delete,name="delete"),
    path('show_user',views.show_user,name="show_user"),
    path('deleteuser/<int:pk>',views.deleteuser,name="deleteuser"),
    path('admin_logout',views.admin_logout,name="admin_logout"),
    path('user_logout',views.user_logout,name="user_logout"),
    path('products/<int:pk>',views.products,name="products"),
    path('add_to_cart/<int:pk>',views.add_to_cart,name="add_to_cart"),
    path('cartpage',views.cartpage,name="cartpage"),
    path('cart/<int:pk>',views.cart,name="cart"),
    
    path('quantity_inc/<int:pk>',views.quantity_inc,name="quantity_inc"),
    path('quantity_dec/<int:pk>',views.quantity_dec,name="quantity_dec"),

    path('remove_cart/<int:pk>',views.remove_cart,name="remove_cart"),

    path('checkout',views.checkout,name="checkout"),

     path('your-form-url/', my_form_view, name='your_form_view'),
   

    path('process',views.process,name="process"),
   
   
]