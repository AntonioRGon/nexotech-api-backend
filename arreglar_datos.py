import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexotech.settings')
django.setup()

from inventario.models import Componente

def vincular_total():
    ruta_media = os.path.join('media', 'componentes')
    archivos_reales = os.listdir(ruta_media)
    
    componentes = Componente.objects.all()
    print(f"🛠️ Reparando {componentes.count()} componentes...")

    for c in componentes:
        nombre_up = c.nombre.upper()
        # Sacamos todas las palabras del nombre que tengan más de 2 letras
        palabras_clave = [p for p in nombre_up.replace(",", "").split() if len(p) > 2]
        
        match_encontrado = None
        
        for archivo in archivos_reales:
            archivo_up = archivo.upper()
            # Si el modelo específico (ej: G305) está en el nombre del archivo, es ese.
            # Buscamos la palabra más "rara" del nombre del producto (suele ser el modelo)
            for palabra in palabras_clave:
                if palabra in archivo_up and palabra not in ['GAMER', 'PARA', 'NEGRO', 'BLANCO', 'DDR4', 'DDR5']:
                    match_encontrado = archivo
                    break
            if match_encontrado: break

        if match_encontrado:
            c.imagen = f"componentes/{match_encontrado}"
            # Arreglo de Marca de una vez
            for m in ['LOGITECH', 'ASUS', 'AMD', 'INTEL', 'MSI', 'GIGABYTE', 'KINGSTON', 'CORSAIR', 'ACER', 'HP', 'DELL']:
                if m in match_encontrado.upper() or m in nombre_up:
                    c.marca = m
            c.save()
            print(f"✅ VINCULADO: {c.nombre[:30]}... ➡️ {match_encontrado}")
        else:
            print(f"❌ NO SE ENCONTRÓ: {c.nombre[:40]}")

if __name__ == '__main__':
    vincular_total()