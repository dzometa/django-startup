from django.contrib import admin

from .models import ActividadEconomica
from django.template.response import TemplateResponse
from .models import DistritoMunicipio  # Asegúrate que el import esté correcto


admin.site.site_header = "Portal de Administración de Clientes"
admin.site.site_title = "Admin Clientes"
admin.site.index_title = "Bienvenido al portal de gestión"

# Register your models here.
from .models import Clientemt
@admin.register(Clientemt)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'nombre_comercial', 'tipo_persona', 'dui_documento', 'tarjeta_iva', 'tarjeta_nit')
    search_fields = ('razon_social', 'nombre_comercial', 'nit', 'actividad_economica__descripcion')
    list_filter = ('tipo_persona', 'actividad_economica')
   # Mostrar solo los registros del usuario logueado
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    # Asignar automáticamente el usuario logueado
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Solo en creación, no al editar
            obj.usuario = request.user
        super().save_model(request, obj, form, change)    

    def index(self, request, extra_context=None):
        # Removemos las acciones recientes pasando un contexto sin ellas
        if extra_context is None:
            extra_context = {}
        extra_context['app_list'] = self.get_app_list(request)
        return TemplateResponse(request, self.index_template or 'admin/index.html', extra_context)

@admin.register(ActividadEconomica)
class ActividadEconomicaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')
 


@admin.register(DistritoMunicipio)
class DistritoMunicipioAdmin(admin.ModelAdmin):
    list_display = ('codigo_distrito', 'distrito', 'codigo_municipio', 'municipio')
    search_fields = ('distrito', 'municipio', 'codigo_distrito', 'codigo_municipio')
    list_filter = ('distrito',)