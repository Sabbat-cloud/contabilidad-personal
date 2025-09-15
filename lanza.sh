#Para activar el registro de nuevos usuarios export REGISTRATION_ENABLED=True y luego lanzar la app (recordar de activar a False cuando no sea necesario
#flask run --host=0.0.0.0 desarrollo
gunicorn --workers 3 --bind 0.0.0.0:3560 run:app


