# **Mi App de Contabilidad Personal**


Una aplicación web completa para la gestión de finanzas personales, construida con Python y Flask. Permite a los usuarios registrar ingresos y gastos, gestionar categorías, establecer presupuestos y analizar sus finanzas a través de informes y gráficos.

## **Índice**


1. [Características Principales](https://www.google.com/search?q=%23caracter%C3%ADsticas-principales)
2. [Tecnologías Utilizadas](https://www.google.com/search?q=%23tecnolog%C3%ADas-utilizadas)
3. [Instalación](https://www.google.com/search?q=%23instalaci%C3%B3n)
    * [Desarrollo Local](https://www.google.com/search?q=%23desarrollo-local)
    * [Producción (Debian/Ubuntu)](https://www.google.com/search?q=%23producci%C3%B3n-debianubuntu)
4. [Seguridad](https://www.google.com/search?q=%23seguridad)
    * [Firewall (ufw)](https://www.google.com/search?q=%23firewall-ufw)
    * [Fail2Ban](https://www.google.com/search?q=%23fail2ban)
5. [Backup](https://www.google.com/search?q=%23backup)
6. [Licencia](https://www.google.com/search?q=%23licencia)


## **Características Principales**


* **Autenticación de Usuarios**: Sistema seguro de registro e inicio de sesión.
* **Gestión de Transacciones**: Añadir, ver, editar y eliminar ingresos y gastos.
* **Categorías Personalizadas**: Crea y gestiona tus propias categorías de ingresos y gastos.
* **Sistema de Presupuestos**: Establece límites de gasto mensuales por categoría y visualiza el progreso.
* **Dashboard Interactivo**: Balance total, gráfico de gastos del mes y tabla de últimos movimientos.
* **Informes Detallados**: Filtra transacciones por mes y año y ve resúmenes financieros.
* **Diseño web responsivo.** Se adapta correctamente a cualquier tipo de pantalla de dispositivos móviles.
* **Exportación a CSV**: Descarga los informes filtrados en formato CSV.


## **Tecnologías Utilizadas**


* **Backend**: Python, Flask
* **Base de Datos**: SQLAlchemy ORM con SQLite
* **Frontend**: HTML, Bootstrap 4, Chart.js
* **Servidor de Producción**: Gunicorn + Nginx
* **Gestor de Procesos**: Systemd
* **Seguridad**: Werkzeug, Flask-Login, Fail2Ban


## **Instalación**


<br>
### **Desarrollo Local**


**Requisitos**: Python 3.10+ y `venv`.

1. **Clonar el Repositorio**
    Bash

    ```
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio

    ```
2. **Crear y Activar el Entorno Virtual**
    Bash

    ```
    python3 -m venv venv
    source venv/bin/activate

    ```
3. **Instalar las Dependencias**
    Bash

    ```
    pip install -r requirements.txt

    ```
4. **Crear la Base de Datos**
    Bash

    ```
    export FLASK_APP=run.py
    flask db upgrade

    ```
5. **Crear Directorio de Logs**
    Bash

    ```
    sudo mkdir -p /var/log/contabilidad
    sudo touch /var/log/contabilidad/auth.log
    sudo chown $USER:www-data /var/log/contabilidad/auth.log
    sudo chmod 664 /var/log/contabilidad/auth.log

    ```


### **Producción (Debian/Ubuntu)**


1. **Servicio `systemd`**: Crea `/etc/systemd/system/contabilidad.service` para gestionar la aplicación.
2. **Nginx como Proxy Inverso**: Crea `/etc/nginx/sites-available/contabilidad` para dirigir el tráfico a Gunicorn.
3. **Activar Servicios**:
    Bash

    ```
    sudo systemctl daemon-reload
    sudo systemctl start contabilidad
    sudo systemctl enable contabilidad
    sudo systemctl restart nginx

    ```


## **Seguridad**


<br>
### **Firewall (ufw)**


Asegúrate de que Nginx esté permitido:
Bash

```
sudo ufw allow 'Nginx Full'
sudo ufw status
```


### **Fail2Ban**


Para proteger la aplicación contra ataques de fuerza bruta en el login:

1. **Crear Filtro**: Crea `/etc/fail2ban/filter.d/flask-auth.conf` con la `failregex`.
2. **Crear Jaula**: Añade la jaula `[flask-auth]` a tu archivo `/etc/fail2ban/jail.local`.
3. **Reiniciar y Verificar**:
    Bash

    ```
    sudo systemctl restart fail2ban
    sudo fail2ban-client status flask-auth

    ```


## **Backup**


El proyecto incluye un script de backup en `scripts/backup.sh`. Adáptalo a tu usuario y configúralo con `cron` para automatizar las copias de seguridad de la base de datos y el código.

## **Licencia**


Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
