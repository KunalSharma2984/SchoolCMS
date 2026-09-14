from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegisterForm, UserEditForm
from .models import User
from courses.models import Course, Enrollment, Assignment, Submission


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully.')
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    if user.is_student():
        enrollments = Enrollment.objects.filter(student=user).select_related('course')
        submissions = Submission.objects.filter(student=user).select_related('assignment__course')
        context.update({'enrollments': enrollments, 'submissions': submissions})

    elif user.is_teacher():
        courses = Course.objects.filter(teacher=user)
        assignments = Assignment.objects.filter(course__teacher=user)
        pending = Submission.objects.filter(assignment__course__teacher=user, grade__isnull=True)
        context.update({'courses': courses, 'assignments': assignments, 'pending_submissions': pending})

    elif user.is_admin():
        context.update({
            'total_students': User.objects.filter(role='student').count(),
            'total_teachers': User.objects.filter(role='teacher').count(),
            'total_courses': Course.objects.count(),
            'students': User.objects.filter(role='student'),
            'teachers': User.objects.filter(role='teacher'),
            'courses': Course.objects.all(),
        })

    return render(request, 'accounts/dashboard.html', context)


# Admin-only: manage users
@login_required
def user_list_view(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    role = request.GET.get('role', '')
    users = User.objects.exclude(is_superuser=True)
    if role:
        users = users.filter(role=role)
    return render(request, 'accounts/user_list.html', {'users': users, 'role_filter': role})


@login_required
def user_edit_view(request, pk):
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    form = UserEditForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User updated.')
        return redirect('user_list')
    return render(request, 'accounts/user_edit.html', {'form': form, 'target_user': user})


@login_required
def user_delete_view(request, pk):
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted.')
        return redirect('user_list')
    return render(request, 'accounts/user_confirm_delete.html', {'target_user': user})
