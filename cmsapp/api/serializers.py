import re

from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from cmsapp.models import (
    AdvertisingSource,
    Classroom,
    DepartmentOfCourse,
    Group,
    PaymentMethod,
    Payment,
    RequestStatus,
    Student,
)
from django.utils import timezone

from cmsapp.utils import get_time, get_date
from patches.custom_funcs import validate_phone
from users.models import User


# from cloudinary_storage.storage import MediaCloudinaryStorage


class AdvertisingSourceSerializer(ModelSerializer):
    class Meta:
        model = AdvertisingSource
        fields = [
            'id',
            'name'
        ]


class ClassroomSerializer(ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            'id',
            'name'
        ]


class MentorNameSerializer(ModelSerializer):
    fio = serializers.SerializerMethodField('get_fio')

    class Meta:
        model = User
        fields = ['fio']

    def get_fio(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class GroupNameAndTimeSerializer(ModelSerializer):
    start_at_time = serializers.DateTimeField(format="%H:%M", read_only=True)
    end_at_time = serializers.DateTimeField(format="%H:%M", read_only=True)

    class Meta:
        model = Group
        fields = [
            "name",
            "start_at_time",
            "end_at_time"
        ]


class DepartmentSerializer(ModelSerializer):
    mentor_set = MentorNameSerializer(read_only=True, many=True)
    group_set = GroupNameAndTimeSerializer(read_only=True, many=True)
    current_groups = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentOfCourse
        fields = [
            'id',
            'name',
            'image',
            'duration_month',
            'description',
            'is_archive',
            'mentor_set',
            'group_set',
            'price',
            'color',
            'current_groups',
        ]

    def get_mentor_queryset(self, department):
        dep = DepartmentOfCourse.objects.get(name=department)
        return User.objects.filter(department=dep, user_type='mentor')

    def get_groups_queryset(self, department):
        dep = DepartmentOfCourse.objects.get(name=department)
        return Group.objects.filter(is_archive=False, department=dep)

    def get_current_groups(self, obj):
        return Group.objects.filter(is_archive=False, department=obj).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        mentors = self.get_mentor_queryset(instance)
        groups = self.get_groups_queryset(instance)
        data['mentor_set'] = MentorNameSerializer(mentors, many=True).data
        data['group_set'] = GroupNameAndTimeSerializer(groups, many=True).data
        return data


class ArchiveDepartmentDetailSerializer(ModelSerializer):
    mentor_set = MentorNameSerializer(read_only=True, many=True)
    group_set = GroupNameAndTimeSerializer(read_only=True, many=True)
    current_groups = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentOfCourse
        fields = [
            'id',
            'name',
            'image',
            'duration_month',
            'description',
            'is_archive',
            'mentor_set',
            'group_set',
            'current_groups',
            'price',
            'color',
        ]

    def get_mentor_queryset(self, department):
        dep = DepartmentOfCourse.objects.get(name=department)
        return User.objects.filter(department=dep, user_type='mentor')

    def get_groups_queryset(self, department):
        dep = DepartmentOfCourse.objects.get(name=department)
        return Group.objects.filter(is_archive=True, department=dep)

    def get_current_groups(self, obj):
        return Group.objects.filter(is_archive=True, department=obj).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        mentors = self.get_mentor_queryset(instance)
        groups = self.get_groups_queryset(instance)
        data['mentor_set'] = MentorNameSerializer(mentors, many=True).data
        data['group_set'] = GroupNameAndTimeSerializer(groups, many=True).data
        return data


class ArchiveDepartmentStatusSerializer(ModelSerializer):
    class Meta:
        model = DepartmentOfCourse
        fields = [
            'id',
            'is_archive',
        ]


class DepartmentSerializerOnlyWithImage(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = DepartmentOfCourse
        fields = [
            'id',
            'image',
        ]

    # def update(self, instance, validated_data):
    #     storage = MediaCloudinaryStorage()
    #     storage.delete(name=instance.image.name)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.save()
    #     return instance


class DepartmentNameSerializer(ModelSerializer):
    class Meta:
        model = DepartmentOfCourse
        fields = ['name']


class GroupNameSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class GroupNameSerializerForPayment(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
        extra_kwargs = {
            'name': {'validators': []},
        }


class StudentNameSerializer(ModelSerializer):
    fio = serializers.SerializerMethodField('get_fio')

    class Meta:
        model = Student
        fields = [
            'fio',
            'payment_status'
        ]

    def get_fio(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class StudentIdSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.values_list('id', flat=True))
    # group = serializers.CharField(source="group.name", required=False)

    class Meta:
        model = Student
        fields = [
            'id',
            # 'group',
        ]


class MentorIdSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(user_type='mentor'))

    class Meta:
        model = User
        fields = [
            'id',
        ]


class MentorForListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image']


class GroupBaseSerializer(ModelSerializer):
    classroom = ClassroomSerializer()
    department = DepartmentNameSerializer()
    start_at_date = serializers.DateField(default=get_date)
    end_at_date = serializers.DateField(default=get_date)
    start_at_time = serializers.TimeField(default=get_time)
    end_at_time = serializers.TimeField(default=get_time)

    class Meta:
        abstract = True
        model = Group
        fields = [
            'id',
            'name',
            'mentor',
            'department',
            'students_max',
            'schedule_type',
            'classroom',
            'is_archive',
            'start_at_date',
            'end_at_date',
            'start_at_time',
            'end_at_time',
        ]

    def create(self, validated_data):
        classroom_data = validated_data.pop("classroom")["name"]
        department_data = validated_data.pop("department")["name"]
        mentor_data = validated_data.pop("mentor")["id"]

        dep = get_object_or_404(DepartmentOfCourse.objects.all(), name=department_data)
        room = get_object_or_404(Classroom.objects.all(), name=classroom_data)
        mtr = get_object_or_404(User.objects.all(), email=mentor_data)

        group = Group.objects.create(department=dep, classroom=room, mentor=mtr, **validated_data)
        return group

    def update(self, instance, validated_data):
        classroom_data = validated_data.pop("classroom")["name"]
        department_data = validated_data.pop("department")["name"]
        mentor_data = validated_data.pop("mentor")["id"]

        dep = get_object_or_404(DepartmentOfCourse.objects.all(), name=department_data)
        room = get_object_or_404(Classroom.objects.all(), name=classroom_data)
        mtr = get_object_or_404(User.objects.all(), email=mentor_data)

        instance = Group.objects.get(name=instance.name).update(commit=True, department=dep, mentor=mtr, classroom=room,
                                                                **validated_data)
        return instance


class GroupDetailSerializer(GroupBaseSerializer):
    mentor = MentorIdSerializer()


class GroupListSerializer(GroupBaseSerializer):
    mentor = MentorForListSerializer()
    current_students = serializers.SerializerMethodField()

    class Meta(GroupBaseSerializer.Meta):
        abstract = False
        fields = GroupBaseSerializer.Meta.fields + ['current_students']

    def get_current_students(self, obj):
        return Student.objects.filter(on_request=False, is_archive=False, blacklist=False, group=obj).count()


class ArchiveGroupListSerializer(GroupListSerializer):

    def get_current_students(self, obj):
        return Student.objects.filter(on_request=False, is_archive=True, blacklist=False, group=obj).count()


class ArchiveGroupStatusSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'is_archive',
        ]


class RequestStatusSerializer(ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = [
            'id',
            'name'
        ]


class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'id',
            'name'
        ]


def object_not_found_validate(obj: object, search_set: object) -> object:
   # buff = [key if re.match("[a-zA-Z]+__", key) else False for key, value in search_set.items()]
   # name = list(filter(lambda key: key, buff))[0].split("__")[0] if any(buff) else 'name'
    if search_set is None:
        # raise serializers.ValidationError(f"Object {search_set['name']} does note exist")
        raise serializers.ValidationError(f"Object does not exist.")
    data = obj.filter(**search_set).first()
    if not data:
        # raise serializers.ValidationError(f"Object {search_set['name']} does not exist.")
        raise serializers.ValidationError(f"Object does not exist.")
    return data


class StudentSerializer(ModelSerializer):
    department = DepartmentNameSerializer()
    payment_method = PaymentMethodSerializer()
    came_from = AdvertisingSourceSerializer()
    status = RequestStatusSerializer(required=False)
    request_date = serializers.DateTimeField(required=False, read_only=True)
    reason = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "notes",
            "phone",
            "laptop",
            "department",
            "came_from",
            "payment_method",
            "status",
            "reason",
            "on_request",
            "request_date",
            "is_archive",
        ]

    def validate_phone(self, value):
        return validate_phone(self, value)

    def create(self, validated_data):
        department_data = validated_data.pop("department")
        payment_method_data = validated_data.pop("payment_method")
        came_from_data = validated_data.pop("came_from")

        dep = object_not_found_validate(DepartmentOfCourse.objects, department_data)
        pay = object_not_found_validate(PaymentMethod.objects, payment_method_data)
        source = object_not_found_validate(AdvertisingSource.objects, came_from_data)

        student = Student(payment_method=pay, department=dep, came_from=source, **validated_data)
        student.save()
        return student

    def update(self, instance, validated_data):
        dep = get_object_or_404(DepartmentOfCourse.objects.all(), name=validated_data.pop("department")["name"])
        source = get_object_or_404(AdvertisingSource.objects.all(), name=validated_data.pop("came_from")["name"])
        payment_method = get_object_or_404(PaymentMethod.objects.all(),
                                           name=validated_data.pop("payment_method")["name"])

        status = object_not_found_validate(RequestStatus.objects.all(), search_set=validated_data.pop("status"))

        instance = Student.objects.get(phone=instance.phone, on_request=True).update \
                (
                commit=True,
                department=dep,
                came_from=source,
                payment_method=payment_method,
                status=status,
                **validated_data
            )
        instance.save()
        return instance


