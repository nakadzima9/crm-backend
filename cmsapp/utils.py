from cmsapp.models import Student, Group
from django.db.models import Q
from django.utils import timezone


def find_user_by_name(names):
    qs = Student.objects.all()
    for name in names.split():
        qs = qs.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        #qs = qs.filter(Q(on_request=False) & (Q(first_name__icontains=name) | Q(last_name__icontains=name)))
    return qs


def find_group_by_name(names):
    qs = Group.objects.all()
    for name in names.split():
        qs = qs.filter(Q(name__icontains=name) & Q(is_archive=False))
    return qs


def get_date():
    return timezone.now().date()


def get_time():
    return timezone.now().time()
