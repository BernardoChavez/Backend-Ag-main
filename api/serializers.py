from rest_framework import serializers
from .models import Usuario
from .models import Servicio

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [ 
            'id',
            'user',
            'telefono',
            'direccion',
        ]
        read_only_fields = ['id'] 

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            'id', 
            'nombre'
        ]

#historial de telefono (usuario,fecha)


