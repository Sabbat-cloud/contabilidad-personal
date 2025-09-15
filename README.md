### \#\# `INSTALL.md` 

````markdown
# Mi App de Contabilidad Personal

Una aplicación web completa para la gestión de finanzas personales, construida con Python y Flask. Permite a los usuarios registrar ingresos y gastos, gestionar categorías, establecer presupuestos y analizar sus finanzas a través de informes y gráficos.

---

## Características Principales

* **Autenticación de Usuarios**: Sistema seguro de registro e inicio de sesión.
* **Gestión de Transacciones**: Añadir, ver, **editar** y **eliminar** ingresos y gastos.
* **Categorías Personalizadas**: Los usuarios pueden crear y gestionar sus propias categorías de ingresos y gastos.
* **Sistema de Presupuestos**: Establecer límites de gasto mensuales por categoría y visualizar el progreso.
* **Dashboard Interactivo**: Balance total, gráfico de gastos del mes y tabla de últimos movimientos.
* **Informes Detallados**: Filtrar transacciones por mes y año y ver resúmenes financieros.
* **Exportación a CSV**: Descargar los informes filtrados en formato CSV.
* **Seguridad**: Protección contra fuerza bruta con **Fail2Ban** y control de registro de usuarios.
* **Backup Automatizado**: Incluye un script para realizar copias de seguridad de la aplicación y la base de datos.

---

## Tecnologías Utilizadas

* **Backend**: Python, Flask
* **Base de Datos**: SQLAlchemy ORM con SQLite
* **Frontend**: HTML, Bootstrap 4, Chart.js
* **Servidor de Producción**: Gunicorn + Nginx
* **Gestor de Procesos**: Systemd
* **Seguridad**: Werkzeug, Flask-Login, Fail2Ban

---

## Guía de Instalación (Desarrollo Local)

Sigue estos pasos para poner en marcha la aplicación en tu propio ordenador.

**Requisitos**: Python 3.10+ y `venv`.

1.  **Clonar el Repositorio**
    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd tu-repositorio
    ```

2.  **Crear y Activar el Entorno Virtual**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar las Dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crear la Base de Datos**
    ```bash
    export FLASK_APP=run.py
    flask db upgrade
    ```

5.  **Ejecutar la Aplicación**
    ```bash
    flask run
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000`.

---

## Instalación en Producción (Debian/Ubuntu)

Esta guía explica cómo desplegar la aplicación en un servidor usando Gunicorn como servidor de aplicación y Nginx como proxy inverso.

### 1. Crear el Servicio `systemd`

`systemd` se encargará de que tu aplicación se ejecute en segundo plano y se reinicie automáticamente si falla o si el servidor se reinicia.

Crea el archivo de servicio:
```bash
sudo nano /etc/systemd/system/contabilidad.service
````

```ini
[Unit]
Description=Gunicorn instance to serve Contabilidad Flask App
After=network.target

[Service]
# Cambia 'usuario' por tu nombre de usuario
User=usuario
Group=www-data

# Cambia la ruta a la de tu proyecto
WorkingDirectory=/home/usuario/contabilidad_flask
Environment="PATH=/home/usuario/contabilidad_flask/venv/bin"

# Comando para iniciar Gunicorn.
ExecStart=/home/usuario/contabilidad_flask/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 run:app

Restart=always

[Install]
WantedBy=multi-user.target
```

### 2\. Activar el Servicio

```bash
sudo systemctl daemon-reload
sudo systemctl start contabilidad
sudo systemctl enable contabilidad
# Comprueba que funciona correctamente con:
sudo systemctl status contabilidad
```

### 3\. Configurar Nginx como Proxy Inverso

Nginx recibirá las peticiones de los usuarios (puerto 80) y se las pasará a Gunicorn (puerto 3560).

Crea el archivo de configuración de Nginx:

```bash
sudo nano /etc/nginx/sites-available/contabilidad
```

Pega la siguiente configuración, **modificando la IP/dominio y las rutas**:

```nginx
server {
    listen 80;
    server_name tu_ip_o_dominio.com;

    location / {
        include proxy_params;
        # Esta dirección debe coincidir con el puerto del --bind de Gunicorn
        proxy_pass [http://127.0.0.1:3560](http://127.0.0.1:5000);
    }

    # Sirve los archivos estáticos (CSS, etc.) directamente para mayor eficiencia
    location /static {
        alias /home/usuario/contabilidad_flask/app/static;
    }
}
```

### 4\. Activar la Configuración de Nginx

```bash
sudo ln -s /etc/nginx/sites-available/contabilidad /etc/nginx/sites-enabled
sudo nginx -t  # Comprueba que la sintaxis es correcta
sudo systemctl restart nginx
```

-----

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

````

---
