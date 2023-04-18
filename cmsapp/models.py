from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

from core import settings


class ModelWithUpdate(models.Model):
    class Meta:
        abstract = True

    def update(self, commit=False, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if commit:
            self.save()
        return self


class Classroom(models.Model):
    name = models.CharField(max_length=15, verbose_name="Комната")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


def course_directory_path(instance, filename):
    # extension = filename.split('.')[-1]
    return f"courses/{filename}"


class DepartmentOfCourse(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название курса")
    duration_month = models.PositiveSmallIntegerField(verbose_name="Продолжительность курса в месяцах")
    image = models.ImageField(upload_to=course_directory_path, default='course_default.jpg', blank=True,
                              verbose_name="Аватар")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_archive = models.BooleanField(default=False, blank=True, verbose_name="Архивировать")
    description = models.CharField(max_length=300, verbose_name="Описание")
    color = models.CharField(max_length=10, null=True, verbose_name="Цвет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Group(ModelWithUpdate):
    SCHEDULE_TYPE = (
        (1, "Тип1"),
        (2, "Тип2"),
    )
    name = models.CharField(max_length=50, unique=True, verbose_name="Название группы")
    students_max = models.PositiveSmallIntegerField(verbose_name="Количество максимальных студентов")
    department = models.ForeignKey(DepartmentOfCourse, null=True, on_delete=models.SET_NULL, verbose_name="Департмент")
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                               verbose_name="Преподаватель")
    start_at_date = models.DateField(null=True, verbose_name="Старт группы")
    end_at_date = models.DateField(null=True, verbose_name="Конец группы")
    schedule_type = models.PositiveSmallIntegerField(choices=SCHEDULE_TYPE, default=1, verbose_name="Тип расписания")
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, verbose_name="Комната")
    is_archive = models.BooleanField(default=False, blank=True, verbose_name="Архивировать")
    start_at_time = models.TimeField(null=True, verbose_name="Начало занятий")
    end_at_time = models.TimeField(null=True, verbose_name="Конец занятий")
    # Добавлено поле для счисления прошедших месяцев с начала курса/группы
    month_from_start = models.PositiveSmallIntegerField(
        verbose_name="Количество прошедших месяцев с начала группы", default=1)

    def get_mentor(self):
        return '\n'.join([m.mentor for m in self.mentor.filter(user_type__in='mentor')])

    def __str__(self):
        return f'Name: {self.name}'

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
    color = models.CharField(max_length=10, null=True, blank=True, verbose_name="Цвет")

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


def get_default_status():
    return RequestStatus.objects.filter(name="Ждёт звонка").first()


def get_default_department():
    return DepartmentOfCourse.objects.all()


class Student(ModelWithUpdate):
    STATUS_CHOICES = (
        (1, "Оплатил"),
        (2, "Скоро оплата"),
        (3, "Должен оплатить"),
        (4, "Оплатил полностью")
    )

    REASON_CHOICES = (
        (1, "причина1"),
        (2, "причина2"),
        (3, "причина3"),
        (4, "причина4"),
        (5, "причина5"),
        (6, "причина6"),
        (7, "причина7"),
        (8, "причина8"),
    )

    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    notes = models.CharField(max_length=200, blank=True, verbose_name="Заметка")
    phone = models.CharField(max_length=13, verbose_name="Номер телефона")
    laptop = models.BooleanField(default=False, verbose_name="Наличиее ноутбука")
    department = models.ForeignKey(DepartmentOfCourse, default=get_default_department, on_delete=models.SET_NULL,
                                   null=True,
                                   verbose_name="Департамент")
    came_from = models.ForeignKey(AdvertisingSource, on_delete=models.SET_NULL, null=True, verbose_name="Откуда пришёл")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name="Метод оплаты")
    status = models.ForeignKey(RequestStatus, default=get_default_status, on_delete=models.SET_NULL,
                               blank=True, null=True, verbose_name="Статус заявки")
    reason = ArrayField(models.IntegerField(), null=True, verbose_name="Причина неуспешной сделки")
    on_request = models.BooleanField(default=True, verbose_name="На этапе заявки")
    request_date = models.DateTimeField(default=timezone.now, blank=True, null=True,
                                        verbose_name="Дата создания заявки")
    is_archive = models.BooleanField(default=False, blank=True, verbose_name="Архивировать")
    payment_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=3, verbose_name="Статус оплаты")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, verbose_name="Группа")
    blacklist = models.BooleanField(default=False, blank=True, verbose_name="Чёрный список")
    blacklist_created_at = models.DateField(auto_now_add=True, null=True, verbose_name="Дата добавления в чёрный список")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Сотрудник")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class Payment(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Сумма", default=0)
    client_card = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, verbose_name="Кто оплатил")
    course = models.ForeignKey(DepartmentOfCourse, null=True, on_delete=models.SET_NULL, verbose_name="Курс")
    last_payment_date = models.DateField(auto_now_add=True, null=True, verbose_name="Дата оплаты")
    payment_time = models.TimeField(auto_now_add=True, null=True, verbose_name="Время оплаты")
    payment_type = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name="Тип оплаты")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")

    def __str__(self):
        return f'{self.client_card}'

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"