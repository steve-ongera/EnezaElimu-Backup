from django.shortcuts import render, get_object_or_404 ,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q

def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            admission_number = form.cleaned_data['admission_number']
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']

            # Get the student instance
            student = Student.objects.get(admission_number=admission_number)

            # Create the user with username as admission_number
            user = User.objects.create_user(
                username=admission_number,
                password=password,
                first_name=student.name.split()[0],  # First part of name
                last_name=" ".join(student.name.split()[1:]),  # Rest of the name
            )
            
            # Log the user in
            login(request, user)
            return redirect('dashboard')  # Redirect to a student dashboard

    else:
        form = StudentRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})


def student_login(request):
    if request.method == "POST":
        admission_number = request.POST['admission_number']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=admission_number, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')  # Get intended URL
            return redirect(next_url if next_url else 'dashboard')  # Redirect accordingly
        else:
            messages.error(request, "Invalid admission number or password.")

    return render(request, 'auth/login.html')


def student_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


@login_required
def dashboard(request):
    # Get the logged-in student's details using the admission number
    student = Student.objects.get(admission_number=request.user.username)

    return render(request, 'auth/dashboard.html', {'student': student})

@login_required
def general_student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def student_marks(request, student_id, term_id):
    student = get_object_or_404(Student, id=student_id)
    term = get_object_or_404(Term, id=term_id)
    cats = CAT.objects.filter(student=student, term=term)

    context = {
        'student': student,
        'term': term,
        'cats': cats,
    }
    return render(request, 'marks/student_marks.html', context)


