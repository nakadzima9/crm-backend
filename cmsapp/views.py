from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from patches.permissions import IsManager, IsSuperUser
from cmsapp.models import (
    AdvertisingSource,
    Classroom,
    DepartmentOfCourse,
    Group,
    PaymentMethod,
    Payment,
    RequestStatus,
    ScheduleType,
    Student,
)

from cmsapp.api.serializers import (
    AdvertisingSourceSerializer,
    ArchiveDepartmentDetailSerializer,
    ArchiveDepartmentStatusSerializer,
    ArchiveGroupStatusSerializer,
    ArchiveStudentSerializer,
    BlackListSerializer,
    ClassroomSerializer,
    DepartmentSerializer,
    DepartmentSerializerOnlyWithImage,
    GroupListSerializer,
    GroupDetailSerializer,
    PaymentMethodSerializer,
    PaymentSerializer,
    PaymentListSerializer,
    PaymentSearchSerializer,
    PaymentStudentNameSerializer,
    RequestStatusSerializer,
    ScheduleTypeSerializer,
    StudentSerializer,
    StudentOnStudySerializer, ArchiveGroupListSerializer,
)
from rest_framework.parsers import MultiPartParser

from .utils import find_user_by_name
from analytic.models import DeletionReason


class ArchiveCourseViewSet(ModelViewSet):
    queryset = DepartmentOfCourse.objects.filter(is_archive=True).order_by('id')
    serializer_class = {
        'update': ArchiveDepartmentStatusSerializer,
        'partial_update': ArchiveDepartmentStatusSerializer,
    }
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or ArchiveDepartmentDetailSerializer


class ArchiveGroupViewSet(ModelViewSet):
    queryset = Group.objects.filter(is_archive=True).order_by('id')
    serializer_class = {
        'update': ArchiveGroupStatusSerializer,
        'partial_update': ArchiveGroupStatusSerializer,
    }
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or ArchiveGroupListSerializer


class ArchiveStudentViewSet(ModelViewSet):
    queryset = Student.objects.filter(is_archive=True, on_request=False).order_by('id')
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
    queryset = DepartmentOfCourse.objects.all().order_by('id')


class DepartmentImageUpdateViewSet(ModelViewSet):
    parser_classes = (MultiPartParser,)
    queryset = DepartmentOfCourse.objects.all()
    serializer_class = DepartmentSerializerOnlyWithImage
    http_method_names = ['put', 'patch']


class ClassroomViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all().order_by('id')


class ScheduleTypeViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = ScheduleTypeSerializer
    queryset = ScheduleType.objects.all().order_by('id')


class GroupViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = {
        'list': GroupListSerializer,
        'retrieve': GroupListSerializer,
        'create': GroupDetailSerializer,
        'update': GroupDetailSerializer,
    }
    queryset = Group.objects.filter(is_archive=False).order_by('id')

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
        group = None

        if pk.isdigit():
            group = queryset.filter(id=pk).first()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(group, context={'request': request})
        else:
            queryset = self.get_queryset().filter(department=DepartmentOfCourse.objects.filter(name=pk).first())
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True, context={'request': request})

        return Response(serializer.data)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or GroupDetailSerializer


class AdvertisingSourceViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = AdvertisingSourceSerializer
    queryset = AdvertisingSource.objects.all().order_by('id')


class RequestStatusViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = RequestStatusSerializer
    queryset = RequestStatus.objects.all().order_by('id')


class PaymentMethodViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all().order_by('id')


class StudentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = StudentSerializer
    queryset = Student.objects.filter(is_archive=False, on_request=True).order_by('id')

    def perform_destroy(self, instance):
        deletion_reason = instance.reason
        if deletion_reason:
            for reason in deletion_reason:
                deletion_reason_obj, _ = DeletionReason.objects.get_or_create(reason=reason)
                deletion_reason_obj.student_count += 1
                deletion_reason_obj.save()
                print(deletion_reason_obj)
        super().perform_destroy(instance)


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
        fio = {'id': serializer.data[0]['id'],
               'full_name': serializer.data[0]['first_name'] + ' ' + serializer.data[0]['last_name']}
        return Response(fio, status=status.HTTP_201_CREATED)


class BlackListViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = Student.objects.filter(blacklist=True).order_by('id')
    serializer_class = BlackListSerializer
