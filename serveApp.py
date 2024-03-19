"""
Sirve la app de forma local para poder enviar la imágen creada.
Utiliza gunicorn o waitress dependiendo el sistema operativo
"""
import os
from app import app

if os.name == 'posix':
    # Sistema operativo tipo Unix/Linux, usa gunicorn si está disponible
    from gunicorn.app.wsgiapp import run
    # La función run() de gunicorn necesita ser llamada con argumentos
    # específicos del comando de línea, aquí se simula esos argumentos.
    gunicorn_args = ['gunicorn', 'app:app', '--bind', '0.0.0.0:8080']
    run(gunicorn_args)
else:
    # Sistema operativo no Unix (Windows), usa waitress
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