@login_required
def student_progress(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    terms = Term.objects.all().order_by('-year', 'name')
    subjects = Subject.objects.all()
    progress_data = []

    for term in terms:
        term_data = {
            'term': term,
            'subjects': [],
            'term_average': 0,
            'overall_grade': '',
            'position': ''
        }
        
        total_score = 0
        subject_count = 0
        
        for subject in subjects:
            try:
                cat = CAT.objects.get(student=student, term=term, subject=subject)
                subject_data = {
                    'subject': subject,
                    'cat1': cat.cat1,
                    'cat2': cat.cat2,
                    'cat3': cat.cat3,
                    'average': cat.end_term,
                    'grade': cat.letter_grade,
                    'grade_points': cat.grade_points,
                    'position': cat.position
                }
                total_score += cat.end_term
                subject_count += 1
            except CAT.DoesNotExist:
                subject_data = {
                    'subject': subject,
                    'cat1': 'N/A',
                    'cat2': 'N/A',
                    'cat3': 'N/A',
                    'average': 'N/A',
                    'grade': 'N/A',
                    'grade_points': 'N/A',
                    'position': 'N/A'
                }
            
            term_data['subjects'].append(subject_data)
        
        # Calculate term averages if there are subjects
        if subject_count > 0:
            term_data['term_average'] = round(total_score / subject_count, 2)
            # Determine overall grade based on term average
            if term_data['term_average'] >= 80:
                term_data['overall_grade'] = 'A'
                term_data['position'] = 'First Class'
            elif term_data['term_average'] >= 75:
                term_data['overall_grade'] = 'A-'
                term_data['position'] = 'First Class'
            elif term_data['term_average'] >= 70:
                term_data['overall_grade'] = 'B+'
                term_data['position'] = 'First Class'
            elif term_data['term_average'] >= 65:
                term_data['overall_grade'] = 'B'
                term_data['position'] = 'Second Class Upper'
            elif term_data['term_average'] >= 60:
                term_data['overall_grade'] = 'B-'
                term_data['position'] = 'Second Class Upper'
            elif term_data['term_average'] >= 55:
                term_data['overall_grade'] = 'C+'
                term_data['position'] = 'Second Class Lower'
            elif term_data['term_average'] >= 50:
                term_data['overall_grade'] = 'C'
                term_data['position'] = 'Second Class Lower'
            elif term_data['term_average'] >= 40:
                term_data['overall_grade'] = 'D'
                term_data['position'] = 'Pass'
            else:
                term_data['overall_grade'] = 'F'
                term_data['position'] = 'Fail'
        
        progress_data.append(term_data)

    context = {
        'student': student,
        'progress_data': progress_data,
    }
    return render(request, 'marks/student_progress.html', context)


#logged in user to see his marks

@login_required
def individual_student_progress(request):
    try:
        student = Student.objects.get(admission_number=request.user.username)
    except Student.DoesNotExist:
        return render(request, 'marks/no_results.html', {'message': 'Student record not found.'})

    terms = Term.objects.all().order_by('-year', 'name')
    subjects = Subject.objects.all()
    progress_data = []

    for term in terms:
        term_data = {
            'term': term,
            'subjects': [],
            'term_average': 0,
            'overall_grade': '',
            'position': ''
        }
        
        total_score = 0
        subject_count = 0
        
        for subject in subjects:
            try:
                cat = CAT.objects.get(student=student, term=term, subject=subject)
                subject_data = {
                    'subject': subject.name,
                    'cat1': cat.cat1,
                    'cat2': cat.cat2,
                    'cat3': cat.cat3,
                    'average': cat.end_term,  # Used in graph
                    'grade': cat.letter_grade,
                    'grade_points': cat.grade_points,
                    'position': cat.position
                }
                total_score += cat.end_term
                subject_count += 1
            except CAT.DoesNotExist:
                subject_data = {
                    'subject': subject.name,
                    'cat1': 'N/A',
                    'cat2': 'N/A',
                    'cat3': 'N/A',
                    'average': 0,  # Default to 0 for graph
                    'grade': 'N/A',
                    'grade_points': 'N/A',
                    'position': 'N/A'
                }
            
            term_data['subjects'].append(subject_data)
        
        # Calculate term averages
        if subject_count > 0:
            term_data['term_average'] = round(total_score / subject_count, 2)
            if term_data['term_average'] >= 80:
                term_data['overall_grade'] = 'A'
                term_data['position'] = 'First Class'
            elif term_data['term_average'] >= 75:
                term_data['overall_grade'] = 'A-'
                term_data['position'] = 'First Class'
            elif term_data['term_average'] >= 70:
                term_data['overall_grade'] = 'B+'
                term_data['position'] = 'First Class'
            elif term_data['term_average'] >= 65:
                term_data['overall_grade'] = 'B'
                term_data['position'] = 'Second Class Upper'
            elif term_data['term_average'] >= 60:
                term_data['overall_grade'] = 'B-'
                term_data['position'] = 'Second Class Upper'
            elif term_data['term_average'] >= 55:
                term_data['overall_grade'] = 'C+'
                term_data['position'] = 'Second Class Lower'
            elif term_data['term_average'] >= 50:
                term_data['overall_grade'] = 'C'
                term_data['position'] = 'Second Class Lower'
            elif term_data['term_average'] >= 40:
                term_data['overall_grade'] = 'D'
                term_data['position'] = 'Pass'
            else:
                term_data['overall_grade'] = 'F'
                term_data['position'] = 'Fail'
        
        progress_data.append(term_data)

    context = {
        'student': student,
        'progress_data': progress_data,
    }
    return render(request, 'marks/individual_student_progress.html', context)


@login_required
#list all classes which pertifipated in examinations
def class_lists(request):
    classes = Class_of_study.objects.all().order_by('name', 'stream')
    return render(request, 'school/class_list.html', {
        'classes': classes
    })


@login_required
#terms in the examination session 
def term_list(request, class_id):
    class_of_study = get_object_or_404(Class_of_study, id=class_id)
    terms = Term.objects.filter(
        # your filtering conditions here
    ).order_by('-year', 'name')  # Sort by year descending, then term name
    return render(request, 'school/term_list.html', {
        'class_of_study': class_of_study,
        'terms': terms
    })



@login_required
#student list in certain term year and stream
def student_list(request, class_id, term_id):
    class_of_study = get_object_or_404(Class_of_study, id=class_id)
    term = get_object_or_404(Term, id=term_id)
    students = Student.objects.filter(current_class=class_of_study)
    subjects = Subject.objects.all()
    
    # Create a nested dictionary for easy access to results
    students_results = {}
    student_averages = {}
    
    for student in students:
        students_results[student.id] = {}
        cats = CAT.objects.filter(student=student, term=term)
        total_score = 0
        valid_subjects = 0
        
        for cat in cats:
            students_results[student.id][cat.subject.id] = cat
            total_score += cat.end_term
            valid_subjects += 1
        
        # Calculate average and grade for student
        if valid_subjects > 0:
            term_average = round(total_score / valid_subjects, 2)
            
            # Create a temporary CAT instance to use the grading methods
            temp_cat = CAT(cat1=term_average, cat2=term_average, cat3=term_average)
            temp_cat.end_term = term_average
            
            # Use the existing methods
            grade_points, letter_grade = temp_cat.assign_grade_points()
            position = temp_cat.determine_position()
            
            student_averages[student.id] = {
                'average': term_average,
                'grade': letter_grade,
                'grade_points': grade_points,
                'position': position,
                'name': student.name,
                'admission': student.admission_number
            }
    
    # Sort students by average score (descending)
    sorted_students = dict(sorted(
        student_averages.items(), 
        key=lambda x: x[1]['average'], 
        reverse=True
    ))
    
    # Add position numbers
    position = 1
    for student_id in sorted_students:
        sorted_students[student_id]['position_number'] = position
        position += 1
    
    return render(request, 'school/student_list.html', {
        'class_of_study': class_of_study,
        'term': term,
        'students': sorted_students,
        'subjects': subjects,
        'students_results': students_results,
    })



@login_required
def subject_analysis(request, class_id, term_id):
    class_of_study = get_object_or_404(Class_of_study, id=class_id)
    term = get_object_or_404(Term, id=term_id)
    subjects = Subject.objects.all()
    
    # Calculate average score for each subject
    subject_averages = {}
    for subject in subjects:
        cats = CAT.objects.filter(
            student__current_class=class_of_study,
            term=term,
            subject=subject
        )
        if cats.exists():
            total_score = sum(cat.end_term for cat in cats)
            average = round(total_score / cats.count(), 2)
            subject_averages[subject.name] = average
    
    # Sort subjects by average score
    sorted_subjects = dict(sorted(
        subject_averages.items(), 
        key=lambda x: x[1], 
        reverse=True
    ))
    
    return render(request, 'school/subject_analysis.html', {
        'class_of_study': class_of_study,
        'term': term,
        'subject_averages': sorted_subjects
    })




@login_required
def student_profile(request):
    """View for students to see their profile"""
    # Assuming student is linked to user via admission number or some other field
    student = get_object_or_404(Student, admission_number=request.user.username)
    
    context = {
        'student': student
    }
    return render(request, 'students/profile.html', context)

@login_required
def edit_student_profile(request):
    """View for students to edit certain fields of their profile"""
    student = get_object_or_404(Student, admission_number=request.user.username)
    
    if request.method == 'POST':
        form = StudentProfileEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('student_profile')
    else:
        form = StudentProfileEditForm(instance=student)
    
    context = {
        'form': form,
        'student': student
    }
    return render(request, 'students/edit_profile.html', context)



@login_required
# List all classes
def class_list(request):
    classes = Class_of_study.objects.all()
    return render(request, 'class/class_list.html', {'classes': classes})


@login_required
# Create a new class
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'class/class_form.html', {'form': form})


