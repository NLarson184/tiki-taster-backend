from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # ratings = serializers.HyperlinkedIdentityField(many=True, view_name='ratings-list', read_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'is_official']