from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate, APIRequestFactory
from cmsapp.models import DepartmentOfCourse
from users.models import User
from .views import PopularDepartmentsViewSet
from analytic.api.serializers import PopularDepartmentsSerializer


class PopularDepartmentsViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser("test@test.com", 'admin')
        self.department1 = DepartmentOfCourse.objects.create(
            name='test_department', is_archive=False, duration_month=3, price=15000, description="asdasd"
        )
        self.department2 = DepartmentOfCourse.objects.create(
            name='test_department2', is_archive=False, duration_month=2, price=20000, description="asdasd"
        )

    def test_list_popular_departments(self):
        """
        Test that the viewset returns a list of popular departments
        that are not archived.
        """
        view = PopularDepartmentsViewSet.as_view({'get': 'list'})

        # Make an authenticated request to the view...
        request = self.factory.get('/api/popular-departments/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_popular_departments_unauthenticated(self):
        """
        Test that unauthenticated users can't access the list of popular
        departments.
        """
        url = reverse('departments for analytics-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
