from rest_framework import serializers
from cmsapp.models import Student


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
            if Student.objects.filter(phone=value).first():
                raise serializers.ValidationError("This number already exists in the system")
        return value
