# **Mi App de Contabilidad Personal**

Una aplicación web completa para la gestión de finanzas personales, construida con Python y Flask. Permite a los usuarios registrar ingresos y gastos, gestionar categorías, establecer presupuestos y analizar sus finanzas a través de informes y gráficos.

## **Índice**

1.  [Características Principales](#características-principales)
2.  [Características Avanzadas](#características-avanzadas)
3.  [Tecnologías Utilizadas](#tecnologías-utilizadas)
4.  [Instalación](#instalación)
5.  [Seguridad](#seguridad)
6.  [Backup](#backup)
7.  [Licencia](#licencia)

## **Características Principales**

* **Autenticación de Usuarios**: Sistema seguro de registro e inicio de sesión.
* **Gestión de Transacciones**: Añadir, ver, editar y eliminar ingresos y gastos.
* **Categorías Personalizadas**: Crea y gestiona tus propias categorías de ingresos y gastos.
* **Sistema de Presupuestos**: Establece límites de gasto mensuales por categoría y visualiza el progreso.
* **Dashboard Interactivo**: Balance total, gráfico de gastos del mes y tabla de últimos movimientos.
* **Diseño web responsivo**: Se adapta correctamente a cualquier tipo de pantalla.
* **Exportación a CSV**: Descarga los informes filtrados en formato CSV.

## **Características Avanzadas**

* **Informes Gráficos Avanzados**: Gráfico de barras que muestra la evolución de ingresos y gastos de los últimos 6 meses para un análisis visual rápido.
* **Transacciones Recurrentes**: Automatiza el registro de ingresos y gastos fijos (salarios, alquileres, suscripciones). Configúralos una vez y la aplicación los añadirá automáticamente en la fecha correspondiente.

## **Tecnologías Utilizadas**

* **Backend**: Python, Flask
* **Base de Datos**: SQLAlchemy ORM con SQLite
* **Frontend**: HTML, **Bootstrap 5**, Chart.js
* **Servidor de Producción**: Gunicorn + Nginx
* **Gestor de Procesos**: Systemd, Cron
* **Seguridad**: Werkzeug, Flask-Login, Fail2Ban

## **Instalación**

<br>
### **Desarrollo Local**

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
5.  **Crear Directorio de Logs**
    ```bash
    sudo mkdir -p /var/log/contabilidad
    sudo touch /var/log/contabilidad/auth.log
    sudo chown $USER:www-data /var/log/contabilidad/auth.log
    sudo chmod 664 /var/log/contabilidad/auth.log
    ```

### **Automatización de Tareas (Cron)**

Para que las transacciones recurrentes se procesen automáticamente, necesitas configurar un `cron job` que ejecute el comando personalizado una vez al día.

1.  Abre el editor de `crontab`:
    ```bash
    crontab -e
    ```
2.  Añade la siguiente línea, adaptando las rutas a tu configuración:
    ```bash
    0 3 * * * /home/usuario/contabilidad_flask/ejecutar-recurrentes.sh
    ```
    *Este comando se ejecutará todos los días a las 3:00 AM.*

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
