from django.shortcuts import render

# Create your views here.
def apptwohome(request):
    return render(request,'home.html')
def login(request):
    return render(request,'login.html')
def signup(request):
    return render(request,'signup.html')
def contact(request):
    return render(request,'contacts.html')