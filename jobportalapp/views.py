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
                    messages.info(request, f'Welcome {username}')
                    return redirect('employeer_home')
                except Employee.DoesNotExist:
                    messages.error(request, 'Employer profile not found.')
                    return redirect('loginform')
            else:
                auth.login(request, user)
                messages.info(request, f'Welcome {username}')
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
    username=request.POST['user_name']
    useremail=request.POST['email']
    usermobile=request.POST['mobile1']
    userdob=request.POST['dob']
    user1=Usermember(name=username,email=useremail,mobile=usermobile,dob=userdob)
    user1.save()
    return redirect('/')
def add_user(request):
    if request.method == 'POST':
        first_name=request.POST['firstname']
        user_name=request.POST['user_name']
        last_name=request.POST['lastname']
        email=request.POST['email']
        user_type=request.POST['text']
        if CustomUser.objects.filter(username=user_name).exists():
            messages.info(request,'This username already exists')
            return redirect('seeker_signup')
        else:
            user=CustomUser.objects.create_user(first_name=first_name,username=user_name,last_name=last_name,email=email,user_type=user_type)
            user.save()

            
            mobile=request.POST['mobile1']
            dob=request.POST['dob']
            member=Usermember(mobile=mobile,dob=dob,user=user)
            member.save()
            return redirect('/')
    return render(request,'seeker_signup.html')


