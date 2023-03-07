from rest_framework.serializers import ModelSerializer
from cmsapp.models import (
    Department,
    GroupStatus,
    Classroom,
    Course,
    ScheduleType,
    Group,
    # AdvertisingSource,
    # RequestStatus,
    PaymentMethod,
    Student,
    Payment,
)
from .custom_funcs import validate_phone


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class GroupStatusSerializer(ModelSerializer):
    class Meta:
        model = GroupStatus
        fields = "__all__"


class ClassroomSerializer(ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class ScheduleTypeSerializer(ModelSerializer):
    class Meta:
        model = ScheduleType
        fields = "__all__"


class GroupSerializer(ModelSerializer):
    status = GroupStatusSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    schedule_type = ScheduleTypeSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'number', 'students_max', 'status', 'created_at', 'course', 'schedule_type', 'classroom']


# class AdvertisingSourceSerializer(ModelSerializer):
#     class Meta:
#         model = AdvertisingSource
#         fields = "__all__"
#
#
# class RequestStatusSerializer(ModelSerializer):
#     class Meta:
#         model = RequestStatus
#         fields = "__all__"


class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class StudentSerializer(ModelSerializer):
    department = DepartmentSerializer()
    payment_method = PaymentMethodSerializer()

    class Meta:
        model = Student
        depth = 1
        fields = [
            "id",
            "first_name",
            "last_name",
            "surname",
            "notes",
            "phone",
            "laptop",
            "department",
            "came_from",
            "payment_method",
            "status",
            "paid",
        ]

    def validate_phone(self, value):
        return validate_phone(value)

    def create(self, validated_data):
        department_data = validated_data.pop("department")["name"]
        payment_method_data = validated_data.pop("payment_method")["name"]
        dep = Department.objects.get(name=department_data)
        pay = PaymentMethod.objects.get(name=payment_method_data)
        student = Student(department=dep, payment_method=pay, **validated_data)
        student.save()
        return student


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
