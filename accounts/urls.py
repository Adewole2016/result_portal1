
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from courses import views as course_views
from django.urls import reverse_lazy

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('hod-dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('lecturer-dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # Profile & Password
    path('profile/', views.profile_view, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/dashboard/'
    ), name='password_change'),

    # User Management (Admin)
    path('user/create/', views.UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('departments-courses/', course_views.manage_departments_courses, name='manage_departments_courses'),
    path('system/settings/', views.system_settings_view, name='system_settings'),
    path("system/settings/grading_system/", views.manage_grading_systems, name="grading_system"),
    path("system/settings/grading_system/", views.manage_grading_systems, name="grading_system"),
    path("system/settings/grading_system/", views.add_grading_system, name="grading_system_form"),
    path("system/settings/grading_system/", views.manage_grading_systems, name="grading_system"),
    
    path("system/settings/grading_system/<int:pk>/edit/", views.edit_grading_system, name="edit_grading_system"),
    path('assign-course/<int:lecturer_id>/', views.assign_course, name='assign_course'),
    path('hod-dashboard/lecturers/', views.manage_lecturers, name='manage_lecturers'),
    path('students/', views.student_list, name='student_list'),
 
    path('lecturers/', views.lecturer_list, name='lecturer_list'),
    path('hod-dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('hod-dashboard/lecturers/', views.manage_lecturers, name='manage_lecturers'),
    path('hod-dashboard/lecturers/allocate/', views.allocate_course, name='allocate_course'),
    path('hod-dashboard/lecturers/delete/<int:lecturer_id>/', views.delete_lecturer, name='delete_lecturer'),
    path('grading-system/', views.grading_system_list, name='grading_system'),
    path('grading-system/add/', views.add_grading_system, name='manage_grading_system'),
    path('grading-system/edit/<int:grading_id>/', views.edit_grading_system, name='edit_grading_system'),
    path('assign-course/<int:lecturer_id>/', views.assign_course, name='assign_course'),
    path('delete-allocation/<int:allocation_id>/', views.delete_allocation, name='delete_allocation'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html', success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    # path('register/', views.register_view, name='register'), # If registration is needed
    # path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),


]





