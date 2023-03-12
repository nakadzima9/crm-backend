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
main_page_router.register("departments", DepartmentViewSet)
main_page_router.register("payment-methods", PaymentMethodViewSet)
router.register(r"payments", PaymentViewSet)
main_page_router.register(r"students", StudentViewSet)
main_page_router.register(r"students-on-study", StudentOnStudyViewSet)

urlpatterns = []

# urlpatterns += router.urls
# urlpatterns += main_page_router.urls
