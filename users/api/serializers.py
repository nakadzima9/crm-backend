from rest_framework import serializers, response
from jwt import decode as jwt_decode
from rest_framework_simplejwt.serializers import TokenVerifySerializer as _TokenVerifySerializer
from rest_framework_simplejwt.tokens import UntypedToken, RefreshToken
from rest_framework.exceptions import ValidationError

from just_visit import settings
from users.models import User
from trip.serializers import TravelUpdateSerializer, DirectionSerializer
from trip.models import TravelHistory, Direction


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'image',
                  # 'description',
                  # 'sex',
                  'user_type',
                  ]

    read_only_fields = ['user_type']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)
        else:
            return None


class ProfileSerializer(serializers.ModelSerializer):
    travel_history = TravelUpdateSerializer(many=True)

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'image',
                  # 'description',
                  # 'sex',
                  'user_type',
                  'travel_history',
                  ]

    def update(self, instance, validated_data):
        travel_histories_data = validated_data.pop('travel_history', None)
        travel_histories = (instance.travel_history).all()
        travel_histories = list(travel_histories)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        if travel_histories_data is not None:
            for travel_history_data in travel_histories_data:
                directions_data = travel_history_data.pop('direction')
                travel_history = travel_histories.pop(0)
                directions = (travel_history.direction).all()
                directions = list(directions)
                travel_history.title = travel_history_data.get('title', travel_history.title)
                travel_history.text = travel_history_data.get('text', travel_history.text)
                travel_history.save()

                if directions_data is not None:
                    for direction_data in directions_data:
                        direction = directions.pop(0)
                        direction.name = direction_data.get('name', direction.name)
                        direction.save()

        return instance


class TokenVerifySerializer(_TokenVerifySerializer):

    def validate(self, attrs):
        UntypedToken(attrs['token'])
        data = jwt_decode(attrs['token'], settings.SECRET_KEY, algorithms=['HS256'])
        user_data = User.objects.get(id=data['user_id'])
        refresh = RefreshToken.for_user(user_data)
        data = {
            'access_token': str(refresh.access_token),
            'id': data['user_id'],
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'email': user_data.email,
            'phone': user_data.phone,
            'user_type': user_data.user_type,
        }

        return data
