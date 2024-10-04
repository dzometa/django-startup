from django.contrib import admin

from .forms import GastoForm  # Importar desde .forms, no desde Presupuesto.forms
from .models import Presupuesto
from Presupuesto.models import Gasto, Ingreso

# Register your models here.
@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'monto_total', 'monto_actual', 'monto_gastado', 'saldo_disponible', 'estado', 'fecha_creacion')
    search_fields = ('nombre', 'estado')
    list_filter = ('estado', 'fecha_creacion')

    def monto_gastado(self, obj):
        return obj.monto_gastado

    def saldo_disponible(self, obj):
        return obj.saldo_disponible

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('presupuesto', 'monto', 'fecha')
    search_fields = ('presupuesto__nombre',)
    list_filter = ('fecha',)

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    form = GastoForm
    list_display = ('presupuesto','descripcion', 'monto', 'fecha')
    search_fields = ('presupuesto__nombre',)
    list_filter = ('fecha',)