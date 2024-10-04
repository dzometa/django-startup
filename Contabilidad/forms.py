from django import forms
from .models import Catalogo
from Contabilidad import models
from django.db.models import Sum  # Asegúrate de importar Sum desde django.db.models

class CatalogoForm(forms.ModelForm):
    class Meta:
        model = Catalogo
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar opciones del campo CUEN_DEPE basado en TIPO_CUENTA
        if self.instance and self.instance.pk:
            # Si estamos editando una cuenta existente
            if self.instance.TIPO_CUENTA == 'detalle':
                self.fields['CUEN_DEPE'].queryset = Catalogo.objects.filter(SUMA_DETALLE='suma')
            else:
                self.fields['CUEN_DEPE'].queryset = Catalogo.objects.none()
        else:
            # Si estamos creando una nueva cuenta
            tipo_cuenta = self.data.get('TIPO_CUENTA') if self.data else None
            if tipo_cuenta == 'detalle':
                self.fields['CUEN_DEPE'].queryset = Catalogo.objects.filter(SUMA_DETALLE='suma')
            else:
                self.fields['CUEN_DEPE'].queryset = Catalogo.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        tipo_cuenta = cleaned_data.get("TIPO_CUENTA")
        
        # Validar y ajustar el valor de CUEN_DEPE
        if tipo_cuenta == 'detalle':
            if not cleaned_data.get("CUEN_DEPE"):
                raise forms.ValidationError("Debe seleccionar una cuenta padre para cuentas de tipo detalle.")
        
        return cleaned_data
