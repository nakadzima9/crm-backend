from django.urls import path, re_path
from rest_framework import routers

from .views import (
    AdvertisingSourceViewSet,
    ArchiveCourseViewSet,
    ArchiveGroupViewSet,
    ArchiveStudentViewSet,
    BlackListViewSet,
    ClassroomViewSet,
    GroupStatusViewSet,
    GroupViewSet,
    DepartmentViewSet,
    DepartmentImageUpdateViewSet,
    PaymentViewSet,
    PaymentMethodViewSet,
    PaymentSearchAPIView,
    RequestStatusViewSet,
    StudentViewSet,
    StudentOnStudyViewSet,
    ScheduleTypeViewSet,
    StudentStatusAViewSet,
    StudentStatusBViewSet,
    StudentStatusCViewSet,
    StudentStatusDViewSet,
)

app_name = "cmsapp"

main_page_router = routers.DefaultRouter()
router = routers.DefaultRouter()

router.register(r'archive/courses', ArchiveCourseViewSet, basename='archive-courses')
router.register(r'archive/groups', ArchiveGroupViewSet, basename='archive-groups')
router.register(r'archive/students', ArchiveStudentViewSet, basename='archive-students')
router.register(r'blacklist', BlackListViewSet, basename='blacklist')
router.register(r"classrooms", ClassroomViewSet, basename="classrooms")
router.register(r"groups", GroupViewSet, basename="groups")
router.register(r"group-statuses", GroupStatusViewSet, basename="group-statuses")
router.register(r"departments", DepartmentViewSet, basename="departments")
router.register(r"departments/image", DepartmentImageUpdateViewSet, basename="departments-image")
router.register(r"payments", PaymentViewSet, basename="payments")
main_page_router.register(r"payment-methods", PaymentMethodViewSet, basename="patment-methods")
main_page_router.register(r"request-statuses", RequestStatusViewSet, basename="request-statuses")
main_page_router.register(r"schedule-types", ScheduleTypeViewSet, basename="schedule-types")
main_page_router.register(r"students", StudentViewSet, basename="students")
main_page_router.register(r"students-filter/status1", StudentStatusAViewSet, basename="students-filter-status1")
main_page_router.register(r"students-filter/status2", StudentStatusBViewSet, basename="students-filter-status2")
main_page_router.register(r"students-filter/status3", StudentStatusCViewSet, basename="students-filter-status3")
main_page_router.register(r"students-filter/status4", StudentStatusDViewSet, basename="students-filter-status4")
main_page_router.register(r"students-on-study", StudentOnStudyViewSet, basename="students-on-study")
main_page_router.register(r"sources", AdvertisingSourceViewSet, basename="sources")


urlpatterns = [
    path('payment-search/', PaymentSearchAPIView.as_view(), name='payment-search'),
]
