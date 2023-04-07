from django.urls import re_path
from rest_framework import routers

from .views import (
    ArchiveCourseViewSet,
    ArchiveGroupViewSet,
    ArchiveStudentViewSet,
    GroupStatusViewSet,
    ClassroomViewSet,
    ScheduleTypeViewSet,
    GroupViewSet,
    DepartmentViewSet,
    PaymentMethodViewSet,
    PaymentViewSet,
    StudentViewSet,
    StudentOnStudyViewSet,
    AdvertisingSourceViewSet,
    RequestStatusViewSet,
    ReasonViewSet,
    DepartmentImageUpdateViewSet,
    StudentStatusAViewSet,
    StudentStatusBViewSet,
    StudentStatusCViewSet,
    StudentStatusDViewSet,
    BlackListViewSet,
    # StudentOnStudyFilterAViewSet,
    # StudentOnStudyFilterBViewSet,
    # StudentOnStudyFilterCViewSet,
    # StudentOnStudyFilterDViewSet,
    # StudentOnStudyFilterEViewSet,
    # StudentOnStudyFilterFViewSet,
    # StudentOnStudyFilterGViewSet,
    # StudentOnStudyFilterHViewSet,
)

app_name = "cmsapp"

main_page_router = routers.DefaultRouter()
router = routers.DefaultRouter()

router.register(r'archive/courses', ArchiveCourseViewSet, basename='archive-courses')
router.register(r'archive/groups', ArchiveGroupViewSet, basename='archive-groups')
router.register(r'archive/students', ArchiveStudentViewSet, basename='archive-students')
router.register(r'blacklist', BlackListViewSet, basename='blacklist')
router.register("group-statuses", GroupStatusViewSet)
router.register("classrooms", ClassroomViewSet)
router.register("schedule-types", ScheduleTypeViewSet)
router.register("groups", GroupViewSet)
main_page_router.register("departments", DepartmentViewSet)
main_page_router.register(r"departments/image", DepartmentImageUpdateViewSet)
main_page_router.register("payment-methods", PaymentMethodViewSet)
router.register(r"payments", PaymentViewSet)
main_page_router.register(r"students", StudentViewSet)
main_page_router.register(r"students-filter/status1", StudentStatusAViewSet)
main_page_router.register(r"students-filter/status2", StudentStatusBViewSet)
main_page_router.register(r"students-filter/status3", StudentStatusCViewSet)
main_page_router.register(r"students-filter/status4", StudentStatusDViewSet)
main_page_router.register(r"students-on-study", StudentOnStudyViewSet, basename="students-on-study")
main_page_router.register(r"sources", AdvertisingSourceViewSet)
main_page_router.register(r"request-statuses", RequestStatusViewSet)
main_page_router.register(r"reasons", ReasonViewSet)

urlpatterns = [
    re_path(r'^students-on-study/(?P<id>\d+|[a-zA-Z0-9-]+)$', StudentOnStudyViewSet.as_view({'get': 'retrieve'})),
]

# urlpatterns += router.urls
# urlpatterns += main_page_router.urls
