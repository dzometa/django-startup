# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /code

# Copiar el archivo de requerimientos y luego instalarlos
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copiar el resto de la aplicación
COPY . /code/

# Especificar el comando de inicio por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
