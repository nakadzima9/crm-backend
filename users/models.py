import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from cmsapp.models import Department, ScheduleType, Group


class SuperUser(BaseUserManager):

    def create_user(self, email, **extra_fields):
        if not extra_fields.get('without_generate_password', False):
            if not email:
                raise ValueError("You must provide an email")
            generate_password = self.make_random_password()
            user = self.model(
                email=self.normalize_email(email),
                **extra_fields
            )
            user.set_password(generate_password)
            user.fio = user.first_name +" "+ user.last_name
            user.save()
            send_mail("Пароль от CRM",
                      f"Ваши данные для входа в CRM:\nПочта: {user.email}\nПароль: {generate_password}",
                      "from@crm-project.com",
                      [user.email],
                      fail_silently=False,
                      )
            return user
        extra_fields.pop('without_generate_password')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.fio = user.first_name + " " + user.last_name
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            without_generate_password=True
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.user_type = 'admin'
        user.save()
        return user


def user_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    return f"profiles/{timezone.now().date().strftime('%Y/%m/%d')}/{filename}"

# def user_directory_path(instance, filename):
#     extension = filename.split('.')[-1]
#     filename = f"{instance.unique_id}.{extension}"
#     return f"profiles/user_{instance.owner.unique_id}/{timezone.now().date().strftime('%Y/%m/%d')}/{filename}"
#
#
# class UserImage(models.Model):
#     owner = models.ForeignKey('User', on_delete=models.CASCADE)
#     unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     image = models.ImageField(upload_to=user_directory_path, default='default.jpg', blank=True, null=True,
#                               verbose_name="Аватар")
#
#     def __str__(self):
#         return f"{self.image}"
#
#     class Meta:
#         verbose_name = "Изображение пользователя"
#         verbose_name_plural = "Изображения пользователей"


class User(AbstractBaseUser, PermissionsMixin):
    TYPE_ROLE_CHOICES = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("mentor", "Mentor"),
    ]
    email = models.EmailField(unique=True, verbose_name="Почта")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=13, blank=True, verbose_name="Номер телефона")
    # unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # image = models.ForeignKey(UserImage, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Аватар")
    image = models.ImageField(upload_to=user_directory_path, default='default.jpg', blank=True, verbose_name="Аватар")
    linkedin = models.URLField(blank=True, verbose_name="Ссылка на Linkedin")
    user_type = models.CharField(max_length=255, choices=TYPE_ROLE_CHOICES, verbose_name="Тип пользователя")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='department', verbose_name='Департамент')
    # group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name='group',
    #                            verbose_name='Группа')
    patent_number = models.PositiveIntegerField(blank=True, default=0, verbose_name="Номер патента")
    patent_start = models.DateField(blank=True, null=True, verbose_name="Срок действия патента")
    patent_end = models.DateField(blank=True, null=True, verbose_name="Срок окончания патента")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперь пользователь")

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = SuperUser()

    # def save(self, *args, **kwargs):
    #     try:
    #         update_status = kwargs.pop("update")
    #     except KeyError:
    #         update_status = False
    #
    #     if not update_status:
    #         generate_password = User.objects.make_random_password()
    #         send_mail(
    #             "Ваши данные для входа в CRM:",
    #             f"Ваши данные для входа в CRM:\n"
    #             f"Пароль: {generate_password}",
    #             "from@crm-project.com",
    #             [self.email],
    #         )
    #         self.set_password(generate_password)
    #     super(User, self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'Системный пользователь'
        verbose_name_plural = "Системные пользователи"


class OTP(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.BooleanField(default=False)
    password_life_time = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user} - OTP: {self.code}"

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTP'
