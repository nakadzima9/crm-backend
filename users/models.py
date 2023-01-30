from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


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
        ("traveler", "Traveler"),
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
    image = models.ImageField(upload_to="media/profile_image/", blank=True, null=True, verbose_name="Фото профиля")
    description = models.TextField(verbose_name="О себе", blank=True, null=True)
    sex = models.CharField(max_length=50, choices=TYPE_SEX_CHOICES, blank=True, null=True, verbose_name="Пол")
    user_type = models.CharField(max_length=255, choices=TYPE_ROLE_CHOICES, null=True, default="traveler",
                                 verbose_name="Тип пользователя")
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

