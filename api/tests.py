from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Course, Class, Teacher, TeacherCourseHours, LogbookEntry, File
from datetime import date, time

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.password = "testpassword"
        self.date_of_birth = date(2000, 1, 1)
        self.name = "Test User"
        self.gender = "Male"
        self.class_enrolled = Class.objects.create(name="Class 1")

    def test_create_user(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            date_of_birth=self.date_of_birth,
            name=self.name,
            gender=self.gender,
            class_enrolled=self.class_enrolled,
        )
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(user.date_of_birth, self.date_of_birth)
        self.assertEqual(user.name, self.name)
        self.assertEqual(user.gender, self.gender)
        self.assertEqual(user.class_enrolled, self.class_enrolled)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email=self.email,
            password=self.password,
            name=self.name,
            date_of_birth=self.date_of_birth,
            gender=self.gender,
        )
        self.assertEqual(superuser.email, self.email)
        self.assertTrue(superuser.check_password(self.password))
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)

    def test_missing_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password=self.password,
                date_of_birth=self.date_of_birth,
                name=self.name,
                gender=self.gender,
                class_enrolled=self.class_enrolled,
            )

    def test_missing_required_fields(self):
        with self.assertRaises(TypeError):
            User.objects.create_user()

class CourseModelTest(TestCase):
    def test_create_course(self):
        course = Course.objects.create(name="Course 1")
        self.assertEqual(course.name, "Course 1")

    def test_str_representation(self):
        course = Course.objects.create(name="Course 1")
        self.assertEqual(str(course), "Course 1")

class ClassModelTest(TestCase):
    def test_create_class(self):
        class_instance = Class.objects.create(name="Class 1")
        self.assertEqual(class_instance.name, "Class 1")

    def test_add_courses_to_class(self):
        class_instance = Class.objects.create(name="Class 1")
        course1 = Course.objects.create(name="Course 1")
        course2 = Course.objects.create(name="Course 2")
        class_instance.courses.add(course1, course2)
        self.assertIn(course1, class_instance.courses.all())
        self.assertIn(course2, class_instance.courses.all())

    def test_str_representation(self):
        class_instance = Class.objects.create(name="Class 1")
        self.assertEqual(str(class_instance), "Class 1")

class TeacherModelTest(TestCase):
    def test_create_teacher(self):
        teacher = Teacher.objects.create(name="Teacher 1")
        self.assertEqual(teacher.name, "Teacher 1")

    def test_str_representation(self):
        teacher = Teacher.objects.create(name="Teacher 1")
        self.assertEqual(str(teacher), "Teacher 1")

class TeacherCourseHoursModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="Teacher 1")
        self.course = Course.objects.create(name="Course 1")

    def test_create_teacher_course_hours(self):
        tch = TeacherCourseHours.objects.create(
            teacher=self.teacher,
            course=self.course,
            hours_taught=10.5
        )
        self.assertEqual(tch.teacher, self.teacher)
        self.assertEqual(tch.course, self.course)
        self.assertEqual(tch.hours_taught, 10.5)

    def test_str_representation(self):
        tch = TeacherCourseHours.objects.create(
            teacher=self.teacher,
            course=self.course,
            hours_taught=10.5
        )
        self.assertEqual(str(tch), f"{self.teacher.name} - {self.course.name}")

class LogbookEntryModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="Teacher 1")
        self.course = Course.objects.create(name="Course 1")
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
            date_of_birth=date(1990, 1, 1),
            name="User",
            gender="Male"
        )

    def test_create_logbook_entry(self):
        logbook_entry = LogbookEntry.objects.create(
            start_time=time(9, 0),
            end_time=time(10, 0),
            text="Taught about Django.",
            course=self.course,
            teacher=self.teacher,
            created_by=self.user
        )
        self.assertEqual(logbook_entry.course, self.course)
        self.assertEqual(logbook_entry.teacher, self.teacher)
        self.assertEqual(logbook_entry.text, "Taught about Django.")
        self.assertEqual(logbook_entry.created_by, self.user)

    def test_str_representation(self):
        logbook_entry = LogbookEntry.objects.create(
            start_time=time(9, 0),
            end_time=time(10, 0),
            text="Taught about Django.",
            course=self.course,
            teacher=self.teacher,
            created_by=self.user
        )
        self.assertEqual(
            str(logbook_entry),
            f"Logbook Entry for {self.course.name} by {self.teacher.name}"
        )

class FileModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="Teacher 1")
        self.course = Course.objects.create(name="Course 1")
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
            date_of_birth=date(1990, 1, 1),
            name="User",
            gender="Male"
        )
        self.logbook_entry = LogbookEntry.objects.create(
            start_time=time(9, 0),
            end_time=time(10, 0),
            text="Taught about Django.",
            course=self.course,
            teacher=self.teacher,
            created_by=self.user
        )

    def test_create_file(self):
        test_file = SimpleUploadedFile("file.txt", b"file_content")
        file = File.objects.create(
            logbook_entry=self.logbook_entry,
            file=test_file
        )
        self.assertEqual(file.logbook_entry, self.logbook_entry)
        self.assertTrue(file.file.name.endswith("file.txt"))

    def test_str_representation(self):
        test_file = SimpleUploadedFile("file.txt", b"file_content")
        file = File.objects.create(
            logbook_entry=self.logbook_entry,
            file=test_file
        )
        self.assertEqual(
            str(file),
            f"File for Logbook Entry {self.logbook_entry.course}"
        )
