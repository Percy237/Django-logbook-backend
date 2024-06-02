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
)
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreateUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
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

class TeacherUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class TeacherDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
