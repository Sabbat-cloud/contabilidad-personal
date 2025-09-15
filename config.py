# config.py
import os

# Obtenemos la ruta absoluta del directorio actual del script.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clave secreta para proteger los formularios y las sesiones.
    # Es vital que esto sea una cadena aleatoria y secreta en producción.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-dificil-de-adivinar'
    
    # Configuración de la base de datos SQLite.
    # La base de datos se guardará en un archivo llamado 'app.db' en el directorio raíz.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Desactiva una característica de SQLAlchemy que no necesitamos y que consume recursos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Interruptor para el registro.
    # Lee una variable de entorno. Si no existe, por defecto es 'False'.
    # Comparamos con 'True' para convertir la cadena a un booleano.
    REGISTRATION_ENABLED = os.environ.get('REGISTRATION_ENABLED', 'False').lower() == 'true'

    #Configuración explicita del modo debug. siempre false a menos que se indique en el export
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
