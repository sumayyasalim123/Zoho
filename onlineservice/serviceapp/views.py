from django.contrib import auth
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import logout
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.http import Http404  # Add this line
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login 
from serviceapp.models import CustomUser, Usermember, UserMember1, Categories,Service,Booking,Review
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
import random
from django.contrib.auth.hashers import check_password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from django.db import transaction
from .utils import generate_random_password  # Import the function directly from utils
from django.core.files.storage import FileSystemStorage
import string
from datetime import timedelta
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test


def index(request):
    # Retrieve all service objects from the database
    services = Service.objects.all()
    # Pass the services to the template context
    return render(request, 'index.html', {'services': services})


def usersignup(request):
    return render(request, 'usersignup.html')


def loginpage(request):
    return render(request, 'loginpage.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def user_home(request):
    return render(request, 'user_home.html')


def worker_home(request):
    if request.user.is_authenticated:
        user = request.user
        reviews = Review.objects.all()
        pending_work = Booking.objects.filter(status='2', task_compleated='1', service__added_by=user).count()
        pending_count = Booking.objects.filter(status='1').count()
        booking_count = Booking.objects.filter(status='1', service__added_by=user).count()
        print("Pending work:", pending_work)
        return render(request, 'worker_home.html', {'reviews': reviews, 'pending_work': pending_work,'pending_count': pending_count,'booking_count': booking_count})
    else:
        # Redirect to login page or handle unauthenticated user
        # For example:
        return render(request, 'loginpage.html')





def user_profile(request):
    return render(request, 'user_profile.html')


def worker_signup(request):
  
        categories=Categories.objects.all()
        return render(request,'worker_signup.html',{'category':categories})
  


def worker_approval_table(request):
    return render(request, 'worker_approval_table.html')


def admin_add_categories(request):
    return render(request, 'admin_add_categories.html')

def myservice(request):
    return render(request, 'myservice.html')


def services_in_category(request):
    return render(request, 'services_in_category.html')


def booking_approval(request):
    try:
        user = request.user
        bookings = Booking.objects.select_related('service', 'user').filter(status='1', service__added_by=user)
        
        
        return render(request, 'booking_approval.html', {'bookings': bookings, })
    except Exception as e:
        return HttpResponse("An error occurred: " + str(e))




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
        user_type = request.POST['text']

        if len(number) != 10:
            messages.error(request, 'Contact number should be 10 digits long.')
            return render(request, 'usersignup.html')
        
        if CustomUser.objects.filter(username=uname).exists():
            messages.error(request, 'This username already exists.')
            return render(request, 'usersignup.html')
        
        if not email.endswith('@gmail.com'):
            messages.error(request, 'Please enter a valid Gmail address.')
            return render(request, 'usersignup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return render(request, 'usersignup.html')
        
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Generate a random 6-digit number for the confirmation code
        

        user = CustomUser.objects.create_user(
            first_name=fname,
            last_name=lname,
            username=uname,
            password= random_password, # Assign the randomly generated password
            email=email,
            user_type=user_type,
        )
        user.save()

        member = Usermember(
            address=address,
            c_number=number,
            user=user,
            profilepic=image,
            
        )
        member.save()

        # Sending confirmation email
    subject = 'Your Account Information'
    message = f'Hello {user.username},\n\nYour account has been created. Here are your login details:\n\nUsername: {user.username}\nPassword: {random_password}\n\nPlease log in using this temporary password and change it after logging in.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            


    return redirect('/')

    return render(request, 'usersignup.html')


def generate_random_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def send_email(subject, body, to_email):
    # Replace these with your email details
    from_email = "sumayyasalim810@gmail.com"
    password = "tmeq jibm ieku tevv"

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message.as_string())



def workercreate(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = f"{firstname}_{lastname}".lower()
        address = request.POST.get('address')
        email = request.POST.get('email')
        contactnumber = request.POST.get('contactnumber')
        selected_option_name = request.POST.get('sel')
        other_option_name = request.POST.get('new_category')
        experience = request.POST.get('experience')
        dob = request.POST.get('dob')
        id_type = request.POST.get('id_type')
        profile_picture = request.FILES.get('profile_picture')
        certificate = request.FILES.get('certificate')
        user_type = request.POST.get('text')

        # Perform form validation
        if not email:
            messages.error(request, 'Email is required.')
        elif not email.endswith('@gmail.com'):
            messages.error(request, 'Please enter a valid Gmail address.')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
        elif not contactnumber:
            messages.error(request, 'Contact number is required.')
        elif not contactnumber.isdigit() or len(contactnumber) != 10:
            messages.error(request, 'Contact number must be a 10-digit number.')
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'This username already exists.')

        # If there are any error messages, render the form again with errors
        if messages.get_messages(request):
            categories = Categories.objects.all() 
            return render(request, 'worker_signup.html', {'categories': categories})
            
        else:
            # All form validation passed, proceed with creating user and member instances
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
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
        
            with transaction.atomic():
                if selected_option_name == 'other':
                    option, created = Categories.objects.get_or_create(category_name=other_option_name)
                else:
                    option, created = Categories.objects.get_or_create(category_name=selected_option_name)

                option.created_by_type = '3'
                option.save()

                member = UserMember1.objects.create(
                    user=user,
                    a_ddress=address,
                    contactnumber=contactnumber,
                    experience=experience,
                    dob=dob,
                    categories=option,
                    id_type=id_type,
                    profile_picture=profile_picture,
                    certificate=pdf_filename,
                    status='1',
                )

                subject = 'Your Account Information'
                message = f'Hello {user.username},\n\nYour account has been created. Here are your login details:\n\nUsername: {user.username}\nPassword: {random_password}\n\nPlease log in using this temporary password and change it after logging in.'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'Thank you for registering. Please wait until your account is approved by the admin. You will receive login details via email after approval.')
            return redirect('worker_signup')  # Redirect to the signup page after successful registration

    else:
        categories = Categories.objects.all() 
        return render(request, 'worker_signup.html', {'categories': categories})
    

