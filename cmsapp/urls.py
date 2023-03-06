from rest_framework import routers

from .views import *

app_name = "cmsapp"

main_page_router = routers.DefaultRouter()
router = routers.DefaultRouter()

router.register("group-statuses", GroupStatusViewSet)
router.register("classrooms", ClassroomViewSet)
router.register("courses", CourseViewSet)
router.register("schedule-types", ScheduleTypeViewSet)
router.register("groups", GroupViewSet)
router.register("departments", DepartmentViewSet)
router.register("advertising-sources", AdvertisingSourceViewSet)
router.register("payment-methods", PaymentMethodViewSet)
router.register(r"request-statuses", RequestStatusViewSet)
router.register(r"payments", PaymentViewSet)

router.register(r"student-requests", StudentRequestViewSet)
router.register(r"students", StudentViewSet)

urlpatterns = []

# urlpatterns += router.urls
# urlpatterns += main_page_router.urls
