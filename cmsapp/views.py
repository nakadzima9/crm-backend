from django.shortcuts import get_object_or_404
from django.db.models.functions import Concat
from django.db.models import Value, Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

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
    StudentOnStudySerializer,
    ArchiveDepartmentSerializer,
    ArchiveGroupSerializer,
    ArchiveStudentSerializer, PaymentListSerializer, BlackListSerializer,
    StudentNameSerializer, PaymentSearchSerializer, PaymentStudentNameSerializer  # , PaymentSearchSerializer
)
from rest_framework.parsers import MultiPartParser

from .utils import find_user_by_name


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


class PaymentMethodViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()


class StudentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.filter(is_archive=False, on_request=True).order_by('id')


class StudentStatusAViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(is_archive=False, on_request=True,
                                      status=RequestStatus.objects.filter(name="Ждёт звонка").first())


class StudentStatusBViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(is_archive=False, on_request=True,
                                      status=RequestStatus.objects.filter(name="Звонок совершён").first())


class StudentStatusCViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(is_archive=False, on_request=True,
                                      status=RequestStatus.objects.filter(name="Записан на пробный урок").first())


class StudentStatusDViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        return Student.objects.filter(is_archive=False, on_request=True,
                                      status=RequestStatus.objects.filter(name="Посетил пробный урок").first())


class StudentOnStudyViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.filter(blacklist=False, is_archive=False, on_request=False).order_by('id')
    serializer_class = StudentOnStudySerializer

    @swagger_auto_schema(
        operation_id='retrieve_student',
        operation_description='Retrieve student details by ID.',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='ID of the student. Can be an integer or a string.'
            )
        ],
    )
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        student = None

        if pk.isdigit():
            student = queryset.filter(id=pk).first()
            serializer = self.serializer_class(student)
        else:
            queryset = self.get_queryset().filter(department=DepartmentOfCourse.objects.filter(name=pk).first())
            serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)


class PaymentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = {
        'list': PaymentListSerializer,
    }
    queryset = Payment.objects.all()
    #http_method_names = ['get', 'post']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or PaymentSerializer


class PaymentSearchAPIView(APIView):

    @swagger_auto_schema(operation_description='Search by student name for payment',
                         request_body=PaymentStudentNameSerializer)
    def post(self, request):
        full_name = request.data.get('full_name')
        students = find_user_by_name(full_name)
        if not students:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PaymentSearchSerializer(students, many=True)
        print(serializer.data)
        fio = {'id': serializer.data[0]['id'],
               'full_name': serializer.data[0]['first_name'] + ' ' + serializer.data[0]['last_name']}
        return Response(fio, status=status.HTTP_201_CREATED)


class BlackListViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.filter(blacklist=True)
    serializer_class = BlackListSerializer
