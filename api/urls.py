from django.urls import path
from . import views


urlpatterns = [
    path("course/", views.CourseListCreateView.as_view(), name="list-create-course"),
    path("class/", views.ClassListCreateView.as_view(), name="list-create-class"),
    path("userprofile/", views.ListAUserView.as_view(), name="user-account"),
    path(
        "class/courses/",
        views.CourseListForAClassView.as_view(),
        name="class-courses-list",
    ),
    path(
        "courses/<int:course_id>/logbook-entries/",
        views.LogbookEntryListCreateView.as_view(),
        name="logbook-entry-create",
    ),
    path(
        "teacher/",
        views.TeacherListCreateView.as_view(),
        name="teacher-list-create",
    ),
]
