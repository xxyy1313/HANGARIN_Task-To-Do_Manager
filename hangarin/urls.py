from tasks.views import profile_settings
from django.contrib import admin
from django.urls import path, include
from tasks.views import (
    login_view, register_view,logout_view,
    dashboard,

    task_list, task_create, task_update, task_delete,
    subtask_list, subtask_create, subtask_update, subtask_delete,
    note_list, note_create, note_update, note_delete,
    category_list, category_create, category_update, category_delete,
    priority_list, priority_create, priority_update, priority_delete,
)

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path('', include('pwa.urls')),

    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),

    path("", dashboard, name="dashboard"),

    path("tasks/", task_list, name="task_list"),
    path("tasks/create/", task_create, name="task_create"),
    path("tasks/<int:pk>/edit/", task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", task_delete, name="task_delete"),

    path("subtasks/", subtask_list, name="subtask_list"),
    path("subtasks/create/", subtask_create, name="subtask_create"),
    path("subtasks/<int:pk>/edit/", subtask_update, name="subtask_update"),
    path("subtasks/<int:pk>/delete/", subtask_delete, name="subtask_delete"),

    path("notes/", note_list, name="note_list"),
    path("notes/create/", note_create, name="note_create"),
    path("notes/<int:pk>/edit/", note_update, name="note_update"),
    path("notes/<int:pk>/delete/", note_delete, name="note_delete"),

    path("categories/", category_list, name="category_list"),
    path("categories/create/", category_create, name="category_create"),
    path("categories/<int:pk>/edit/", category_update, name="category_update"),
    path("categories/<int:pk>/delete/", category_delete, name="category_delete"),

    path("priorities/", priority_list, name="priority_list"),
    path("priorities/create/", priority_create, name="priority_create"),
    path("priorities/<int:pk>/edit/", priority_update, name="priority_update"),
    path("priorities/<int:pk>/delete/", priority_delete, name="priority_delete"),

    path("settings/", profile_settings, name="profile_settings"),

    path("admin/", admin.site.urls),
]