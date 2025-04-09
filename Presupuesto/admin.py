from sys import path
from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape, letter
from .forms import GastoForm  # Importar desde .forms, no desde Presupuesto.forms
from .models import Presupuesto
from Presupuesto.models import Gasto, Ingreso
import openpyxl


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
    

     # Acción para exportar a PDF
    actions = ['exportar_pdf']

    def exportar_pdf(self, request, queryset):
        # Crear el archivo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="presupuestos.pdf"'
        #response['Content-Disposition'] = 'attachment; filename="presupuestos.pdf"'

        # Crear un PDF canvas
        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle("Reporte de Presupuestos")

        # Ajustes iniciales del PDF
        y = 750  # Posición vertical inicial
        pdf.setFont("Helvetica", 12)
        
        # Título del documento
        pdf.drawString(100, y, "REPORTE DE PRESUPUESTO MENSUAL")
        y -= 30

        # Cabeceras de la tabla
        pdf.drawString(30, y, "Nombre")
        pdf.drawString(120, y, "Monto Total")
        pdf.drawString(220, y, "Monto Actual")
        pdf.drawString(320, y, "Monto Gastado")
        pdf.drawString(420, y, "Saldo Disponible")
        pdf.drawString(520, y, "Fecha Creación")
        y -= 20

        # Añadir datos de los presupuestos
        for presupuesto in queryset:
            pdf.drawString(30, y, presupuesto.nombre)
            pdf.drawString(120, y, f"${presupuesto.monto_total}")
            pdf.drawString(220, y, f"${presupuesto.monto_actual}")
            pdf.drawString(320, y, f"${presupuesto.monto_gastado}")
            pdf.drawString(420, y, f"${presupuesto.saldo_disponible}")
            pdf.drawString(520, y, presupuesto.fecha_creacion.strftime('%Y-%m-%d'))
            y -= 20

            # Verificar si hemos llegado al final de la página
            if y <= 50:
                pdf.showPage()  # Crear una nueva página si es necesario
                y = 750

        pdf.save()  # Guardar el PDF

        return response

    exportar_pdf.short_description = "Exportar a PDF"

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

  # Acciones para exportar a PDF y Excel
    actions = ['exportar_pdf', 'exportar_excel']

    def exportar_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="gastos.pdf"'
        pdf = canvas.Canvas(response, pagesize=landscape(letter))
        pdf.setTitle("Reporte de Gastos")
        y = 550
        pdf.setFont("Helvetica", 12)
        pdf.drawString(200, y, "REPORTE DE GASTOS")
        y -= 30
        pdf.drawString(30, y, "Presupuesto")
        pdf.drawString(220, y, "Descripción")
        pdf.drawString(520, y, "Monto")
        pdf.drawString(620, y, "Fecha")
        y -= 20
        total_monto = 0
        for gasto in queryset:
            pdf.drawString(30, y, gasto.presupuesto.nombre)
            pdf.drawString(220, y, gasto.descripcion)
            pdf.drawString(520, y, f"${gasto.monto:.2f}")
            pdf.drawString(620, y, gasto.fecha.strftime('%Y-%m-%d') if gasto.fecha else '')
            total_monto += gasto.monto
            y -= 20
            if y <= 50:
                pdf.showPage()
                y = 550
        y -= 20
        pdf.drawString(520, y, f"Total: ${total_monto:.2f}")
        pdf.save()
        return response

    def exportar_excel(self, request, queryset):
        # Crear un libro de trabajo
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Gastos"

        # Agregar cabeceras
        ws.append(["Presupuesto", "Descripción", "Monto", "Fecha"])

        total_monto = 0

        # Agregar datos de los gastos
        for gasto in queryset:
            ws.append([gasto.presupuesto.nombre, gasto.descripcion, gasto.monto, gasto.fecha.strftime('%Y-%m-%d') if gasto.fecha else ''])
            total_monto += gasto.monto

        # Agregar la fila de total
        ws.append(["", "Total:", total_monto])

        # Configuración de la respuesta HTTP
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="gastos.xlsx"'
        wb.save(response)

        return response

    exportar_pdf.short_description = "Exportar a PDF"
    exportar_excel.short_description = "Exportar a Excel"

