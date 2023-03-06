from rest_framework.viewsets import ModelViewSet

from .models import *

from cmsapp.api.serializers import *


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


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


# class AdvertisingSourceViewSet(ModelViewSet):
#     serializer_class = AdvertisingSourceSerializer
#     queryset = AdvertisingSource.objects.all()
#
#
# class RequestStatusViewSet(ModelViewSet):
#     serializer_class = RequestStatusSerializer
#     queryset = RequestStatus.objects.all()


class PaymentMethodViewSet(ModelViewSet):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
