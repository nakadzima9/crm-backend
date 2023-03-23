from django.contrib import admin

from .models import (
    AdvertisingSource,
    Classroom,
    Course,
    Department,
    Group,
    GroupStatus,
    Payment,
    PaymentMethod,
    Reason,
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


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'duration_month', 'image', 'get_mentors', 'archived')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'students_max', 'status', 'created_at', 'schedule_type', 'classroom',)


class GroupStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'client_card', 'created_at', 'user',)


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class ReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class RequestStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class ScheduleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'start_time', 'end_time',)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'first_name', 'last_name', 'surname', 'phone', 'came_from',
                    'notes', 'status', 'laptop', 'payment_method',
                    )


admin.site.register(AdvertisingSource, AdvertisingSourceAdmin)
admin.site.register(Reason, ReasonAdmin)
admin.site.register(RequestStatus, RequestStatusAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Course, CourseAdmin)
# admin.site.register(Course)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupStatus, GroupStatusAdmin)
admin.site.register(Payment, PaymentAdmin)
# admin.site.register(Payment)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(ScheduleType, ScheduleTypeAdmin)
admin.site.register(Student, StudentAdmin)
