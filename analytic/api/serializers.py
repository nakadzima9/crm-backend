from cmsapp.models import Student, DepartmentOfCourse, AdvertisingSource, RequestStatus
from rest_framework import serializers
from analytic.models import DeletionReason
from cmsapp.models import RequestStatus
from django.db.models import Count, Q


class PopularDepartmentsSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = DepartmentOfCourse
        fields = ['name', 'quantity', 'color']

    def get_queryset(self):
        # Используем annotate для добавления поля num_students в queryset
        queryset = DepartmentOfCourse.objects.annotate(num_students=Count('student', 
            filter=Q(
                student__on_request=False, 
                student__is_archive=False, 
                student__blacklist=False
                )
            )
        )
        return queryset

    def to_representation(self, instance):
        data = super().to_representation(instance)
        queryset = self.get_queryset()
        department = queryset.get(name=data['name'])
        data['quantity'] = department.num_students
        return data


class PopularSourceSerializer(serializers.ModelSerializer):
    percent_value = serializers.FloatField(read_only=True)

    class Meta:
        model = AdvertisingSource
        fields = ['name', 'percent_value', 'color']

    def get_students(self, source):
        sc = AdvertisingSource.objects.filter(name=source).first()
        return Student.objects.filter(came_from=sc, is_archive=False, blacklist=False)

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
            is_archive=False,
            blacklist=False
        ).count() * 100, 1)


class ReasonPercentSerializer(serializers.ModelSerializer):
    percent_value = serializers.FloatField(read_only=True)

    class Meta:
        model = DeletionReason
        fields = ['reason', 'percent_value', 'color']

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


class DepartmentSerializer(serializers.ModelSerializer):
    num_students = serializers.IntegerField(default=0)

    class Meta:
        model = DepartmentOfCourse
        fields = ['name', 'num_students', 'color']


class RequestStatusesCounterSerializer(serializers.ModelSerializer):
    departments = serializers.SerializerMethodField()

    class Meta:
        model = RequestStatus
        fields = ['name', 'departments']

    def get_departments(self, obj):
        popular_departments = DepartmentOfCourse.objects.annotate(
            num_students=Count('student', 
                filter=Q(
                    student__on_request=True, 
                    student__is_archive=False, 
                    student__blacklist=False,
                    student__status=obj,
                )
            )
        )
        serializer = DepartmentSerializer(popular_departments, many=True)
        return serializer.data
  