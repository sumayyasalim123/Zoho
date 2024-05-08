from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name="index"),
    path('addStudent',views.addStudent,name="addStudent"),
    path('displayStud',views.displayStud,name="displayStud"),
    path('studDetails/<int:pk>',views.studDetails,name="studDetails"),
    path('edit/<int:pk>',views.edit,name="edit"),
    path('update/<int:pk>',views.update,name="update"),
    path('delete/<int:pk>',views.delete,name="delete")
]