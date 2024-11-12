# Proyecto en Flask API DOLAR

Este es un proyecto hecho con Flask. Este README explica cómo configurar el entorno y ejecutar la aplicación.

## Requisitos

- Python 3.7 o superior
- Git (para clonar el proyecto)

## Instalación

Sigue estos pasos para clonar el repositorio, configurar el entorno virtual y ejecutar la aplicación.

### 1. Clonar el repositorio

Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/[CaetanoDelbono/utn-tp-final-tup5]
cd utn-tp-final-tup5

###2. Crea un entorno virtual en la carpeta .venv:
python -m venv .venv

###3. Activar el entorno virtual
Para activar el entorno virtual:

En Windows:

bash
.\.venv\Scripts\activate

4. Instalar las dependencias
Una vez activado el entorno virtual, instala las dependencias del proyecto:

pip install -r requirements.txt


### Explicación de los archivos importantes:

- **`requirements.txt`**: Este archivo contiene la lista de dependencias de Python que tu proyecto necesita. Puedes generarlo usando `pip freeze > requirements.txt` desde el entorno virtual configurado.
- **`.env`**: En este archivo puedes almacenar configuraciones sensibles (como claves API o configuraciones de bases de datos). Asegúrate de agregar `.env` al archivo `.gitignore` para no compartirlo en el repositorio.