@login_required
# View class details
def class_detail(request, pk):
    class_instance = get_object_or_404(Class_of_study, pk=pk)
    return render(request, 'class/class_detail.html', {'class_instance': class_instance})


@login_required
# Update a class
def class_update(request, pk):
    class_instance = get_object_or_404(Class_of_study, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_instance)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm(instance=class_instance)
    return render(request, 'class/class_form.html', {'form': form})


@login_required
# Delete a class
def class_delete(request, pk):
    class_instance = get_object_or_404(Class_of_study, pk=pk)
    if request.method == 'POST':
        class_instance.delete()
        return redirect('class_list')
    return render(request, 'class/class_confirm_delete.html', {'class_instance': class_instance})





@login_required
# List all subjects
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject/subject_list.html', {'subjects': subjects})


@login_required
# Create a new subject
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subject/subject_form.html', {'form': form})


@login_required
# View subject details
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'subject/subject_detail.html', {'subject': subject})


@login_required
# Update an existing subject
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'subject/subject_form.html', {'form': form})


@login_required
# Delete a subject
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')
    return render(request, 'subject/subject_confirm_delete.html', {'subject': subject})


@login_required
# List all students
def students_list(request):
    students = Student.objects.all()
    return render(request, 'students/database_student_list.html', {'students': students})


@login_required
# Create a new student
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})


@login_required
# View student details
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


