from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from datetime import date, datetime
from django.conf import settings


class CustomUserManager(UserManager):
    def create_user(
        self, email, date_of_birth, name, gender, class_enrolled=None, password=None
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            name=name,
            gender=gender,
            class_enrolled=class_enrolled,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, gender, date_of_birth=None, password=None):

        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth or date.today(),
            name=name,
            gender=gender,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255, blank=True, default="")
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, default="")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_delegate = models.BooleanField(default=False)
    class_enrolled = models.ForeignKey(
        "Class",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth", "name", "gender"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):

        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Course(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=30)
    courses = models.ManyToManyField(Course, related_name="class_courses")

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TeacherCourseHours(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    hours_taught = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.teacher.name} - {self.course.name}"


class LogbookEntry(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    text = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=2
    )

    def __str__(self):
        return f"Logbook Entry for {self.course.name} by {self.teacher.name}"


class File(models.Model):
    logbook_entry = models.ForeignKey(
        LogbookEntry, on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to="logbook_files/")

    def __str__(self):
        return f"File for Logbook Entry {self.logbook_entry.course}"
