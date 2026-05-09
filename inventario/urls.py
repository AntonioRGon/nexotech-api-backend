from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComponenteListView, ComponenteDetailView, ComponenteViewSet, ConfiguracionPCViewSet


# Configuración del Router para la API
router = DefaultRouter()
router.register(r'componentes', ComponenteViewSet)
router.register(r'configuraciones', ConfiguracionPCViewSet)

urlpatterns = [
    # -----------------------------------
    # RUTAS WEB (Tu catálogo visual en HTML)
    # -----------------------------------
    path('', ComponenteListView.as_view(), name='catalogo'),
    path('componente/<int:pk>/', ComponenteDetailView.as_view(), name='detalle_componente'),
    
    # -----------------------------------
    # RUTAS API (Tu Backend JSON para NexoTech)
    # -----------------------------------
    path('api/', include(router.urls)), 
]