@login_required
# Update an existing student
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})


@login_required
# Delete a student
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})



@login_required
# List all terms
def term_lists(request):
    terms = Term.objects.all()
    return render(request, 'terms/term_list.html', {'terms': terms})


@login_required
# Create a new term
def term_create(request):
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('term_list')
    else:
        form = TermForm()
    return render(request, 'terms/term_form.html', {'form': form})


@login_required
# View term details
def term_detail(request, pk):
    term = get_object_or_404(Term, pk=pk)
    return render(request, 'terms/term_detail.html', {'term': term})


@login_required
# Update an existing term
def term_update(request, pk):
    term = get_object_or_404(Term, pk=pk)
    if request.method == 'POST':
        form = TermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            return redirect('term_list')
    else:
        form = TermForm(instance=term)
    return render(request, 'terms/term_form.html', {'form': form})


@login_required
# Delete a term
def term_delete(request, pk):
    term = get_object_or_404(Term, pk=pk)
    if request.method == 'POST':
        term.delete()
        return redirect('term_list')
    return render(request, 'terms/term_confirm_delete.html', {'term': term})




@login_required
# List all CATs
def cat_list(request):
    cats = CAT.objects.all()
    return render(request, 'cats/cat_list.html', {'cats': cats})


@login_required
# Create a new CAT record
def cat_create(request):
    if request.method == 'POST':
        form = CATForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cat_list')
    else:
        form = CATForm()
    return render(request, 'cats/cat_form.html', {'form': form})


@login_required
# View a single CAT record's details
def cat_detail(request, pk):
    cat = get_object_or_404(CAT, pk=pk)
    return render(request, 'cats/cat_detail.html', {'cat': cat})


@login_required
# Update an existing CAT record
def cat_update(request, pk):
    cat = get_object_or_404(CAT, pk=pk)
    if request.method == 'POST':
        form = CATForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('cat_list')
    else:
        form = CATForm(instance=cat)
    return render(request, 'cats/cat_form.html', {'form': form})


@login_required
# Delete a CAT record
def cat_delete(request, pk):
    cat = get_object_or_404(CAT, pk=pk)
    if request.method == 'POST':
        cat.delete()
        return redirect('cat_list')
    return render(request, 'cats/cat_confirm_delete.html', {'cat': cat})




@login_required
def student_population_graph(request):
    # Get data aggregated by year
    population_data = Term.objects.values('year').annotate(
        student_count=Count('cat__student', distinct=True)
    ).order_by('year')
    
    # Prepare data for the template
    years = [data['year'] for data in population_data]
    counts = [data['student_count'] for data in population_data]
    
    context = {
        'years': years,  
        'counts': counts,
        'population_data': population_data,
    }
    
    return render(request, 'graph/population_graph.html', context)


@login_required
#view for students who sat for cat that year
def class_distribution_view(request):
    # Get all available years from Term model
    available_years = Term.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Get the selected year (default to latest year if none selected)
    selected_year = request.GET.get('year', available_years.first())
    
    # Get students who have CATs in the selected year
    students_in_year = CAT.objects.filter(
        term__year=selected_year
    ).values_list('student', flat=True).distinct()
    
    # Get the count of students in each class and stream for the selected year
    class_distribution = Class_of_study.objects.annotate(
        student_count=Count(
            'students',
            filter=Q(students__id__in=students_in_year),
            distinct=True
        )
    ).values('name', 'stream', 'student_count').order_by('name', 'stream')
    
    # Prepare data for the chart
    classes = []
    counts = []
    labels = []
    
    for item in class_distribution:
        classes.append(item['name'])
        counts.append(item['student_count'])
        labels.append(f"{item['name']} - {item['stream']}")
    
    context = {
        'class_distribution': class_distribution,
        'classes': classes,
        'counts': counts,
        'labels': labels,
        'available_years': available_years,
        'selected_year': int(selected_year) if selected_year else None,
    }
    
    return render(request, 'graph/class_distribution.html', context)


@login_required
def search_student(request):
    form = StudentSearchForm(request.GET or None)
    students = None

    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            students = Student.objects.filter(
                models.Q(name__icontains=query) | 
                models.Q(admission_number__icontains=query) |
                models.Q(current_class__name__icontains=query)
            )

    return render(request, "search/search_student.html", {"form": form, "students": students})