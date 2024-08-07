from django.shortcuts import render,redirect , get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from jobportalapp.models import Usermember,CustomUser,Employee,Job_details,Job,Profile,JobApplication
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User,auth
from django.contrib import messages
import secrets,os
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str 
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import FileSystemStorage
import json
import re
from django.db.models import Count
from django.contrib.auth.hashers import make_password
from django.urls import reverse


# Create your views here.
def index3(request):
    return render(request,'index3.html')
def loginform(request):
    return render(request,'loginform.html')
def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.user_type == '1':
                auth.login(request, user)
                return redirect('adminhome')
            elif user.user_type == '2':
                auth.login(request, user)
                try:
                    employer = Employee.objects.get(user=user)
                    request.session['employer_id'] = employer.id  # Store employer ID in session
                    # messages.info(request, f'Welcome {username}')
                    return redirect('employeer_home')
                except Employee.DoesNotExist:
                    messages.error(request, 'Employer profile not found.')
                    return redirect('loginform')
            else:
                auth.login(request, user)
                #messages.info(request, f'Welcome {username}')
                return redirect('seeker_home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('loginform')
    else:
        return redirect('loginform')
def employeesignup(request):
    return render(request,'employeesignup.html')
def seeker_signup(request):
    return render(request,'seeker_signup.html')
def add_user(request):
    if request.method == 'POST':
         user_name = request.POST['username']
         firstname = request.POST['firstname']
         lastname = request.POST['lastname']
         email = request.POST['email']
         user_type = request.POST['text']
         mobile = request.POST['mobile1']
         dob = request.POST['dob']
        
         # Mobile number validation
         if not re.match(r'^[0-9]{10}$', mobile):
            messages.error(request, "Mobile number must be 10 digits.")
            return render(request, 'seeker_signup.html', {
                'username': user_name, 'email': email, 'text': user_type ,
                'first_name':firstname, 'last_name':lastname, 'mobile':mobile,
                'dob':dob
            })
         if not re.match(r'^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$', email):
                messages.error(request, "Please enter a valid email address.")
                return render(request, 'seeker_signup.html', {
                    'username': user_name, 'email': email, 'text': user_type ,
                    'first_name':firstname, 'last_name':lastname, 'mobile':mobile,
                    'dob':dob
            })
          # Check if username or email already exists
         if CustomUser.objects.filter(username=user_name).exists():
            messages.error(request, "This username already exists.")
            return render(request, 'seeker_signup.html', {
                'username': user_name, 'email': email, 'text': user_type, 
                 'first_name':firstname, 'last_name':lastname, 'mobile':mobile,
                'dob':dob
            })
         elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "This email already exists.")
            return render(request, 'seeker_signup.html', {
                'username': user_name, 'email': email, 'text': user_type ,
                'first_name':firstname, 'last_name':lastname, 'mobile':mobile,
                'dob':dob
               
            })

        # Create the CustomUser instance
         user = CustomUser.objects.create_user(username=user_name,first_name=firstname,last_name=lastname, email=email, user_type=user_type)
         user.save()
         member = Usermember(
                mobile=mobile,
                dob=dob,
                user=user
            )
         member.save()
            
            # Add a success message
         messages.success(request, "Your submission was successful! Wait for admin approval, thank you.")
         return redirect('seeker_signup')
            
    return render(request, 'seeker_signup.html')
# def add_user(request):
    
#     if request.method == 'POST':
#         user_name = request.POST['username']
#         email = request.POST['email']
#         user_type = request.POST['text']
#         companyname = request.POST['companyname']
#         mobile = request.POST['mobile1']
#         logo = request.FILES.get('logo')
#         website = request.POST['website']
#         address = request.POST['address']

#         # Mobile number validation
#         if not re.match(r'^[0-9]{10}$', mobile):
#             messages.error(request, "Mobile number must be 10 digits.")
#             return redirect('employeesignup')

#         # Logo validation
#         if not logo:
#             messages.error(request, "Please upload your company logo.")
#             return redirect('employeesignup')

#         # Website validation
#         if not re.match(r'^https?:\/\/[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+([/?].*)?$', website):
#             messages.error(request, "Please enter a valid URL.")
#             return redirect('employeesignup')

#         # Address validation
#         if len(address) < 10:
#             messages.error(request, "Address must be at least 10 characters long.")
#             return redirect('employeesignup')

