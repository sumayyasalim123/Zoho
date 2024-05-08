from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')
def thiruvananthapuram(request):
    return render(request,'thiruvananthapuram.html')
def ernakulam(request):
    return render(request,'ernakulam.html')
def palakkad(request):
    return render(request,'palakkad.html')

