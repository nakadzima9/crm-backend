# from cloudinary_storage.storage import MediaCloudinaryStorage
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    ValidationError
)

from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .api.custom_funcs import get_token
from .api.login_serializers import PersonalLoginWebSerializer
from .api.serializers import (
    UserSerializer,
    AdminSerializer,
    ManagerSerializer,
    MentorListSerializer,
    MentorDetailSerializer,
    ProfileSerializer,
    UserSerializerWithoutEmailAndImage,
    ProfileSerializerOnlyWithImage,
    UserArchiveSerializer,
)

from .models import User
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


class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.filter(user_type="admin").order_by('id')
    serializer_class = {
        'update': UserArchiveSerializer,
        'partial_update': UserArchiveSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            if request.user.id == instance.id:
                return Response(data="You can't delete yourself", status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or AdminSerializer


class AllUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.all().order_by('id')
    serializer_class = {
        'update': UserArchiveSerializer,
        'partial_update': UserArchiveSerializer,
    }
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or UserSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.filter(user_type="manager").order_by('id')
    serializer_class = {
        'update': UserArchiveSerializer,
        'partial_update': UserArchiveSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            if request.user.id == instance.id:
                return Response(data="You can't delete yourself", status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or ManagerSerializer


class MentorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser | IsManager]
    queryset = User.objects.filter(user_type="mentor").order_by('id')
    serializer_class = {
        'list': MentorListSerializer,
        'retrieve': MentorDetailSerializer,
    }
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or MentorDetailSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type__in=['admin', 'manager']).order_by('id')
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     storage = MediaCloudinaryStorage()
    #     storage.delete(name=instance.image.name)
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=UserSerializerWithoutEmailAndImage)
    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ['PUT', 'PATCH']:
            serializer_class = UserSerializerWithoutEmailAndImage
        return serializer_class


class ProfileImageUpdateViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,)
    queryset = User.objects.filter(user_type__in=['admin', 'manager']).order_by('id')
    serializer_class = ProfileSerializerOnlyWithImage
    http_method_names = ['put', 'patch']


class ArchiveAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='admin', is_active=False)
    serializer_class = {
        'update': UserArchiveSerializer,
        'partial_update': UserArchiveSerializer,
    }
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or UserSerializer


class ArchiveManagerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='manager', is_active=False)
    serializer_class = {
        'update': UserArchiveSerializer,
        'partial_update': UserArchiveSerializer,
    }
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or UserSerializer


class ArchiveMentorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='mentor', is_active=False)
    serializer_class = {
        'update': UserArchiveSerializer,
        'partial_update': UserArchiveSerializer,
    }
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        return self.serializer_class.get(self.action) or UserSerializer