def add_employee(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        email = request.POST['email']
        user_type = request.POST['text']

        if CustomUser.objects.filter(username=user_name).exists():
            messages.info(request, 'This username already exists')
            return redirect('employeesignup')
        else:
            # Create the CustomUser instance
            user = CustomUser.objects.create_user(username=user_name, email=email, user_type=user_type)
            user.save()

            # Create the Usermember instance
            companyname=request.POST['companyname']
            mobile = request.POST['mobile1']
            logo = request.FILES['logo']
            website = request.POST['website']
            address = request.POST['address']

            member =Employee(
                companyname=companyname,
                mobile=mobile,
                logo=logo,
                website=website,
                address=address,
                user=user
            )
            member.save()
            return redirect('/')
    return render(request,'employeesignup.html')

def show_employee(request):
    employees = Employee.objects.all()
    user=Usermember.objects.all()
    return render(request, 'show_employee.html', {'employee': employees,'user': user})
def show_jobseeker(request):
    user=Usermember.objects.all()
    return render(request, 'show_jobseeker.html', {'user': user})
def adminhome(request):
    pending_users_count = Usermember.objects.filter(is_approved=False).count()
    pending_employers_count = Employee.objects.filter(is_approved=False).count()
    pending_job_count = Job_details.objects.filter(is_approved=False).count()
    total_pending_count = pending_users_count + pending_employers_count
    return render(request, 'adminhome.html', {'total_pending_count': total_pending_count,'pending_job_count':pending_job_count})
def seeker_home(request):
    job_titles = Job.objects.values_list('job_title', flat=True).distinct()
    locations = Job.objects.values_list('location', flat=True).distinct()
    context = {
        'job_titles': job_titles,
        'locations': locations,
    }
    return render(request, 'seeker_home.html', context)

def search_jobs(request):
    job_title = request.GET.get('job_title', '')
    location = request.GET.get('location', '')

    jobs = Job.objects.all()

    if job_title:
        jobs = jobs.filter(job_title__icontains=job_title)

    if location:
        jobs = jobs.filter(location__icontains=location)

    jobs_list = list(jobs.values('id', 'job_title', 'companyname', 'job_des', 'job_exp', 'job_file', 'job_salary', 'job_schedule', 'job_type', 'location', 'posted_on'))

    return JsonResponse(jobs_list, safe=False)
def employeer_home(request):
     # Assume the employer's ID is stored in the session
    employer_id = request.session.get('employer_id')
    if not employer_id:
        return HttpResponse("Unauthorized", status=401)

    employer = get_object_or_404(Employee, id=employer_id)
    applications = JobApplication.objects.filter(job__companyname=employer.companyname)
    
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

    users = Usermember.objects.filter(is_approved=False)
    employers = Employee.objects.filter(is_approved=False)
    return render(request, 'admin_approve.html', {'users': users, 'employers': employers})
def emp_view_profile(request):
    user=request.user.id
    employee=Employee.objects.get(user_id=user)
    return render(request,"emp_view_profile.html",{'emp':employee})
def emp_edit_profilepage(request,pk):
    user=Usermember.objects.get(id=pk)
    employee=Employee.objects.get(id=pk)
    return render(request,"emp_edit_profile.html",{'emp':employee,'user':user})
def emp_edit_profile(request):
     return render(request, 'edit_profile.html')
@login_required
def emp_editprofile(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    print(f"Employer PK: {emp.pk}, User ID: {emp.user.id}")  # Debugging line

    if request.method == 'POST':
        emp.companyname = request.POST.get('companyname')
        emp.user.username = request.POST.get('username')
        emp.user.email = request.POST.get('email')
        emp.mobile = request.POST.get('mobile1')
        emp.address = request.POST.get('address')
        emp.website = request.POST.get('website')

        if 'logo' in request.FILES:
                try:
        # Check if the employer has an existing logo
                   if emp.logo:
            # If there's an existing logo, remove it
                        os.remove(emp.logo.path)
                        print("Existing image removed successfully")
                except Exception as e:
                    print("Error removing existing image:", e)

        # Assign the new logo
        emp.logo = request.FILES['logo']
        emp.user.save()  # Save the related user instance
        emp.save()  # Save the employer instance with the new logo

        return redirect('emp_view_profile')

    return render(request, 'emp_edit_profile.html', {'emp': emp})

@login_required
def password_reset_form(request):
    
    return render(request, 'password_reset_form.html')
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
        user_id=user_id
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
    return render(request,'view_jobs.html',{'job':job}) 
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

    try:
        profile = user.profile
        if not (profile.name and profile.email and profile.resume):
            return JsonResponse({'profile_complete': False})
    except Profile.DoesNotExist:
        return JsonResponse({'profile_complete': False})

    application, created = JobApplication.objects.get_or_create(user=user, job=job)
    return JsonResponse({'profile_complete': True, 'application_created': created})

# def check_new_applications(request):
#     new_applications = JobApplication.objects.filter(status='Pending').exists()
#     return JsonResponse({'new_applications': new_applications})

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

# def emp_application(request):
#     employer = request.user

#     # Ensure you are fetching the job instance correctly
#     try:
#         job = get_object_or_404(Job, user=employer)  # Assuming you want to filter by the employer's jobs
#     except Job.DoesNotExist:
#         return render(request, 'emp_application.html', {'applications': [], 'message': 'No job application found for this employer.'})

#     applications = JobApplication.objects.filter(job=job)
#     context = {'applications': applications}
#     return render(request, 'emp_application.html', context)




import logging
from django.shortcuts import render, get_object_or_404
from .models import Job, JobApplication

logger = logging.getLogger(__name__)

@login_required
def emp_application(request):
    employer = request.user  # Get the logged-in employer (CustomUser)

    try:
        jobs = Job.objects.filter(user=employer)
    except Job.DoesNotExist:
        jobs = []

    applications = JobApplication.objects.filter(job__in=jobs)

    context = {'applications': applications}
    return render(request, 'emp_application.html', context)



def user_profile(request):
    try:
        usermember = Usermember.objects.get(user=request.user)
    except ObjectDoesNotExist: # type: ignore
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
        
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']
        if 'profileimage' in request.FILES:
            profile.user_img = request.FILES['profileimage']
        
        # Save changes
        usermember.user.save()
        usermember.save()
        profile.save()

        return redirect('user_profile')

    context = {
        'usermember': usermember,
        'profile': profile
    }
    return render(request, 'user_profile.html', context)




# def user_profile(request):
    
#     usermember = Usermember.objects.get(user=request.user)
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         # Update UserMember fields
#         usermember.user.first_name = request.POST['firstname']
#         usermember.user.last_name = request.POST['lastname']
#         usermember.user.username = request.POST['user_name']
#         usermember.user.email = request.POST['email']
#         usermember.mobile = request.POST['mobile1']
#         usermember.dob = request.POST['dob']
#         address=request.POST['address']
#         resume=request.POST['resume']
#         user_img=request.POST.FILES['profileimage']
    
#         profile = Profile(
#             address=address,
#             resume=resume,
#             user_img=user_img
#         )
#         usermember.save()

#         # Update Profile fields
#         profile.address = request.POST.get('address')
#         if 'resume' in request.FILES:
#             profile.resume = request.FILES['resume']
#         if 'userImage' in request.FILES:
#             profile.user_img = request.FILES['userImage']
#         # if 'img' in request.FILES:
    
#         #     print("Existing image path:", profile.user_img.path)
    
    
#         # try:
#         #     if profile.user_img:
#         #         os.remove(profile.user_img.path)
#         #         print("Existing image removed successfully")
#         # except Exception as e:
#         #     print("Error removing existing image:", e)

        
#         # profile.user_img = request.FILES['img']
#         profile.save()

#         return redirect('user_profile')

#     context = {
#         'usermember': usermember,
#         'profile': profile
#     }
#     return render(request, 'user_profile.html', context)
# def user_profile(request):
#     mobile = request.POST['mobile1']
#     dob = request.POST['dob']
    
#     usermember = Usermember(
#         mobile=mobile,
#         dob=dob 
#     )
#     usermember.save()
#     return redirect('user_profile')
# def show_user(request):
#     return render(request,'show_user.html')
# def shows_users(request):
#     address=request.POST['address']
#     resume=request.POST['resume']
#     user_img=request.POST.FILES['profileimage']
    
#     profile = Profile(
#         address=address,
#         resume=resume,
#         user_img=user_img
#     )
#     profile.save()
#     return redirect('show_user')

def about(request):
    return render(request,'about.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

# @login_required
# def apply_for_job(request, job_id):
#     if request.method == 'POST':
#         user = request.user
#         job = Job.objects.get(id=job_id)
        
#         # Check if the user has already applied
#         if JobApplication.objects.filter(user=user, job=job).exists():
#             return JsonResponse({'success': False, 'message': 'You have already applied for this job.'})
        
#         # Create a new job application
#         JobApplication.objects.create(user=user, job=job)
#         return JsonResponse({'success': True, 'message': 'Application successful.'})
#     return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# @login_required
# @csrf_exempt
# def apply_for_job(request,job_id):
#     if request.method == 'POST':
#         user = request.user
#         job = Job.objects.get(id=job_id)
        
#         # Check if the user has already applied
#         if JobApplication.objects.filter(user=user, job=job).exists():
#             return JsonResponse({'success': False, 'message': 'You have already applied for this job.'})
        
#         # Create a new job application
#         JobApplication.objects.create(user=user, job=job)
#         return JsonResponse({'success': True, 'message': 'Application successful.'})
    
    
#     return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
@csrf_exempt
def apply_for_jobs(request, job_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            user = request.user
            job = Job.objects.get(id=job_id)
            
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