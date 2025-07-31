from django.shortcuts import render
from rest_framework import viewsets
from .models import Servicio, Usuario, User
from .serializers import ServicioSerializer, UsuarioSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        try:
            usuario = Usuario.objects.get(user=user)
            data['user_id'] = user.id
            data['username'] = user.username
            data['email'] = user.email
            data['telefono'] = usuario.telefono
            data['direccion'] = usuario.direccion
        except Usuario.DoesNotExist:
            data['user_id'] = user.id
            data['username'] = user.username
            data['email'] = user.email

        return data
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Sesion cerrada correctamente"}, status = status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Token invalido o ya fue usado"}, status = status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        telefono = data.get("telefono")
        direccion = data.get("direccion")
        if User.objects.filter(username = username).exists():
            return Response({"error": "El nombre de usuario ya existe"}, status = status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username = username, password = password, email = email)
        usuario = Usuario.objects.create(user = user, telefono = telefono, direccion = direccion)
        return Response({"id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "telefono": usuario.telefono,
                        "direccion": usuario.direccion}, status = status.HTTP_201_CREATED)

@api_view(['POST'])
def create_test_users(request):
    try:
        # Usuario 1
        user1 = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        usuario1 = Usuario.objects.create(
            user=user1,
            telefono='123456789',
            direccion='Calle Admin 123'
        )
        
        # Usuario 2
        user2 = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        usuario2 = Usuario.objects.create(
            user=user2,
            telefono='987654321',
            direccion='Calle Test 456'
        )
        
        return Response({
            'message': 'Usuarios de prueba creados exitosamente',
            'usuarios': [
                {
                    'username': user1.username,
                    'password': 'admin123',
                    'email': user1.email
                },
                {
                    'username': user2.username,
                    'password': 'testpass123',
                    'email': user2.email
                }
            ]
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Error creando usuarios: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)