from rest_framework import serializers
from .models import Componente, ConfiguracionPC

# El que ya tenías
class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = '__all__'

# EL NUEVO
class ConfiguracionPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionPC
        fields = '__all__'