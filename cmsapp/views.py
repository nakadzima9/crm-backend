from rest_framework.viewsets import ModelViewSet

from .models import *

from cmsapp.api.serializers import *


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class GroupStatusViewSet(ModelViewSet):
    serializer_class = GroupStatusSerializer
    queryset = GroupStatus.objects.all()


class ClassroomViewSet(ModelViewSet):
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ScheduleTypeViewSet(ModelViewSet):
    serializer_class = ScheduleTypeSerializer
    queryset = ScheduleType.objects.all()


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class AdvertisingSourceViewSet(ModelViewSet):
    serializer_class = AdvertisingSourceSerializer
    queryset = AdvertisingSource.objects.all()


class CardStatusViewSet(ModelViewSet):
    serializer_class = CardStatusSerializer
    queryset = CardStatus.objects.all()


class PaymentMethodViewSet(ModelViewSet):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class StudentCardViewSet(ModelViewSet):
    serializer_class = StudentCardSerializer
    queryset = StudentCard.objects.all()


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class BlackListViewSet(ModelViewSet):
    serializer_class = BlackListSerializer
    queryset = BlackList.objects.all()
