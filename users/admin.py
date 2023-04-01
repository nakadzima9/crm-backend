from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, OTP #, UserImage
# from users.models import User, OTP #, UserImage


class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'user_type', 'is_active')
    exclude = ('password', 'username', 'last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_superuser',)
    # fieldsets = (
    #     (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'image',
    #                                      'description', 'sex', 'user_type', 'is_active')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'first_name', 'last_name',  'phone', 'image',
    #                    'description', 'sex', 'user_type', 'is_active',),
    #     }),
    # )


# class MentorAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'department',)
#     exclude = ('password', 'last_login', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_superuser',)


admin.site.register(User, StaffAdmin)
# admin.site.register(Mentor, MentorAdmin)
admin.site.register(OTP)
# admin.site.register(UserImage)
