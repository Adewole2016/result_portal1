from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, UserProfile, AuditLog
from .models import CourseAllocation



# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')


# Custom User Change Form
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 
            'role', 'is_active', 'is_staff'
        )


# Inline profile with User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'role', 'is_active', 'date_joined'
    )
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'staff_id')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name', 'email',
                'phone_number', 'date_of_birth', 'address'
            )
        }),
        ("Role & Department", {"fields": ("role", "staff_id", "department")}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Profile', {'fields': ('profile_picture',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    inlines = [UserProfileInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_admin:
            return qs
        elif request.user.is_hod:
            return qs.filter(department=request.user.department)
        return qs.filter(id=request.user.id)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ('user__username', 'user__email', 'location')
    list_filter = ('birth_date',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'description', 'timestamp')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'description', 'object_id')
    readonly_fields = (
        'user', 'action', 'model_name', 'object_id', 'description',
        'ip_address', 'user_agent', 'timestamp'
    )
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser






@admin.register(CourseAllocation)
class CourseAllocationAdmin(admin.ModelAdmin):
    list_display = ('lecturer', 'course', 'session', 'semester', 'allocated_at')
    list_filter = ('session', 'semester')
    search_fields = ('lecturer__username', 'course__name')
