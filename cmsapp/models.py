from django.db import models

from core import settings


class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name="Департамент")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"


class Teacher(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    patent_number = models.IntegerField(null=True, verbose_name="Номер патента")
    patent_start = models.DateField(null=True, verbose_name="Срок действия патента")
    patent_end = models.DateField(null=True, verbose_name="Срок окончания патента")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


class GroupStatus(models.Model):
    status_name = models.CharField(max_length=15, verbose_name="Статус группы")

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = "Статус группы"
        verbose_name_plural = "Статусы групп"


class Classroom(models.Model):
    name = models.CharField(max_length=15, verbose_name="Комната")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название курса")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Департамент")
    started_at = models.DateField(verbose_name="Старт курса")
    duration_month = models.IntegerField(verbose_name="Продолжительность курса в месяцах")

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
    number = models.IntegerField(verbose_name="Номер группы")
    students_max = models.IntegerField(verbose_name="Количество максимальных студентов")
    status = models.ForeignKey(GroupStatus, on_delete=models.CASCADE, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    schedule_type = models.ForeignKey(ScheduleType, on_delete=models.CASCADE, verbose_name="Тип расписания")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, verbose_name="Комната")

    def __str__(self):
        return f'Number: {self.number}, status: {self.status}'

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class AdvertisingSource(models.Model):
    name = models.CharField(max_length=15, verbose_name="Рекламный курс")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рекламный курс"
        verbose_name_plural = "Рекламные курсы"


class CardStatus(models.Model):
    status = models.CharField(max_length=15, verbose_name="Статус карточки")

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Статус карточки"
        verbose_name_plural = "Статусы карточек"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=20, verbose_name="Метод оплаты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метод оплаты"
        verbose_name_plural = "Методы оплат"


class Student(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    email = models.CharField(max_length=20, null=True, verbose_name="Почта")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Группа")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class StudentCard(models.Model):
    card_number = models.IntegerField(unique=True, verbose_name="Номер карты")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    note = models.CharField(max_length=100, blank=True, verbose_name="Заметка")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Департамент")
    came_from = models.ForeignKey(AdvertisingSource, on_delete=models.CASCADE, verbose_name="Откуда пришёл")
    status = models.ForeignKey(CardStatus, on_delete=models.CASCADE, verbose_name="Статус")
    laptop = models.BooleanField(verbose_name="Наличиее ноутбука")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, verbose_name="Метод оплаты")

    def __str__(self):
        return f'number {self.card_number}, student {self.student}'

    class Meta:
        verbose_name = "Карточка студента"
        verbose_name_plural = "Карточки студентов"


class Payment(models.Model):
    amount = models.FloatField(verbose_name="Скидка")
    client_card = models.ForeignKey(StudentCard, on_delete=models.CASCADE, verbose_name="Карта клиента")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата оплаты")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")

    def __str__(self):
        return f'{self.client_card}'

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платёжы"


class BlackList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    reason = models.CharField(max_length=100, verbose_name="Причина")
    added_at = models.DateField(verbose_name="Дата добавления")

    def __str__(self):
        return f'Student: {self.student}, reason: {self.reason}'

    class Meta:
        verbose_name = "Чёрный список"
        verbose_name_plural = "Чёрные списки"
