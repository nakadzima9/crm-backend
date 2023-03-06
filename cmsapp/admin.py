from django.contrib import admin

from .models import (
    # AdvertisingSource,
    # RequestStatus,
    Classroom,
    Course,
    Department,
    Group,
    GroupStatus,
    Payment,
    PaymentMethod,
    ScheduleType,
    Student,
)


class AdvertisingSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
#
#
# class BlackListAdmin(admin.ModelAdmin):
#     list_display = ('id', 'student', 'reason', 'added_at',)
#
#
# class RequestStatusAdmin(admin.ModelAdmin):
#     list_display = ('id', 'status',)
#
#
# class ClassroomAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)
#
#
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'started_at', 'duration_month',)
#
#
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)
#
#
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('id', 'number', 'students_max', 'status', 'created_at', 'course', 'schedule_type', 'classroom',)
#
#
# class GroupStatusAdmin(admin.ModelAdmin):
#     list_display = ('id', 'status_name',)
#
#
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'amount', 'client_card', 'created_at', 'user',)
#
#
# class PaymentMethodAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)
#
#
# class ScheduleTypeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'type_name', 'start_time', 'end_time',)
#
#
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone_number', 'group',)
#
#
# class StudentRequestAdmin(admin.ModelAdmin):
#     list_display = ('id', 'card_number', 'note', 'department', 'came_from', 'status', 'laptop', 'payment_method',)

# admin.site.register(AdvertisingSource)
# admin.site.register(RequestStatus)
admin.site.register(Classroom)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Group)
admin.site.register(GroupStatus)
admin.site.register(Payment)
admin.site.register(PaymentMethod)
admin.site.register(ScheduleType)
admin.site.register(Student)


# admin.site.register(AdvertisingSource, AdvertisingSourceAdmin)
# admin.site.register(RequestStatus, RequestStatusAdmin)
# admin.site.register(Classroom, ClassroomAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Department, DepartmentAdmin)
# admin.site.register(Group, GroupAdmin)
# admin.site.register(GroupStatus, GroupStatusAdmin)
# admin.site.register(Payment, PaymentAdmin)
# admin.site.register(PaymentMethod, PaymentMethodAdmin)
# admin.site.register(ScheduleType, ScheduleTypeAdmin)
# admin.site.register(Student, StudentAdmin)
# admin.site.register(StudentRequest, StudentRequestAdmin)
