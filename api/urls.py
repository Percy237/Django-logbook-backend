from django.urls import path
from . import views


urlpatterns = [
    path("course/", views.CourseListCreateView.as_view(), name="list-create-course"),
    path("class/", views.ClassListCreateView.as_view(), name="list-create-class"),
    path("userprofile/", views.ListAUserView.as_view(), name="user-account"),
    path(
        "classes/<int:class_id>/courses/",
        views.CourseListForAClassView.as_view(),
        name="class-courses-list",
    ),
]
