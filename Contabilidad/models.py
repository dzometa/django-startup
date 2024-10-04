from datetime import timezone
from django.utils import timezone
from django.db import models
from django.forms import ValidationError


# Create your models here.

class Claseficacion_Partidas(models.Model):
    Clasificacion = models.CharField(max_length=20, unique=True)
    Descripcion = models.TextField(blank=True, null=True)
   

    def __str__(self):
        return self.Clasificacion
    class Meta:
        verbose_name_plural = "Clasificacion de Partidas"

class Perfill_Empresa(models.Model): 
    Codigo_Empresa = models.CharField(max_length=20, unique=True)
    Nombre_Empresa = models.CharField(max_length=20, unique=True)
    Nombre_Comercial = models.CharField(max_length=20, unique=True)
    Numero_NIT = models.CharField(max_length=20, unique=True)
    Registro_Fiscal = models.CharField(max_length=20, unique=True)
    Giro = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.Nombre_Empresa    
    class Meta:
        verbose_name_plural = "Perfil Empresa"

class Documento(models.Model):
    Tipo_Documento = models.CharField(max_length=20, unique=True)
    Descripcion = models.TextField(blank=True, null=True)    
   
    def __str__(self):
        return self.Tipo_Documento
    
class Document(models.Model):
    Tipo_Documento = models.CharField(max_length=20, unique=True)
    Descripcion = models.TextField(blank=True, null=True)    
   
    def __str__(self):
        return self.Tipo_Documento    
    class Meta:
        verbose_name_plural = "Tipos de Documentos"
#Centro de costos
class CentroDeCosto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)  # Código único del centro de costo
    nombre = models.CharField(max_length=100)  # Nombre del centro de costo
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional
    activo = models.BooleanField(default=True)  # Estado del centro de costo, si está activo o inactivo

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
#Catalogo
class Catalogo(models.Model):
    COD_EMPRE = models.CharField(max_length=10)
    NUMERO_CUENTA = models.CharField(max_length=20)
    DESC_CUENTA = models.CharField(max_length=255)
    NIVEL_CUENTA = models.IntegerField()
    TIPO_CUENTA = models.CharField(max_length=50, choices=[
        ('activo', 'Activo'),
        ('pasivo', 'Pasivo'),
        ('patrimonio', 'Patrimonio'),
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
        ('costo', 'Costo'),
    ])
    SUMA_DETALLE = models.CharField(max_length=50, choices=[
        ('suma', 'Suma'),
        ('detalle', 'Detalle'),
    ])
    CUEN_DEPE = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcuentas')
    TIPO_SALDO = models.CharField(max_length=50, choices=[
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
    ])
    CLASIF_RESUL = models.CharField(max_length=50, choices=[
        ('resultado', 'Resultado'),
        ('balance', 'Balance'),
    ])
    CENTRO_COSTO = models.ForeignKey(CentroDeCosto, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con Centro de Costo
    AGRUPADOR_FLUJOE = models.CharField(max_length=100, blank=True, null=True)
    MANUAL_CUENTA = models.BooleanField(default=False)
    AGRUPADOR_FINANCIERO = models.CharField(max_length=100, blank=True, null=True)
    CUENTA_INACTIVA = models.BooleanField(default=False)
    DESC_CUENTA2 = models.CharField(max_length=255, blank=True, null=True)
    MOSTRAR_CONSULTA = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.NUMERO_CUENTA} - {self.DESC_CUENTA}"

    class Meta:
        verbose_name_plural = "Catálogos"

#Departamentos

class Departamentosv(models.Model):
    empresa = models.ForeignKey(Perfill_Empresa, on_delete=models.CASCADE, related_name='departamentos')
    codigo_distrito = models.CharField(max_length=10, unique=True)
    departamento_distrito = models.CharField(max_length=100)  
    encargado = models.CharField(max_length=100)

    def __str__(self):
        return self.codigo_distrito 
    class Meta:
        verbose_name_plural = "Departamentos / Distritos"    


### MODELO: Partida (Encabezado)
class Partida(models.Model):
    numero_partida = models.IntegerField(editable=False, unique=True, null=True)
    fecha = models.DateField(default=timezone.now)
    descripcion = models.TextField()
    empresa = models.ForeignKey(Perfill_Empresa, on_delete=models.CASCADE)
   # tipo_documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
   # centro_costo = models.ForeignKey(CentroDeCosto, on_delete=models.SET_NULL, null=True, blank=True)
    valor_movimiento = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.numero_partida:
            max_num = Partida.objects.aggregate(models.Max('numero_partida'))['numero_partida__max']
            self.numero_partida = (max_num or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Partida {self.numero_partida} - {self.empresa.Nombre_Empresa}"


### MODELO: DetallePartida (Detalle)
class DetallePartida(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='detalles')
    cuenta = models.ForeignKey('Catalogo', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255, blank=True)
    abono = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cargo = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Detalle {self.partida.numero_partida} - {self.cuenta.DESC_CUENTA}"


