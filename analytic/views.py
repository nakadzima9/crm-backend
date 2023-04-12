from .api.serializers import PopularDepartmentsSerializer
from cmsapp.models import DepartmentOfCourse
from rest_framework.viewsets import ModelViewSet
from patches.permissions import IsManager, IsSuperUser


class PopularDepartmentsViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = DepartmentOfCourse.objects.filter(is_archive=False)
    serializer_class = PopularDepartmentsSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        total = self.get_serializer().get_total()
        response.data.append({'total': total})
        return response


