from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

class CustomUserCreateSerializer(UserCreateSerializer):
  class Meta(UserCreateSerializer.Meta):
    model = get_user_model()
    fields = ('email', 'password')

class RegisterUserSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True, 
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  username = serializers.CharField(
    required=True, 
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

  class Meta:
    model = User
    fields = ['email', 'password', 'username', 'ava']
    extra_kwargs = {
      'password': {'write_only': True, 'min_length': 3},
    }
    
  def create(self, validated_data):
    user = self.Meta.model.objects.create(
      email=validated_data['email'],
      username=validated_data['username'],
      ava=validated_data['ava'],
    )

    user.set_password(validated_data['password'])
    user.save()

    return user
    
class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email']