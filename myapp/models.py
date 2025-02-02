from django.db import models
import random
import string
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Department(models.Model):
    head_of_department = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Class_of_study(models.Model):
    name = models.CharField(max_length=50)  # Form 1, Form 2, etc.
    stream = models.CharField(max_length=50)  # Stream A, B, C, etc.

    def __str__(self):
        return f"{self.name} - {self.stream}"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Math, English, etc.
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    current_class = models.ForeignKey(Class_of_study, on_delete=models.SET_NULL, null=True, related_name='students')
    
    # Personal Information
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # Parent/Guardian Information
    father_name = models.CharField(max_length=100, null=True, blank=True)
    father_phone = models.CharField(max_length=15, null=True, blank=True)
    father_occupation = models.CharField(max_length=100, null=True, blank=True)
    
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    mother_phone = models.CharField(max_length=15, null=True, blank=True)
    mother_occupation = models.CharField(max_length=100, null=True, blank=True)
    
    # Guardian Information (if different from parents)
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_phone = models.CharField(max_length=15, null=True, blank=True)
    guardian_relationship = models.CharField(max_length=50, null=True, blank=True)
    guardian_address = models.TextField(null=True, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True)
    
    # Additional Information
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    medical_conditions = models.TextField(null=True, blank=True)
    previous_school = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['admission_number']

    def __str__(self):
        return f"{self.name} ({self.admission_number})"
    
    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

class Term(models.Model):
    name = models.CharField(max_length=50)  # Term 1, Term 2, Term 3
    year = models.IntegerField()  # e.g., 2023

    def __str__(self):
        return f"{self.name} {self.year}"

class CAT(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='cats')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    cat1 = models.FloatField(default=0)
    cat2 = models.FloatField(default=0)
    cat3 = models.FloatField(default=0)
    end_term = models.FloatField(default=0)  # Will store the average of CATs
    grade_points = models.FloatField(default=0.0)  # Store the numerical grade points
    letter_grade = models.CharField(max_length=2, default='F')  # Store the letter grade
    position = models.CharField(max_length=20, default='Fail')  # Store the class position

    def calculate_end_term(self):
        # Calculate average of CATs instead of sum
        total_cats = 3
        self.end_term = round((self.cat1 + self.cat2 + self.cat3) / total_cats, 2)
        return self.end_term

    def calculate_average(self):
        # Now just return end_term since it's already the average
        return self.end_term

    def assign_grade_points(self):
        average = self.calculate_average()
        
        if average >= 80:
            return 4.0, 'A'
        elif average >= 75:
            return 3.7, 'A-'
        elif average >= 70:
            return 3.3, 'B+'
        elif average >= 65:
            return 3.0, 'B'
        elif average >= 60:
            return 2.7, 'B-'
        elif average >= 55:
            return 2.3, 'C+'
        elif average >= 50:
            return 2.0, 'C'
        elif average >= 45:
            return 1.7, 'C-'
        elif average >= 40:
            return 1.3, 'D+'
        elif average >= 35:
            return 1.0, 'D'
        else:
            return 0.0, 'F'

    def determine_position(self):
        average = self.calculate_average()
        
        if average >= 70:
            return "First Class"
        elif average >= 60:
            return "Second Class Upper"
        elif average >= 50:
            return "Second Class Lower"
        elif average >= 40:
            return "Pass"
        else:
            return "Fail"

    def save(self, *args, **kwargs):
        # Calculate and store all values before saving
        self.end_term = self.calculate_end_term()
        self.grade_points, self.letter_grade = self.assign_grade_points()
        self.position = self.determine_position()
        super().save(*args, **kwargs)

    def get_full_grade_info(self):
        return {
            'end_term': self.end_term,
            'grade_points': self.grade_points,
            'letter_grade': self.letter_grade,
            'position': self.position
        }

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.term.name}"
    


class Teacher(models.Model):
    id_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)
    
    # Assigned Class
    assigned_class = models.ForeignKey(Class_of_study, on_delete=models.SET_NULL, null=True, blank=True, related_name="teachers")
    
    # Profile Picture
    profile_image = models.ImageField(upload_to="teachers_profiles/", default="profile.png" ,  null=True, blank=True)

    # Unique 6-character Teacher Code
    teacher_code = models.CharField(max_length=6, unique=True, blank=True)
    
    # Additional Information
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    
    # Employment Details
    employment_date = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)  # e.g., Senior Teacher, HOD

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_code})"

# Signal to generate a unique 6-character Teacher Code
def generate_teacher_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@receiver(pre_save, sender=Teacher)
def generate_unique_teacher_code(sender, instance, **kwargs):
    if not instance.teacher_code:
        unique_code = generate_teacher_code()
        while Teacher.objects.filter(teacher_code=unique_code).exists():
            unique_code = generate_teacher_code()
        instance.teacher_code = unique_code




class Staff(models.Model):
    # Basic Information
    id_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    
    # Employment Details
    department = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)  # e.g., Admin, Teacher, Security, etc.
    employment_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

    # Profile Picture
    profile_image = models.ImageField(upload_to="staff_profiles/", default="profile.png", null=True, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"



class NonStaff(models.Model):
    # Basic Information
    id_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    
    # Non-Staff Role (e.g., Cleaner, Security, etc.)
    role = models.CharField(max_length=100, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Profile Picture
    profile_image = models.ImageField(upload_to="nonstaff_profiles/", default="profile.png", null=True, blank=True)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Intern(models.Model):
    # Basic Information
    id_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    # Internship Details
    department = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)  # e.g., IT Intern, Admin Intern
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    stipend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Profile Picture
    profile_image = models.ImageField(upload_to="intern_profiles/", default="profile.png", null=True, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"
