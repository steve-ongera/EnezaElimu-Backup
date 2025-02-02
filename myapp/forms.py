from django import forms
from django.contrib.auth.models import User
from .models import *

class StudentRegistrationForm(forms.ModelForm):
    admission_number = forms.CharField(max_length=20, help_text="Enter your admission number")
    name = forms.CharField(max_length=100, help_text="Enter your full name")
    password = forms.CharField(widget=forms.PasswordInput, help_text="Enter a strong password")

    class Meta:
        model = User
        fields = ['admission_number', 'name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        admission_number = cleaned_data.get("admission_number")
        name = cleaned_data.get("name")

        # Check if admission number exists
        try:
            student = Student.objects.get(admission_number=admission_number)
        except Student.DoesNotExist:
            raise forms.ValidationError("Admission number does not exist.")

        # Ensure the name matches the student’s actual name
        if student.name.lower() != name.lower():
            raise forms.ValidationError("Name does not match our records.")

        return cleaned_data





class StudentProfileEditForm(forms.ModelForm):
    class Meta:
        model = Student
        # Only include fields that are safe for students to edit
        fields = [
            'address',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relationship',
            'medical_conditions',
            'blood_group'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and placeholders
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class_of_study
        fields = ['name', 'stream']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code']


class StudentForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    admission_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Student
        fields = '__all__'



class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['name', 'year']



class CATForm(forms.ModelForm):
    class Meta:
        model = CAT
        fields = ['student', 'subject', 'term', 'cat1', 'cat2', 'cat3']

class StudentSearchForm(forms.Form):
    query = forms.CharField(label="Search Student", max_length=100, required=False)




class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['id_number', 'first_name', 'last_name', 'email', 'phone', 'address', 'assigned_class', 
                  'profile_image', 'date_of_birth', 'gender', 'nationality', 'employment_date', 'department', 
                  'position', 'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship']
    
class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['id_number', 'first_name', 'last_name', 'email', 'phone', 'address', 'assigned_class', 
                  'profile_image', 'date_of_birth', 'gender', 'nationality', 'employment_date', 'department', 
                  'position', 'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship']




class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'id_number', 'first_name', 'last_name', 'email', 'phone', 'address',
            'date_of_birth', 'gender', 'nationality', 'department', 'position',
            'employment_date', 'salary', 'status', 'profile_image', 
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship'
        ]


class NonStaffForm(forms.ModelForm):
    class Meta:
        model = NonStaff
        fields = [
            'id_number', 'first_name', 'last_name', 'email', 'phone', 'address',
            'date_of_birth', 'gender', 'nationality', 'role', 'hire_date', 
            'salary', 'profile_image', 
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship'
        ]



class InternForm(forms.ModelForm):
    class Meta:
        model = Intern
        fields = [
            'id_number', 'first_name', 'last_name', 'email', 'phone', 'address',
            'date_of_birth', 'gender', 'nationality', 'department', 'position',
            'start_date', 'end_date', 'stipend', 'profile_image',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship'
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_image', 'full_names', 'about', 'role', 'Region', 
            'county', 'address', 'phone', 'email'
        ]
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'full_names': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full names'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write about yourself'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'Region': forms.Select(attrs={'class': 'form-control'}),
            'county': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter county'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'})
        }
        labels = {
            'profile_image': 'Profile Image',
            'full_names': 'Full Names',
            'about': 'About Me',
            'role': 'Role',
            'Region': 'Region',
            'county': 'County',
            'address': 'Address',
            'phone': 'Phone Number',
            'email': 'Email Address'
        }
        help_texts = {
            'email': 'Please enter a valid email address.'
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be 10 digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email




class NewsUpdateForm(forms.ModelForm):
    class Meta:
        model = NewsUpdate
        fields = ['title', 'description', 'category', 'image']  # Include relevant fields


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'photo', 'pdf']  # Include only content, photo, and pdf
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Type your message'}),
        }

