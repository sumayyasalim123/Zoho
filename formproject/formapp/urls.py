from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.add,name="add"),
    path('addemp',views.addemp,name='addemp'),
    path('show/',views.show,name='show'),
    path('update/<int:id>',views.update,name='update'),
    path('delete/<int:id>',views.delete,name='delete')
   

]