#         # Email validation (must be valid and end with .com)
#         if not re.match(r'^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+\.com$', email):
#             messages.error(request, "Please enter a valid email address ending with .com.")
#             return redirect('employeesignup')

#         # Check if username or email already exists
#         if CustomUser.objects.filter(username=user_name).exists():
#             messages.error(request, "This username already exists.")
#             return redirect('employeesignup')
#         elif CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "This email already exists.")
#             return redirect('employeesignup')

#         # Create the CustomUser instance
#         user = CustomUser.objects.create_user(username=user_name, email=email, user_type=user_type)
#         user.save()

#         # Create the Employee instance
#         member = Employee(
#             companyname=companyname,
#             mobile=mobile,
#             logo=logo,
#             website=website,
#             address=address,
#             user=user
#         )
#         member.save()
#         return redirect('employeesignup')
#     return render(request, 'employeesignup.html')


def add_employee(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        email = request.POST['email']
        user_type = request.POST['text']
        companyname = request.POST['companyname']
        mobile = request.POST['mobile1']
        logo = request.FILES.get('logo')
        website = request.POST['website']
        address = request.POST['address']

        # Mobile number validation
        if not re.match(r'^[0-9]{10}$', mobile):
            messages.error(request, "Mobile number must be 10 digits.")
            return render(request, 'employeesignup.html', {
                'username': user_name, 'email': email, 'text': user_type, 
                'companyname': companyname, 'mobile1': mobile, 
                'website': website, 'address': address
            })

        # Logo validation
        if not logo:
            messages.error(request, "Please upload your company logo.")
            return render(request, 'employeesignup.html', {
                'username': user_name, 'email': email, 'text': user_type, 
                'companyname': companyname, 'mobile1': mobile, 
                'website': website, 'address': address
            })

        # Website validation
        if not re.match(r'^https?:\/\/[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+([/?].*)?$', website):
            messages.error(request, "Please enter a valid URL.")
            return render(request, 'employeesignup.html', {
                'username': user_name, 'email': email, 'text': user_type, 
                'companyname': companyname, 'mobile1': mobile, 
                'website': website, 'address': address
            })

        # Address validation
        if len(address) < 10:
            messages.error(request, "Address must be at least 10 characters long.")
            return render(request, 'employeesignup.html', {
                'username': user_name, 'email': email, 'text': user_type, 
                'companyname': companyname, 'mobile1': mobile, 
                'website': website, 'address': address
            })

        # Email validation (must be valid and end with .com)
        if not re.match(r'^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$', email):
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'employeesignup.html', {
                'username': user_name, 'email': email, 'text': user_type, 
                'companyname': companyname, 'mobile1': mobile, 
                'website': website, 'address': address
        })

        # Check if username or email already exists
        if CustomUser.objects.filter(username=user_name).exists():
            messages.error(request, "This username already exists.")
            return render(request, 'employeesignup.html', {
                'username': user_name, 'email': email, 'text': user_type, 
                'companyname': companyname, 'mobile1': mobile, 
                'website': website, 'address': address
            })
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "This email already exists.")
            return render(request, 'employeesignup.html', {
                'username': user_name, 'email': email, 'text': user_type, 
                'companyname': companyname, 'mobile1': mobile, 
                'website': website, 'address': address
            })

        # Create the CustomUser instance
        user = CustomUser.objects.create_user(username=user_name, email=email, user_type=user_type)
        user.save()

        # Create the Employee instance
        member = Employee(
            companyname=companyname,
            mobile=mobile,
            logo=logo,
            website=website,
            address=address,
            user=user
        )
        member.save()
        
        # Add a success message
        messages.success(request, "Your submission was successful! Wait for admin approval, thank you.")
        return redirect('employeesignup')
        
    return render(request, 'employeesignup.html')

def show_employee(request):
    employees = Employee.objects.all()
    user=Usermember.objects.all()
    pending_users_count = Usermember.objects.filter(is_approved=False).count()
    pending_employers_count = Employee.objects.filter(is_approved=False).count()
    pending_job_count = Job_details.objects.filter(is_approved=False).count()
    total_pending_count = pending_users_count + pending_employers_count
    return render(request, 'show_employee.html', {'employee': employees,'user': user,'total_pending_count': total_pending_count,'pending_job_count':pending_job_count})
