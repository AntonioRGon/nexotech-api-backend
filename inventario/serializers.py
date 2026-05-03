from rest_framework import serializers
from .models import Componente

class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = '__all__' # Expone todos los campos del modelo