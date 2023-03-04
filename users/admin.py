from django.contrib import admin
from users.models import User, Mentor, OTP


class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'user_type',)

    def get_form(self, request, obj=User, **kwargs):
        if obj.user_type == 'mentor':
            self.exclude = ('password', 'last_login')
        elif 'password' in self.exclude:
            self.exclude = ('last_login',)
        form = super(StaffAdmin, self).get_form(request, obj, **kwargs)
        return form



class MentorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'department',)
    exclude = ('password', 'last_login', 'groups', 'user_permissions',)

admin.site.register(User, StaffAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(OTP)
