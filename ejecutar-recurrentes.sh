#!/bin/bash

# ================================================================
# Script para procesar las transacciones recurrentes de la app
# ================================================================

echo "--- Iniciando el proceso de transacciones recurrentes ---"

# 1. Navegar al directorio raíz de la aplicación
# Nos aseguramos de que el script se ejecuta desde la ubicación correcta.
cd /home/sabbat/contabilidad_flask

# 2. Activar el entorno virtual de Python
# Es crucial para que estén disponibles Flask y las demás librerías.
source /home/sabbat/contabilidad_flask/venv/bin/activate

# 3. Exportar la variable de entorno que indica dónde está la app
export FLASK_APP=run.py

# 4. Ejecutar el comando personalizado de Flask
echo "-> Ejecutando el comando 'process-recurring'..."
flask process-recurring

# 5. Desactivar el entorno virtual
deactivate

echo "--- Proceso finalizado ---"
