from django.db import models
from django.contrib.auth.models import User
class Clientemt(models.Model):
    TIPO_PERSONA = [
        ('N', 'Persona Natural'),
        ('J', 'Persona Jurídica'),

    ]

    CATEGORIA_CONTRIBUYENTE = [
        ('P', 'Pequeño'),
        ('M', 'Mediano'),
        ('G', 'Grande'),
        ('N', 'No aplica'),
    ]

    tipo_persona = models.CharField(max_length=1, choices=TIPO_PERSONA)
    categoria_contribuyente = models.CharField(
        max_length=1,
        choices=CATEGORIA_CONTRIBUYENTE,
        null=True
    )
    razon_social = models.CharField(max_length=255, null=True, unique=True)
    nombre_comercial = models.CharField(max_length=255, null=True, unique=True)
    actividad_economica = models.ForeignKey(
    'ActividadEconomica',
    on_delete=models.SET_NULL,
    null=True

     )   
    

#Seleccionar distritos 
    distritos = models.ForeignKey(
    'DistritoMunicipio',
    on_delete=models.SET_NULL,
    null=True

     )   
    
    direccion = models.TextField(null=True)
    telefonos = models.CharField(max_length=100 , null=True)
    email = models.EmailField( null=True)
    nit = models.CharField(max_length=20 , null=True,unique=True)
    dui = models.CharField(max_length=10 , null=True, unique=True)
    nrc = models.CharField(max_length=20 , null=True, unique=True)
    tarjeta_iva = models.FileField(upload_to='documentos/tarjeta_iva/', null=True, blank=True)
    tarjeta_nit = models.FileField(upload_to='documentos/tarjeta_nit/', null=True, blank=True)
    dui_documento = models.FileField(upload_to='documentos/dui/', null=True, blank=True)

    # 🧾 Información de quien recibe la factura
    nombre_receptor_factura = models.CharField(max_length=255, null=True, blank=True)
    telefono_receptor_factura = models.CharField(max_length=20, null=True, blank=True)
    correo_receptor_factura = models.EmailField(null=True, blank=True) 
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.tipo_persona == 'J' and self.razon_social:
            return f'Empresa: {self.razon_social}'
        return f'Persona Natural - NIT: {self.nit}'
    

    
class ActividadEconomica(models.Model):
    codigo = models.CharField(max_length=10 , null=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.codigo or 'Sin código'} - {self.descripcion[:50]}"


class DistritoMunicipio(models.Model):
    codigo_distrito = models.CharField(max_length=10, unique=True)
    distrito = models.CharField(max_length=100)
    codigo_municipio = models.CharField(max_length=10)
    municipio = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.distrito} - {self.municipio}"
