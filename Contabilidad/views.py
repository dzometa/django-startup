from django.shortcuts import render, redirect, get_object_or_404
from .forms import CatalogoForm
from .models import Partida
from .models import Catalogo

def crear_cuenta(request, pk=None):
    if pk:
        cuenta = get_object_or_404(Catalogo, pk=pk)
    else:
        cuenta = None

    if request.method == 'POST':
        form = CatalogoForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('nombre_de_tu_vista')  # Cambia 'nombre_de_tu_vista' por el nombre adecuado
    else:
        form = CatalogoForm(instance=cuenta)

    return render(request, 'Contabilidad/crear_editar_cuenta.html', {'form': form})


def partidas_por_fecha(request):
    partidas = Partida.objects.all()

    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    if fecha_desde and fecha_hasta:
        partidas = partidas.filter(fecha__range=[fecha_desde, fecha_hasta])

    context = {
        'partidas': partidas,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    }

    return render(request, 'partidas_por_fecha.html', context)