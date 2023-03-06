from rest_framework.viewsets import ModelViewSet
from .permissions import IsManager, IsUser, IsSuperUser
from .models import *

from cmsapp.api.serializers import *


class DepartmentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class GroupStatusViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = GroupStatusSerializer
    queryset = GroupStatus.objects.all()


class ClassroomViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()


class CourseViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ScheduleTypeViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = ScheduleTypeSerializer
    queryset = ScheduleType.objects.all()


class GroupViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
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
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()


class StudentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class PaymentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
