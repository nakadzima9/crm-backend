from cmsapp.models import Student
from django.db.models import Q


def find_user_by_name(names):
    qs = Student.objects.all()
    for name in names.split():
        qs = qs.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
    return qs
