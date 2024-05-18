from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html')
def login(request):
    return render(request,'login.html')
def signup(request):
    return render(request,'signup.html')
def about(request):
    return render(request,'about.html')
   
    
  
def usercreate(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email']

        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists!!!!')
                return redirect('signup')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                user.save()

    else:
        messages.info(request,'password doesnt match!!!!!!!!!!')
        print ("password is not matching....")
        return redirect('signup')
    

    return render(request,'signup.html')



def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username, password=password)
        if user is not None:
            
            auth.login(request, user)
            messages.info(request, F'Welcome {username}')
            return redirect('about')
        else:
            messages.info(request,'Invalid username or password . try again.')
            return redirect('loginpage')
    else:
        return redirect('loginpage')
    
    
def displayStud(request):
    stud=User.objects.all()
    return render(request,'about.html',{'user':stud})
    

def  logout(request):
    
    auth.logout(request)
    return redirect('home')  