def show_jobseeker(request):
    user=Usermember.objects.all()
    pending_users_count = Usermember.objects.filter(is_approved=False).count()
    pending_employers_count = Employee.objects.filter(is_approved=False).count()
    pending_job_count = Job_details.objects.filter(is_approved=False).count()
    total_pending_count = pending_users_count + pending_employers_count
    return render(request, 'show_jobseeker.html', {'user': user,'total_pending_count': total_pending_count,'pending_job_count':pending_job_count})
def adminhome(request):
    pending_users_count = Usermember.objects.filter(is_approved=False).count()
    pending_employers_count = Employee.objects.filter(is_approved=False).count()
    pending_job_count = Job_details.objects.filter(is_approved=False).count()
    total_pending_count = pending_users_count + pending_employers_count
    return render(request, 'adminhome.html', {'total_pending_count': total_pending_count,'pending_job_count':pending_job_count})
def seeker_home(request):
    jobs = Job.objects.all()
    job_titles = Job.objects.values_list('job_title', flat=True).distinct()
    locations = Job.objects.values_list('location', flat=True).distinct()
    job_types = Job.objects.values_list('job_type', flat=True).distinct()
    return render(request, 'seeker_home.html', {
        'jobs': jobs,
        'job_titles': job_titles,
        'locations': locations,
        'job_types': job_types,
          
    })

def search_jobs(request):
    job_title = request.GET.get('job_title', '')
    location = request.GET.get('location', '')
    posting_date = request.GET.get('posting_date', '')
    job_type = request.GET.get('job_type', '')

    jobs = Job.objects.all()

    if job_title:
        jobs = jobs.filter(job_title=job_title)
    if location:
        jobs = jobs.filter(location=location)
    if posting_date:
        jobs = jobs.filter(posted_on=posting_date)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    jobs = jobs.order_by('-posted_on')
    jobs = jobs.values('id', 'job_title', 'companyname', 'job_des', 'job_exp', 'job_salary', 'location', 'posted_on', 'job_type', 'job_file')
    return JsonResponse(list(jobs), safe=False)
def employeer_home(request):
     # Assume the employer's ID is stored in the session
    employer_id = request.session.get('employer_id')
    if not employer_id:
        return HttpResponse("Unauthorized", status=401)

    employer = get_object_or_404(Employee, id=employer_id)
    # jobs = Job.objects.filter(user=employer)
    # applications = JobApplication.objects.filter(job__in=jobs)
    applications = JobApplication.objects.filter(job__companyname=employer.companyname)
    # pending_applications_count = applications.filter(is_accepted=False, is_rejected=False).count()
    return render(request, 'employeer_home.html', {'applications': applications})

def admin_approve(request):
    if request.method == 'POST':
        if 'approve_user' in request.POST:
            user_id = request.POST.get('approve_user')
            user_registration = Usermember.objects.get(id=user_id)
            user = user_registration.user
            
            # Generate a random password
            password = f"{secrets.randbelow(1000000):06d}"
            user.password = make_password(password)
            user.save()
            
            # Send email with the password
            send_mail(
                'Registration Approved',
                f'Hi {user.username},\n Your registration is approved. Your password is {password}',
                'jyotsnasabu08@gmail.com',
                [user.email],
                fail_silently=False,
            )
            
            user_registration.is_approved = True
            user_registration.save()
        
        elif 'approve_employer' in request.POST:
            employer_id = request.POST.get('approve_employer')
            employer_registration = Employee.objects.get(id=employer_id)
            employer = employer_registration.user
            
            # Generate a random password
            password = f"{secrets.randbelow(1000000):06d}"
            employer.password = make_password(password)
            employer.save()
            
            # Send email with the password
            send_mail(
                'Registration Approved',
                f'Hi {employer.username},\n Your registration is approved. Your password is {password}',
                'jyotsnasabu08@gmail.com',
                [employer.email],
                fail_silently=False,
            )
            
            employer_registration.is_approved = True
            employer_registration.save()

        elif 'disapprove_user' in request.POST:
            user_id = request.POST.get('disapprove_user')
            user_registration = Usermember.objects.get(id=user_id)
            user = user_registration.user
            user_registration.delete()
            user.delete()
            

        elif 'disapprove_employer' in request.POST:
            employer_id = request.POST.get('disapprove_employer')
            employer_registration = Employee.objects.get(id=employer_id)
            employer = employer_registration.user
            employer_registration.delete()
            employer.delete()
           

    users = Usermember.objects.filter(is_approved=False)
    employers = Employee.objects.filter(is_approved=False)
    return render(request, 'admin_approve.html', {'users': users, 'employers': employers})