@receiver(post_save, sender=Categories)
def set_created_by_type(sender, instance, created, **kwargs):
    if created and instance.created_by:
        if instance.created_by.user_type == '3':  # If the category is created by a worker
            instance.created_by_type = '3'  # Set created_by_type to '3'
            instance.save()



        
def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        password1 = request.POST.get('password')
        print(f"Username: {user_name}, Password: {password1}")
        user = auth.authenticate(username=user_name, password=password1)

        if user is not None:
            # Check if the user is a worker and if the password matches the autogenerated one
            if user.user_type == '3' and check_password(password1, user.password):
                login(request, user)
                auth.login(request, user)
                print("Redirecting to worker_home")
                return redirect('worker_home')
            elif user.user_type == '1':
                login(request, user)
                auth.login(request,user)
                return redirect('admin_home')
            elif user.user_type == '2':
                login(request,user)
                auth.login(request,user)
                return redirect('user_home')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('loginpage')

    return render(request, 'loginpage.html')



def user_home(request):
    user_categories = UserMember1.objects.values('categories__category_name').distinct()
    return render(request, 'user_home.html', {'user_categories': user_categories})



def works_in_category(request, category_name):
    works_in_category = UserMember1.objects.filter(categories__category_name=category_name)
    return render(request, 'works_in_category.html', {'works_in_category': works_in_category})












def reset_user_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Password validation regex
        regex = (
            r'^(?=.*[0-9])'     # At least one digit
            r'(?=.*[a-z])'      # At least one lowercase letter
            r'(?=.*[A-Z])'      # At least one uppercase letter
            r'(?=.*[@#$%^&+=])'  # At least one special character
            r'(?=\S+$)'         # No whitespace allowed
            r'.{8,}'            # Minimum 8 characters
        )

        if len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
        elif not re.match(regex, new_password):
            messages.error(request, 'New password must contain at least one digit, one lowercase letter, one uppercase letter, one special character, and no whitespace.')
        elif new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
        elif not request.user.check_password(current_password):
            messages.error(request, 'Invalid current password.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password was successfully updated!')

    return render(request, 'reset_user_password.html')


def worker_list(request):
    workers = UserMember1.objects.all()
    return render(request, 'worker_list.html', {'workers': workers})

def worker_details(request, worker_id):
    worker = get_object_or_404(UserMember1, id=worker_id)
    return render(request, 'worker_details.html', {'worker': worker})



def add_catogoriesdb(request):
    if request.method == 'POST':
        categories_name = request.POST.get('category')
        
        catogory = Categories(category_name=categories_name)
        catogory.save()
        messages.success(request, 'Category added successfully.')
        return render(request, 'admin_add_categories.html')







    



