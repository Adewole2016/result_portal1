from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('', views.result_dashboard, name='dashboard'),
    path('upload/', views.upload_scores, name='upload_scores'),
    path('view/<int:course_id>/', views.view_results, name='view_results'),
    path('upload/<int:course_id>/', views.upload_results, name='upload_results'),
    path('results/view/<int:course_id>/<int:semester_id>/', views.view_results, name='view_results'),
    path('download-broadsheet-excel/', views.download_broadsheet_excel, name='download_broadsheet_excel'),
    path('upload/', views.upload_scores, name='upload_scores'),           # list allocations / pick course
    path('upload/<int:course_id>/', views.upload_results, name='upload_results'),  # course-specific upload
    path('view/<int:course_id>/', views.view_results, name='view_results'),       # view results for a course
    path('download-template/<int:course_id>/', views.download_score_template, name='download_template'),
      
    path('download/excel/<int:course_id>/', views.download_excel, name='download_excel'),
    path('download/pdf/<int:course_id>/', views.download_pdf, name='download_pdf'),
 


    path('approve/', views.approve_results, name='approve_results'),
    path('student/', views.student_results, name='student_results'),
    path('download-template/<int:course_id>/', views.download_score_template, name='download_template'),
    path('broadsheet/', views.broadsheet_view, name='broadsheet_view'),

    # Session URLs
    path('sessions/', views.manage_sessions, name='manage_sessions'),
    path('sessions/add/', views.add_session, name='add_session'),
    path('sessions/edit/<int:pk>/', views.edit_session, name='edit_session'),
    path('sessions/delete/<int:pk>/', views.delete_session, name='delete_session'),

    # Semester URLs
    path('semesters/', views.manage_semesters, name='manage_semesters'),
    path('semesters/add/', views.add_semester, name='add_semester'),
    path('semesters/edit/<int:pk>/', views.edit_semester, name='edit_semester'),
    path('semesters/delete/<int:pk>/', views.delete_semester, name='delete_semester'),

    # Grading System URLs
    path('grading/manage/', views.manage_grading_system, name='manage_grading_system'),
    path('grading/add/', views.add_grading_system, name='add_grading'),
    path('grading/<int:pk>/edit/', views.edit_grading_system, name='edit_grading'),
    path('sessions-semesters/', views.manage_sessions_semesters, name='manage_sessions_semesters')

]

