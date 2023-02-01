from django.db import models

from users.models import User


class Department(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    patent_number = models.IntegerField(null=True)
    patent_start = models.DateField(null=True)
    patent_end = models.DateField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class GroupStatus(models.Model):
    status_name = models.CharField(max_length=15)

    def __str__(self):
        return self.status_name


class Classroom(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    started_at = models.DateField()
    duration_month = models.IntegerField()

    def __str__(self):
        return self.name


class ScheduleType(models.Model):
    type_name = models.CharField(max_length=10)


class Group(models.Model):
    number = models.IntegerField()
    students_max = models.IntegerField()
    status = models.ForeignKey(GroupStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    schedule_type = models.ForeignKey(ScheduleType, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f'Number {self.number}, status {self.status}, teacher {self.teacher}'


class AdvertisingSource(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class CardStatus(models.Model):
    status = models.CharField(max_length=15)

    def __str__(self):
        return self.status


class PaymentMethod(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class StudentCard(models.Model):
    card_number = models.IntegerField(unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    note = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    came_from = models.ForeignKey(AdvertisingSource, on_delete=models.CASCADE)
    status = models.ForeignKey(CardStatus, on_delete=models.CASCADE)
    laptop = models.BooleanField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    def __str__(self):
        return f'number {self.card_number}, student {self.student}'


class Payment(models.Model):
    amount = models.FloatField()
    client_card = models.ForeignKey(StudentCard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.client_card}'


class BlackList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    added_at = models.DateField()


class StudentCardOperation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(StudentCard, on_delete=models.CASCADE)
    status_changed_to = models.ForeignKey(CardStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
