from rest_framework import routers

from .views import *

app_name = "cmsapp"

router = routers.DefaultRouter()
router.register("departments", DepartmentViewSet)
router.register("teachers", TeacherViewSet)
router.register("group-statuses", GroupStatusViewSet)
router.register("classrooms", ClassroomViewSet)
router.register("courses", CourseViewSet)
router.register("schedule-types", ScheduleTypeViewSet)
router.register("groups", GroupViewSet)
router.register("advertising-sources", AdvertisingSourceViewSet)
router.register("card-statuses", CardStatusViewSet)
router.register("payment-methods", PaymentMethodViewSet)
router.register("students", StudentViewSet)
router.register("student-cards", StudentCardViewSet)
router.register("payments", PaymentViewSet)
router.register("blacklists", BlackListViewSet)

urlpatterns = []

urlpatterns += router.urls
