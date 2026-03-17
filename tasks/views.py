from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required



from .models import Task, SubTask, Note, Category, Priority
from .forms import TaskForm, SubTaskForm, NoteForm, CategoryForm, PriorityForm, RegisterForm

@login_required
def profile_settings(request):
    return render(request, "tasks/profile_settings.html", {
        "page_name": "settings",
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        login_input = request.POST.get("login_input")
        password = request.POST.get("password")

        user = authenticate(request, username=login_input, password=password)

        if user is None:
            try:
                found_user = User.objects.get(email=login_input)
                user = authenticate(request, username=found_user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username/email or password.")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

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

    overdue_count = Task.objects.filter(deadline__lt=timezone.now()).exclude(status="Completed").count()

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

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()
    priority_filter = request.GET.get("priority", "").strip()
    category_filter = request.GET.get("category", "").strip()

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    if priority_filter:
        tasks = tasks.filter(priority__id=priority_filter)

    if category_filter:
        tasks = tasks.filter(category__id=category_filter)

    categories = Category.objects.all().order_by("name")
    priorities = Priority.objects.all().order_by("name")
    statuses = ["Pending", "In Progress", "Completed"]

    return render(request, "tasks/task_list.html", {
        "page_name": "tasks",
        "tasks": tasks,
        "categories": categories,
        "priorities": priorities,
        "statuses": statuses,
        "search_query": search_query,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "category_filter": category_filter,
    })


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/form.html", {
        "page_name": "tasks",
        "title": "Create Task",
        "form": form,
    })


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        deadline_value = task.deadline.strftime("%Y-%m-%dT%H:%M") if task.deadline else ""
        form = TaskForm(instance=task)
        form.fields["deadline"].widget.attrs["value"] = deadline_value

    return render(request, "tasks/form.html", {
        "page_name": "tasks",
        "title": "Edit Task",
        "form": form,
    })


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/confirm_delete.html", {
        "page_name": "tasks",
        "title": "Delete Task",
        "object": task,
        "cancel_url": "task_list",
    })


def subtask_list(request):
    subtasks = SubTask.objects.select_related("parent_task").all().order_by("-created_at")

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()

    if search_query:
        subtasks = subtasks.filter(
            Q(title__icontains=search_query) |
            Q(parent_task__title__icontains=search_query)
        )

    if status_filter:
        subtasks = subtasks.filter(status=status_filter)

    statuses = ["Pending", "In Progress", "Completed"]

    return render(request, "tasks/subtask_list.html", {
        "page_name": "subtasks",
        "subtasks": subtasks,
        "statuses": statuses,
        "search_query": search_query,
        "status_filter": status_filter,
    })


def subtask_create(request):
    if request.method == "POST":
        form = SubTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subtask_list")
    else:
        form = SubTaskForm()

    return render(request, "tasks/form.html", {
        "page_name": "subtasks",
        "title": "Create Sub Task",
        "form": form,
    })


def subtask_update(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)

    if request.method == "POST":
        form = SubTaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect("subtask_list")
    else:
        form = SubTaskForm(instance=subtask)

    return render(request, "tasks/form.html", {
        "page_name": "subtasks",
        "title": "Edit Sub Task",
        "form": form,
    })


def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)

    if request.method == "POST":
        subtask.delete()
        return redirect("subtask_list")

    return render(request, "tasks/confirm_delete.html", {
        "page_name": "subtasks",
        "title": "Delete Sub Task",
        "object": subtask,
        "cancel_url": "subtask_list",
    })


def note_list(request):
    notes = Note.objects.select_related("task").all().order_by("-created_at")

    search_query = request.GET.get("q", "").strip()
    created_filter = request.GET.get("created_at", "").strip()

    if search_query:
        notes = notes.filter(
            Q(content__icontains=search_query) |
            Q(task__title__icontains=search_query)
        )

    now = timezone.now()

    if created_filter == "today":
        notes = notes.filter(created_at__date=now.date())
    elif created_filter == "week":
        notes = notes.filter(created_at__gte=now - timedelta(days=7))
    elif created_filter == "month":
        notes = notes.filter(created_at__year=now.year, created_at__month=now.month)

    return render(request, "tasks/note_list.html", {
        "page_name": "notes",
        "notes": notes,
        "search_query": search_query,
        "created_filter": created_filter,
    })

def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm()

    return render(request, "tasks/form.html", {
        "page_name": "notes",
        "title": "Create Note",
        "form": form,
    })


def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm(instance=note)

    return render(request, "tasks/form.html", {
        "page_name": "notes",
        "title": "Edit Note",
        "form": form,
    })


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        note.delete()
        return redirect("note_list")

    return render(request, "tasks/confirm_delete.html", {
        "page_name": "notes",
        "title": "Delete Note",
        "object": note,
        "cancel_url": "note_list",
    })


def category_list(request):
    categories = Category.objects.annotate(task_count=Count("tasks")).order_by("name")

    search_query = request.GET.get("q", "").strip()

    if search_query:
        categories = categories.filter(name__icontains=search_query)

    return render(request, "tasks/category_list.html", {
        "page_name": "categories",
        "categories": categories,
        "search_query": search_query,
    })


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm()

    return render(request, "tasks/form.html", {
        "page_name": "categories",
        "title": "Create Category",
        "form": form,
    })


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)

    return render(request, "tasks/form.html", {
        "page_name": "categories",
        "title": "Edit Category",
        "form": form,
    })


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect("category_list")

    return render(request, "tasks/confirm_delete.html", {
        "page_name": "categories",
        "title": "Delete Category",
        "object": category,
        "cancel_url": "category_list",
    })


def priority_list(request):
    priorities = Priority.objects.annotate(task_count=Count("tasks")).order_by("name")

    search_query = request.GET.get("q", "").strip()

    if search_query:
        priorities = priorities.filter(name__icontains=search_query)

    return render(request, "tasks/priority_list.html", {
        "page_name": "priorities",
        "priorities": priorities,
        "search_query": search_query,
    })

def priority_create(request):
    if request.method == "POST":
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("priority_list")
    else:
        form = PriorityForm()

    return render(request, "tasks/form.html", {
        "page_name": "priorities",
        "title": "Create Priority",
        "form": form,
    })


def priority_update(request, pk):
    priority = get_object_or_404(Priority, pk=pk)

    if request.method == "POST":
        form = PriorityForm(request.POST, instance=priority)
        if form.is_valid():
            form.save()
            return redirect("priority_list")
    else:
        form = PriorityForm(instance=priority)

    return render(request, "tasks/form.html", {
        "page_name": "priorities",
        "title": "Edit Priority",
        "form": form,
    })


def priority_delete(request, pk):
    priority = get_object_or_404(Priority, pk=pk)

    if request.method == "POST":
        priority.delete()
        return redirect("priority_list")

    return render(request, "tasks/confirm_delete.html", {
        "page_name": "priorities",
        "title": "Delete Priority",
        "object": priority,
        "cancel_url": "priority_list",
    })