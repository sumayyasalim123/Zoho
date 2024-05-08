from django.shortcuts import render,redirect
from studentapp.models import studentRegister

def index(request):
    return render(request,'index.html')

def addStudent(request):
    if request.method=="POST":
        n=request.POST.get('studname')
        addr=request.POST.get('addr')
        a=request.POST.get('age')
        mailid=request.POST.get('email')
        jod=request.POST.get('doj')
        q=request.POST.get('qual')
        gen=request.POST.get('gender')
        m=request.POST.get('mob')
        stud=studentRegister(name=n,address=addr,age=a,email=mailid,joiningDate=jod,qualification=q,gender=gen,mobile=m)
        stud.save()
        return redirect('displayStud')
    
def displayStud(request):
    stud=studentRegister.objects.all()
    return render(request,'display.html',{'stud':stud})

def studDetails(request,pk):
    stud=studentRegister.objects.get(id=pk)
    return render(request,'details.html',{'stud':stud})

def edit(request,pk):
    stud=studentRegister.objects.get(id=pk)
    return render(request,'edit.html',{'stud':stud})

def update(request,pk):
    if request.method=="POST":
        student=studentRegister.objects.get(id=pk)
        student.name=request.POST.get('stud_name')
        student.address=request.POST.get('stud_addr')
        student.age=request.POST.get('stud_age')
        student.email=request.POST.get('stud_email')
        student.joiningDate=request.POST.get('stud_doj')
        student.qualification=request.POST.get('stud_qual')
        student.gender=request.POST.get('stud_gender')
        student.mobile=request.POST.get('stud_mob')
        student.save()
        return redirect('displayStud')
    
def delete(request,pk):
    stud=studentRegister.objects.get(id=pk)
    stud.delete()
    return redirect('displayStud')