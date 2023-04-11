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


# class BlackListAdmin(admin.ModelAdmin):
#     list_display = ('id', 'student', 'reason', 'added_at',)


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class DepartmentOfCourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration_month', 'image', 'is_archive', 'description')


class GroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Group._meta.get_fields()]


class GroupStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'client_card', 'course', 'created_at', 'user',)


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class RequestStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class ScheduleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'start_time', 'end_time',)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'first_name', 'last_name', 'surname', 'phone', 'came_from',
                    'notes', 'status', 'laptop', 'payment_method', 'is_archive',
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
