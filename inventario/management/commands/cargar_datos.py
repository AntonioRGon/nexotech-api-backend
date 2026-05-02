import csv
from django.core.management.base import BaseCommand
from inventario.models import Componente, Categoria

class Command(BaseCommand):
    help = 'Carga componentes desde un archivo CSV'

    def handle(self, *args, **options):
        # Asegúrate de que el nombre del archivo coincida con el tuyo
        path = 'datos_tecnologia.csv' 
        
        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 1. Buscamos o creamos la categoría (ej: CPU, GPU)
                cat, _ = Categoria.objects.get_or_create(nombre=row['categoria'])
                
                # 2. Creamos el componente
                # Ajusta los nombres entre corchetes [] si Kiro les puso otros nombres en el CSV
                obj, created = Componente.objects.get_or_create(
                    nombre=row['nombre'],
                    marca=row['marca'].upper(),
                    categoria=cat,
                    precio=row['precio'],
                    defaults={
                        'stock': 15,
                        'descripcion': row.get('descripcion', ''),
                        # Si tu CSV tiene specs, las guardamos como JSON
                        'especificaciones_tecnicas': {'info': row.get('especificaciones', 'N/A')}
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Añadido: {row['nombre']}"))

        self.stdout.write(self.style.SUCCESS('--- ¡Proceso de importación terminado! ---'))