from rest_framework import routers
from .views import (
    PopularDepartmentsViewSet,
    PopularSourcesViewSet,
    ReasonPercentViewSet,
    RequestStatusesCounterViewSet,
)

app_name = "analytic"

analytics_router = routers.DefaultRouter()

analytics_router.register(r'popular-departments', PopularDepartmentsViewSet, basename='departments for analytics')
analytics_router.register(r'popular-sources', PopularSourcesViewSet, basename='sources for analytics')
analytics_router.register(r'leaving-reasons', ReasonPercentViewSet, basename='reasons of leaving')
analytics_router.register(r'request-statuses', RequestStatusesCounterViewSet, basename='request statuses counter')
