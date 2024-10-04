from audioop import reverse
from django.http import HttpResponseRedirect # type: ignore
from os import path
from django.contrib import admin # type: ignore

from register import form
from django import forms # type: ignore
from register.form import FacturaForm
from register.views import generate_invoice_pdf # type: ignore
from .models import Cliente# Importa el modelo que acabas de crear
from .models import Factura
from .models import Proyecto
from .models import Estatu
from .models import SeguimientoProyectos
from .models import Fase


@admin.register(Fase)
class Fase(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(SeguimientoProyectos)
class SeguimientoProyectosAdmin(admin.ModelAdmin):
    list_display = ('id_proyecto', 'id_fase', 'descripcion', 'fecha_inicio', 'fecha_fin', 'id_estatus')
    search_fields = ('descripcion',)




@admin.register(Estatu)
class Estatus(admin.ModelAdmin):
     search_fields=('nom_estatu','Descripcion')
     list_display = ('nom_estatu','Descripcion')



@admin.register(Proyecto)
class Proyecto(admin.ModelAdmin):
    search_fields=('nombre','descripcion')
    list_display = ('nombre','descripcion','fecha_inicio','fecha_fin', 'monto_total')
    
    

 
@admin.register(Cliente)

class RegisCli(admin.ModelAdmin):
    search_fields=('nombre','empresa')
    list_display = ('nombre','empresa','proyecto','monto_formateado')

    def monto_formateado(self, obj):# Formatea el monto con signo de dólar
        return f"${obj.monto:,.2f}" 
    
    monto_formateado.short_description = 'Monto Dolar' #Nombre de la columna en la vista de lista
    list_per_page =2

    def generate_invoice_pdf(self, request, queryset):
        ids = ",".join(str(factura.id) for factura in queryset)
        url = reverse('generate_invoice_pdf', args=[ids])
        return HttpResponseRedirect(url) 

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    form = FacturaForm

    search_fields = ('numero_factura', 'estatus')
    list_display = ('numero_factura', 'monto','estatus', 'cliente_formateado','fecha_pago')

    def cliente_formateado(self, obj):
        return f"{obj.cliente.nombre} ({obj.cliente.empresa})"
    
    cliente_formateado.short_description = 'Cliente-Factura'

    