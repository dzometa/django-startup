from django.utils import timezone # type: ignore
import re
from django.db import models # type: ignore
from django.core.exceptions import ValidationError # type: ignore


#ESTATUS
class Estatu(models.Model):
    nom_estatu = models.CharField(max_length=200)
    Descripcion = models.CharField(max_length=200)
    def __str__(self):
        return self.nom_estatu
    

#FASES 
class Fase(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

      
# MODEL PROYECTO
class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)  # Puedes agregar una descripción del proyecto
    fecha_inicio = models.DateField()  # Fecha de inicio del proyecto
    fecha_fin = models.DateField(blank=True, null=True)  # Fecha de finalización del proyecto (opcional)
    monto_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)  # Monto total del proyecto

    def __str__(self):
        return self.nombre
#SEGUIMEINTO PROYECTOS
class SeguimientoProyectos(models.Model):
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='seguimientos')
    id_fase = models.ForeignKey(Fase, on_delete=models.CASCADE, related_name='seguimientos')
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    id_estatus = models.ForeignKey(Estatu, on_delete=models.CASCADE, related_name='seguimientos')
    
    def __str__(self):
        return f"{self.id_proyecto.nombre} - {self.id_fase.nombre} - {self.descripcion}"  
#CLIENTES
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del cliente
    empresa = models.CharField(max_length=100, blank=True, null=True)  # Empresa asociada (opcional)
    nit = models.CharField(max_length=17, unique=True)  # NIT, con validación de longitud y único
    dui = models.CharField(max_length=10, unique=True)  # DUI, único y con longitud de 10
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='clientes')  # Relación con Proyecto
    monto = models.DecimalField(max_digits=100, decimal_places=2)  # Monto relacionado con el cliente
   

    def __str__(self):
        return f"{self.nombre} - {self.empresa}- {self.proyecto}- {self.monto}"
    #def __str__(self):
     #   return 'Nombre %s Empresa %s'% (self.nombre, self.empresa)
        
    #class Meta:
     #   verbose_name_plural = "Clientes"
    def clean(self):
        super().clean()
        
        # Validar NIT
        if len(self.nit) < 10 or len(self.nit) > 20:
            raise ValidationError({'nit': 'El NIT debe tener entre 10 y 20 caracteres.'})
        if not re.match(r'^\d+$', self.nit):
            raise ValidationError({'nit': 'El NIT debe contener solo números.'})
        
        # Validar DUI
        if len(self.dui) != 10:
            raise ValidationError({'dui': 'El DUI debe tener exactamente 10 caracteres.'})
        if not re.match(r'^\d+$', self.dui):
            raise ValidationError({'dui': 'El DUI debe contener solo números.'})
        
class Factura(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha_pago = models.DateField(default=timezone.now)  # Fecha en la que se realiza el pago
    monto = models.DecimalField(max_digits=100, decimal_places=2)
    estatus = models.ForeignKey(Estatu, on_delete=models.CASCADE, related_name='estatus')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='facturas')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='facturas')  # Relación con Proyecto
    
   
    def save(self, *args, **kwargs):
        # Sumar todas las facturas existentes del cliente
        total_facturas_cliente = sum(factura.monto for factura in self.cliente.facturas.all())

        # Verificar que el monto de la nueva factura no exceda el monto disponible del cliente
        if total_facturas_cliente + self.monto > self.cliente.monto:
            raise ValidationError(f"El monto total de las facturas ({total_facturas_cliente + self.monto}) excede el monto disponible del cliente ({self.cliente.monto}).")

        # Abonar el monto al proyecto
        self.proyecto.monto_total += self.monto
        self.proyecto.save()

        # Guardar la factura
        super(Factura, self).save(*args, **kwargs)
