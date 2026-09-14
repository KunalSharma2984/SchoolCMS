"""
Management command: python manage.py seed
Creates demo users, courses, assignments, and submissions.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment, Assignment, Submission

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Admin
        admin = User.objects.create_superuser(
            username='admin', password='admin123',
            email='admin@school.com', role='admin',
            first_name='Admin', last_name='User'
        )

        # Teachers
        t1 = User.objects.create_user(
            username='teacher1', password='pass1234',
            email='t1@school.com', role='teacher',
            first_name='Alice', last_name='Brown'
        )
        t2 = User.objects.create_user(
            username='teacher2', password='pass1234',
            email='t2@school.com', role='teacher',
            first_name='Bob', last_name='Smith'
        )

        # Students
        s1 = User.objects.create_user(
            username='student1', password='pass1234',
            email='s1@school.com', role='student',
            first_name='Charlie', last_name='Day'
        )
        s2 = User.objects.create_user(
            username='student2', password='pass1234',
            email='s2@school.com', role='student',
            first_name='Diana', last_name='Lane'
        )

        # Courses
        c1 = Course.objects.create(
            title='Introduction to Python',
            description='Learn Python from scratch. Covers variables, loops, functions, and OOP.',
            teacher=t1
        )
        c2 = Course.objects.create(
            title='Web Development with Django',
            description='Build full-stack web apps using Python and Django.',
            teacher=t1
        )
        c3 = Course.objects.create(
            title='Mathematics for CS',
            description='Discrete math, logic, and probability for computer science students.',
            teacher=t2
        )

        # Enrollments
        Enrollment.objects.create(student=s1, course=c1)
        Enrollment.objects.create(student=s1, course=c2)
        Enrollment.objects.create(student=s2, course=c1)
        Enrollment.objects.create(student=s2, course=c3)

        # Assignments
        a1 = Assignment.objects.create(
            course=c1, title='Hello World Program',
            description='Write a Python program that prints Hello, World! and your name.',
            max_score=100
        )
        a2 = Assignment.objects.create(
            course=c1, title='FizzBuzz',
            description='Print numbers 1–100. For multiples of 3 print Fizz, for 5 print Buzz, for both print FizzBuzz.',
            max_score=100
        )
        a3 = Assignment.objects.create(
            course=c2, title='Build a Django Model',
            description='Create a Django model for a Blog with title, content, and author fields.',
            max_score=50
        )

        # Submissions
        sub1 = Submission.objects.create(
            assignment=a1, student=s1,
            content='print("Hello, World!")\nprint("My name is Charlie")',
            grade=95, feedback='Great work! Clean and correct.'
        )
        sub2 = Submission.objects.create(
            assignment=a1, student=s2,
            content='print("Hello World")',
        )
        sub3 = Submission.objects.create(
            assignment=a2, student=s1,
            content='for i in range(1, 101):\n    if i % 15 == 0: print("FizzBuzz")\n    elif i % 3 == 0: print("Fizz")\n    elif i % 5 == 0: print("Buzz")\n    else: print(i)',
            grade=100, feedback='Perfect solution!'
        )

        self.stdout.write(self.style.SUCCESS(
            '\nDone! Sample accounts created:\n'
            '  admin / admin123  (Admin)\n'
            '  teacher1 / pass1234  (Teacher - Alice Brown)\n'
            '  teacher2 / pass1234  (Teacher - Bob Smith)\n'
            '  student1 / pass1234  (Student - Charlie Day)\n'
            '  student2 / pass1234  (Student - Diana Lane)\n'
        ))
