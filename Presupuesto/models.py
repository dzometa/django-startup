from django.db import models
from django.forms import ValidationError

# Create your models here.
class Presupuesto(models.Model):
    nombre = models.CharField(max_length=255, help_text="Nombre del presupuesto")
    descripcion = models.TextField(blank=True, help_text="Descripción del presupuesto")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto total inicial del presupuesto")
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Monto actual disponible")
    fecha_creacion = models.DateField(auto_now_add=True, help_text="Fecha de creación del presupuesto")
    fecha_inicio = models.DateField(help_text="Fecha de inicio del presupuesto")
    fecha_fin = models.DateField(help_text="Fecha de finalización del presupuesto")
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado')], default='Pendiente', help_text="Estado del presupuesto")

    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"
        ordering = ['fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - {self.monto_actual}"

    def actualizar_monto(self):
        # Actualiza el monto actual en función de los ingresos y gastos relacionados
        ingresos_total = sum(ingreso.monto for ingreso in self.ingresos.all())
        gastos_total = sum(gasto.monto for gasto in self.gastos.all())
        self.monto_actual = self.monto_total + ingresos_total - gastos_total
        self.save()

    @property
    def monto_gastado(self):
        # Calcula la suma de todos los gastos relacionados con este presupuesto
        total_gastado = self.gastos.aggregate(total=models.Sum('monto'))['total'] or 0
        return total_gastado

    @property
    def saldo_disponible(self):
        # Resta el total gastado del monto total del presupuesto
        return self.monto_actual - self.monto_gastado    

class Ingreso(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, related_name='ingresos', on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto del ingreso")
    descripcion = models.TextField(blank=True, help_text="Descripción del ingreso")
    fecha = models.DateField(help_text="Fecha del ingreso")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.presupuesto.actualizar_monto()

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"

    def __str__(self):
        return f"Ingreso de {self.monto} para {self.presupuesto.nombre}"

class Gasto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, related_name='gastos', on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto del gasto")
    descripcion = models.TextField(blank=True, help_text="Descripción del gasto")
    fecha = models.DateField(help_text="Fecha del gasto")
    
    def save(self, *args, **kwargs):
        # Verificar si hay suficiente saldo en el presupuesto antes de guardar el gasto
        presupuesto_disponible = self.presupuesto.monto_actual
        if self.monto > presupuesto_disponible:
            raise ValidationError(f"No se puede gastar {self.monto}. El presupuesto disponible es {presupuesto_disponible}.")
        
        super().save(*args, **kwargs)
        self.presupuesto.actualizar_monto()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.presupuesto.actualizar_monto()

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self):
        return f"Gasto de {self.monto} para {self.presupuesto.nombre}"