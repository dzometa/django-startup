import csv
from django.core.management.base import BaseCommand
from tu_app.models import ActividadEconomica

class Command(BaseCommand):
    help = 'Importa actividades económicas desde un archivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ruta al archivo CSV')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                obj, created = ActividadEconomica.objects.update_or_create(
                    codigo=row['codigo'],
                    defaults={'descripcion': row['descripcion']}
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Importadas/actualizadas {count} actividades económicas.'))
