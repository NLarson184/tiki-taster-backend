from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'is_official', 'password']
    
    def create(self, validated_data):
        print(validated_data)
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            is_official=False
        )
        
        return user