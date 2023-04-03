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
    # CourseSerializer,
    # CourseSerializerOnlyWithImage,
    ScheduleTypeSerializer,
    GroupSerializer,
    AdvertisingSourceSerializer,
    RequestStatusSerializer,
    PaymentMethodSerializer,
    StudentSerializer,
    PaymentSerializer,
    ReasonSerializer,
    StudentOnStudySerializer,
    # ArchiveCourseSerializer,
    ArchiveGroupSerializer,
    ArchiveStudentSerializer,
)
from rest_framework.parsers import MultiPartParser


# class ArchiveCourseViewSet(ModelViewSet):
#     queryset = Course.objects.filter(is_archive=True)
#     serializer_class = {
#         'update': ArchiveCourseSerializer,
#         'partial_update': ArchiveCourseSerializer,
#     }
#     http_method_names = ['get', 'put', 'patch', 'delete']

#     def get_serializer_class(self):
#         return self.serializer_class.get(self.action) or CourseSerializer


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


class StudentOnStudyFilterAViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.all()
    serializer_class = StudentOnStudySerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="UX/UI"))


class StudentOnStudyFilterBViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.all()
    serializer_class = StudentOnStudySerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="Front-End"))


class StudentOnStudyFilterCViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.all()
    serializer_class = StudentOnStudySerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="PM"))


class StudentOnStudyFilterDViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.all()
    serializer_class = StudentOnStudySerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="Back-End"))


class StudentOnStudyFilterEViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.all()
    serializer_class = StudentOnStudySerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="Android"))


class StudentOnStudyFilterFViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.all()
    serializer_class = StudentOnStudySerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="iOS"))


class StudentOnStudyFilterGViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.all()
    serializer_class = StudentOnStudySerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="Flutter"))


class StudentOnStudyFilterHViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.all()
    serializer_class = StudentOnStudySerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(on_request=False, department=DepartmentOfCourse.objects.get(name="Олимпиадное программирование"))


class PaymentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
