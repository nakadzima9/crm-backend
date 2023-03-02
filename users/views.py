from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import (AuthenticationFailed, NotFound,
                                       ValidationError)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.views import TokenVerifyView

from .api.custom_funcs import get_token
from .api.login_serializers import PersonalLoginWebSerializer
from .api.register_serializers import (RegisterAdminSerializer,
                                       RegisterManagerSerializer)
from .api.serializers import TokenVerifySerializer, UserSerializer, AdminSerializer, ManagerSerializer, MentorSerializer
from .models import User
from .permissions import IsManager, IsSuperUser, IsUser

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class RegisterAdminView(generics.CreateAPIView):
    permission_classes = [IsSuperUser | IsManager]
    serializer_class = RegisterAdminSerializer
    queryset = User.objects.all()


class RegisterManagerView(generics.CreateAPIView):
    serializer_class = RegisterManagerSerializer
    queryset = User.objects.all()


class PersonalLoginWebView(generics.GenericAPIView):
    serializer_class = PersonalLoginWebSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(data={"detail": "НЕФИГ ЩАСТАТЬ!!!"}, status=status.HTTP_200_OK)

    def post(self, request):
        email = request.data['email']
        password = request.data["password"]
        user = User.objects.filter(email=email).first()
        if user is None or User.objects.filter(email=email, is_active=False):
            raise NotFound("User not found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        return get_token(user)


class MentorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser | IsManager | IsUser]
    queryset = User.objects.filter(user_type="teacher")
    serializer_class = MentorSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.filter(user_type="admin")
    serializer_class = AdminSerializer
    http_method_names = ['get', 'post','put', 'patch', 'delete']


class ManagerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.filter(user_type="manager")
    serializer_class = ManagerSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class AllUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class TokenVerifyView(TokenVerifyView):
    serializer_class = TokenVerifySerializer