def approve_worker(request, worker_id):
    # Get the worker object or return a 404 error if not found
    worker = get_object_or_404(UserMember1, id=worker_id)
    
    # Perform approval actions here, e.g., send email
    if worker.status == '1':  # Check if the worker is pending approval
        # Update approval status to 'Approved'
        worker.status = '2'
        worker.save()

        # Check if the worker's user is not None before accessing its username
        if worker.user:
            messages.success(request, f'Worker {worker.user.username} has been approved and notified via email.')
        else:
            messages.success(request, f'Worker with ID {worker_id} has been approved and notified via email.')
    else:
        messages.warning(request, f'Worker {worker_id} is not pending approval.')

    return redirect('worker_approval_table')


def disapprove_worker(request, worker_id):
    worker = get_object_or_404(UserMember1, id=worker_id)
    
    # Perform disapproval actions here, e.g., update approval status
    if worker.status == '1':  # Check if the worker is pending approval
        # Update approval status to 'Disapproved'
        worker.status = '3'
        worker.save()

    return redirect('worker_approval_table')



def categories_approval(request):
    categories_exist = Categories.objects.exists()
    latest_unapproved_category = Categories.objects.filter(status='1').order_by('-id').first()

    context = {'categories_exist': categories_exist}

    if latest_unapproved_category:
        context['latest_unapproved_category'] = latest_unapproved_category

    return render(request, 'categories_approval.html', context)


def worker_approval_table(request):
    workers = UserMember1.objects.filter(status='1')  # Assuming '1' means approved status
    catgy = Categories.objects.all()


    context = {'workers': workers,'catgy':catgy}
    return render(request, 'worker_approval_table.html', context)

       
