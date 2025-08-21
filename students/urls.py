from django.urls import path
from . import views

urlpatterns = [
    path('bulk-upload/', views.bulk_upload_students, name='bulk_upload_students'),
    path('export/', views.export_students, name='export_students'),
]
