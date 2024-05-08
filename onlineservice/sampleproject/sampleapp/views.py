from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login 
from .models import CustomUser, Usermember, UserMember1, Categories
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
import random
from .utils import generate_random_password  # Import the function directly from utils
from django.core.files.storage import FileSystemStorage
import string
from django.core.files.storage import FileSystemStorage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test



def index(request):
    return render(request, 'index.html')


def usersignup(request):
    return render(request, 'usersignup.html')


def loginpage(request):
    return render(request, 'loginpage.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def user_home(request):
    return render(request, 'user_home.html')


def worker_home(request):
    return render(request, 'worker_home.html')


def workersignup(request):
    return render(request, 'workersignup.html')


def worker_approval_table(request):
    return render(request, 'worker_approval_table.html')




def usercreate(request):
    if request.method == 'POST':
        # User signup logic
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        address = request.POST['address']
        number = request.POST['cnumber']
        email = request.POST['email']
        image = request.FILES.get('file')  # Use get() to safely get the file data
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        user_type = request.POST['text']
       
        if password == cpassword:
            if CustomUser.objects.filter(username=uname).exists():
                messages.info(request, 'This username already exists.....')
            else:
                # Generate a random 6-digit number for the confirmation code
                confirmation_code = generate_random_number()

                user = CustomUser.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=uname,
                    password=password,
                    email=email,
                    user_type=user_type,
                    
                )
                user.save()

                member = Usermember(
                    address=address,
                    c_number=number,
                    user=user,
                    profilepic=image,
                    confirmation_code=confirmation_code  # Save confirmation code here
                )
                member.save()

                # Sending confirmation email
                send_mail(
                    'Account Confirmation',
                    f'Your confirmation code is: {confirmation_code}',
                    'your_email@example.com',  # Update with your email
                    [email],
                    fail_silently=False,
                )

                return redirect('/')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'usersignup.html')



def convert_image_to_pdf(image_path, pdf_path):
    # Function to convert an image to PDF using ReportLab
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])
    c.showPage()
    c.save()

def generate_random_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))



def workercreate(request):
    categories = Categories.objects.all()

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        address = request.POST['address']
        email = request.POST['email']
        contactnumber = request.POST['contactnumber']

        category_id = request.POST.get('categories')
        new_category_name = request.POST.get('new_category')

        if category_id == 'other' and new_category_name:
            # Create a new category if the selected category is "other" and a new category name is provided
            new_category = Categories.objects.create(category_name=new_category_name)
            category_id = new_category.id

        experience = request.POST['experience']
        dob = request.POST['dob']
        id_type = request.POST['id_type']
        profile_picture = request.FILES.get('profile_picture')
        certificate = request.FILES.get('certificate')
        user_type = request.POST['text']
        random_password = str(random.randint(100000, 999999))

        if CustomUser.objects.filter(username=username).exists():
            messages.info(request, 'This username already exists.....')
            return redirect('signup_page')
        else:
            user = CustomUser.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                user_type=user_type,
                password=random_password
            )
            user.user_type = '3'
            user.save()

            pdf_filename = None
            if certificate and certificate.name.endswith('.pdf'):
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                certificate_filename = fs.save('certificates/' + certificate.name, certificate)
                pdf_filename = 'certificates/' + certificate.name.rsplit('.', 1)[0] + '.pdf'

            member = UserMember1(
                user=user,  
                a_ddress=address,
                contactnumber=contactnumber,
                experience=experience,
                dob=dob,
                categories=Categories.objects.get(id=category_id) if category_id != 'other' else None,
                id_type=id_type,
                profile_picture=profile_picture,
                certificate=pdf_filename,
                status='1' 
            )
            member.save()

            subject = 'Your Account Information'
            message = f'Hello {user.username},\n\nYour account has been created. Here are your login details:\n\nUsername: {user.username}\n Password: {random_password}\n\nPlease change your password after logging in.'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            messages.success(request, 'Signup successful. You can now login.')
            return redirect('loginpage')

    else:
        return render(request, 'workersignup.html', {'categories': categories})



def user_login(request):
    if request.method=='POST':
        username=request.POST.get('name')
        password=request.POST.get('password')
        pending_cust=UserMember1.objects.filter(status='pending')
        apprvd_cust=UserMember1.objects.filter(status='approved')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin_home')

            elif user.user_type == '2':
                auth.login(request,user)
                return redirect('user_home')

            elif user.is_authenticated and user.user_type=='3':
                worker = UserMember1.objects.get(user=user)
                if worker.status == 'pending':
                        messages.info(request, 'Please wait for admin approval')
                        return redirect('loginpage')
                elif UserMember1.status == 'approved':
                        login(request, user)
                        messages.info(request, f'Welcome {username}')
                        return redirect('Worker_home')
                else:
                        messages.info(request, 'Sorry, your request is rejected')
                        return redirect('loginpage')
            
            else:
                messages.info(request,"invalid username or password")
                return redirect('/')
        else:
            messages.info(request,"invalid username or password")
            return redirect('/')
    
    return render(request,'index.html')


def user_home(request):
    user_categories = UserMember1.objects.values('categories__category_name').distinct()
    return render(request, 'user_home.html', {'user_categories': user_categories})



def works_in_category(request, category_name):
    works_in_category = UserMember1.objects.filter(categories__category_name=category_name)
    return render(request, 'works_in_category.html', {'works_in_category': works_in_category})





def user_profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    member = Usermember.objects.get(user=user)

    context = {
        'user': user,
        'member': member,
    }

    return render(request, 'user_profile.html', context)


def edit_user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    member = get_object_or_404(Usermember, user=user)

    if request.method == 'POST':
        # Update Usermember details based on the submitted form data
        member.address = request.POST.get('address')
        member.c_number = request.POST.get('c_number')
        if request.FILES.get('profilepic'):
            member.profilepic = request.FILES['profilepic']
        member.save()

        # Redirect to the user profile page after successful update
        return redirect('user_profile', user_id=user.id)

    context = {
        'user': user,
        'member': member,
    }

    return render(request, 'edit_user_profile.html', context)



def reset_user_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if request.user.check_password(current_password) and new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Invalid current password or passwords do not match.')

    return render(request, 'reset_user_password.html')



def worker_list(request):
    workers = UserMember1.objects.all()
    return render(request, 'worker_list.html', {'workers': workers})

def worker_details(request, worker_id):
    worker = get_object_or_404(UserMember1, id=worker_id)
    return render(request, 'worker_details.html', {'worker': worker})







def approve_worker(request, pk):
    try:
        wworker = get_object_or_404(UserMember1, user_id=pk)
        wworker.status = 'approved'
        wworker.save()
    except UserMember1.DoesNotExist:
        

       return redirect('admin_home')
    

    def worker_approval_table(request):
     if request.user.is_authenticated and request.user.is_staff:
        user=CustomUser.objects.all()
        pending_worker=UserMember1.objects.filter(status='pending')
       
        
        return render(request,'worker_approval_table.html',{'pending':pending_worker})
     return redirect('/')







