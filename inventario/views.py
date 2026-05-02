from django.views.generic import ListView, DetailView
from .models import Componente

# Verifica que el nombre sea exactamente ComponenteListView
class ComponenteListView(ListView):
    model = Componente
    template_name = 'inventario/catalogo.html'
    context_object_name = 'componentes'

# Verifica que el nombre sea exactamente ComponenteDetailView
class ComponenteDetailView(DetailView):
    model = Componente
    template_name = 'inventario/detalle.html'
    context_object_name = 'componente'