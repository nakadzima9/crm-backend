from django.db import models

from core import settings


class Classroom(models.Model):
    name = models.CharField(max_length=15, verbose_name="Комната")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name="Департамент")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"


class GroupStatus(models.Model):
    status_name = models.CharField(max_length=15, verbose_name="Статус группы")

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = "Статус группы"
        verbose_name_plural = "Статусы групп"


def course_directory_path(instance, filename):
    # extension = filename.split('.')[-1]
    return f"courses/{filename}"


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название курса")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Департамент")
    duration_month = models.PositiveSmallIntegerField(verbose_name="Продолжительность курса в месяцах")
    image = models.ImageField(upload_to=course_directory_path, default='course_default.jpg', blank=True, null=True,
                              verbose_name="Аватар")
    mentor = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Преподаватели")
    is_archive = models.BooleanField(default=False, blank=True, null=True, verbose_name="Архивировать")

    def get_mentors(self):
        return '\n'.join([m.mentor for m in self.mentor.filter(user_type__in='mentor')])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class ScheduleType(models.Model):
    type_name = models.CharField(max_length=10, verbose_name="Тип расписания")
    start_time = models.TimeField(null=True, blank=True, verbose_name="Начало урока")
    end_time = models.TimeField(null=True, blank=True, verbose_name="Конец урока")

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"


class Group(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name="Номер группы")
    students_max = models.PositiveSmallIntegerField(verbose_name="Количество максимальных студентов")
    status = models.ForeignKey(GroupStatus, on_delete=models.CASCADE, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    schedule_type = models.ForeignKey(ScheduleType, on_delete=models.CASCADE, verbose_name="Тип расписания")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, verbose_name="Комната")
    is_archive = models.BooleanField(default=False, blank=True, null=True, verbose_name="Архивировать")

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
        verbose_name = "Метод оплаты"
        verbose_name_plural = "Методы оплат"


class AdvertisingSource(models.Model):
    name = models.CharField(max_length=15, verbose_name="Название источника")

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
        verbose_name_plural = "Статусы заявок"


class Reason(models.Model):
    name = models.CharField(max_length=30, verbose_name="Причина неуспеха")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Причина неуспеха"
        verbose_name_plural = "Причины неуспехов"


def get_default_status():
    return RequestStatus.objects.filter(name="Ждёт звонка").first()


class Student(models.Model):
    first_name = models.CharField(max_length=30, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=30, null=True, verbose_name="Фамилия")
    surname = models.CharField(max_length=30, null=True, blank=True, verbose_name="Отчество")
    notes = models.CharField(max_length=200, null=True, blank=True, verbose_name="Заметка")
    phone = models.CharField(max_length=13, blank=True, null=True, verbose_name="Номер телефона")
    laptop = models.BooleanField(default=False, null=True, verbose_name="Наличиее ноутбука")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Департамент", null=True)
    came_from = models.ForeignKey(AdvertisingSource, on_delete=models.CASCADE, null=True, verbose_name="Откуда пришёл")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, verbose_name="Метод оплаты")
    status = models.ForeignKey(RequestStatus, blank=True, default=get_default_status, on_delete=models.CASCADE, verbose_name="Статус заявки")
    paid = models.BooleanField(default=False, null=True, verbose_name="Оплатил или нет")
    reason = models.ForeignKey(Reason, null=True, on_delete=models.CASCADE, verbose_name="Причина неуспешной сделки")
    on_request = models.BooleanField(default=True, null=True, verbose_name="На этапе заявки")
    request_created_at = models.TimeField(auto_now_add=True, null=True, blank=True, verbose_name="Время создания заявки")
    is_archive = models.BooleanField(default=False, blank=True, null=True, verbose_name="Архивировать")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class Payment(models.Model):
    amount = models.FloatField(verbose_name="Сумма")
    client_card = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Кто оплатил")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата оплаты")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")

    def __str__(self):
        return f'{self.client_card}'

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
