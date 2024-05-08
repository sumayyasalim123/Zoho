from fnmatch import fnmatchcase
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from collageapp.models import Course,Student,Usermember
import os
# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_login(request):
    if request.method=='POST':
        username=request.POST.get['name']
        password=request.POST.get['password']
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

def admin_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')

# def add_course(request):
#     if request.user.is_authenticated:
#         return render(request,'add_course.html')
#     return redirect('/')

# def add_coursedb(request):
#     if request.method=='POST':
#         course_name=request.POST.get('course')
#         course_fee=request.POST.get('fee')
#         course=Course(course_name=course_name,fee=course_fee)
#         course.save()
#         return redirect('/')
    

# def add_student(request):
#     courses=Course.objects.all()
#     return render(request,'add_student.html',{'course':courses})

# def add_studentdb(request):
#     if request.method=='POST':
#         student_name=request.POST['name']
#         print(student_name)
#         student_address=request.POST['address']
#         print(student_address)
#         age=request.POST['age']
#         print(age)
#         jdate=request.POST['jdate']
#         print(jdate)
#         sel=request.POST['sel']
#         print(sel)
#         course1=Course.objects.get(id=sel)
#         print(course1)
#         student=Student(student_name=student_name,student_address=student_address,student_age=age,joining_date=jdate,course=course1)
#         student.save()
#         return redirect('/')
    
# def show_details(request):
#     student=Student.objects.all()
#     return render(request,'show_details.html',{'students':student})

# def edit(request,pk):
#     course=Course.objects.all()
#     student=Student.objects.get(id=pk)
#     return render(request,'edit.html',{'stud':student,'course':course})

# def editdb(request,pk):
#     if request.method=="POST":
#         student=Student.objects.get(id=pk)
#         student.student_name=request.POST['name']
#         student.student_address=request.POST['address']
#         student.student_age=request.POST['age']
#         student.joining_date=request.POST['jdate']
#         sel=request.POST['sel']
#         student.course=Course.objects.get(id=sel)
#         student.save()
#         return redirect('show_details')
    
# def delete(request,pk):
#     stud=Student.objects.get(id=pk)
#     stud.delete()
#     return redirect('show_details')

# def teacher_signup(request):
#     courses=Course.objects.all()
#     return render(request,'signup.html',{'course':courses})

# def add_teacherdb(request):
#     if request.method=='POST':
#         fname=request.POST.get('fname')
#         lname=request.POST.get('lname')
#         uname=request.POST.get('uname')
#         password=request.POST.get('password')
#         cpassword=request.POST.get('cpassword')
#         email=request.POST.get('email')
#         address=request.POST.get('address')
#         age=request.POST.get('age')
#         number=request.POST.get('number')
#         image=request.FILES.get('file')
#         sel=request.POST['sel']
#         course1=Course.objects.get('file')
#         if password==cpassword:
#             if User.objects.filter(username=uname).exists():
#                 messages.info(request,"This username already exist!!!")
#                 return redirect('teacher_signup')
#             else:
#                 user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=password,email=email)
#                 User.save()

#                 member=Usermember(address=address,age=age,number=number,image=image,user=user,course=course1)
#                 member.save()
#                 return redirect('/')
#         else:
#             messages.info(request,'password doesnot match!')
#             return redirect('teacher_signup')
#     else:
#         return render(request,'signup.html')
    

# def user_home(request):
#     if request.user.is_authenticated:
#         return render(request,'user_home.html')
#     return redirect('/')

# def user_edit(request):
#     if request.user.is_authenticated:
#         current_user=request.user.id
#         print(current_user)
#         user1=Usermember.objects.get(user.id=current_user)
#         user2=User.objects.get(id=current_user)
#         if request.method=='POST': 
#             if len(request.FILES)!=0:
#                 if len(user1.image)>0:
#                     os.remove(user1.image.path)
#                 user1.image=request.FILES.get('file')
#             user2.first_name=request.POST.get('fname')
#             user2.last_name=request.POST.get('lname')
#             user2.user_name=request.POST.get('uname')
#             user2.password=request.POST.get('password')
#             user2.email=request.POST.get('email')
#             user1.age=request.POST.get('age')
#             user1.addresss=request.POST.get('address')
#             user1.number=request.POST.get('number')
#             user1.save()
#             user2.save()
#             return redirect('profile')
#         return render(request,'user_edit.html',{'users':user1})
#     return redirect('/')

# def profile(request):
#     if request.user.is_authenticated:
#         current_user = request.user.id

#         user1=Usermember.objects.get(user_id=current_user)
#         return render(request,'profile.html',{'user':user1})
    
# def show_teacher(request):
#     if request.user.is_authenticated:
#         user1=Usermember.objects.all()
#         return render(request,'show_teacher.html',{'user':user1})
#     return redirect('/')

# def delete(request,pk):
#     user=Usermember.objects.get(id=pk)
#     if user.image:
#         user.image.delete()
#     user.delete()
#     user.user.delete()
#     return redirect('show_teacher')