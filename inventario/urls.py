from django.urls import path
from .views import ComponenteListView, ComponenteDetailView

urlpatterns = [
    # Esta es la ruta raíz de la app (ej: http://127.0.0.1:8000/)
    path('', ComponenteListView.as_view(), name='catalogo'),
    
    # Esta es la ruta para ver un producto específico
    path('componente/<int:pk>/', ComponenteDetailView.as_view(), name='detalle_componente'),
]