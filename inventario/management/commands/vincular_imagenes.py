import csv
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from inventario.models import Componente


class Command(BaseCommand):
    help = (
        'Vincula las imágenes locales de media/componentes/ con los componentes '
        'en la base de datos usando el SKU del CSV.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            default='nexotech_hardware_20260430_162654.csv',
            help='Ruta al archivo CSV con la columna imagen_url (default: nexotech_hardware_20260430_162654.csv)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué se haría sin guardar cambios en la BD.',
        )

    def handle(self, *args, **options):
        csv_path = Path(options['csv'])
        dry_run = options['dry_run']

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f'No se encontró el CSV: {csv_path}'))
            return

        # Construir un mapa { nombre_archivo: ruta_relativa } de las imágenes disponibles
        componentes_dir = Path(settings.MEDIA_ROOT) / 'componentes'
        if not componentes_dir.exists():
            self.stdout.write(self.style.ERROR(f'No existe la carpeta: {componentes_dir}'))
            return

        imagenes_disponibles = {
            f.name: f'componentes/{f.name}'
            for f in componentes_dir.iterdir()
            if f.is_file()
        }
        self.stdout.write(f'Imágenes encontradas en disco: {len(imagenes_disponibles)}')

        actualizados = 0
        sin_imagen = 0
        no_encontrado = 0

        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                nombre = row.get('nombre', '').strip()
                imagen_url = row.get('imagen_url', '').strip()

                if not nombre:
                    continue

                # Extraer el nombre de archivo desde la URL del CSV
                # Ej: "https://.../CP-AMD-100-100001585BOX-97045a.jpg" → "CP-AMD-100-100001585BOX-97045a.jpg"
                nombre_archivo = imagen_url.split('/')[-1] if imagen_url else ''

                ruta_relativa = imagenes_disponibles.get(nombre_archivo)

                try:
                    componente = Componente.objects.get(nombre=nombre)
                except Componente.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'  [NO ENCONTRADO EN BD] {nombre[:60]}')
                    )
                    no_encontrado += 1
                    continue

                if not ruta_relativa:
                    self.stdout.write(
                        self.style.WARNING(f'  [SIN IMAGEN LOCAL] {nombre_archivo or "(sin url)"} → {nombre[:50]}')
                    )
                    sin_imagen += 1
                    continue

                if dry_run:
                    self.stdout.write(
                        f'  [DRY-RUN] {nombre[:50]} => {ruta_relativa}'
                    )
                else:
                    componente.imagen = ruta_relativa
                    componente.save(update_fields=['imagen'])
                    self.stdout.write(
                        self.style.SUCCESS(f'  OK {nombre[:50]} => {ruta_relativa}')
                    )
                actualizados += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Resumen: {actualizados} vinculados, {sin_imagen} sin imagen local, {no_encontrado} no encontrados en BD.'
        ))
        if dry_run:
            self.stdout.write(self.style.WARNING('(Modo dry-run: no se guardó nada en la BD)'))
