from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Componente(models.Model):
    MARCAS_CHOICES = [
        ('INTEL', 'Intel'),
        ('AMD', 'AMD'),
        ('NVIDIA', 'NVIDIA'),
        ('ASUS', 'Asus'),
        ('GIGABYTE', 'Gigabyte'),
        ('CORSAIR', 'Corsair'),
    ]

    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=20, choices=MARCAS_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='componentes/', null=True, blank=True)
    especificaciones_tecnicas = models.JSONField(default=dict) # Para guardar núcleos, frecuencia, etc.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.marca})"