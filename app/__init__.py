# app/__init__.py
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os

# Creación de la instancia de la aplicación Flask.
app = Flask(__name__)
# Carga de la configuración desde el objeto Config.
app.config.from_object(Config)
app.debug = app.config['DEBUG']

# Inicialización de las extensiones.
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# Le decimos a Flask-Login cuál es la vista (ruta) de login.
# Si un usuario no logueado intenta acceder a una página protegida,
# será redirigido a esta ruta.
login_manager.login_view = 'login'

# --- Configuración del Logging ---
if not app.debug:
    if not os.path.exists('/var/log/contabilidad'):
        os.mkdir('/var/log/contabilidad')
    file_handler = RotatingFileHandler('/var/log/contabilidad/auth.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Contabilidad startup')

# Importamos los modelos y las rutas al final para evitar importaciones circulares.
from app import routes, models
