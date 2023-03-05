from rest_framework.serializers import ModelSerializer
from cmsapp.models import (
    Department,
    Teacher,
    GroupStatus,
    Classroom,
    Course,
    ScheduleType,
    Group,
    AdvertisingSource,
    CardStatus,
    PaymentMethod,
    Student,
    StudentCard,
    Payment,
    BlackList,
)


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
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


class AdvertisingSourceSerializer(ModelSerializer):
    class Meta:
        model = AdvertisingSource
        fields = "__all__"


class CardStatusSerializer(ModelSerializer):
    class Meta:
        model = CardStatus
        fields = "__all__"


class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class StudentCardSerializer(ModelSerializer):
    class Meta:
        model = StudentCard
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class BlackListSerializer(ModelSerializer):
    class Meta:
        model = BlackList
        fields = "__all__"
