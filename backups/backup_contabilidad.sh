#!/bin/bash

# ===============================================
# SCRIPT DE BACKUP PARA LA APP DE CONTABILIDAD
# ===============================================

# --- CONFIGURACIÓN DE RUTAS (Modifica si es necesario) ---
APP_DIR="/home/usuario/contabilidad_flask"
BACKUP_DIR="/home/usuario/backups/contabilidad"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")

echo "--- Iniciando backup: $TIMESTAMP ---"

# --- 1. CREAR DIRECTORIO DE BACKUP (si no existe) ---
mkdir -p "$BACKUP_DIR"

# --- 2. BACKUP DE LA BASE DE DATOS (Método seguro para SQLite) ---
# Es importante usar el comando '.backup' de sqlite3 en lugar de 'cp'
# para evitar copiar una base de datos corrupta si está en medio de una escritura.
echo "-> Realizando backup de la base de datos..."
sqlite3 "$APP_DIR/app.db" ".backup '$BACKUP_DIR/database_$TIMESTAMP.db'"
echo "-> Backup de la base de datos completado."

# --- 3. BACKUP DEL CÓDIGO DE LA APLICACIÓN ---
echo "-> Realizando backup del código fuente..."
# Comprimimos todo el directorio de la aplicación en un archivo .tar.gz
tar -czf "$BACKUP_DIR/app_code_$TIMESTAMP.tar.gz" -C "$(dirname "$APP_DIR")" "$(basename "$APP_DIR")"
echo "-> Backup del código completado."

# --- 4. LIMPIEZA DE BACKUPS ANTIGUOS ---
echo "-> Limpiando backups de más de 30 días..."
# Borra archivos .db más antiguos de 30 días
find "$BACKUP_DIR" -type f -mtime +30 -name '*.db' -delete
# Borra archivos .tar.gz más antiguos de 30 días
find "$BACKUP_DIR" -type f -mtime +30 -name '*.tar.gz' -delete
echo "-> Limpieza completada."

echo "--- Proceso de backup finalizado ---"
