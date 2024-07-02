from django.urls import path
from .import views
from .views import password_reset_form
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.index3,name='index3'),
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
    path('show_user/<int:application_id>/', views.show_user, name='show_user'),
   
    path('about', views.about, name='about'),
    path('apply/<int:job_id>/', views.apply_for_jobs, name='apply_for_jobs'),
    # path('check-new-applications/', views.check_new_applications, name='check_new_applications'),
     path('seeker_applied_job', views.seeker_applied_job, name='seeker_applied_job'),
     path('download-resume/<int:application_id>/', views.download_resume, name='download_resume'),
     path('verify_employee/<int:employee_id>/',views.verify_employee, name='verify_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('verify_user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('employer/jobs/', views.job_list_view, name='employer_jobs_list'),
    path('employer/jobs/<int:pk>/edit/', views.job_edit_view, name='employer_job_edit'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('admin_jobs/',views.admin_jobs, name='admin_jobs'),
    path('admin_password_change', views.admin_password_change, name='admin_password_change'),
    path('admin_profile/<int:pk>/',views.admin_profile,name='admin_profile'),

    path('edit_admin_page/<int:pk>',views.edit_admin_page,name='edit_admin_page'),
    path('editadmin/<int:pk>/',views.editadmin,name='editadmin'),
    path('edit_admin',views.edit_admin,name='edit_admin'),
] 