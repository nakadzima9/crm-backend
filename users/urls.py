from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)
from rest_auth.views import (
    PasswordResetView, PasswordResetConfirmView
)
from . import views
from .views import (
    AdminViewSet,
    TravelerViewSet,
    PersonalLoginWebView, ManagerViewSet, AllUserViewSet, TokenVerifyView, ProfileViewSet
)

user_router = DefaultRouter()
user_router.register(r'admins', AdminViewSet, basename='admins')
user_router.register(r'allusers', AllUserViewSet, basename='allusers')
user_router.register(r'managers', ManagerViewSet, basename='managers')
user_router.register(r'travelers', TravelerViewSet, basename='travelers')
user_router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path("register/traveler/", views.RegisterTravelerView.as_view()),
    path("register/admin/", views.RegisterAdminView.as_view()),
    path("google/", views.GoogleLogin.as_view(), name='google_login'),
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
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("confirm-email/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="confirm-email"),
]
