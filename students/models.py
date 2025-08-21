from django.db import models
from accounts.models import User
from courses.models import Department

class Student(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="student_profile")
    
    matric_no = models.CharField(max_length=20, unique=True, null=True, blank=True, default='')
    level = models.CharField(max_length=10, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    passport_photo = models.ImageField(upload_to="student_passports/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["matric_no"]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matric_no})"
