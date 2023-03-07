from rest_framework import serializers


def validate_phone(value):
    if not value[1:].isnumeric():
        raise serializers.ValidationError('Phone must be numeric symbols')
    if value[:4] != '+996':
        raise serializers.ValidationError('Phone number should start with +996 ')
    elif len(value) != 13:
        raise serializers.ValidationError("Phone number must be 13 characters long")
    return value
