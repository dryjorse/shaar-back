from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterUserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, permissions
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class RegisterUserView(APIView):
  def post(self, request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()

      refresh = RefreshToken.for_user(user)
      access_token = str(refresh.access_token)
      refresh_token = str(refresh)

      response_data = {
        'user': {
          'id': user.id,
          'username': user.username,
          'email': user.email,
        },
        'tokens': {
          'access': access_token,
          'refresh': refresh_token
        }
      }
      return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
  def post(self, request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
      return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      # Найти пользователя по email
      user = User.objects.get(email=email)
      # Аутентификация пользователя
      user = authenticate(email=user.email, password=password)
    
      if user is not None:
        # Создание JWT токенов  
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Создание ответа
        response_data = {
          'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
          },
          'tokens': {
            'access': access_token,
            'refresh': refresh_token
          }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
      return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
  
class ProfileView(generics.RetrieveAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = ProfileSerializer

  def get_object(self):
    return self.request.user