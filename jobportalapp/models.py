from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.conf import settings

# Create your models here.
class  CustomUser(AbstractUser):
    user_type=models.CharField(default=1,max_length=10)
class Usermember(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)

    mobile=models.IntegerField(null=True)
    dob=models.DateField(null=True)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
class Employee(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    companyname=models.CharField(max_length=255,null=True)
    mobile=models.IntegerField(null=True)
    logo=models.ImageField(blank=True,upload_to="images/",null=True)
    website=models.URLField(max_length=255,null=True)
    address=models.CharField(max_length=255,null=True)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username   
    
class Reset_password(models.Model):
    current_password=models.CharField(max_length=255,null=True)
    new_password=models.CharField(max_length=255,null=True)
class Job_details(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='job_details',null=True)
    job_title=models.CharField(max_length=255,null=True)
    companyname=models.CharField(max_length=255,null=True)
    location=models.CharField(max_length=255,null=True)
    job_schedule=models.CharField(max_length=255,null=True)
    job_type=models.CharField(max_length=255,null=True)
    job_des=models.CharField(max_length=255,null=True)
    job_salary=models.IntegerField(null=True)
    job_exp=models.IntegerField(null=True)
    posted_on=models.DateField(max_length=255,null=True)
    job_file=models.ImageField(blank=True,upload_to="images/",null=True)
    is_approved = models.BooleanField(default=False)
    
class Job(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='posted_jobs',null=True) 
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True)
    job_title=models.CharField(max_length=255,null=True)
    companyname=models.CharField(max_length=255,null=True)
    location=models.CharField(max_length=255,null=True)
    job_schedule=models.CharField(max_length=255,null=True)
    job_type=models.CharField(max_length=255,null=True)
    job_des=models.CharField(max_length=255,null=True)
    job_salary=models.IntegerField(null=True)
    job_exp=models.IntegerField(null=True)
    posted_on=models.DateField(max_length=255,null=True)
    job_file=models.ImageField(blank=True,upload_to="images/",null=True)
    
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.job_title



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    user_img=models.ImageField(blank=True,upload_to="images/",null=True)
    address=models.CharField(max_length=255,null=True)
    resume = models.FileField(upload_to='resumes/',null=True)
    dob = models.ForeignKey(Usermember, on_delete=models.CASCADE, related_name='profile_dob', null=True, blank=True)
    mobile = models.ForeignKey(Usermember, on_delete=models.CASCADE, related_name='profile_mobile', null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    resume_viewed = models.BooleanField(default=False)  
    profile_visited = models.BooleanField(default=False)

    def send_acceptance_email(self):
        send_mail(
            'Job Application Accepted',
            'Your application has been accepted.We will contact you soon',
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email]
        )

    def __str__(self):
        return f"{self.user.username} applied for {self.job.job_title}"
    
class Admin_profile(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    mobile=models.IntegerField(null=True)
    image=models.ImageField(blank=True,upload_to="images/",null=True)


