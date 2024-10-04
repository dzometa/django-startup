from django import forms
from django.core.exceptions import ValidationError
from .models import Factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        monto = cleaned_data.get("monto")
        cliente = cleaned_data.get("cliente")

        if cliente and monto:
            # Calcular el total de facturas existentes del cliente
            total_facturas_cliente = sum(factura.monto for factura in cliente.facturas.all())

            # Verificar que el monto de la nueva factura no exceda el monto disponible del cliente
            if total_facturas_cliente + monto > cliente.monto:
                raise ValidationError(f"El monto total de las facturas ({total_facturas_cliente + monto}) excede el monto disponible del cliente ({cliente.monto}).")

        return cleaned_data
