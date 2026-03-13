from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone

from .models import Task, SubTask, Note, Category, Priority


def dashboard(request):
    tasks = Task.objects.select_related("category", "priority").all().order_by("-created_at")[:5]
    subtasks = SubTask.objects.select_related("parent_task").all().order_by("-created_at")[:5]
    notes = Note.objects.select_related("task").all().order_by("-created_at")[:5]

    total_tasks = Task.objects.count()
    in_progress_count = Task.objects.filter(status="In Progress").count()
    completed_count = Task.objects.filter(status="Completed").count()
    pending_count = Task.objects.filter(status="Pending").count()
    total_subtasks = SubTask.objects.count()
    total_notes = Note.objects.count()

    overdue_count = Task.objects.filter(
        deadline__lt=timezone.now()
    ).exclude(status="Completed").count()

    this_month_count = Task.objects.filter(
        created_at__month=timezone.now().month,
        created_at__year=timezone.now().year
    ).count()

    top_categories = Category.objects.annotate(task_count=Count("tasks")).order_by("-task_count", "name")
    priority_breakdown = Priority.objects.annotate(task_count=Count("tasks")).order_by("-task_count", "name")

    context = {
        "page_name": "dashboard",
        "tasks": tasks,
        "subtasks": subtasks,
        "notes": notes,
        "total_tasks": total_tasks,
        "in_progress_count": in_progress_count,
        "completed_count": completed_count,
        "pending_count": pending_count,
        "total_subtasks": total_subtasks,
        "total_notes": total_notes,
        "overdue_count": overdue_count,
        "this_month_count": this_month_count,
        "top_categories": top_categories,
        "priority_breakdown": priority_breakdown,
    }
    return render(request, "tasks/dashboard.html", context)


def task_list(request):
    tasks = Task.objects.select_related("category", "priority").all().order_by("-created_at")
    return render(request, "tasks/task_list.html", {
        "page_name": "tasks",
        "tasks": tasks,
    })


def subtask_list(request):
    subtasks = SubTask.objects.select_related("parent_task").all().order_by("-created_at")
    return render(request, "tasks/subtask_list.html", {
        "page_name": "subtasks",
        "subtasks": subtasks,
    })


def note_list(request):
    notes = Note.objects.select_related("task").all().order_by("-created_at")
    return render(request, "tasks/note_list.html", {
        "page_name": "notes",
        "notes": notes,
    })


def category_list(request):
    categories = Category.objects.annotate(task_count=Count("tasks")).order_by("name")
    return render(request, "tasks/category_list.html", {
        "page_name": "categories",
        "categories": categories,
    })


def priority_list(request):
    priorities = Priority.objects.annotate(task_count=Count("tasks")).order_by("name")
    return render(request, "tasks/priority_list.html", {
        "page_name": "priorities",
        "priorities": priorities,
    })