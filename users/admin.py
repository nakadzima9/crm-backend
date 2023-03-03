from django.contrib import admin
from users.models import User, OTP

admin.site.register(User)
admin.site.register(OTP)
