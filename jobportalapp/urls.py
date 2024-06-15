from django.urls import path
from .import views
from .views import password_reset_form
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.index,name='index'),
    path('index1',views.index1,name='index1'),
    path('index3',views.index3,name='index3'),
    path('loginform',views.loginform,name='loginform'),
    path('login1',views.login1,name='login1'),
    path('employeesignup',views.employeesignup,name='employeesignup'),
    path('seeker_signup',views.seeker_signup,name='seeker_signup'),
    path('add_user',views.add_user,name='add_user'),
    path('add_employee',views.add_employee,name='add_employee'),
    path('show_employee',views.show_employee,name='show_employee'),
    path('show_jobseeker',views.show_jobseeker,name='show_jobseeker'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('employeer_home',views.employeer_home,name='employeer_home'),
    path('seeker_home',views.seeker_home,name='seeker_home'),
    path('admin_approve',views.admin_approve,name='admin_approve'),
    path('emp_view_profile',views.emp_view_profile,name='emp_view_profile'),

    
    path('emp_edit_profilepage/<int:pk>',views.emp_edit_profilepage,name='emp_edit_profilepage'),
    path('emp_editprofile/<int:pk>',views.emp_editprofile,name='emp_editprofile'),
    path('emp_edit_profile',views.emp_edit_profile,name='emp_edit_profile'),
    path('password_reset_form', password_reset_form, name='password_reset_form'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete')
    path('update_password', views.update_password, name='update_password'),
    path('logout', views.logout, name='logout'),

    path('jobs', views.jobs, name='jobs'),
    path('add_job', views.add_job,name='add_job'),
    path('job_list', views.job_list, name='job_list'),
    path('approve/<int:job_id>/', views.approve_job, name='approve_job'),
    path('disapprove_job/<int:job_id>', views.disapprove_job, name='disapprove_job'),
    path('view_jobs', views.view_jobs, name='view_jobs'),
    path('search_jobs', views.search_jobs, name='search_jobs'),
    path('check_profile_complete',views.check_profile_complete, name='check_profile_complete'),
    path('apply_for_job',views. apply_for_job, name='apply_for_job'),
    path('accept_application/<int:application_id>',views. accept_application, name='accept_application'),
    path('reject_application/<int:application_id>',views. reject_application, name='reject_application'),
    path('emp_application',views. emp_application, name='emp_application'),
    path('user_profile',views.user_profile,name='user_profile'),
    # path('show_user',views.show_user,name='show_user'),
    # path('shows_users',views.shows_users,name='shows_users'),
    path('about', views.about, name='about'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
]