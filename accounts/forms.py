from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, get_user_model
from django.forms import inlineformset_factory

from accounts.models import User, UserProfile
from students.models import Student
from courses.models import Department, Course
from results.models import GradingSystem, GradeScale

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from courses.models import Department
from students.models import Student
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    staff_id = forms.CharField(max_length=20, required=False)
    matric_no = forms.CharField(max_length=20, required=False)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label="Select Department"
    )
    level = forms.ChoiceField(
        choices=[
            ('ND1', 'ND1'),
            ('ND2', 'ND2'),
            ('HND1', 'HND1'),
            ('HND2', 'HND2'),
        ],
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'role', 'department', 'level', 'phone_number',
            'staff_id', 'matric_no', 'password1', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if field_name in ['role', 'department', 'level']:
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class

    def clean_level(self):
        role = self.cleaned_data.get('role')
        level = self.cleaned_data.get('level')

        if role != 'student':
            return level  # allow blank for non-students

        if not level:
            raise forms.ValidationError("Level is required for students.")

        return level

    def clean_staff_id(self):
        role = self.cleaned_data.get('role')
        staff_id = self.cleaned_data.get('staff_id')

        # For staff roles, require and check uniqueness
        if role in ['hod', 'lecturer', 'admin']:
            if not staff_id:
                raise forms.ValidationError("Staff ID is required for staff members.")
            if User.objects.filter(staff_id=staff_id).exists():
                raise forms.ValidationError("User with this Staff ID already exists.")
        else:
            # Ensure students don't store any staff_id value
            staff_id = None

        return staff_id



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'address', 'profile_picture')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['date_of_birth', 'address', 'profile_picture']:
                field.widget.attrs['class'] = 'form-control'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'location', 'birth_date', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")

        return cleaned_data


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your old password was entered incorrectly.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("The two password fields didn't match.")

        return cleaned_data

    def save(self):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        self.user.save()
        return self.user


class BulkUserUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx,.xls,.csv'})
    )
    default_role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith(('.xlsx', '.xls', '.csv')):
                raise forms.ValidationError("Please upload a valid Excel or CSV file.")
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size should not exceed 5MB.")
        return file


class GradingSystemForm(forms.ModelForm):
    class Meta:
        model = GradingSystem
        fields = ['name', 'is_active']


class GradeScaleForm(forms.ModelForm):
    class Meta:
        model = GradeScale
        fields = ['grade', 'min_score', 'max_score', 'grade_point']


GradeScaleFormSet = inlineformset_factory(
    GradingSystem,
    GradeScale,
    form=GradeScaleForm,
    extra=1,
    can_delete=True
)


class CourseAllocationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['lecturer']
