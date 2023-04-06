from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .permissions import IsManager, IsSuperUser
from cmsapp.models import (
    DepartmentOfCourse,
    GroupStatus,
    Classroom,
    # Course,
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
    DepartmentSerializerOnlyWithImage,
    GroupStatusSerializer,
    ClassroomSerializer,
    ScheduleTypeSerializer,
    GroupSerializer,
    AdvertisingSourceSerializer,
    RequestStatusSerializer,
    PaymentMethodSerializer,
    StudentSerializer,
    PaymentSerializer,
    ReasonSerializer,
    StudentOnStudySerializer,
    ArchiveDepartmentSerializer,
    ArchiveGroupSerializer,
    ArchiveStudentSerializer,
)
from rest_framework.parsers import MultiPartParser


class ArchiveCourseViewSet(ModelViewSet):
    queryset = DepartmentOfCourse.objects.filter(is_archive=True)
    serializer_class = {
        'update': ArchiveDepartmentSerializer,
        'partial_update': ArchiveDepartmentSerializer,
    }
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or DepartmentSerializer


class ArchiveGroupViewSet(ModelViewSet):
    queryset = Group.objects.filter(is_archive=True)
    serializer_class = {
        'update': ArchiveGroupSerializer,
        'partial_update': ArchiveGroupSerializer,
    }
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or GroupSerializer


class ArchiveStudentViewSet(ModelViewSet):
    queryset = Student.objects.filter(is_archive=True)
    serializer_class = {
        'update': ArchiveStudentSerializer,
        'partial_update': ArchiveStudentSerializer,
    }
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or StudentSerializer


class DepartmentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = DepartmentSerializer
    queryset = DepartmentOfCourse.objects.all()


class DepartmentImageUpdateViewSet(ModelViewSet):
    parser_classes = (MultiPartParser,)
    queryset = DepartmentOfCourse.objects.all()
    serializer_class = DepartmentSerializerOnlyWithImage
    http_method_names = ['put', 'patch']


class GroupStatusViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = GroupStatusSerializer
    queryset = GroupStatus.objects.all()


class ClassroomViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()


# class CourseViewSet(ModelViewSet):
#     permission_classes = [IsSuperUser | IsManager]
#     serializer_class = CourseSerializer
#     queryset = Course.objects.all()


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


class StudentStatusAViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=True, status=RequestStatus.objects.get(name="Ждёт звонка"))


class StudentStatusBViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=True, status=RequestStatus.objects.get(name="Звонок совершён"))


class StudentStatusCViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=True, status=RequestStatus.objects.get(name="Записан на пробный урок"))


class StudentStatusDViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=True, status=RequestStatus.objects.get(name="Посетил пробный урок"))


class StudentOnStudyViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.filter(on_request=False)
    serializer_class = StudentOnStudySerializer

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        student = None

        if pk.isdigit():
            student = queryset.filter(id=pk).first()
            serializer = self.serializer_class(student)
        else:
            queryset = self.get_queryset().filter(department=DepartmentOfCourse.objects.get(name=pk))
            serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)


# class StudentOnStudyFilterAViewSet(ModelViewSet):
#     permission_classes = [IsSuperUser | IsManager]
#     queryset = Student.objects.all()
#     serializer_class = StudentOnStudySerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="ux/ui"))
#
#
# class StudentOnStudyFilterBViewSet(ModelViewSet):
#     permission_classes = [IsSuperUser | IsManager]
#     queryset = Student.objects.all()
#     serializer_class = StudentOnStudySerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="front-end"))
#
#
# class StudentOnStudyFilterCViewSet(ModelViewSet):
#     permission_classes = [IsSuperUser | IsManager]
#     queryset = Student.objects.all()
#     serializer_class = StudentOnStudySerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="pm"))
#
#
# class StudentOnStudyFilterDViewSet(ModelViewSet):
#     permission_classes = [IsSuperUser | IsManager]
#     queryset = Student.objects.all()
#     serializer_class = StudentOnStudySerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="back-end"))
#
#
# class StudentOnStudyFilterEViewSet(ModelViewSet):
#     permission_classes = [IsSuperUser | IsManager]
#     queryset = Student.objects.all()
#     serializer_class = StudentOnStudySerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="android"))
#
#
# class StudentOnStudyFilterFViewSet(ModelViewSet):
#     permission_classes = [IsSuperUser | IsManager]
#     queryset = Student.objects.all()
#     serializer_class = StudentOnStudySerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="ios"))
#
#
# class StudentOnStudyFilterGViewSet(ModelViewSet):
#     permission_classes = [IsSuperUser | IsManager]
#     queryset = Student.objects.all()
#     serializer_class = StudentOnStudySerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="flutter"))
#
#
# class StudentOnStudyFilterHViewSet(ModelViewSet):
#     permission_classes = [IsSuperUser | IsManager]
#     queryset = Student.objects.all()
#     serializer_class = StudentOnStudySerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="olimped_programming"))


class PaymentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
