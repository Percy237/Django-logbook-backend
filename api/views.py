from django.shortcuts import render
from .models import User, Course, Class
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserSerializer, CourseSerializer, ClassSerializer
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
