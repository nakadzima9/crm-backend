from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from PIL import Image


class SuperUser(BaseUserManager):
    def create_user(self, username, email, **extra_fields):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.user_type = 'admin'
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    TYPE_ROLE_CHOICES = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("teacher", "Teacher"),
    ]
    TYPE_SEX_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    username = models.CharField(max_length=255, null=True, verbose_name="Логин")
    email = models.EmailField(unique=True, null=True, verbose_name="Почта")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    phone = models.CharField(max_length=13, unique=True, blank=True, null=True, verbose_name="Номер телефона")
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="О себе")
    sex = models.CharField(max_length=50, choices=TYPE_SEX_CHOICES, blank=True, null=True, verbose_name="Пол")
    user_type = models.CharField(max_length=255, choices=TYPE_ROLE_CHOICES, null=True, verbose_name="Тип пользователя")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперь пользователь")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Дата создания учётной записи")

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = SuperUser()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'Системный пользователь'
        verbose_name_plural = "Системные пользователи"


class OTP(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    # life_time_in_seconds = models.PositiveSmallIntegerField(default=60)


class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics', blank=True, null=True)

