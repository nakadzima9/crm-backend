import datetime
import uuid

import pytz
from django.core.mail import send_mail
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import OTP, User

from .serializers import (ChangePasswordSerializer,
                          PasswordEmailCheckSerializer,
                          PasswordCodeCheckSerializer)
from .utils import generate_otp


# for create otp and send mail
class PasswordResetEmailView(APIView):
    # will be adding later object permission
    # self.check_object_permissions(request, contact)


    @swagger_auto_schema(
        responses={"201": "created", "400": "bad request", "404": "not found"},
        operation_description="for create code and send mail",
        request_body=PasswordEmailCheckSerializer,
    )
    def post(self, request):
        otp = generate_otp()
        request_email = request.data.get('email', None)
        if request_email is None:
            return Response(data="Required field email", status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=request_email).first()
        OTP.objects.filter(
                    created_time__lte=datetime.datetime.fromtimestamp(
                        timezone.now().timestamp() - 120, tz=timezone.utc
                    )
                ).delete()
        if not user:
            return Response(data='Email doesn\'t exists or check email', status=status.HTTP_404_NOT_FOUND)

        OTP.objects.filter(user=user).delete()


        otp_obj = OTP.objects.create(user=user, code=otp)

        send_mail(
                    "Код активации",
                    f"Ваш код для сброса пароля: {otp} ",
                    "from@crm-project.com",
                    [user.email],
                    fail_silently=False,
                )
        return Response(
                    data={'detail' : "Code expired after 2 minutes", 'unique_id' : otp_obj.unique_id},
            status=status.HTTP_201_CREATED
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
        request_unique_id = request.data.get('unique_id', None)

        if request_otp is None:
            fields_errors['code'] = "Required field code"

        if request_unique_id is None:
            fields_errors['unique_id'] = "Required field unique_id"

        if fields_errors:
            return Response(data=fields_errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            uuid.UUID(request_unique_id)
            otp_obj = OTP.objects.filter(unique_id=request_unique_id, code=request_otp).first()
        except ValueError:
            return Response(data='Your unique_id is not valid', status=status.HTTP_400_BAD_REQUEST)

        if not otp_obj:
            return Response(data='Your code or unique_id is not valid', status=status.HTTP_400_BAD_REQUEST)

        # if otp_queryset:
        #     otp_queryset = otp_queryset.filter(code=request_otp)
        #     if not otp_queryset:
        #         return Response(data='Your code is not valid', status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(data='Your unique_id is not valid', status=status.HTTP_400_BAD_REQUEST)

        # otp_obj = otp_queryset.first()

        # request_email = otp_obj.user.email
        # user_queryset = User.objects.filter(email=request_email)
        # if not user_queryset:
        #     return Response(data="This user does not exist", status=status.HTTP_404_NOT_FOUND)
        # user = user_queryset.first()

        if otp_obj.created_time <= datetime.datetime.fromtimestamp(timezone.now().timestamp() - 120,
                                                                   tz=timezone.utc) and not otp_obj.status:
            otp_obj.delete()
            return Response(data="Code has expired", status=status.HTTP_400_BAD_REQUEST)

        otp_obj.status=True
        otp_obj.password_life_time = timezone.now() + datetime.timedelta(seconds=300)
        otp_obj.save()
        return Response(data="You can change password during 5 minutes", status=status.HTTP_200_OK)


# for change password
class PasswordChangeView(APIView):

    @swagger_auto_schema(
        responses={"200": "Ok", "400": "bad request", "404": "not found"},
        operation_description="For change password",
        request_body=ChangePasswordSerializer,
    )
    def post(self, request):
        fields_errors = {}
        request_unique_id = request.data.get('unique_id', None)

        if request_unique_id is None:
            fields_errors['unique_id'] = "Required unique_id email"

        if fields_errors:
            return Response(data=fields_errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            uuid.UUID(request_unique_id)
            otp_obj = OTP.objects.filter(unique_id=request_unique_id, status=True).first()
        except ValueError:
            return Response(data='Your unique_id is not valid', status=status.HTTP_400_BAD_REQUEST)


        if not otp_obj:
            return Response(data='Current user can\'t change the password!', status=status.HTTP_404_NOT_FOUND)

        user = otp_obj.user

        # user_email  = otp.user.email
        # user_queryset = User.objects.filter(email=user_email)
        #
        # if not user_queryset:
        #     return Response(data='Email not exists or check email', status=status.HTTP_404_NOT_FOUND)
        #
        # user = user_queryset.first()

        if otp_obj.password_life_time <= timezone.now():
            return Response(data='Password change time has expired', status=status.HTTP_401_UNAUTHORIZED)

        #request.data.pop('unique_id')

        serializer = ChangePasswordSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            otp_obj.delete()
            return Response(data='Password changed successfully!', status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
