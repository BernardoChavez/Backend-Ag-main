from rest_framework import routers
router = routers.DefaultRouter()

from django.urls import path, include
from .views import ServicioViewSet, UsuarioViewSet, CustomTokenObtainPairView, LogoutView, RegisterView

router.register('api/Servicios', ServicioViewSet)
router.register('api/usuarios', UsuarioViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),    
    path('api/logout/', LogoutView.as_view(), name='logout'),   
    path('api/register/', RegisterView.as_view(), name='register'),     
]