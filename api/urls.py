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
        "teacher-course-hour/<int:course_id>/",
        views.TeacherCourseHoursListCreateView.as_view(),
        name="teacher-course-hour",
    ),
    path(
        "teacher/",
        views.TeacherListCreateView.as_view(),
        name="teacher-list-create",
    ),
    path(
        "teacher/",
        views.TeacherListCreateView.as_view(),
        name="teacher-list-create",
    ),
    path(
        "teachers/<int:pk>/update/",
        views.TeacherUpdateView.as_view(),
        name="teacher-update",
    ),
    path(
        "teachers/<int:pk>/delete/",
        views.TeacherDeleteView.as_view(),
        name="teacher-delete",
    ),
    path(
        "class/<int:pk>/update/",
        views.ClassUpdateView.as_view(),
        name="class-update",
    ),
    path(
        "class/<int:pk>/delete/",
        views.ClassDeleteView.as_view(),
        name="class-delete",
    ),
    path(
        "course/<int:pk>/update/",
        views.CourseUpdateView.as_view(),
        name="course-update",
    ),
    path(
        "course/<int:pk>/delete/",
        views.CourseDeleteView.as_view(),
        name="course-delete",
    ),
    path(
        "user/<int:pk>/update/",
        views.UserUpdateView.as_view(),
        name="user-update",
    ),
    path(
        "user/<int:pk>/delete/",
        views.UserDeleteView.as_view(),
        name="user-delete",
    ),
]
