import os
from django.shortcuts import redirect, render
from .models import product

# Create your views here.

#load page...
def index(request):
    return render(request,'add_product.html')

def add_product(request):
    if request.method == 'POST':
        pname=request.POST['pname']
        price=request.POST['price']
        qty=request.POST['qty']        #request.POST.get(')
        #image=request.FILES['file']
        image=request.FILES.get('file')
        prd = product(product_name=pname,price=price,quantity=qty,image=image)
        print("Save data...")
        prd.save()
        return redirect('show_products')
    


def show_products(request):
    prdts = product.objects.all()
    return render(request,'show_product.html',{'prdts':prdts})

def editpage(request,pk):
    prdts = product.objects.get(id=pk)
    return render(request,'Edit.html',{'prdts':prdts})

def edit_product(request,pk):    
    if request.method=='POST':
        prdcts = product.objects.get(id=pk)
        prdcts.product_name = request.POST.get('pname')
        prdcts.Price = request.POST.get('price')
        prdcts.quantity = request.POST.get('qty')
        prdcts.image = request.FILES.get('file')
        prdcts.save()
        return redirect('show_products')
    return render(request, 'Edit.html',)
    

def delete(request,pk):
    p = product.objects.filter(id=pk)
    p.delete()
    return redirect('show_products')

