from rest_framework import serializers

from octofit_tracker.models import Activity, Leaderboard, Team, User, Workout


class ObjectIdToStringMixin:
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.pk)


class TeamSerializer(ObjectIdToStringMixin, serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class UserSerializer(ObjectIdToStringMixin, serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'team']


class ActivitySerializer(ObjectIdToStringMixin, serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Activity
        fields = ['id', 'user', 'type', 'duration', 'distance']


class LeaderboardSerializer(ObjectIdToStringMixin, serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'score']


class WorkoutSerializer(ObjectIdToStringMixin, serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description']
