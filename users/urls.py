from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

from . import views
from .views import (
    AdminViewSet,
    StudentViewSet,
    PersonalLoginWebView, ManagerViewSet, AllUserViewSet, TokenVerifyView
)

from .api.password_reset_views import PasswordResetCheckCodeView, PasswordResetEmailView, PasswordChangeView

user_router = DefaultRouter()
user_router.register(r'admins', AdminViewSet, basename='admins')
user_router.register(r'allusers', AllUserViewSet, basename='allusers')
user_router.register(r'managers', ManagerViewSet, basename='managers')
user_router.register(r'students', StudentViewSet, basename='students')

urlpatterns = [
    path("register/student/", views.RegisterStudentView.as_view()),
    path("register/admin/", views.RegisterAdminView.as_view()),
    path("login/personal/", PersonalLoginWebView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path('jwt/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('jwt/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('jwt/token/verify',
         TokenVerifyView.as_view(),
         name='token_verify'),
    path("password_reset/", PasswordResetEmailView.as_view(), name="password_reset_email"),
    path("password_reset_code/", PasswordResetCheckCodeView.as_view(), name="password_reset_code"),
    path("password_reset_change/", PasswordChangeView.as_view(), name="password_reset_change")
]
