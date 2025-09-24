from django.contrib import admin
from django.urls import path, include
from tasks.views import (
    home_view,
    signup_view,
    CustomLoginView,
    task_interface_view,
)

urlpatterns = [
    path(
        "admin/login/",
        CustomLoginView.as_view(template_name="admin/login.html"),
        name="admin_login",
    ),
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("signup/", signup_view, name="signup"),
    path("tasks/", task_interface_view, name="task_list"),
    path("api/", include("tasks.urls")),
]
