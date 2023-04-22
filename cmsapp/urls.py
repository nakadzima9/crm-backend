from django.urls import path, re_path
from rest_framework import routers

from .views import (
    AdvertisingSourceViewSet,
    ArchiveCourseViewSet,
    ArchiveGroupViewSet,
    ArchiveStudentViewSet,
    BlackListViewSet,
    ClassroomViewSet,
    GroupViewSet,
    DepartmentViewSet,
    DepartmentImageUpdateViewSet,
    PaymentViewSet,
    PaymentMethodViewSet,
    PaymentSearchGetAPIView,
    PaymentSearchPostAPIView,
    RequestStatusViewSet,
    StudentViewSet,
    StudentOnStudyViewSet, PaymentSearchGroup,
)

app_name = "cmsapp"

cmsapp_router = routers.DefaultRouter()

cmsapp_router.register(r'archive/courses', ArchiveCourseViewSet, basename='archive-courses')
cmsapp_router.register(r'archive/groups', ArchiveGroupViewSet, basename='archive-groups')
cmsapp_router.register(r'archive/students', ArchiveStudentViewSet, basename='archive-students')
cmsapp_router.register(r'blacklist', BlackListViewSet, basename='blacklist')
cmsapp_router.register(r"classrooms", ClassroomViewSet, basename="classrooms")
cmsapp_router.register(r"groups", GroupViewSet, basename="groups")
cmsapp_router.register(r"departments", DepartmentViewSet, basename="departments")
cmsapp_router.register(r"departments/image", DepartmentImageUpdateViewSet, basename="departments-image")
cmsapp_router.register(r"payments", PaymentViewSet, basename="payments")
cmsapp_router.register(r"payment-methods", PaymentMethodViewSet, basename="patment-methods")
cmsapp_router.register(r"request-statuses", RequestStatusViewSet, basename="request-statuses")
cmsapp_router.register(r"students", StudentViewSet, basename="students")
cmsapp_router.register(r"students-on-study", StudentOnStudyViewSet, basename="students-on-study")
cmsapp_router.register(r"sources", AdvertisingSourceViewSet, basename="sources")


urlpatterns = [
    path(r'payment-search/', PaymentSearchPostAPIView.as_view(), name='payment-search-get'),
    path(r'payment-search/<str:names>/', PaymentSearchGetAPIView.as_view(), name='payment-search-post'),
    path(r'payment-search-group/<str:names>/', PaymentSearchGroup.as_view(), name='payment-search-group')
]
