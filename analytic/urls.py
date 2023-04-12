from rest_framework import routers
from .views import (
    PopularDepartmentsViewSet,
)

app_name = "analytic"

analytics_router = routers.DefaultRouter()

analytics_router.register(r'popular-departments', PopularDepartmentsViewSet, basename='archive-courses')
