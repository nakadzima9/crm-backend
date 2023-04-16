from cmsapp.models import Student, DepartmentOfCourse, AdvertisingSource, RequestStatus
from rest_framework import serializers
from analytic.models import DeletionReason
from cmsapp.models RequestStatus


class PopularDepartmentsSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = DepartmentOfCourse
        fields = ['name', 'quantity']

    def get_students(self, department):
        dep = DepartmentOfCourse.objects.filter(name=department).first()
        return Student.objects.filter(department=dep, on_request=False, is_archive=False, blacklist=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        queryset = self.get_students(instance)
        if queryset.exists():
            data['quantity'] = queryset.count()
        else:
            data['quantity'] = 0
        return data

    def get_total(self):
        return Student.objects.filter(on_request=False, is_archive=False, blacklist=False).count()


class PopularSourceSerializer(serializers.ModelSerializer):
    percent_value = serializers.FloatField(read_only=True)

    class Meta:
        model = AdvertisingSource
        fields = ['name', 'percent_value']

    def get_students(self, source):
        sc = AdvertisingSource.objects.filter(name=source).first()
        return Student.objects.filter(came_from=sc, on_request=False, is_archive=False, blacklist=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        queryset = self.get_students(instance)
        quantity = self.get_percent_value(queryset.count())
        if queryset.exists():
            data['percent_value'] = quantity
        else:
            data['percent_value'] = 0
        return data

    def get_percent_value(self, quantity):
        return round(quantity / Student.objects.filter(
            on_request=False,
            is_archive=False,
            blacklist=False
        ).count() * 100, 1)


class ReasonPercentSerializer(serializers.ModelSerializer):
    percent_value = serializers.FloatField(read_only=True)

    class Meta:
        model = DeletionReason
        fields = ['reason', 'percent_value']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        current_quantity = instance.student_count
        total = self.get_total_values()
        if total > 0:
            data['percent_value'] = round(current_quantity / total * 100, 1)
        else:
            data['percent_value'] = 100
        return data

    def get_total_values(self):
        total = 0
        queryset = DeletionReason.objects.all()
        for _ in queryset:
            total += _.student_count
        return total


class RequestStatusesCounterSerializer(ModelSerializer):
    departments = PopularDepartmentsSerializer()

    class Meta:
        model = RequestStatus
        fields = ['name', 'departments']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['departments'] = PopularDepartmentsSerializer()
        return data
  