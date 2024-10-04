from django.shortcuts import render # type: ignore
from django.http import HttpResponse # type: ignore
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle # type: ignore
from reportlab.lib import colors # type: ignore
from .models import  Factura
from io import BytesIO





def generate_invoice_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Obtener todos los datos de las facturas
    facturas = Factura.objects.all().values_list('numero_factura', 'fecha_pago', 'estatus', 'cliente__nombre', 'cliente__empresa')

    # Encabezado de la tabla
    data = [['Número de Factura', 'Fecha de Pago', 'Estatus', 'Nombre del Cliente', 'Empresa del Cliente']]
    
    # Agregar los datos de las facturas a la tabla
    for factura in facturas:
        data.append(factura)
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura_report.pdf"'
    return response


