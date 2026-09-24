from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Course, Enrollment, Assignment, Submission
from .forms import CourseForm, AssignmentForm, SubmissionForm, GradeForm


@login_required
def course_list(request):
    courses = Course.objects.select_related('teacher').all()
    enrolled_ids = []
    if request.user.is_student():
        enrolled_ids = list(
            Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        )
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrolled_ids': enrolled_ids,
    })


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = False
    student_assignments = []

    if request.user.is_student():
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        if is_enrolled:
            assignments = course.assignments.all()
            submitted_ids = Submission.objects.filter(
                student=request.user, assignment__course=course
            ).values_list('assignment_id', flat=True)
            student_assignments = [(a, a.id in submitted_ids) for a in assignments]

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'student_assignments': student_assignments,
    })


@login_required
def course_create(request):
    if not request.user.is_teacher():
        messages.error(request, 'Only teachers can create courses.')
        return redirect('course_list')
    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        course = form.save(commit=False)
        course.teacher = request.user
        course.save()
        messages.success(request, 'Course created.')
        return redirect('course_detail', pk=course.pk)
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Create'})


@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user != course.teacher and not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('course_list')
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Course updated.')
        return redirect('course_detail', pk=course.pk)
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Edit', 'course': course})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user != course.teacher and not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('course_list')
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted.')
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@require_POST
@login_required
def enroll(request, pk):
    if not request.user.is_student():
        messages.error(request, 'Only students can enroll.')
        return redirect('course_detail', pk=pk)
    course = get_object_or_404(Course, pk=pk)
    _, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, f'Enrolled in {course.title}.')
    else:
        messages.info(request, 'You are already enrolled.')
    return redirect('course_detail', pk=pk)


@require_POST
@login_required
def unenroll(request, pk):
    course = get_object_or_404(Course, pk=pk)
    Enrollment.objects.filter(student=request.user, course=course).delete()
    messages.success(request, f'Unenrolled from {course.title}.')
    return redirect('course_list')


@login_required
def assignment_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.user != course.teacher:
        messages.error(request, 'Only the course teacher can add assignments.')
        return redirect('course_detail', pk=course_pk)
    form = AssignmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        assignment = form.save(commit=False)
        assignment.course = course
        assignment.save()
        messages.success(request, 'Assignment created.')
        return redirect('course_detail', pk=course_pk)
    return render(request, 'courses/assignment_form.html', {'form': form, 'course': course})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submission = None
    if request.user.is_student():
        submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    return render(request, 'courses/assignment_detail.html', {
        'assignment': assignment,
        'submission': submission,
    })


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    course = assignment.course
    if request.user != course.teacher and not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('course_detail', pk=course.pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted.')
        return redirect('course_detail', pk=course.pk)
    return render(request, 'courses/assignment_confirm_delete.html', {'assignment': assignment})


@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not request.user.is_student():
        messages.error(request, 'Only students can submit.')
        return redirect('assignment_detail', pk=pk)
    if not Enrollment.objects.filter(student=request.user, course=assignment.course).exists():
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('assignment_detail', pk=pk)

    existing = Submission.objects.filter(assignment=assignment, student=request.user).first()
    form = SubmissionForm(request.POST or None, request.FILES or None, instance=existing)
    if request.method == 'POST' and form.is_valid():
        submission = form.save(commit=False)
        submission.assignment = assignment
        submission.student = request.user
        submission.save()
        messages.success(request, 'Submitted successfully.')
        return redirect('assignment_detail', pk=pk)
    return render(request, 'courses/submission_form.html', {
        'form': form,
        'assignment': assignment,
        'existing': existing,
    })


@login_required
def submission_list(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    if request.user != assignment.course.teacher and not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('course_detail', pk=assignment.course.pk)
    submissions = assignment.submissions.select_related('student').all()
    return render(request, 'courses/submission_list.html', {
        'assignment': assignment,
        'submissions': submissions,
    })


@login_required
def grade_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if request.user != submission.assignment.course.teacher and not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    form = GradeForm(request.POST or None, instance=submission)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Grade saved.')
        return redirect('submission_list', assignment_pk=submission.assignment.pk)
    return render(request, 'courses/grade_form.html', {
        'form': form,
        'submission': submission,
    })


@login_required
def my_grades(request):
    if not request.user.is_student():
        return redirect('dashboard')
    submissions = Submission.objects.filter(
        student=request.user
    ).select_related('assignment__course').order_by('assignment__course__title')
    return render(request, 'courses/my_grades.html', {'submissions': submissions})