def emp_view_profile(request):
    user=request.user.id
    employee=Employee.objects.get(user_id=user)
    return render(request,"emp_view_profile.html",{'emp':employee})
def emp_edit_profilepage(request,pk):
    employee=Employee.objects.get(id=pk)

    return render(request,"emp_edit_profile.html",{'emp':employee})
def emp_edit_profile(request):
     return render(request, 'edit_profile.html')

@login_required
def emp_editprofile(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    print(f"Employer PK: {emp.pk}, User ID: {emp.user.id}")  # Debugging line

    if request.method == 'POST':
        # Validate username
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        mobile = request.POST.get('mobile1')
        
        # Validation checks
        if not new_username.isalnum():
            messages.error(request, "Username should be alphanumeric.")
            return render(request, 'emp_edit_profile.html', {'emp': emp})
        elif CustomUser.objects.filter(username=new_username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'emp_edit_profile.html', {'emp': emp})
        elif CustomUser.objects.filter(email=new_email).exists():
            messages.error(request, "Email is already taken.")
            return render(request, 'emp_edit_profile.html', {'emp': emp})
        elif not re.match(r'^[0-9]{10}$', mobile):
            messages.error(request, "Mobile number must be 10 digits.")
            return render(request, 'emp_edit_profile.html', {'emp': emp})
        elif not re.match(r'^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$', new_email):
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'emp_edit_profile.html', {'emp': emp})

        # If all validations pass, update the employee data
        emp.companyname = request.POST.get('companyname')
        emp.user.username = new_username
        emp.user.first_name = request.POST.get('firstname')
        emp.user.last_name = request.POST.get('lastname')
        emp.user.email = new_email
        emp.mobile = mobile
        emp.address = request.POST.get('address')
        emp.website = request.POST.get('website')

        # Handling logo upload
        if 'logo' in request.FILES:
            try:
                if emp.logo:
                    os.remove(emp.logo.path)  # Remove existing logo
                    print("Existing image removed successfully")
            except Exception as e:
                print("Error removing existing image:", e)

            emp.logo = request.FILES['logo']

        emp.user.save()  # Save the related user instance
        emp.save()  # Save the employer instance with the new data

    return render(request, 'emp_edit_profile.html', {'emp': emp})


@login_required
def password_reset_form(request):
    return render(request, 'password_reset_form.html')
def admin_password_change(request):
    return render(request, 'admin_password_change.html')
@login_required
@require_POST
@csrf_exempt    
def update_password(request):
    try:
        data = json.loads(request.body)
        new_password = data.get('new_password')
        if not new_password:
            return JsonResponse({'success': False, 'error': 'New password not provided.'}, status=400)

        user = request.user
        user.set_password(new_password)
        user.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
def jobs(request):
    return render(request, 'jobs.html')
def add_job(request):
    job_title=request.POST['jobTitle']
    company_name=request.POST['companyName']
    location=request.POST['location']
    job_schedule = request.POST.get('jobSchedule')
    job_type = request.POST.get('jobType')
    description = request.POST.get('description')
    job_exp = request.POST.get('jobexp')
    salary = request.POST.get('salary')
    file = request.FILES.get('file')
    posted_on = request.POST.get('posted_on')
    user_id = request.POST.get('userId')
    
    job = Job_details(
        job_title=job_title,
        companyname=company_name,
        location=location,
        job_schedule=job_schedule,
        job_type=job_type,
        job_des=description,
        job_exp=job_exp,
        job_salary=salary,
        job_file=file,
        posted_on=posted_on,
        user_id=user_id,
        
    )
    job.save()
    return redirect('jobs')


def job_list(request):
    jobs = Job_details.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})


def approve_job(request, job_id):
    job_detail = get_object_or_404(Job_details, id=job_id)
    approved_job = Job(job_title=job_detail.job_title,
        companyname=job_detail.companyname,
        location=job_detail.location,
        job_schedule=job_detail.job_schedule,
        job_type=job_detail.job_type,
        job_des=job_detail.job_des,
        job_exp=job_detail.job_exp,
        job_salary=job_detail.job_salary,
        job_file=job_detail.job_file,
        posted_on=job_detail.posted_on,
        user_id=job_detail.user_id
        )
    approved_job.save()
    job_detail.delete()
    return redirect('job_list')

# Admin view to disapprove a job

def disapprove_job(request, job_id):
    job_detail = get_object_or_404(Job_details, id=job_id)
    job_detail.delete()
    return redirect('job_list')
