from datetime import datetime

from django.db import models
from django.utils import timezone

from core import settings


class Classroom(models.Model):
    name = models.CharField(max_length=15, verbose_name="Комната")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


# class Department(models.Model):
#     name = models.CharField(max_length=20, verbose_name="Департамент")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Департамент"
#         verbose_name_plural = "Департаменты"


class GroupStatus(models.Model):
    status_name = models.CharField(max_length=50, verbose_name="Статус группы")

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = "Статус группы"
        verbose_name_plural = "Статусы групп"


def course_directory_path(instance, filename):
    # extension = filename.split('.')[-1]
    return f"courses/{filename}"


class Department(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название курса")
    # department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Департамент")
    duration_month = models.PositiveSmallIntegerField(verbose_name="Продолжительность курса в месяцах", default=0)
    image = models.ImageField(upload_to=course_directory_path, default='course_default.jpg', blank=True,
                              verbose_name="Аватар")
    # mentor = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Преподаватели")
    is_archive = models.BooleanField(default=False, blank=True, verbose_name="Архивировать")
    description = models.CharField(max_length=300, verbose_name="Описание")

    def get_mentors(self):
        return '\n'.join([m.mentor for m in self.mentor.filter(user_type__in='mentor')])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class ScheduleType(models.Model):
    type_name = models.CharField(max_length=10, verbose_name="Тип расписания")
    start_time = models.TimeField(blank=True, null=True, verbose_name="Начало урока")
    end_time = models.TimeField(blank=True, null=True, verbose_name="Конец урока")

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название группы")
    students_max = models.PositiveSmallIntegerField(verbose_name="Количество максимальных студентов")
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                               verbose_name="Преподаватель")
    status = models.ForeignKey(GroupStatus, on_delete=models.CASCADE, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    schedule_type = models.ForeignKey(ScheduleType, on_delete=models.CASCADE, verbose_name="Тип расписания")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, verbose_name="Комната")
    is_archive = models.BooleanField(default=False, blank=True, verbose_name="Архивировать")

    def __str__(self):
        return f'Number: {self.number}, status: {self.status}'

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=20, verbose_name="Метод оплаты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метод оплат"
        verbose_name_plural = "Метод оплаты"


class AdvertisingSource(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название источника")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Название источника"
        verbose_name_plural = "Названия источников"


class RequestStatus(models.Model):
    name = models.CharField(max_length=30, default="Ждёт звонка", verbose_name="Статус заявки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус завяки"
        verbose_name_plural = "Статус заявок"


class Reason(models.Model):
    name = models.CharField(max_length=30, verbose_name="Причина неуспеха")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Причина неуспеха"
        verbose_name_plural = "Причины неуспехов"


def get_default_status():
    return RequestStatus.objects.filter(name="Ждёт звонка").first()


def get_default_department():
    return Department.objects.all()


class Student(models.Model):
    STATUS_CHOICES = (
        (1, "Обучается"),
        (2, "Закончил"),
        (3, "Прервал")
    )
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    surname = models.CharField(max_length=30, blank=True, verbose_name="Отчество")
    notes = models.CharField(max_length=200, blank=True, verbose_name="Заметка")
    phone = models.CharField(max_length=13, blank=True, verbose_name="Номер телефона")
    laptop = models.BooleanField(default=False, verbose_name="Наличиее ноутбука")
    department = models.ForeignKey(Department, default=get_default_department, on_delete=models.CASCADE, null=True,
                                   verbose_name="Департамент")
    came_from = models.ForeignKey(AdvertisingSource, on_delete=models.CASCADE, null=True, verbose_name="Откуда пришёл")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, verbose_name="Метод оплаты")
    status = models.ForeignKey(RequestStatus, default=get_default_status, on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name="Статус заявки")
    paid = models.BooleanField(default=False, verbose_name="Оплатил или нет")
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE, null=True, verbose_name="Причина неуспешной сделки")
    on_request = models.BooleanField(default=True, verbose_name="На этапе заявки")
    request_date = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Дата создания заявки")
    is_archive = models.BooleanField(default=False, blank=True, verbose_name="Архивировать")
    learning_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    payment_status = models.CharField(max_length=15, default="Оплачено", verbose_name="Статус оплаты")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class Payment(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Сумма")
    client_card = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, verbose_name="Кто оплатил")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Время оплаты")
    payment_type = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, verbose_name="Тип оплаты")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")

    def __str__(self):
        return f'{self.client_card}'

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
