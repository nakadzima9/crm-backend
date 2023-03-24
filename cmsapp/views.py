from rest_framework.viewsets import ModelViewSet
from .permissions import IsManager, IsSuperUser
from cmsapp.models import (
    Department,
    GroupStatus,
    Classroom,
    Course,
    ScheduleType,
    Group,
    AdvertisingSource,
    RequestStatus,
    PaymentMethod,
    Student,
    Payment,
    Reason,
)

from cmsapp.api.serializers import (
    DepartmentSerializer,
    GroupStatusSerializer,
    ClassroomSerializer,
    CourseSerializer,
    CourseSerializerOnlyWithImage,
    ScheduleTypeSerializer,
    GroupSerializer,
    AdvertisingSourceSerializer,
    RequestStatusSerializer,
    PaymentMethodSerializer,
    StudentSerializer,
    PaymentSerializer,
    ReasonSerializer,
    StudentOnStudySerializer,
)
from rest_framework.parsers import MultiPartParser


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


class CourseImageUpdateViewSet(ModelViewSet):
    parser_classes = (MultiPartParser,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializerOnlyWithImage
    http_method_names = ['put', 'patch']


class ScheduleTypeViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = ScheduleTypeSerializer
    queryset = ScheduleType.objects.all()


class GroupViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class AdvertisingSourceViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = AdvertisingSourceSerializer
    queryset = AdvertisingSource.objects.all()


class RequestStatusViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = RequestStatusSerializer
    queryset = RequestStatus.objects.all()


class ReasonViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = ReasonSerializer
    queryset = Reason.objects.all()


class PaymentMethodViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()


class StudentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.filter(on_request=True)


class StudentOnStudyViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.filter(on_request=False)
    # queryset = Student.objects.all()
    serializer_class = StudentOnStudySerializer


class PaymentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