def view_jobs(request):
    job=Job.objects.all()
    pending_users_count = Usermember.objects.filter(is_approved=False).count()
    pending_employers_count = Employee.objects.filter(is_approved=False).count()
    pending_job_count = Job_details.objects.filter(is_approved=False).count()
    total_pending_count = pending_users_count + pending_employers_count
    return render(request,'view_jobs.html',{'job':job,'total_pending_count': total_pending_count,'pending_job_count':pending_job_count}) 
def check_profile_complete(request):
    user = request.user
    profile_complete = False
    if user.is_authenticated:
        profile = user.profile
        # Check if profile is complete
        if profile.address and profile.user_img and profile.resume:  # Add other necessary fields
            profile_complete = True
    return JsonResponse({'profile_complete': profile_complete})  
@login_required
def apply_for_job(request):
    job_id = request.POST.get('job_id')
    job = get_object_or_404(Job, id=job_id)
    user = request.user
    if not request.user.profile.is_complete:
        return JsonResponse({'message': 'Please complete your profile before applying.'}, status=400)
    try:
        profile = user.profile
        if not (profile.name and profile.email and profile.resume):
            return JsonResponse({'profile_complete': False})
    except Profile.DoesNotExist:
        return JsonResponse({'profile_complete': False})

    application, created = JobApplication.objects.get_or_create(user=user, job=job)
    return JsonResponse({'profile_complete': True, 'application_created': created})


@login_required
def accept_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    application.is_accepted = True
    application.save()
    application.send_acceptance_email()
    return HttpResponse('Application accepted and email sent.')


@csrf_exempt
def reject_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    application.is_rejected = True
    application.save()
    return HttpResponse('Application rejected.')


import logging
from django.shortcuts import render, get_object_or_404
from .models import Job, JobApplication

logger = logging.getLogger(__name__)

@login_required

def emp_application(request):
    employer = request.user  
    jobs = Job.objects.filter(user=employer)
    applications = JobApplication.objects.filter(job__in=jobs)
    total_applications_count = applications.count()
    pending_applications_count = applications.filter(is_accepted=False, is_rejected=False).count()

    context = {
        'applications': applications,
        'total_applications_count': total_applications_count,
        'pending_applications_count': pending_applications_count
    }
    return render(request, 'emp_application.html', context)

def user_profile(request):
    try:
        usermember = Usermember.objects.get(user=request.user)
    except ObjectDoesNotExist:  # type: ignore
        # Handle the case where the Usermember does not exist
        usermember = Usermember.objects.create(user=request.user)
        
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update Usermember fields
        usermember.user.first_name = request.POST.get('firstname', usermember.user.first_name)
        usermember.user.last_name = request.POST.get('lastname', usermember.user.last_name)
        usermember.user.username = request.POST.get('user_name', usermember.user.username)
        usermember.user.email = request.POST.get('email', usermember.user.email)
        usermember.mobile = request.POST.get('mobile1', usermember.mobile)
        usermember.dob = request.POST.get('dob', usermember.dob)
        
        # Update Profile fields
        profile.address = request.POST.get('address', profile.address)
        profile.qualification = request.POST.get('qualification', profile.qualification)
        profile.job_des = request.POST.get('description', profile.job_des)
        profile.exp = request.POST.get('jobexp', profile.exp)
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']
        if 'profileimage' in request.FILES:
            profile.user_img = request.FILES['profileimage']

        # Get the submitted email and mobile number for validation
        email = request.POST.get('email')
        mobile = request.POST.get('mobile1')

        # Validate mobile number
        if not re.match(r'^[0-9]{10}$', mobile):
            messages.error(request, "Mobile number must be 10 digits.")
            return render(request, 'user_profile.html', {'usermember': usermember, 'profile': profile})
        
        # Validate email format
        if not re.match(r'^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$', email):
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'user_profile.html', {'usermember': usermember, 'profile': profile})
        
        # Check for existing username
        username = request.POST.get('user_name')
        if CustomUser.objects.filter(username=username).exists() and username != request.user.username:
            messages.error(request, "This username already exists.")
            return render(request, 'user_profile.html', {'usermember': usermember, 'profile': profile})

        # Check for existing email
        if CustomUser.objects.filter(email=email).exists() and email != request.user.email:
            messages.error(request, "This email already exists.")
            return render(request, 'user_profile.html', {'usermember': usermember, 'profile': profile})
        
        # Save changes if validation passes
        usermember.user.save()
        usermember.save()
        profile.save()

        return redirect('user_profile')

    context = {
        'usermember': usermember,
        'profile': profile
    }
    
    return render(request, 'user_profile.html', context)
      

