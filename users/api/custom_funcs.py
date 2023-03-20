from datetime import date, timedelta

from django.utils import timezone
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from rest_framework.response import Response
from users.models import User


def validate_phone(self, value):
    if value is not None:
        if not value:
            return ""
        if not value[1:].isnumeric():
            raise serializers.ValidationError('Phone must be numeric symbols')
        if value[:4] != '+996':
            raise serializers.ValidationError('Phone number should start with +996 ')
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        if not self.partial and not self.instance:
            if User.objects.filter(phone=value).first():
                raise serializers.ValidationError("This number already exists in the system")
        return value


def validate_email(value):
    if value is None:
        raise serializers.ValidationError('Это поле не может быть пустым.')
    return value


def create(validated_data, model):
    password = validated_data.pop('password')
    user = model(**validated_data)
    user.set_password(password)
    user.save()
    return user


def validate(self, data, model, serializer):
    user = model(**data)
    password = data.get('password')
    errors = dict()
    try:
        validators.validate_password(password=password, user=user)
    except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)
    if errors:
        raise serializers.ValidationError(errors)
    return super(serializer, self).validate(data)


def password_reset_validate(self, data, serializer):
    password = data.get('password')
    repeat_password = data.pop('repeat_password')
    errors = dict()
    if password != repeat_password:
        raise serializers.ValidationError({"password": "Password fields didn't match."})

    try:
        validators.validate_password(password=password, user=self.instance)
    except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)
    if errors:
        raise serializers.ValidationError(errors)
    return super(serializer, self).validate(data)


def get_token(user):
    refresh = RefreshToken.for_user(user)
    expires_in = refresh.access_token.lifetime.total_seconds()
    print(expires_in)
    expires_day = (timezone.now() + datetime.timedelta(seconds=expires_in)).strftime('%d/%m/%Y %H:%M:%S')
    # try:
    #     image_url = user.image.url
    # except ValueError:
    #     image_url = "null"

    return Response(
        {
            'id': user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            # "image": image_url,
            "expires_day": expires_day,
            "user_type": user.user_type,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    )
