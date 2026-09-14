from django.urls import path
from . import views

urlpatterns = [
    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Enrollment
    path('courses/<int:pk>/enroll/', views.enroll, name='enroll'),
    path('courses/<int:pk>/unenroll/', views.unenroll, name='unenroll'),

    # Assignments
    path('courses/<int:course_pk>/assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
    path('assignments/<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),

    # Submissions & Grading
    path('assignments/<int:assignment_pk>/submissions/', views.submission_list, name='submission_list'),
    path('submissions/<int:pk>/grade/', views.grade_submission, name='grade_submission'),

    # Student grades
    path('my-grades/', views.my_grades, name='my_grades'),
]
