from django.contrib import admin
from .models import Categoria, Componente

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'precio', 'stock')
    list_filter = ('marca', 'categoria') # Filtros laterales pro
    search_fields = ('nombre',) # Buscador de hardware