from datetime import timezone
from django import forms
from django.contrib import admin

from Contabilidad.forms import CatalogoForm
from .models import  DetallePartida, Partida, Perfill_Empresa
from .models import Claseficacion_Partidas
from .models import Document
from .models import CentroDeCosto
from .models import Catalogo
from .models import Departamentosv

# Register your models here.
@admin.register(Perfill_Empresa)
class PerfilEmpresa(admin.ModelAdmin):
    list_display = ('Codigo_Empresa', 'Nombre_Empresa', 'Nombre_Comercial')
    #search_fields = ('Nombre_Empresa', 'Codigo_Empresa')
    #list_display = ('Codigo_Empresa', 'Nombre_Empresa',  'Nombre_Comercial', 'Numero_NIT', 'Registro_Fiscal')

@admin.register(CentroDeCosto)
class CentroDeCostoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'activo')
    search_fields = ('codigo', 'nombre')
    list_filter = ('activo',)

class CatalogoAdmin(admin.ModelAdmin):
    form = CatalogoForm
    list_display = ('NUMERO_CUENTA', 'DESC_CUENTA', 'NIVEL_CUENTA', 'TIPO_CUENTA', 'is_padre', 'CENTRO_COSTO', 'CUENTA_INACTIVA')
    search_fields = ('NUMERO_CUENTA', 'DESC_CUENTA', 'CENTRO_COSTO')
    list_filter = ('TIPO_CUENTA', 'NIVEL_CUENTA')  # Agrega filtros si es necesario
    ordering = ('NUMERO_CUENTA',)  # Ordena por el campo NUMERO_CUENTA por defecto

    def is_padre(self, obj):
        return obj.CUEN_DEPE is None
    is_padre.boolean = True
    is_padre.short_description = 'Es Cuenta Padre'



admin.site.register(Catalogo, CatalogoAdmin)

@admin.register(Claseficacion_Partidas)
class Claseficacion_Partidas(admin.ModelAdmin):
    list_display = ('Clasificacion', 'Descripcion')    


@admin.register(Document)
class Tipos_Documentos(admin.ModelAdmin):
    list_display = ('Tipo_Documento', 'Descripcion')


@admin.register(Departamentosv)
class Departamentos(admin.ModelAdmin):
    list_display = ('empresa','codigo_distrito','departamento_distrito'
                    ,'encargado')
    

class DetallePartidaInline(admin.TabularInline):
    model = DetallePartida
    extra = 1  # Permitir agregar más detalles al crear una partida

class PartidaAdmin(admin.ModelAdmin):
    list_display = ('numero_partida', 'empresa', 'fecha', 'valor_movimiento')
    inlines = [DetallePartidaInline]  # Mostrar los detalles como parte del formulario de partida

#admin.site.register(Partida, PartidaAdmin)

class PartidaDateFilter(admin.SimpleListFilter):
    title = 'Fecha de creación'  # Nombre del filtro en la interfaz
    parameter_name = 'fecha'

    def lookups(self, request, model_admin):
        return (
            ('hoy', 'Hoy'),
            ('ultima_semana', 'Última semana'),
            ('este_mes', 'Este mes'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'hoy':
            return queryset.filter(fecha__date=timezone.now().date())
        if self.value() == 'ultima_semana':
            return queryset.filter(fecha__gte=timezone.now() - timezone.timedelta(days=7))
        if self.value() == 'este_mes':
            return queryset.filter(fecha__month=timezone.now().month)
        return queryset


class PartidaAdmin(admin.ModelAdmin):
    list_display = ('numero_partida', 'empresa', 'fecha', 'valor_movimiento')
    list_filter = ('empresa', 'numero_partida', PartidaDateFilter)  # Filtros disponibles en el admin
    search_fields = ('numero_partida', 'empresa__nombre', 'descripcion')
    inlines = [DetallePartidaInline]
admin.site.register(Partida, PartidaAdmin)