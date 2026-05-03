from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from .models import Componente
from .serializers import ComponenteSerializer

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