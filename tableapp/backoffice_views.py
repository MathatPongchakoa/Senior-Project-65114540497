from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Booking, Menu, Order, Table, Zone


User = get_user_model()


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["food_name", "price", "category", "image"]
        widgets = {
            "food_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "ชื่ออาหาร"}),
            "price": forms.NumberInput(attrs={"class": "form-input", "min": "0", "step": "0.01"}),
            "category": forms.Select(attrs={"class": "form-input"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-input"}),
        }


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ["table_name", "table_status", "seating_capacity", "zone"]
        widgets = {
            "table_name": forms.TextInput(attrs={"class": "form-input"}),
            "table_status": forms.Select(attrs={"class": "form-input"}),
            "seating_capacity": forms.NumberInput(attrs={"class": "form-input", "min": "1"}),
            "zone": forms.Select(attrs={"class": "form-input"}),
        }


def _backoffice_context(request, **kwargs):
    return {"backoffice_user": request.user, **kwargs}


@staff_member_required(login_url="login")
def dashboard(request):
    today = timezone.localdate()
    today_bookings = Booking.objects.filter(booking_date=today)
    context = {
        "active_page": "dashboard",
        "today": today,
        "table_total": Table.objects.count(),
        "table_available": Table.objects.filter(table_status="available").count(),
        "table_booked": Table.objects.filter(table_status="booked").count(),
        "table_occupied": Table.objects.filter(table_status="occupied").count(),
        "booking_today_count": today_bookings.exclude(status="cancelled").count(),
        "booking_pending_count": Booking.objects.filter(status="pending").count(),
        "member_count": User.objects.count(),
        "menu_count": Menu.objects.count(),
        "recent_bookings": Booking.objects.select_related("table", "user").order_by("-booking_date", "-booking_time", "-id")[:8],
        "recent_orders": Order.objects.select_related("user").order_by("-created_at")[:5],
    }
    return render(request, "backoffice/dashboard.html", _backoffice_context(request, **context))


@staff_member_required(login_url="login")
def booking_list(request):
    bookings = Booking.objects.select_related("table", "user").order_by("-booking_date", "-booking_time", "-id")
    status = request.GET.get("status", "").strip()
    query = request.GET.get("q", "").strip()
    if status in {"pending", "occupied", "cancelled"}:
        bookings = bookings.filter(status=status)
    if query:
        bookings = bookings.filter(
            Q(table__table_name__icontains=query)
            | Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
        )
    return render(request, "backoffice/bookings.html", _backoffice_context(
        request, active_page="bookings", bookings=bookings, selected_status=status, query=query
    ))


@staff_member_required(login_url="login")
@require_POST
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking.objects.select_related("table"), pk=booking_id)
    new_status = request.POST.get("status", "")
    valid_statuses = {choice[0] for choice in Booking._meta.get_field("status").choices}
    if new_status not in valid_statuses:
        messages.error(request, "สถานะการจองไม่ถูกต้อง")
        return redirect("backoffice:bookings")

    booking.status = new_status
    booking.save()

    # Booking.save() updates the table too; recalculate to respect other active bookings.
    table = booking.table
    active_bookings = Booking.objects.filter(table=table, status__in=["pending", "occupied"])
    if active_bookings.filter(status="occupied").exists():
        table.table_status = "occupied"
    elif active_bookings.filter(status="pending").exists():
        table.table_status = "booked"
    else:
        table.table_status = "available"
    table.save(update_fields=["table_status"])

    messages.success(request, f"อัปเดตสถานะการจองโต๊ะ {table.table_name} แล้ว")
    return redirect("backoffice:bookings")


@staff_member_required(login_url="login")
def table_list(request):
    tables = Table.objects.select_related("zone").order_by("id")
    return render(request, "backoffice/tables.html", _backoffice_context(
        request, active_page="tables", tables=tables
    ))


@staff_member_required(login_url="login")
def table_form(request, table_id=None):
    instance = get_object_or_404(Table, pk=table_id) if table_id else None
    form = TableForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        table = form.save()
        messages.success(request, f"บันทึกข้อมูลโต๊ะ {table.table_name} แล้ว")
        return redirect("backoffice:tables")
    return render(request, "backoffice/table_form.html", _backoffice_context(
        request, active_page="tables", form=form, table=instance
    ))


@staff_member_required(login_url="login")
def menu_list(request):
    menus = Menu.objects.select_related("category").order_by("category__name", "food_name")
    query = request.GET.get("q", "").strip()
    if query:
        menus = menus.filter(Q(food_name__icontains=query) | Q(category__name__icontains=query))
    return render(request, "backoffice/menus.html", _backoffice_context(
        request, active_page="menus", menus=menus, query=query
    ))


@staff_member_required(login_url="login")
def menu_form(request, menu_id=None):
    instance = get_object_or_404(Menu, pk=menu_id) if menu_id else None
    form = MenuForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        menu = form.save()
        messages.success(request, f"บันทึกเมนู {menu.food_name} แล้ว")
        return redirect("backoffice:menus")
    return render(request, "backoffice/menu_form.html", _backoffice_context(
        request, active_page="menus", form=form, menu=instance
    ))


@staff_member_required(login_url="login")
@require_POST
def menu_delete(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    name = menu.food_name
    menu.delete()
    messages.success(request, f"ลบเมนู {name} แล้ว")
    return redirect("backoffice:menus")


@staff_member_required(login_url="login")
def member_list(request):
    members = User.objects.order_by("-date_joined")
    query = request.GET.get("q", "").strip()
    if query:
        members = members.filter(
            Q(username__icontains=query)
            | Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
    return render(request, "backoffice/members.html", _backoffice_context(
        request, active_page="members", members=members, query=query
    ))


@staff_member_required(login_url="login")
@require_POST
def update_member(request, user_id):
    # Only superusers may change staff/active permissions.
    if not request.user.is_superuser:
        messages.error(request, "เฉพาะ Superuser เท่านั้นที่จัดการสิทธิ์สมาชิกได้")
        return redirect("backoffice:members")

    member = get_object_or_404(User, pk=user_id)
    if member.pk == request.user.pk and request.POST.get("action") == "deactivate":
        messages.error(request, "ไม่สามารถปิดใช้งานบัญชีของตัวเองได้")
        return redirect("backoffice:members")

    action = request.POST.get("action")
    if action == "toggle_staff":
        if member.is_superuser:
            messages.error(request, "ไม่สามารถเปลี่ยนสิทธิ์ Superuser ผ่านหน้านี้ได้")
        else:
            member.is_staff = not member.is_staff
            member.save(update_fields=["is_staff"])
            messages.success(request, "อัปเดตสิทธิ์พนักงานแล้ว")
    elif action == "toggle_active":
        if member.is_superuser:
            messages.error(request, "ไม่สามารถปิดใช้งาน Superuser ผ่านหน้านี้ได้")
        else:
            member.is_active = not member.is_active
            member.save(update_fields=["is_active"])
            messages.success(request, "อัปเดตสถานะบัญชีแล้ว")
    else:
        messages.error(request, "คำสั่งไม่ถูกต้อง")

    return redirect("backoffice:members")
