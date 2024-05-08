from django.shortcuts import render

# Create your views here.
def appthreehome(request):
    return render(request,'home1.html')
def detail(request):
    return render(request,'details.html')
def register(request):
    return render(request,'register.html')