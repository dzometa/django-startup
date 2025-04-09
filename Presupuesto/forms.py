from django import forms
from django.core.exceptions import ValidationError
from .models import Gasto

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['presupuesto', 'monto', 'descripcion', 'fecha']

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        presupuesto = self.cleaned_data.get('presupuesto')

        # Verificar que el gasto no exceda el presupuesto disponible
        presupuesto_disponible = presupuesto.monto_actual
        if monto > presupuesto_disponible:
            raise ValidationError(f"El gasto de {monto} excede el presupuesto disponible ({presupuesto_disponible}).")
        
        return monto
