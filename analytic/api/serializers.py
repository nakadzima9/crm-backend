from django.db.models import Count

from cmsapp.models import Student, DepartmentOfCourse
from rest_framework import serializers


class PopularDepartmentsSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = DepartmentOfCourse
        fields = ['name', 'quantity']

    def get_students(self, department):
        dep = DepartmentOfCourse.objects.get(name=department)
        return Student.objects.filter(department=dep, on_request=False, is_archive=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        queryset = self.get_students(instance)
        if queryset.exists():
            data['quantity'] = queryset.count()
        else:
            data['quantity'] = 0
        return data

    def get_total(self):
        return Student.objects.filter(on_request=False, is_archive=False).count()