class StudentOnStudySerializer(ModelSerializer):
    department = DepartmentNameSerializer()
    came_from = AdvertisingSourceSerializer()
    group = serializers.CharField(source="group.name", required=False)

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "came_from",
            "department",
            "on_request",
            "is_archive",
            "blacklist",
            "laptop",
            "payment_status",
            "notes",
            "group",
        ]

    def validate_phone(self, value):
        return validate_phone(self, value)

    def get_group(self, obj):
        group_name = obj.group.name
        serializer = GroupNameSerializer(group_name)
        return serializer.data

    def create(self, validated_data):
        department_data = validated_data.pop("department")["name"]
        came_from_data = validated_data.pop("came_from")["name"]
        group_data = validated_data.pop("group")["name"]

        department = get_object_or_404(DepartmentOfCourse.objects.filter(is_archive=False), name=department_data)
        source = get_object_or_404(AdvertisingSource.objects.all(), name=came_from_data)
        group = get_object_or_404(Group.objects.filter(is_archive=False), name=group_data)

        student = Student.objects.create(department=department, came_from=source, group=group, **validated_data)
        return student

    def update(self, instance, validated_data):
        department_data = validated_data.pop("department")["name"]
        came_from_data = validated_data.pop("came_from")["name"]
        group_data = validated_data.pop("group")["name"]

        department = get_object_or_404(DepartmentOfCourse.objects.all(), name=department_data)
        source = get_object_or_404(AdvertisingSource.objects.all(), name=came_from_data)
        group = get_object_or_404(Group.objects.filter(is_archive=False), name=group_data)

        user = self.context['request'].user
        instance = Student.objects.get(phone=instance.phone, on_request=False).update(
            user=user, commit=True, department=department, group=group, came_from=source, **validated_data
        )
        return instance


class ArchiveStudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'is_archive',
        ]


class UserNameSerializer(ModelSerializer):
    acceptBy = serializers.SerializerMethodField('get_fio')

    class Meta:
        model = User
        fields = [
            'acceptBy'
        ]

    def get_fio(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class PaymentStudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'payment_status'
        ]


class PaymentListSerializer(ModelSerializer):
    user = UserNameSerializer(read_only=True)
    payment_type = PaymentMethodSerializer(read_only=True)
    client_card = StudentNameSerializer(read_only=True)
    course = DepartmentNameSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'client_card',
            'course',
            'payment_type',
            'last_payment_date',
            'payment_time',
            'user',
            'amount',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['user'] is not None:
            data['acceptBy'] = data['user']['acceptBy']
        else:
            data['acceptBy'] = data['user']
        data.pop('user')
        return data


class PaymentSerializer(ModelSerializer):
    payment_type = PaymentMethodSerializer()
    course = DepartmentNameSerializer()
    client_card = StudentIdSerializer()
    group = GroupNameSerializerForPayment(required=False)

    class Meta:
        model = Payment
        fields = [
            'id',
            'client_card',
            'group',
            'course',
            'payment_type',
            'last_payment_date',
            'payment_time',
            'amount',
        ]

    def create(self, validated_data):
        payment_type_data = validated_data.pop('payment_type')
        group = None
        if "group" in validated_data:
            group_name = validated_data.pop('group')['name']
            group = object_not_found_validate(Group.objects, {"name": group_name})
        client_card_dict = validated_data.pop('client_card')
        client_card_id = client_card_dict['id']
        #client_card_group = client_card_dict['group']
        # client_card_firstname = client_card_dict['id']
        # client_card_lastname = client_card_dict['last_name']
        course_data = validated_data.pop('course')

        pay = object_not_found_validate(PaymentMethod.objects, payment_type_data)
        # client_card = object_not_found_validate(Student.objects, {"first_name": client_card_firstname,
        # client_card = object_not_found_validate(Student.objects,
        #                                         {'id': client_card_id, 'group__name': client_card_group['name']})
        client_card = object_not_found_validate(Student.objects, {'id': client_card_id})
        course = object_not_found_validate(DepartmentOfCourse.objects, course_data)
        user = self.context['request'].user
        payment = Payment(payment_type=pay, client_card=client_card, course=course, user=user, group=group, **validated_data)
        payment.save()
        # Вызов этого самого метода для проверки всех платежей студента
        return self.check_payment(payment)

    # Метод для проверки и изменения статуса студента после оплаты
    def check_payment(self, payment):
        course = payment.course
        course_price = course.price
        client_card = payment.client_card
        course_duration_in_months = course.duration_month
        # округление ежемесячного мимимума оплаты до 2 знаков после запятой
        course_price_per_month = float(format(course_price / course_duration_in_months, '.2f'))
        total_student_amount_for_course = Payment.objects.filter(client_card=client_card,
                                                                 course=course).aggregate(sum=Sum('amount')).get('sum')
        if total_student_amount_for_course is None:
            total_student_amount_for_course = 0

        if client_card.group is None:
            if total_student_amount_for_course >= course_price_per_month:
                client_card.payment_status = 1
                if total_student_amount_for_course >= course_price:
                    client_card.payment_status = 4
                payment.save()
            return payment

        if total_student_amount_for_course < course_price_per_month * client_card.group.month_from_start:
            client_card.payment_status = 3  # Должен оплатить

        elif total_student_amount_for_course >= course_price:
            client_card.payment_status = 4  # Полностью оплатил

        else:
            client_card.payment_status = 1  # Оплачено
        payment.save()
        return payment


class BlackListSerializer(ModelSerializer):
    user = UserNameSerializer(read_only=True)
    fio = serializers.SerializerMethodField('get_fio')

    class Meta:
        model = Student
        fields = [
            'id',
            'fio',
            'user',
            'blacklist',
            'blacklist_created_at'
        ]

    def get_fio(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['user'] is not None:
            data['acceptBy'] = data['user']['acceptBy']
        else:
            data['acceptBy'] = data['user']
        data.pop('user')
        return data


class PaymentStudentNameSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()

    class Meta:
        model = Student
        fields = [
            'full_name',
        ]


class PaymentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
        ]
