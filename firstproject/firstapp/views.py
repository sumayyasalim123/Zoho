from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'hello.html')
def welcome(request):
    return render(request,'welcome.html')
def sumayya(request):
    return render(request,'sumayya.html')
def link(request):
    return render(request,'hello.html')
def styletag(request):
    return render(request,'styletag.html')
from django.shortcuts import render

def add_numbers(request):
    if request.method == 'POST':
        num1 = int(request.POST['num1'])
        num2 = int(request.POST['num2'])
        result = num1 + num2
        return render(request,'result.html', {'result': result})
    return render(request, 'add_numbers.html')


def calculator(request):
    return render(request,'calculator.html')
def calculate(request):
    n1=int(request.POST.get('num1'))
    n2=int(request.POST.get('num'))
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
        r="select operator"
    return render(request,'calculator.html',{'result':r})
