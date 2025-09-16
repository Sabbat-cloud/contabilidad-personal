### ## `INSTALL.md`

```markdown
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

5. Creamos las rutas para guardar los logs

# Creamos el directoriosudo mkdir -p /var/log/contabilidad
# Creamos el archivo de log vacío
sudo touch /var/log/contabilidad/auth.log
# Hacemos que tu usuario (usuario) y el grupo www-data (nginx/gunicorn) sean los propietarios
sudo chown usuario:www-data /var/log/contabilidad/auth.log
# Damos permisos de escritura al propietario y al grupo
sudo chmod 664 /var/log/contabilidad/auth.log

---

## Instalación en Producción (Debian/Ubuntu)

Esta guía explica cómo desplegar la aplicación en un servidor usando Gunicorn como servidor de aplicación y Nginx como proxy inverso.

### 1. Crear el Servicio `systemd`

`systemd` se encargará de que tu aplicación se ejecute en segundo plano y se reinicie automáticamente si falla o si el servidor se reinicia.

Crea el archivo de servicio:
```bash
sudo nano /etc/systemd/system/contabilidad.service
```

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


#### 

#### \#\#\# \. Configura el Firewall \(`ufw`)


El firewall es tu principal línea de defensa. Debemos decirle que solo permita el tráfico web a través de Nginx y bloquee todo lo demás.

1. Asegúrate de que el puerto `3560` **no** esté permitido:
    Bash

    ```
    sudo ufw deny 3560
    
    ```

<br>
2. Asegúrate de que Nginx **sí** esté permitido:
    Bash

    ```
    sudo ufw allow 'Nginx Full'
    
    ```

<br>
3. Comprueba el estado del firewall:
    Bash

    ```
    sudo ufw status
    
    ```

    La salida debería mostrar que solo los puertos de Nginx (80, 443) y SSH (22) están permitidos desde cualquier lugar (`Anywhere`).

Después de hacer estos cambios, reinicia los servicios para aplicarlos:
Bash

```
sudo systemctl daemon-reload
sudo systemctl restart contabilidad
```

Ahora, el acceso directo a `http://tu_ip:3560` debería fallar, pero el acceso a través de `http://tu_ip` seguirá funcionando, servido de forma segura por Nginx.

***

<br>
### \#\# 2\. Crear una Jaula de Fail2Ban para el Login 🛡️


Esta es una medida de seguridad fantástica. El proceso consiste en tres pasos:

1. **Flask**: Registrar los intentos de login fallidos en un archivo de log.
2. **Fail2Ban (Filtro)**: Enseñarle a Fail2Ban a reconocer el mensaje de error en ese log.
3. **Fail2Ban (Jaula)**: Decirle a Fail2Ban que vigile ese log con ese filtro y que bloquee las IPs que fallen repetidamente.


#### 

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

***

<br>
### 5\. Jaula Fail2Ban


#### \#\#\# Paso 5\.1: Crear el Filtro de Fail2Ban


Ahora, enséñale a Fail2Ban qué buscar.

1. Crea un nuevo archivo de filtro:
    Bash

    ```
    sudo nano /etc/fail2ban/filter.d/flask-auth.conf
    
    ```

<br>
2. Pega esta definición. El `failregex` debe coincidir exactamente con el mensaje que configuramos en el log.
    Ini, TOML

    ```
    [Definition]
    failregex = ^.*WARNING.*Failed login attempt for user '.*' from IP <HOST>$
    ignoreregex =
    
    ```

<br>


#### \#\#\# Paso 5\.2: Crear y Activar la Jaula


Finalmente, une todas las piezas. **Nunca edites `jail.conf`**. Crea un archivo local para tus personalizaciones.

1. Crea o edita `jail.local`:
    Bash

    ```
    sudo nano /etc/fail2ban/jail.local
    
    ```

<br>
2. Añade tu nueva jaula al final del archivo:
    Ini, TOML

    ```
    [flask-auth]
    enabled  = true
    filter   = flask-auth
    logpath  = /var/log/contabilidad/auth.log
    port     = http,https
    maxretry = 5
    findtime = 600
    bantime  = 3600
    
    ```
    * **maxretry = 5**: Bloquea después de 5 intentos fallidos.
    * **findtime = 600**: Si los 5 intentos ocurren en un plazo de 600 segundos (10 minutos).
    * **bantime = 3600**: Bloquea la IP durante 3600 segundos (1 hora).


#### \#\#\# Paso 5\.3: Aplicar y Probar


1. Reinicia Fail2Ban para que cargue la nueva configuración:
    Bash

    ```
    sudo systemctl restart fail2ban
    
    ```

<br>
2. Comprueba el estado de tu nueva jaula:
    Bash

    ```
    sudo fail2ban-client status flask-auth
    
    ```

    Debería decir que ha encontrado 1 archivo y que el número de IPs baneadas es 0.


### 7\. Script de Backup


Dentro de /backups tienes un script que realiza una copia de la aplicación y la base de datos. Recuerda adaptarlo a tu usuario.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

