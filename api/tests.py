from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Course, Class

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

    # def test_create_superuser(self):
    #     superuser = User.objects.create_superuser(
    #         email=self.email,
    #         password=self.password,
    #         name=self.name,
    #     )
    #     self.assertEqual(superuser.email, self.email)
    #     self.assertTrue(superuser.check_password(self.password))
    #     self.assertTrue(superuser.is_admin)

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

