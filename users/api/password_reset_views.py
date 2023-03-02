import datetime

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import IntegrityError
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
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

    on_get = {"email": "User email for change password"}
    on_error = {"Bad Request": "Email not exists or check email"}

    @swagger_auto_schema(
        responses={"201": "created", "400": "bad request", "404": "not found"},
        operation_description="for create code and send mail",
        request_body=PasswordCheckEmailSerializer,
    )
    def post(self, request):
        try:
            otp = generate_otp()
            req_email = request.data["email"]
            try:
                user = User.objects.get(email=req_email)
                queries = OTP.objects.filter(
                    created_time__lte=datetime.datetime.fromtimestamp(
                        timezone.now().timestamp() - 60, tz=timezone.utc
                    )
                )
                for q_otp in queries:
                    q_otp.delete()

                while True:
                    try:
                        OTP.objects.create(user=user, code=otp)
                        break
                    except IntegrityError:
                        otp = generate_otp()

                send_mail(
                    "Код активации",
                    f"Ваш код для сброса пароля: {otp} ",
                    "from@crm-backend-production.up.railway.app",
                    [user.email],
                    fail_silently=False,
                )
                request.session["email"] = req_email
                return Response(
                    data="Code expired after 60 seconds", status=status.HTTP_201_CREATED
                )
            except ObjectDoesNotExist:
                return Response(
                    data=PasswordResetEmailView.on_error,
                    status=status.HTTP_404_NOT_FOUND,
                )
        except KeyError:
            return Response(
                data=PasswordResetEmailView.on_error, status=status.HTTP_400_BAD_REQUEST
            )


# for check otp
class PasswordResetCheckCodeView(APIView):
    on_get = {"email": "user@example.com"}
    opt_not_exists = {"detail": "Wrong code or code has expired"}

    # for check otp
    @swagger_auto_schema(
        responses={"200": "Ok", "400": "bad request", "404": "not found"},
        operation_description="for check code",
        security=[],
        request_body=PasswordCodeCheckSerializer,
    )
    def post(self, request):
        try:
            req_email = request.session["email"]
            req_otp = request.data["code"]
            try:
                user = User.objects.get(email=req_email)
                try:
                    otp_ob = OTP.objects.get(user=user, code=req_otp)

                    if otp_ob.created_time <= datetime.datetime.fromtimestamp(
                        timezone.now().timestamp() - 60, tz=timezone.utc
                    ):
                        return Response(
                            {"detail": "code has expired"},
                            status=status.HTTP_202_ACCEPTED,
                        )

                    request.session["opt_status"] = True

                    opt_status_lifetime = datetime.datetime.fromtimestamp(
                        timezone.now().timestamp() + 600, tz=timezone.utc
                    )
                    opt_status_lifetime = opt_status_lifetime.strftime(
                        "%Y-%m-%d-%H-%M-%S"
                    )
                    request.session["opt_status_lifetime"] = opt_status_lifetime

                    return Response(
                        data="you can change password during 10 minutes",
                        status=status.HTTP_200_OK,
                    )
                except ObjectDoesNotExist:
                    return Response(
                        PasswordResetCheckCodeView.opt_not_exists,
                        status=status.HTTP_404_NOT_FOUND,
                    )
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# for change password
class PasswordChangeView(APIView):
    on_get = {"password": "new password", "repeat_password": "repeat new password"}
    on_error = {"detail": "you have not provide send email and check"}

    @swagger_auto_schema(
        responses={"200": "Ok", "400": "bad request", "404": "not found"},
        operation_description="for change password",
        request_body=ChangePasswordSerializer,
    )
    def post(self, request):
        try:
            req_email = request.session["email"]
            opt_status = request.session["opt_status"]
            otp_lifetime = datetime.datetime.strptime(
                request.session["opt_status_lifetime"], "%Y-%m-%d-%H-%M-%S"
            )
            try:
                if opt_status is True:
                    user = User.objects.get(email=req_email)
                    utc = pytz.UTC
                    if timezone.now() <= utc.localize(otp_lifetime):
                        serializer = ChangePasswordSerializer(
                            user, data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            del request.session["email"]
                            del request.session["opt_status"]
                            del request.session["opt_status_lifetime"]
                            return Response(status=status.HTTP_200_OK)
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response(
                    {"detail", "User not exists"}, status.HTTP_404_NOT_FOUND
                )
        except KeyError:
            return Response(
                data=PasswordChangeView.on_error, status=status.HTTP_400_BAD_REQUEST
            )
