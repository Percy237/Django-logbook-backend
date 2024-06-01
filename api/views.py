from django.shortcuts import render
from .models import User, Course, Class, LogbookEntry
from rest_framework import generics
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    CourseSerializer,
    ClassSerializer,
    LogbookEntrySerializer,
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
        # Filter the users to return only the currently authenticated user
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
        return Course.objects.filter()


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

        serializer.save(course_id=course_id, created_by=self.request.user)
