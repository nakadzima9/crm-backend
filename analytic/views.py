from .api.serializers import (
    PopularDepartmentsSerializer, 
    PopularSourceSerializer, 
    ReasonPercentSerializer,
    RequestStatusesCounterSerializer,
)
from cmsapp.models import DepartmentOfCourse, AdvertisingSource, RequestStatus
from rest_framework.viewsets import ModelViewSet
from patches.permissions import IsManager, IsSuperUser
from .models import DeletionReason


class PopularDepartmentsViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = DepartmentOfCourse.objects.filter(is_archive=False)
    serializer_class = PopularDepartmentsSerializer
    http_method_names = ['get']


class PopularSourcesViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = AdvertisingSource.objects.all()
    serializer_class = PopularSourceSerializer
    http_method_names = ['get']


class ReasonPercentViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = DeletionReason.objects.all()
    serializer_class = ReasonPercentSerializer
    http_method_names = ['get']


class RequestStatusesCounterViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = RequestStatus.objects.all()
    serializer_class = RequestStatusesCounterSerializer
    http_method_names = ['get']
