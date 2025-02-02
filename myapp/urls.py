from django.urls import path
from . import views

urlpatterns = [
    path('', views.general_student_list, name='student_list'),
    path('student/<int:student_id>/term/<int:term_id>/', views.student_marks, name='student_marks'),
    path('student/<int:student_id>/progress/', views.student_progress, name='student_progress'),

    path('classes_lists/', views.class_lists, name='class_lists'),
    path('classes/<int:class_id>/terms/', views.term_list, name='term_list'),
    path('classes/<int:class_id>/terms/<int:term_id>/students/',  views.student_list, name='student_list'),


    # urls.py
    path('classes/<int:class_id>/terms/<int:term_id>/analysis/', views.subject_analysis, name='subject_analysis'),
    path('register/', views.register, name='register'),
    path('login/', views.student_login, name='login'),
    path('logout/', views.student_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('individual_student_progress/' , views.individual_student_progress , name='individual_student_progress'),
    path('profile/', views.student_profile, name='student_profile'),
    path('profile/edit/', views.edit_student_profile, name='edit_student_profile'),

    #classs list view
    path('class_lists/', views.class_list, name='class_list'),
    path('create/', views.class_create, name='class_create'),
    path('<int:pk>/', views.class_detail, name='class_detail'),
    path('<int:pk>/update/', views.class_update, name='class_update'),
    path('<int:pk>/delete/', views.class_delete, name='class_delete'),

    #subject list views
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('subjects/<int:pk>/update/', views.subject_update, name='subject_update'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),

    #students
    path('list_of_students/', views.students_list, name='students_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    #terms
    path('terms/', views.term_lists, name='term_lists'),
    path('terms/create/', views.term_create, name='term_create'),
    path('terms/<int:pk>/', views.term_detail, name='term_detail'),
    path('terms/<int:pk>/update/', views.term_update, name='term_update'),
    path('terms/<int:pk>/delete/', views.term_delete, name='term_delete'),

    #cats
    path('cats/', views.cat_list, name='cat_list'),
    path('cats/create/', views.cat_create, name='cat_create'),
    path('cats/<int:pk>/', views.cat_detail, name='cat_detail'),
    path('cats/<int:pk>/update/', views.cat_update, name='cat_update'),
    path('cats/<int:pk>/delete/', views.cat_delete, name='cat_delete'),

    #graphs
    path('population-graph/', views.student_population_graph, name='population-graph'),
    path('class-distribution/', views.class_distribution_view, name='class-distribution'),
    #search
    path("search-student/", views.search_student, name="search_student"),
    
    
]