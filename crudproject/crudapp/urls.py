from django.urls import path,include
from .import views
urlpatterns = [
   path('',views.show_employee,name="show_employee"),
   path('add_employee',views.add_employee,name="add_employee"),
   path('show_employee_details',views.show_employee_details,name="show_employee_details"),
   path('editpage/<int:pk>',views.editpage,name="editpage"),
   path('edit_employee_details/<int:pk>',views.edit_employee_details,name="edit_employee_details"),
   path('deletepage/<int:pk>',views.deletepage,name="deletepage")

]