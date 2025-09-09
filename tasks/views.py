from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from .models import Task

from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    tasks = Task.objects.all()
    return render(request, "tasks/index.html", {"tasks": tasks})


def _render_list(request, qs=None):
    tasks = qs if qs is not None else Task.objects.all()
    return render(request, "tasks/_task_list.html", {"tasks": tasks})


def _render_item(request, task):
    return render(request, "tasks/_task_item.html", {"t": task})


def create_task(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    title = (request.POST.get("title") or "").strip()
    details = (request.POST.get("details") or "").strip()
    priority = int(request.POST.get("priority") or 1)
    if not title:
        return HttpResponseBadRequest("Title required")
    t = Task.objects.create(title=title, details=details, priority=priority)
    # Return a single <li> to append
    return _render_item(request, t)


def toggle_task(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    t = get_object_or_404(Task, pk=pk)
    t.is_done = not t.is_done
    t.save(update_fields=["is_done"])
    # Replace the current <li> with updated markup
    return _render_item(request, t)


def update_task(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    t = get_object_or_404(Task, pk=pk)
    t.title = (request.POST.get("title") or "").strip() or t.title
    t.details = (request.POST.get("details") or "").strip()
    t.priority = int(request.POST.get("priority") or t.priority)
    t.save()
    return _render_item(request, t)  # outerHTML swap on closest li


def delete_task(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    t = get_object_or_404(Task, pk=pk)
    t.delete()
    # If HTMX, return empty string so hx-swap="delete" removes the li
    if getattr(request, "htmx", False):
        return HttpResponse("")
    # Non-HTMX fallback: re-render full list
    return _render_list(request)


def search_tasks(request):
    q = (request.GET.get("q") or "").strip()
    done = request.GET.get("done_only")
    qs = Task.objects.all()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(details__icontains=q))
    if done:
        qs = qs.filter(is_done=True)
    return _render_list(request, qs)


def task_detail(request, pk):
    t = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/_task_detail.html", {"t": t})
