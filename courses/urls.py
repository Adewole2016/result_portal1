from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),
    path('departments/edit/<int:pk>/', views.department_edit, name='department_edit'),
    path('departments/delete/<int:pk>/', views.department_delete, name='department_delete'),

    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/edit/<int:pk>/', views.course_edit, name='course_edit'),
    path('courses/delete/<int:pk>/', views.course_delete, name='course_delete'),
    path('manage/', views.manage_courses_departments, name='manage'),
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('system/settings/', views.system_settings_view, name='system_settings'),
    path('departments-courses/', views.manage_departments_courses, name='manage_departments_courses'),
    path('add-department/', views.add_department, name='add_department'),
    path('add-course/', views.add_course, name='add_course'),
    path('departments-courses/', views.manage_departments_courses, name='manage_departments_courses'),
    path('add-department/', views.add_department, name='add_department'),
    path('edit-department/<int:pk>/', views.edit_department, name='edit_department'),
    path('delete-department/<int:pk>/', views.delete_department, name='delete_department'),
    path('sessions-semesters/', views.manage_sessions_semesters, name='manage_sessions_semesters'),
    path('add-session/', views.add_session, name='add_session'),
    path('edit-session/<int:pk>/', views.edit_session, name='edit_session'),
    path('delete-session/<int:pk>/', views.delete_session, name='delete_session'),
    path('add-semester/', views.add_semester, name='add_semester'),
    path('edit-semester/<int:pk>/', views.edit_semester, name='edit_semester'),
    path('delete-semester/<int:pk>/', views.delete_semester, name='delete_semester'),
    path('', views.course_list, name='course_list'),
    path('add-course/', views.add_course, name='add_course'),
    path('edit-course/<int:pk>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:pk>/', views.delete_course, name='delete_course'),

]
