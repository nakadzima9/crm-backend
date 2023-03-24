from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    AdminViewSet,
    AllUserViewSet,
    ManagerViewSet,
    MentorViewSet,
    PersonalLoginWebView,
    ProfileViewSet,
    ProfileImageUpdateViewSet,
    ArchiveAdminViewSet,
    ArchiveManagerViewSet,
    ArchiveMentorViewSet,
)

from .api.password_reset_views import PasswordResetCheckCodeView, PasswordResetEmailView, PasswordChangeView

user_router = DefaultRouter()
user_router.register(r'admins', AdminViewSet, basename='admins')
user_router.register(r'all-users', AllUserViewSet, basename='all-users')
user_router.register(r'managers', ManagerViewSet, basename='managers')
user_router.register(r'mentors', MentorViewSet, basename='mentors')
user_router.register(r'profiles', ProfileViewSet, basename='profiles')
user_router.register(r'profiles/avatar', ProfileImageUpdateViewSet, basename='profiles-avatar')
user_router.register(r'archive/admins', ArchiveAdminViewSet, basename='archives-admins')
user_router.register(r'archive/managers', ArchiveManagerViewSet, basename='archive-managers')
user_router.register(r'archive/mentors', ArchiveMentorViewSet, basename='archive-mentors')

urlpatterns = [
    path("login/personal/", PersonalLoginWebView.as_view()),

    path('jwt/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path("password_reset/", PasswordResetEmailView.as_view(), name="password_reset_email"),
    path("password_reset_code/", PasswordResetCheckCodeView.as_view(), name="password_reset_code"),
    path("password_reset_change/", PasswordChangeView.as_view(), name="password_reset_change"),
]
