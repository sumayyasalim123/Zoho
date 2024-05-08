from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')
def kannur(request):
    return render(request,'kannur.html')
def ernakulam(request):
    return render(request,'ernakulam.html')
def palakkad(request):
    return render(request,'palakkad.html')
def sum(request):
    return render(request,'sum.html')
def result(request):
    n1=int(request.GET['num1'])
    n2=int(request.GET['num2'])
    s=n1+n2
    return render(request,'sum.html',{'sum':s})
def calculator(request):
    return render(request,'calculator.html')

def calculate(request):
    n1=int(request.POST['num1'])
    n2=int(request.POST['num2'])
    op=request.POST['operator']
    if op=='+':
        r=n1+n2
    elif op=='-':
        r=n1-n2
    elif op=='*':
        r=n1*n2
    elif op=='/':
        r=n1/n2
    else:
        r="Select operator"
    return render(request,'calculator.html',{'result':r})


    