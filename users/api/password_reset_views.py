import datetime

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import OTP, User

from .serializers import (ChangePasswordSerializer,
                          PasswordCheckEmailSerializer,
                          PasswordCodeCheckSerializer)
from .utils import generate_otp


# for create otp and send mail
class PasswordResetEmailView(APIView):
    # will be adding later object permission
    # self.check_object_permissions(request, contact)


    @swagger_auto_schema(
        responses={"201": "created", "400": "bad request", "404": "not found"},
        operation_description="for create code and send mail",
        request_body=PasswordCheckEmailSerializer,
    )
    def post(self, request):
        otp = generate_otp()
        request_email = request.data.get('email', None)
        if request_email is None:
            return Response(data="Required field email", status=status.HTTP_400_BAD_REQUEST)
        user_queryset = User.objects.filter(email=request_email)
        OTP.objects.filter(
                    created_time__lte=datetime.datetime.fromtimestamp(
                        timezone.now().timestamp() - 60, tz=timezone.utc
                    )
                ).delete()
        if not user_queryset:
            return Response(data='Email not exists or check email', status=status.HTTP_404_NOT_FOUND)
        user = user_queryset.first()
        otp_queryset = OTP.objects.filter(user=user)
        if not otp_queryset:
            otp_queryset.delete()
        OTP.objects.create(user=user, code=otp)
        send_mail(
                    "Код активации",
                    f"Ваш код для сброса пароля: {otp} ",
                    "from@crm-backend-production.up.railway.app",
                    [user.email],
                    fail_silently=False,
                )
        return Response(
                    data="Code expired after 60 seconds", status=status.HTTP_201_CREATED
            )


# for check otp
class PasswordResetCheckCodeView(APIView):
    opt_not_exists = {"detail": "Wrong code or code has expired"}

    # for check otp
    @swagger_auto_schema(
        responses={"200": "Ok", "400": "bad request", "404": "not found"},
        operation_description="for check code",
        security=[],
        request_body=PasswordCodeCheckSerializer,
    )
    def post(self, request):
        fields_errors = {}
        request_otp = request.data.get('code', None)
        request_email = request.data.get('email', None)

        if request_otp is None:
            fields_errors['code'] = "Required field code"

        if request_email is None:
            fields_errors['email'] = "Required field email"

        if fields_errors:
            return Response(data=fields_errors, status=status.HTTP_400_BAD_REQUEST)

        user_queryset = User.objects.filter(email=request_email)
        if not user_queryset:
            return Response(data="This user does not exist", status=status.HTTP_404_NOT_FOUND)
        user = user_queryset.first()
        otp_queryset = OTP.objects.filter(user=user, code=request_otp)
        if not otp_queryset:
            return Response(data='Your code is not valid', status=status.HTTP_400_BAD_REQUEST)
        otp_obj = otp_queryset.first()
        if otp_obj.created_time <= datetime.datetime.fromtimestamp(timezone.now().timestamp() - 60,
                                                                   tz=timezone.utc):
            return Response(data="Code has expired", status=status.HTTP_400_BAD_REQUEST)
        otp_obj.status=True
        otp_obj.password_life_time = timezone.now() + datetime.timedelta(seconds=300)
        otp_obj.save()
        return Response(data="You can change password during 5 minutes", status=status.HTTP_200_OK)


# for change password
class PasswordChangeView(APIView):
    on_get = {"password": "New password", "repeat_password": "Repeat new password"}
    on_error = {"detail": "You have not provide send email and check"}

    @swagger_auto_schema(
        responses={"200": "Ok", "400": "bad request", "404": "not found"},
        operation_description="For change password",
        request_body=ChangePasswordSerializer,
    )
    def post(self, request):
        fields_errors = {}
        request_email = request.data.get('email', None)

        if request_email is None:
            fields_errors['email'] = "Required field email"

        if fields_errors:
            return Response(data=fields_errors, status=status.HTTP_400_BAD_REQUEST)

        user_queryset = User.objects.filter(email=request_email)
        user = user_queryset.first()
        otp_queryset = OTP.objects.filter(user=user, status=True)
        if not otp_queryset:
            return Response(data='Current user can\'t change the password!', status=status.HTTP_404_NOT_FOUND)
        otp = otp_queryset.first()
        otp_user = otp.user
        if otp.password_life_time <= timezone.now():
            return Response(data='Password change time has expired', status=status.HTTP_401_UNAUTHORIZED)
        serializer = ChangePasswordSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data='Password changed successfully!', status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
