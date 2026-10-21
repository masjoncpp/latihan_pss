from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from catalog.models import Assignment, Course, Enrollment, Lesson, Submission

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds database with initial sample data idempotently as per Modul 4"

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample data...")

        # 1. Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
        else:
            admin_user.role = User.Role.ADMIN
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
        self.stdout.write(f"- Admin user: {admin_user.username}")

        # 2. Lecturers
        lecturers_data = [
            ("suprayogi", "suprayogi@gmail.com", "12345"),
            ("agus", "agus@gmail.com", "123"),
            ("ayu", "ayu@gmail.com", "123"),
            ("bagus", "bagus@gmail.com", "123"),
            ("heru", "heru@gmail.com", "123"),
        ]
        lecturer_objects = {}
        for username, email, password in lecturers_data:
            user, u_created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": User.Role.LECTURER,
                },
            )
            if u_created:
                user.set_password(password)
                user.save()
            elif user.role != User.Role.LECTURER:
                user.role = User.Role.LECTURER
                user.save()
            lecturer_objects[username] = user
        self.stdout.write(f"- Lecturers created/verified: {len(lecturer_objects)}")

        # 3. Student (fauzan)
        student, s_created = User.objects.get_or_create(
            username="fauzan",
            defaults={
                "email": "fauzan@gmail.com",
                "role": User.Role.STUDENT,
            },
        )
        if s_created:
            student.set_password("12345")
            student.save()
        elif student.role != User.Role.STUDENT:
            student.role = User.Role.STUDENT
            student.save()
        self.stdout.write(f"- Student: {student.username}")

        # 4. Course (PSS01)
        course, c_created = Course.objects.get_or_create(
            code="PSS01",
            defaults={
                "title": "Pemrograman Sisi Server",
                "description": "Django Framework dan ORM",
                "lecturer": lecturer_objects["suprayogi"],
                "is_active": True,
            },
        )
        self.stdout.write(f"- Course: {course.code} - {course.title}")

        # 5. Lessons
        lessons_data = [
            (1, "Pengenalan Backend", "Pengenalan dasar backend architecture dan konsep web server."),
            (2, "Pola Arsitektur Backend", "Memahami konsep Model-View-Template (MVT) dan arsitektur aplikasi."),
            (3, "Kontaienerisasi dengan Docker", "Membangun reproducible development environment menggunakan Docker Compose."),
        ]
        for order, title, content in lessons_data:
            lesson, _ = Lesson.objects.update_or_create(
                course=course,
                order=order,
                defaults={
                    "title": title,
                    "content": content,
                },
            )
        self.stdout.write(f"- Lessons verified for {course.code}")

        # 6. Enrollment
        enrollment, _ = Enrollment.objects.get_or_create(
            student=student,
            course=course,
        )
        self.stdout.write(f"- Enrollment: {enrollment}")

        # 7. Assignment
        assignment, _ = Assignment.objects.get_or_create(
            course=course,
            title="Tugas Django ORM",
            defaults={
                "description": "Implementasikan model dan relationship menggunakan Django ORM.",
                "deadline": timezone.now() + timedelta(days=7),
            },
        )
        self.stdout.write(f"- Assignment: {assignment.title}")

        # 8. Submission
        submission, _ = Submission.objects.get_or_create(
            assignment=assignment,
            student=student,
            defaults={
                "content": "Saya telah menyelesaikan implementasi Django ORM dan relationship.",
                "grade": 87.50,
            },
        )
        self.stdout.write(f"- Submission by {student.username}: Grade {submission.grade}")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