def about(request):
    return render(request,'about.html')

def logout(request):
    auth.logout(request)
    return redirect('index3')

@login_required
@csrf_exempt
def apply_for_jobs(request, job_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            user = request.user
            job = Job.objects.get(id=job_id)
            
            # Check if the user has completed their profile
            if not user.profile.is_profile_complete():
                return JsonResponse({'success': False, 'message': 'Please complete your profile before applying.'}, status=400)
            
            job_application = JobApplication.objects.create(
                user=user,
                job=job,
                is_accepted=False,
                is_rejected=False
            )
            
            return JsonResponse({'success': True, 'message': 'Application successful.'})
        
        except Job.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Job not found.'}, status=404)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method or not AJAX.'}, status=400)



@login_required
def seeker_applied_job(request):
    applications = JobApplication.objects.filter(user=request.user)
    context = {
        'applications': applications
    }
    return render(request, 'seeker_applied_job.html', context)

def download_resume(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    application.resume_viewed = True
    application.save()
    resume_url = application.user.profile.resume.url
    return redirect(resume_url)
@csrf_exempt
def verify_employee(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=employee_id)
        employee.is_verified = True
        employee.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
@csrf_exempt
def delete_employee(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=employee_id)
        user = employee.user  # Save reference to the related user
        employee.delete()     # Delete the employee
        user.delete()         # Delete the related user
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
@csrf_exempt
def verify_user(request, user_id):
    if request.method == 'POST':
        user = Usermember.objects.get(id=user_id)
        user.is_verified = True
        user.save()
        return JsonResponse
@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'POST':
        user_member = get_object_or_404(Usermember, id=user_id)
        user = user_member.user  # Reference to the related user
        user_member.delete()     # Delete the Usermember instance
        user.delete()            # Delete the related User instance
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
    
 

def show_user(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    profile = get_object_or_404(Profile, user=application.user)
    
    if not application.profile_visited:
        application.profile_visited = True
        application.save()

    usermember = Usermember.objects.filter(user=application.user).first()
    
    return render(request, "show_user.html", {
        'application': application,
        'profile': profile,
        'usermember': usermember,
    })


@login_required
def job_list_view(request):
    jobs = Job.objects.filter(user=request.user)
    context = {
        'jobs': jobs
    }
    return render(request, 'employer_jobs_list.html', context)

@login_required
def job_edit_view(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == 'POST':
        # Update job details
        job.job_title = request.POST.get('job_title')
        job.companyname = request.POST.get('companyName')
        job.location = request.POST.get('location')
        job.job_schedule = request.POST.get('job_schedule')
        job.job_type = request.POST.get('job_type')
        job.job_des= request.POST.get('description')
        job.job_exp = request.POST.get('jobexp')
        job.job_salary = request.POST.get('salary')
        job.posted_on = request.POST.get('posted_on')
        job.save()
        return redirect('employer_jobs_list')

    context = {
        'job': job
    }
    return render(request, 'employer_job_edit.html', context)
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('view_jobs') 
def admin_jobs(request):
    jobs = Job.objects.annotate(applicant_count=Count('jobapplication'))
    applications =JobApplication.objects.all()

    context = {
        'jobs': jobs,
        'applications': applications
    }
    
    return render(request, 'admin_jobs.html', context)
@login_required  # Ensure the user is authenticated to view this page
def admin_profile(request, pk):
    User = get_user_model() 
    admin_user = get_object_or_404(User, pk=pk)
    return render(request, 'admin_profile.html',{'admin_user':admin_user})
def edit_admin_page(request,pk):
    user=CustomUser.objects.get(id=pk)
    
    return render(request,"edit_admin.html",{'user':user})
def edit_admin(request):
     return render(request, 'edit_admin.html')
@login_required


def editadmin(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    
    if request.method == 'POST':
        user_name = request.POST['username']
        email = request.POST['email']
        
        if CustomUser.objects.filter(username=user_name).exclude(id=pk).exists():
            messages.info(request, 'This username already exists')
            return redirect('edit_admin', pk=pk)
        else:
            # Update the CustomUser instance
            user.username = user_name
            user.email = email
            user.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('edit_admin')
    
    return render(request, 'edit_admin.html', {'user': user})