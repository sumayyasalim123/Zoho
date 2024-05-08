from fnmatch import fnmatchcase
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from eccomapp.models import Catogories,Product,Usermember,Cart
from django.http import HttpResponse
import os
# Create your views here.
def index(request):
    return render(request,'index.html')
def user_signup(request):
    return render(request,'user_signup.html')
def loginpage(request):
    return render(request,'loginpage.html')
def admin_home(request):
    return render(request,'admin_home.html')


def user_home(request):
    return render(request,'user_home.html')

def user_signup(request):
    
    return render(request,'user_signup.html')



def usercreate(request):
        if request.method=='POST':
            fname=request.POST['fname']  
            lname=request.POST['lname']  
            uname=request.POST['uname'] 
            address=request.POST['address'] 
            number=request.POST['cnumber']
            email=request.POST['email']
            image=request.FILES.get('file')
            password=request.POST['password']  
            cpassword=request.POST['cpassword']
            if password==cpassword:
                if User.objects.filter(username=uname).exists():
                    messages.info(request,'This username already exists.....')
                    return redirect('user_signup')
                else:
                    user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=password,email=email)
                    user.save()

                    member=Usermember(address=address,c_number=number,user=user,profilepic=image)
                    member.save()
                    return redirect('/')
            else:
                messages.info(request,'password does not match..')
                return redirect('user_signup')
            
        else:
            return redirect('index.html')
        

def show_user(request):
    if request.user.is_authenticated:
        user1=Usermember.objects.all()
        return render(request,'show_user.html',{'user':user1})
    return redirect('/')

def deleteuser(request,pk):
        User=Usermember.objects.get(id=pk)
        if User.profilepic:
            User.profilepic.delete()
        User.delete()
        User.user.delete()
        return redirect('show_user')
        
def admin_login(request):
    if request.method=='POST':
        username=request.POST.get('name')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin_home')
            else:
                login(request,user)
                auth.login(request,user)
                messages.info(request,f'welcome {username}')
                return redirect('user_home')
        else:
            messages.info(request,"invalid username or password")
            return redirect('/')
    return render(request,'index.html')

def admin_home(request):
    if request.user.is_authenticated and request.user.is_staff:
        print(request.user.id)
        return render(request,'admin_home.html')
    return render(request,'index.html')

def add_catogories(request):
    return render(request,'add_catogories.html')


def add_catogoriesdb(request):
    if request.method=='POST':
        catogories_name=request.POST.get('catogory')
        
        catogory=Catogories(catogory_name=catogories_name)
        catogory.save()
        return render(request,'admin_home.html')
def add_products(request):
    if request.user.is_authenticated:
        categories=Catogories.objects.all()
        return render(request,'add_products.html',{'category':categories})
    return redirect('add_products')

    
def add_productdb(request):
     if request.method=='POST':
        productname=request.POST['pname']
        print(productname)
        description=request.POST['description']
        print(description)
        price=request.POST['price']
        print(price)
        sel=request.POST['sel']  
        catogories=Catogories.objects.get(id=sel)  
        image=request.FILES.get('file')
        catlog=Product(add_product=productname,description=description,price=price,catogories=catogories,image=image)
        catlog.save()
        return render(request,'admin_home.html')
     
def show_products(request):
    prdts=Product.objects.all()
    return render(request,'show_products.html',{'prdts':prdts})

def delete(request,pk):
   p=Product.objects.get(id=pk)
   p.delete()
   return redirect('show_products')

def user_home(request):
    if request.user.is_authenticated:
        cat=Catogories.objects.all()
        return render(request,'user_home.html',{'catgy':cat})
       
    return redirect('/')



def add_catedb(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            name=request.POST.get('catogories')
            
            category=Catogories(catogory=name)
            category.save()
            return render(request,'add_category.html')
    return redirect('/')





     



def admin_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')


def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')

def cart(request):
      return render(request,'cart.html')



def products(request,pk):
    if request.user.is_authenticated:
        prdts=Product.objects.filter(catogories_id=pk)
        cat=Catogories.objects.get(id=pk)
        catgy=Catogories.objects.all()
        return render(request,'products.html',{'prdts':prdts,'cat':cat,'catgy':catgy})
    return redirect('/')


def add_to_cart(request,pk):
    product_instance=Product.objects.get(id=pk)
    
    item,created =Cart.objects.get_or_create(user=request.user,product=product_instance)

    if not created:
        item.quantity +=1
        item.save()
        

    return redirect('cartpage')    

def cartpage(request):
    ct_item=Cart.objects.filter(user=request.user)

    category=Catogories.objects.all()
    total_price=sum(item.product.price * item.quantity for item in ct_item)
    return render(request,'cart.html',{'cart_items':ct_item,'totalprice':total_price,'category':category})

  

   


def quantity_inc(request,pk):
        cart_item=Cart.objects.get(user=request.user,id=pk)  
        cart_item.quantity +=1
        cart_item.save()
        return redirect('cartpage')

def quantity_dec(request,pk):
        cart_item=Cart.objects.get(user=request.user,id=pk)  
        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        return redirect('cartpage')


def remove_cart(request,pk):
    c=Cart.objects.get(id=pk)
    c.delete()
    return redirect('cartpage')

def checkout(request):
    return render(request,'checkout.html')


def my_form_view(request):
    success_message = None

    if request.method == 'POST':
        # Process the form data
        form_data = request.POST.get('your_input_field_name')

        # Perform any necessary validation or processing here

        # Set success message
        success_message = 'Your order has placed successfully!'

        # Print success message to the console
        print(f'Form submitted successfully. Form data: {form_data}')

    # Render the form template with the success message in the context
    return render(request, 'checkout.html', {'success_message': success_message})

def process(request):
      return render(request,'checkout.html')





