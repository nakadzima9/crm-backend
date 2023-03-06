from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import (AuthenticationFailed, NotFound,
                                       ValidationError)
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .api.custom_funcs import get_token
from .api.login_serializers import PersonalLoginWebSerializer
from .api.serializers import UserSerializer, AdminSerializer, ManagerSerializer, MentorSerializer, \
    AdminSerializerWithoutEmail, ManagerSerializerWithoutEmail, ProfileSerializer, UserSerializerWithoutEmail
from .models import User, Mentor
from .permissions import IsManager, IsSuperUser

from drf_yasg.utils import swagger_auto_schema

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class PersonalLoginWebView(generics.GenericAPIView):
    serializer_class = PersonalLoginWebSerializer
    permission_classes = (AllowAny,)

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
    # parser_classes = [FileUploadParser]
    permission_classes = [IsSuperUser | IsManager]
    queryset = Mentor.objects.filter(user_type="mentor")
    serializer_class = MentorSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class AdminViewSet(viewsets.ModelViewSet):
    # parser_classes = [FileUploadParser]
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.filter(user_type="admin")
    serializer_class = AdminSerializer
    http_method_names = ['get', 'post','put', 'patch', 'delete']

    @swagger_auto_schema(request_body=AdminSerializerWithoutEmail)
    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ['PUT','PATCH']:
            serializer_class = AdminSerializerWithoutEmail
        return serializer_class


class ManagerViewSet(viewsets.ModelViewSet):
    # parser_classes = [FileUploadParser]
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.filter(user_type="manager")
    serializer_class = ManagerSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    @swagger_auto_schema(request_body=ManagerSerializerWithoutEmail)
    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ['PUT', 'PATCH']:
            serializer_class = ManagerSerializerWithoutEmail
        return serializer_class


class AllUserViewSet(viewsets.ModelViewSet):
    # parser_classes = [FileUploadParser]
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    http_method_names = ['get', 'delete']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type__in=['admin', 'manager'])
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    @swagger_auto_schema(request_body=UserSerializerWithoutEmail)
    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ['PUT', 'PATCH']:
            serializer_class = UserSerializerWithoutEmail
        return serializer_class
