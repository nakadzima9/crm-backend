from celery import shared_task
from .models import Payment, Student, Group

from django.utils import timezone
from django.db.models import Sum

from datetime import timedelta


# Задача для celery проверяющяя количество месяцев пройденных с начала учёбы группы
# Когда функция узнаёт что 30 дней пройдены т.е прошёл месяц то меняет запись в бд с количеством пройденных
# месяцев с начала учёбы группы

@shared_task
def courses_activity_check():
    groups = Group.objects.filter(is_archive=False)
    for group in groups.iterator():
        if group.start_at_date + timedelta(days=30 * group.month_from_start) < timezone.now().date():
            group.month_from_start += 1


# Проверяет платежи студентов, после прохождения 15 дней с последней оплаты минимума месяца студентом меняется его статус
# на "скоро оплата", если студент не оплатил минимум текущего месяца то его статус меняется на "должен оплатить"

# если студент оплатил минимум текущего месяца то его статус меняется на "Оплатил"
# если сумма всех оплат студента на определённый курс выше цены этого курса, то его статус меняется на "оплатил полность"

@shared_task
def students_payment_check():
    groups = Group.objects.filter(is_archive=False)
    for group in groups.iterator():
        students = Student.objects.filter(is_archive=False, blacklist=False, on_request=False, group=group)
        course = group.department
        course_price = course.price
        course_duration_in_months = course.duration_month
        course_price_per_month = float(format(course_price / course_duration_in_months, '.2f'))

        for student in students:
            total_student_amount_for_course = Payment.objects.filter(client_card=student,
                                                                     course=course).aggregate(sum=Sum('amount')).get('sum')
            if total_student_amount_for_course < course_price_per_month * group.month_from_start:
                student.payment_status = 3

            elif total_student_amount_for_course >= course_price:
                student.payment_status = 4

            else:
                student.payment_status = 1
                if group.start_at_date + timedelta(days=15 + (30 * (group.month_from_start - 1))) < timezone.now().date():
                    student.payment_status = 2
            student.save()
