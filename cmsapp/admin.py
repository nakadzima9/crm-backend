from django.contrib import admin

from .models import (
    AdvertisingSource,
    Classroom,
    DepartmentOfCourse,
    Group,
    GroupStatus,
    Payment,
    PaymentMethod,
    RequestStatus,
    ScheduleType,
    Student,
)


class AdvertisingSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class DepartmentOfCourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration_month', 'image', 'is_archive', 'description')


class GroupAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Group._meta.get_fields()]
    list_display = ['id', 'name', 'students_max', 'department', 'mentor', 'status', 'start_at_date', 'end_at_date',
                    'is_archive', 'month_from_start']


class GroupStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'client_card', 'course', 'last_payment_date', 'user',)


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class RequestStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class ScheduleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'start_time', 'end_time',)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'first_name', 'last_name', 'phone', 'came_from', 'on_request',
                    'notes', 'status', 'laptop', 'payment_method', 'is_archive', 'blacklist',
                    )


admin.site.register(AdvertisingSource, AdvertisingSourceAdmin)
admin.site.register(RequestStatus, RequestStatusAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(DepartmentOfCourse, DepartmentOfCourseAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupStatus, GroupStatusAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(ScheduleType, ScheduleTypeAdmin)
admin.site.register(Student, StudentAdmin)
