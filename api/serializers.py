from rest_framework import serializers
from .models import User, Course, Class, File, LogbookEntry


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name"]


class ClassSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ["id", "name", "courses"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "date_of_birth",
            "gender",
            "password",
            "is_delegate",
            "class_enrolled",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["id", "logbook_entry", "file"]


class LogbookEntrySerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    files = FileSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = LogbookEntry
        fields = [
            "id",
            "start_time",
            "end_time",
            "text",
            "course_name",
            "created_at",
            "files",
            "uploaded_files",
        ]

    def create(self, validated_data):
        uploaded_files = validated_data.pop("uploaded_files", [])
        logbook_entry = LogbookEntry.objects.create(**validated_data)
        for file in uploaded_files:
            File.objects.create(logbook_entry=logbook_entry, file=file)
        return logbook_entry

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["uploaded_files"] = FileSerializer(
            instance.files.all(), many=True
        ).data
        return representation
    
