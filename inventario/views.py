from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from .models import Componente, ConfiguracionPC
from .serializers import ComponenteSerializer, ConfiguracionPCSerializer

# ==========================================
# 1. VISTAS TRADICIONALES (Para páginas HTML)
# ==========================================
class ComponenteListView(ListView):
    model = Componente
    template_name = 'inventario/catalogo.html'
    context_object_name = 'componentes'

class ComponenteDetailView(DetailView):
    model = Componente
    template_name = 'inventario/detalle.html'
    context_object_name = 'componente'

# ==========================================
# 2. VISTAS DE LA API (Para regresar JSON)
# ==========================================
class ComponenteViewSet(viewsets.ModelViewSet):
    queryset = Componente.objects.all()
    serializer_class = ComponenteSerializer
    
class ConfiguracionPCViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionPC.objects.all()
    serializer_class = ConfiguracionPCSerializer
    
class ComponenteViewSet(viewsets.ModelViewSet):
    # Ordenamos por ID para que la paginación sea exacta
    queryset = Componente.objects.all().order_by('id')
    serializer_class = ComponenteSerializer

class ConfiguracionPCViewSet(viewsets.ModelViewSet):
    # Hacemos lo mismo para las PCs ensambladas
    queryset = ConfiguracionPC.objects.all().order_by('id')
    serializer_class = ConfiguracionPCSerializer