def approve_category(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    category.status = '2'  # Assuming '2' represents approved status, adjust as needed
    category.save()
    messages.success(request, f"The category '{category.category_name}' has been approved.")

    return redirect('worker_approval_table') 




def notifications_redirect(request):
    latest_unapproved_category = Categories.objects.filter(status='1', created_by_type='3').order_by('-id').first()
    

    if latest_unapproved_category:  # Check if a new unapproved category exists
        return redirect('categories_approval')
    
    else:
        return redirect('worker_approval_table')  # Redirect to some other page if no new category or booking exists
    

    
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = '2'  # Set status to 'Approved'
    booking.save()
    return redirect('worker_approval_table')  # Redirect to a success page



def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    
    try:
        usermember = Usermember.objects.get(user=user)
    except Usermember.DoesNotExist:
        # If Usermember does not exist, you can handle it here
        usermember = None

    context = {
        'user': user,
        'usermember': usermember,
    }

    return render(request, 'user_profile.html', context)


def edit_user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        user_member = get_object_or_404(Usermember, user=user)

        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            uname = request.POST['uname']
            email = request.POST['email']
            address = request.POST['address']
            cnumber = request.POST['cnumber']
            profile_pic = request.FILES.get('file')

            # Check if the new username is unique
            if CustomUser.objects.exclude(pk=user.pk).filter(username=uname).exists():
                messages.error(request, 'Username is already taken.')
            # Check if the new email is unique
            elif CustomUser.objects.exclude(pk=user.pk).filter(email=email).exists():
                messages.error(request, 'Email is already in use.')
            # Check if the contact number is exactly 10 digits long
            elif len(cnumber) != 10 or not cnumber.isdigit():
                messages.error(request, 'Contact number must be 10 digits.')
            else:
                try:
                    # Validate email format
                    validate_email(email)
                except ValidationError:
                    messages.error(request, 'Invalid email format.')
                else:
                    if not email.endswith("@gmail.com"):
                        messages.error(request, 'Email must end with @gmail.com.')
                    else:
                        user.first_name = fname
                        user.last_name = lname
                        user.username = uname
                        user.email = email
                        user.save()

                        user_member.address = address
                        user_member.c_number = cnumber
                        if profile_pic:
                            user_member.profilepic = profile_pic
                        user_member.save()

                        messages.success(request, 'Your profile was successfully updated!')
        else:
            messages.error(request, 'Invalid request method.')

    else:
        messages.error(request, 'User is not authenticated.')

    return render(request, 'edit_user_profile.html', {'user': user, 'user_member': user_member})





def worker_profile(request, username):
    
 
    u_ser = get_object_or_404(CustomUser, username=username)
    
    try:
        user_member = UserMember1.objects.get(user=u_ser)
    except UserMember1.DoesNotExist:
        # If Usermember does not exist, you can handle it here
        user_member = None

    context = {
        'u_ser': u_ser,
        'user_member': user_member,
        'user': request.user 
        
    }

    return render(request, 'worker_profile.html', context)

def edit_worker_profile(request, user_id):
   
    user_member = get_object_or_404(UserMember1, user_id=user_id)
    categories = Categories.objects.all()

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        contact_number = request.POST.get('contactnumber')

        # Validate contact number
        if contact_number is not None and (len(contact_number) != 10 or not contact_number.isdigit()):
            messages.error(request, 'Contact number must be 10 digits.')
            return render(request, 'edit_worker_profile.html', {'user_member': user_member, 'categories': categories})

        # Validate username uniqueness
        if CustomUser.objects.filter(username=username).exclude(id=user_member.user.id).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'edit_worker_profile.html', {'user_member': user_member, 'categories': categories})
        if not email.endswith('@gmail.com'):
            messages.error(request, 'Please enter a valid Gmail address.')
            return render(request, 'edit_worker_profile.html', {'user_member': user_member, 'categories': categories})
        # Validate email uniqueness
        if CustomUser.objects.filter(email=email).exclude(id=user_member.user.id).exists():
            messages.error(request, 'Email address is already registered. Please use a different email.')
            return render(request, 'edit_worker_profile.html', {'user_member': user_member, 'categories': categories})

        user_member.user.username = username
        user_member.user.first_name, user_member.user.last_name = request.POST.get('name').split(' ', 1)
        user_member.user.email = email
        user_member.user.save()
        
        user_member.a_ddress = request.POST.get('address')
        user_member.contactnumber = contact_number

        user_member.experience = request.POST.get('experience')
        if 'profile_picture' in request.FILES:
            user_member.profile_picture = request.FILES['profile_picture']


        selected_option_name = request.POST.get('sel')
        other_option_name = request.POST.get('new_category')

        if selected_option_name == 'other':
            category, created = Categories.objects.get_or_create(category_name=other_option_name)
        else:
            category = get_object_or_404(Categories, category_name=selected_option_name)

        user_member.categories = category
        user_member.save()

        messages.success(request, 'Your profile has been successfully updated!')
        return redirect('worker_profile', username=request.user.username)
    

    context = {
        'user_member': user_member,
        'categories': categories,
        'user': request.user  # Assuming request.user contains the user object
    }

    return render(request, 'edit_worker_profile.html', context)


@login_required
def reset_worker_password(request, username):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = CustomUser.objects.get(username=username)

                # Check if the current password entered matches the user's actual password
        if not check_password(current_password, user.password):
            messages.error(request, 'Incorrect current password.')
            return render(request, 'reset_worker_password.html', {'username': username})

        # Validate that the new password and confirm new password match
        if new_password != confirm_new_password:
            messages.error(request, 'New password and confirm new password do not match.')
            return render(request, 'reset_worker_password.html', {'username': username})

        # Validate new password complexity
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_=+{};:,<.>]).{8,}$', new_password):
            messages.error(request, 'Password must contain at least one digit, one lowercase letter, one uppercase letter, one special character, and be at least 8 characters long.')
            return render(request, 'reset_worker_password.html', {'username': username})


        # Update the user's password with the new password
        user.set_password(new_password)
        user.save()

        # Authenticate the user with the new password and log in
        updated_user = authenticate(username=username, password=new_password)
        if updated_user is not None:
            login(request, updated_user)

        messages.success(request, 'Password has been successfully reset.')
        return redirect('reset_worker_password', username=username)
    else:
        return render(request, 'reset_worker_password.html', {'username': username})


def add_service(request):
    categories = Categories.objects.all()
    error_message = ""

    if request.method == 'POST':
        categories_id = request.POST.get('categories')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        image = request.FILES.get('image')

        if categories_id and title and price and duration:
            try:
                categories_obj = Categories.objects.get(pk=categories_id)
                price = float(price)

                service = Service.objects.create(
                    added_by=request.user, 
                    categories=categories_obj,
                    title=title,
                    description=description,
                    price=price,
                    duration=duration,
                    status='1',
                    image=image
                )
                messages.success(request, 'Service added successfully.')
                return redirect('add_service')
            except Categories.DoesNotExist:
                error_message = "Selected category does not exist"
        else:
            error_message = "All fields are required"
    
    return render(request, 'add_service.html', {'error_message': error_message, 'categories': categories})

