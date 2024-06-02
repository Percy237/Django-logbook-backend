from datetime import datetime
from decimal import Decimal
from django.shortcuts import render
from .models import User, Course, Class, LogbookEntry, TeacherCourseHours, Teacher
from rest_framework import generics
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    CourseSerializer,
    ClassSerializer,
    LogbookEntrySerializer,
    TeacherSerializer,
    TeacherCourseHoursSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreateUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListAUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class CourseListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class ClassListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class CourseListForAClassView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        class_id = self.kwargs["class_id"]
        return Course.objects.filter(class_courses__id=class_id)


class ClassCourseListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class CourseListForAClassView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        class_enrolled = self.request.user.class_enrolled.id
        return Course.objects.filter(class_courses=class_enrolled)


class ClassCourseListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class LogbookEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = LogbookEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return LogbookEntry.objects.filter(course_id=course_id).order_by("created_at")

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_id")
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise serializer.ValidationError({"course": "Course not found"})

        teacher_id = serializer.validated_data["teacher"].id
        start_time = serializer.validated_data["start_time"]
        end_time = serializer.validated_data["end_time"]

        start = datetime.combine(datetime.today(), start_time)
        end = datetime.combine(datetime.today(), end_time)

        hours_taught = Decimal((end - start).total_seconds() / 3600)

        teacher_course_hours, created = TeacherCourseHours.objects.get_or_create(
            teacher_id=teacher_id, course_id=course_id
        )

        teacher_course_hours.hours_taught += hours_taught
        teacher_course_hours.save()

        serializer.save(course_id=course_id, created_by=self.request.user)


class TeacherListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return Teacher.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class TeacherCourseHoursListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherCourseHoursSerializer

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return TeacherCourseHours.objects.filter(course=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_id")
        teacher_id = self.request.data.get("teacher")
        try:
            course = Course.objects.get(pk=course_id)
            teacher = Teacher.objects.get(pk=teacher_id)
        except Course.DoesNotExist:
            raise serializer.ValidationError({"course": "Course not found"})
        except Teacher.DoesNotExist:
            raise serializer.ValidationError({"teacher": "Teacher not found"})

        # Check if the TeacherCourseHours already exists
        try:
            teacher_course_hours = TeacherCourseHours.objects.get(
                teacher=teacher, course=course
            )
            teacher_course_hours.hours_taught = serializer.validated_data.get(
                "hours_taught", 0
            )
            teacher_course_hours.save()
            serializer.instance = teacher_course_hours
        except TeacherCourseHours.DoesNotExist:
            serializer.save(teacher=teacher, course=course)


class TeacherUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class TeacherDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CourseUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ClassUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassSerializer
    queryset = Class.objects.all()


class ClassDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassSerializer
    queryset = Class.objects.all()
