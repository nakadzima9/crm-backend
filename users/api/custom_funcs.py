from datetime import date, timedelta
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from rest_framework.response import Response


def validate_phone(value):
    if not value[1:].isnumeric():
        raise serializers.ValidationError('Phone must be numeric symbols')
    if value[:4] != '+996':
        raise serializers.ValidationError('Phone number should start with +996 ')
    elif len(value) != 13:
        raise serializers.ValidationError("Phone number must be 13 characters long")
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


def get_token(user):
    refresh = RefreshToken.for_user(user)
    expires_in = refresh.access_token.lifetime.total_seconds()
    expires_day = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
    try:
        image_url = user.image.url
    except ValueError:
        image_url = "null"

    return Response(
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "image": image_url,
            'user_id': user.id,
            # "status": "You successfully logged in",
            "expires_day": expires_day,
            "is_superuser": user.is_superuser,
            "user_type": user.user_type,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    )