def myservice(request):
    # Retrieve services added by the current worker
    my_services = Service.objects.filter(added_by=request.user)

   

    return render(request, 'myservice.html', {'my_services': my_services})


def delete(request,pk):
   p=Service.objects.get(id=pk)
   p.delete()
   return redirect('myservice')



def works_in_category(request, category_name):
    category = get_object_or_404(Categories, category_name=category_name)
    services_in_category = Service.objects.filter(categories=category)
    return render(request, 'services_in_category.html', {'category': category, 'services': services_in_category})





def book_service(request, service_id):
    if request.user.is_authenticated:
        current_user = request.user

        service = Service.objects.get(pk=service_id)
        user = request.user
        worker = service.added_by

        usermember = Usermember.objects.get(user=current_user)
        booking = Booking.objects.create(user=usermember, service=service,worker=worker)

        # Set the status of the created booking
        booking.status = '1'  # or any other status
        booking.save()
        
        messages.success(request, f"The service  has been successfully booked.")
        return redirect('user_home')  # Redirect to a success page
   






def all_bookings(request):
    # Fetch all bookings with related service and user info
    bookings = Booking.objects.select_related('service', 'user__user').all()

    # Pass the data to the template for rendering
    return render(request, 'all_bookings.html', {'bookings': bookings})


def admin_home(request):
    pending_count = Booking.objects.count()
    approved_count = Booking.objects.filter(status='2').count()
    rejected_count = Booking.objects.filter(status='3').count()
    unapp_worker_count=UserMember1.objects.filter(status='1').count()
    worker_count =UserMember1.objects.filter(status='2').count()
    customer_count = Usermember.objects.filter(status='1').count()
    print("Pending Count:", pending_count)

    
    return render(request, 'admin_home.html', {
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'worker_count': worker_count,
        'customer_count': customer_count,
        'unapp_worker_count': unapp_worker_count

    })




def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.status = '2'  # Assuming '2' represents 'Approved' status
    booking.save()
    return redirect('worker_home')  # Redirect to the admin's home page after approval

def disapprove_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.status == '1':  # Check if the booking is pending approval
        # Update approval status to 'Disapproved'
        booking.status = '3'
        booking.save()
    return redirect('worker_home') 




def admin_worker_list(request, username):
    u_ser = get_object_or_404(CustomUser, username=username)
    
    try:
        user_member = UserMember1.objects.get(user=u_ser)
    except UserMember1.DoesNotExist:
        user_member = None

    # Assuming you have a queryset of workers that you want to display
    workers = UserMember1.objects.all()  # Change this queryset according to your requirements

    context = {
        'u_ser': u_ser,
        'user_member': user_member,
        'user': request.user,
        'workers': workers,  # Pass the workers queryset to the template
    }
    return render(request, 'admin_worker_list.html', context)


def delete_worker(request, worker_id):
    # Retrieve the worker object
    worker = get_object_or_404(UserMember1, id=worker_id)
    
    if request.method == 'POST':
        # Delete the worker
        worker.delete()
        messages.success(request, f'worker has been deleted successfully.')
        return redirect(reverse('admin_worker_list', args=[request.user.username]))
    


def admin_customer_list(request):
    workers = Usermember.objects.select_related('user').all()  # Fetch all Usermembers with associated CustomUser
    return render(request, 'admin_customer_list.html', {'workers': workers})


def delete_customer(request, customer_id):
    if request.method == 'POST':
        try:
            worker = Usermember.objects.get(id=customer_id)
            worker.delete()
        except Usermember.DoesNotExist:
            raise Http404("Usermember with ID {} does not exist.".format(customer_id))
        
    return redirect('admin_customer_list')




def booking_approval_table(request):
    user = request.user
    bookings = Booking.objects.filter(service__added_by=user)
    
    context = {'bookings': bookings}
    return render(request, 'booking_approval_table.html', context)





