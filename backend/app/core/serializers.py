from rest_framework import serializers
from .models import User, Exercise, TelemetryData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'email',
            'nickname',
            'picture',
            'is_staff',
        ]


class ExerciseSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Exercise
        fields = ['course', 'slug', 'tags']


class TelemetryDataSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    exercise = ExerciseSerializer()

    class Meta:
        model = TelemetryData
        fields = ['author', 'exercise', 'points', 'submission_date', 'log']