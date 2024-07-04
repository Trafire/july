from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Activities


def home(request):
    activities_list = Activities.objects.all().order_by("-planned", "description", "name")
    paginator = Paginator(activities_list, 10000)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home.html",
        {"page_obj": page_obj, "dares_rating": calculate_completed_activities_rating()},
    )


def calculate_completed_activities_rating():
    completed_activities = Activities.objects.filter(completed=True)
    total_rating = completed_activities.aggregate(Sum("daring_rating"))[
        "daring_rating__sum"
    ]
    return total_rating or 0


def add_activity(request):
    if request.method == "POST":
        name = request.POST["name"]
        daring_rating = request.POST["daring_rating"]
        location = request.POST["location"]
        date_time = request.POST["date_time"] or None
        description = request.POST["description"]
        cost = request.POST["cost"] or 0

        completed = False

        activity = Activities(
            name=name,
            location=location,
            date_time=date_time,
            description=description,
            cost=cost,
            daring_rating=daring_rating,
            completed=completed,
        )
        activity.save()

    activities_list = Activities.objects.all().order_by("-planned", "description", "name")
    paginator = Paginator(activities_list, 10000)  # Show 10 activities per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home.html",
        {"page_obj": page_obj, "dares_rating": calculate_completed_activities_rating()},
    )


@csrf_exempt
def update_activity_completed_status(request):
    if request.method == "POST":
        activity_id = request.POST.get("id")
        completed = request.POST.get("completed")

        activity = Activities.objects.get(id=activity_id)
        activity.completed = bool(int(completed))
        activity.save()
        total_rating = calculate_completed_activities_rating()
        return JsonResponse({"success": True, "total_rating": total_rating})
    return JsonResponse({"success": False})


def get_edit_activity_form(request):
    activity_id = request.GET.get("id")
    activity = Activities.objects.get(id=activity_id)
    total_rating = calculate_completed_activities_rating()
    return render(
        request, "edit_form.html", {"activity": activity, "total_rating": total_rating}
    )


@csrf_exempt
def update_activity(request):
    if request.method == "POST":
        planned = request.POST.get("planned") == "true"
        activity_id = request.POST.get("id")
        name = request.POST.get("name")
        location = request.POST.get("location")
        date_time = request.POST.get("date_time")
        description = request.POST.get("description")
        cost = request.POST.get("cost")
        daring_rating = request.POST.get("daring_rating")
        completed = request.POST.get("completed")

        activity = Activities.objects.get(id=activity_id)
        activity.name = name
        activity.location = location
        activity.date_time = date_time
        activity.description = description
        activity.cost = cost
        activity.daring_rating = daring_rating
        activity.completed = bool(int(completed))
        activity.planned = planned
        activity.save()
        total_rating = calculate_completed_activities_rating()
        return JsonResponse({"success": True, "total_rating": total_rating})

    return JsonResponse({"success": False})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_activity(request):
    activity_id = request.GET.get("id")
    try:
        activity = Activities.objects.get(id=activity_id)
        activity.delete()
        return JsonResponse({"success": True}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Activity does not exist"}, status=404
        )


@csrf_exempt
def update_activity_planned_status(request):
    if request.method == "POST":
        activity_id = request.POST.get("id")
        planned = request.POST.get("planned")

        activity = Activities.objects.get(id=activity_id)
        activity.planned = bool(int(planned))
        activity.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@csrf_exempt
def save_comment(request):
    if request.method == "POST":
        activity_id = request.POST.get("id")
        comment_text = request.POST.get("comment")
        try:
            activity = Activities.objects.get(id=activity_id)
            # Assuming your model has a field named 'comment'
            activity.comment = comment_text
            activity.save()
            return JsonResponse({"success": True, "message": "Comment saved successfully"})
        except Activities.DoesNotExist:
            return JsonResponse({"success": False, "message": "Activity not found"})
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)