def mark_compleated(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.task_compleated = '2'  # Assuming '2' represents 'Approved' status
    booking.save()
    messages.success(request, 'Task completed successfully.')
    return redirect('booking_approval_table')  # Redirect to the worker's home page


def my_orders(request):
    if request.user.is_authenticated:
        # Fetch the Usermember instance corresponding to the current user
        user_member = Usermember.objects.get(user=request.user)
        
        # Filter bookings for the current user using the Usermember instance
        bookings = Booking.objects.filter(user=user_member, task_compleated='2')

        context = {'bookings': bookings}
        return render(request, 'my_orders.html', context)
    

    
def my_orders_updations(request):
    if request.user.is_authenticated:
        # Fetch the Usermember instance corresponding to the current user
        user_member = Usermember.objects.get(user=request.user)
        
        # Filter bookings for the current user using the Usermember instance
        bookings = Booking.objects.filter(user=user_member)

        context = {'bookings': bookings}
        return render(request, 'my_orders_updations.html', context)




def review_form(request, booking_id):
   if request.user.is_authenticated:
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Service, pk=service_id)
        
        # Create a new review object
        review = Review.objects.create(
            rating=rating,
            comments=comments,
            bookings=service.booking_set.first()  # Assuming one service can have multiple bookings
        )
        review.save()
        
        messages.success(request, 'Thank you for your review!')
        return render(request, 'review_form.html', {'thank_you_message': 'Thank you for your review!'})
    else:
        # Fetch the service associated with the booking
        booking = get_object_or_404(Booking, pk=booking_id)
        service = booking.service
        
        context = {
            'service': service,
            'reviews': Review.objects.filter(bookings=booking)
        }

        return render(request, 'review_form.html', context)


def review_list(request):
    if not request.user.is_authenticated:
        return HttpResponse("You need to be logged in to view this page.")

    # Fetching services added by the logged-in user
    user_services = Service.objects.filter(added_by=request.user)

    # Fetching reviews related to services added by the logged-in user
    reviews = Review.objects.select_related('bookings__user', 'bookings__service').filter(bookings__service__in=user_services)

    print("Reviews count:", reviews.count())  # Debugging: Print number of reviews fetched
    for review in reviews:
        print("Review ID:", review.id)  # Debugging: Print review ID
        if review.bookings:
            print("Booking ID:", review.bookings.id)  # Debugging: Print booking ID associated with the review
            if review.bookings.user:
                print("User ID:", review.bookings.user.id)  # Debugging: Print user ID associated with the booking
                print("Username:", review.bookings.user.user.username)  # Debugging: Print username associated with the booking

    return render(request, 'review_list.html', {'reviews': reviews})


def worker_search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        workers = UserMember1.objects.filter(user__first_name__icontains=query)
    else:
        workers = UserMember1.objects.all()
    return render(request, 'worker_search.html', {'workers': workers})

def worker_services(request, worker_id):
    worker = UserMember1.objects.get(pk=worker_id)
    completed_bookings = Booking.objects.filter(worker=worker.user, task_compleated='2')
    return render(request, 'worker_services.html', {'worker': worker, 'completed_bookings': completed_bookings})

def admin_service_serch(request):
    categories = Categories.objects.all()  # Fetch all categories
    selected_category = None
    services = Service.objects.all()
    if 'category' in request.GET:  # Check if a category is selected
        category_id = request.GET['category']
        if category_id:  # If category is selected
            selected_category = Categories.objects.get(pk=category_id)
            services = selected_category.service_set.all()

    return render(request, 'admin_service_serch.html', {'categories': categories, 'selected_category': selected_category, 'services': services})

       
 

def service_reviews(request, service_id):
    # Retrieve the service object
    service = Service.objects.get(id=service_id)
    
    # Retrieve reviews associated with bookings for this service
    reviews = Review.objects.filter(bookings__service=service)
    
    
    # Pass the service and reviews to the template for rendering
    return render(request, 'service_reviews.html', {'service': service, 'reviews': reviews,})





def index(request):
    # Retrieve all service objects from the database
    services = Service.objects.all()
    # Pass the services to the template context
    return render(request, 'index.html', {'services': services})





def admin_category_list(request):
    categories = Categories.objects.all()
    return render(request, 'admin_category_list.html', {'categories': categories})



def user_logout(request):
    logout(request)
    return redirect('loginpage')


def worker_logout(request):
    logout(request)
    return redirect('loginpage')

def admin_logout(request):
    logout(request)
    return redirect('loginpage')