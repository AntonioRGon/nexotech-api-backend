import csv
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from inventario.models import Componente

class Command(BaseCommand):
    help = 'Importa hardware desde el archivo CSV'

    def handle(self, *args, **options):
        # Usamos el nombre exacto que aparece en tu terminal
        csv_path = Path('nexotech_hardware_20260430_162654.csv')
        
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f'No se encontró: {csv_path}'))
            return

        with open(csv_path, encoding='utf-8') as f:
            # DictReader usa la primera fila como nombres de columnas
            reader = csv.DictReader(f)
            count = 0
            
            for row in reader:
                # 1. Gestión de imagen (Asumiendo que el CSV tiene la ruta local)
                # Si el CSV no tiene la ruta, usaremos el nombre del producto
                nombre_foto = f"{row['nombre'][:15].lower().replace(' ', '_')}.jpg"
                
                # Intentamos buscar la foto en una carpeta probable
                # Si tienes las fotos en otro lado, ajusta 'data/imagenes'
                origen = Path('../data/imagenes') / nombre_foto
                destino = Path('media/productos') / nombre_foto
                
                if origen.exists():
                    destino.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(origen, destino)

                # 2. Carga en Base de Datos
                Componente.objects.update_or_create(
                    nombre=row['nombre'],
                    defaults={
                        'marca': row.get('marca', 'S/M'),
                        'precio': float(row['precio'].replace('$', '').replace(',', '')),
                        'imagen': f"productos/{nombre_foto}" if origen.exists() else None,
                        'stock': 10,
                    }
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se cargaron {count} productos desde el CSV.'))