from rest_framework import serializers
from just_visit import settings
from rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
from users.models import User


class PasswordResetSerializer(_PasswordResetSerializer):

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'EMAIL_HOST_USER'),

            'email_template_name': 'reset_password.html',

            'request': request
        }
        self.reset_form.save(**opts)

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError('Error')

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Invalid e-mail address')

        return value
