from django.urls import path

from . import backoffice_views as views

app_name = "backoffice"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("bookings/", views.booking_list, name="bookings"),
    path("bookings/<int:booking_id>/status/", views.update_booking_status, name="update_booking_status"),
    path("tables/", views.table_list, name="tables"),
    path("tables/add/", views.table_form, name="table_add"),
    path("tables/<int:table_id>/edit/", views.table_form, name="table_edit"),
    path("menus/", views.menu_list, name="menus"),
    path("menus/add/", views.menu_form, name="menu_add"),
    path("menus/<int:menu_id>/edit/", views.menu_form, name="menu_edit"),
    path("menus/<int:menu_id>/delete/", views.menu_delete, name="menu_delete"),
    path("members/", views.member_list, name="members"),
    path("members/<int:user_id>/update/", views.update_member, name="member_update"),
]
