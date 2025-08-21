from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    """
    Custom User model with role-based access control
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hod', 'Head of Department'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields for different roles
    staff_id = models.CharField(max_length=20, blank=True, null=True)
    department = models.ForeignKey(
        'courses.Department', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='users'
    )    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_hod(self):
        return self.role == 'hod'
    
    @property
    def is_lecturer(self):
        return self.role == 'lecturer'
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    def can_manage_users(self):
        return self.is_admin
    
    def can_approve_results(self):
        return self.is_hod or self.is_admin
    
    def can_upload_scores(self):
        return self.is_lecturer or self.is_hod or self.is_admin
    
    def can_view_analytics(self):
        return self.is_hod or self.is_admin


class UserProfile(models.Model):
    """
    Extended profile information for users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class AuditLog(models.Model):
    """
    Model to track user actions for security and audit purposes
    """
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('upload', 'Upload'),
        ('download', 'Download'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50, blank=True, null=True)
    object_id = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.timestamp}"


class CourseAllocation(models.Model):
    lecturer = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'lecturer'}
    )
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    session = models.ForeignKey('results.Session', on_delete=models.CASCADE)
    semester = models.ForeignKey('results.Semester', on_delete=models.CASCADE)
    allocated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lecturer', 'course', 'session', 'semester')
        verbose_name = "Course Allocation"
        verbose_name_plural = "Course Allocations"

    def __str__(self):
        return f"{self.lecturer.get_full_name()} - {self.course.code} ({self.session.name} - {self.semester.semester})"


