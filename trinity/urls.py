from django.urls import path

from .views import (
    add_activity,
    delete_activity,
    get_edit_activity_form,
    home,
    update_activity,
    update_activity_completed_status,
    update_activity_planned_status,
    save_comment
)

urlpatterns = [
    path("", home, name="home"),
    path("add_activity/", add_activity, name="add_activity"),
    path(
        "update_activity_completed_status",
        update_activity_completed_status,
        name="update_activity_completed_status",
    ),
    path(
        "get_edit_activity_form", get_edit_activity_form, name="get_edit_activity_form"
    ),
    path("update_activity", update_activity, name="update_activity"),
    path("delete_activity/", delete_activity, name="delete_activity"),
    path(
        "update_activity_planned_status",
        update_activity_planned_status,
        name="update_activity_planned_status",
    ),
    path('save_comment/', save_comment, name='save_comment'),
]
