# Frontend - Aplicación Web con Flask

## Descripción
Frontend desarrollado en Python con el framework Flask que proporciona una interfaz web moderna para la gestión de usuarios. Esta solución ha sido diseñada específicamente para operar en una arquitectura de tres capas en AWS, utilizando contenedores Docker para asegurar la escalabilidad, portabilidad y el aislamiento de componentes solicitado por Innovatech.

## Versiones y Herramientas Requeridas

### Lenguaje y Runtime
- **Python**: Versión 3.8 o superior
- **pip**: Versión 21.0 o superior (gestor de paquetes de Python)

### Dependencias Principales
- **Flask**: ^2.3.3 - Framework web micro para Python
- **Flask-CORS**: ^4.0.0 - Middleware para habilitar el intercambio de recursos de origen cruzado.
- **requests**: ^2.31.0 - Librería para realizar peticiones HTTP RESTful hacia el Backend.
- **python-dotenv**: ^1.0.0 - Gestión de variables de entorno para configuración segura.
- **Jinja2**: ^3.1.2 - Motor de plantillas para la generación de HTML dinámico.

## Instalación

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

El sistema utiliza variables de entorno para desacoplar la configuración del código fuente, facilitando el despliegue en diferentes etapas (Desarrollo/Producción).

1. Copiar el archivo de variables de entorno:
```bash
cp .env.example .env
```

2. Editar el archivo `.env` con tu configuración:
```
PORT=5000
DEBUG=False
BACKEND_URL=http://localhost:8000
SECRET_KEY=clave_secreta_muy_segura_aqui
```

## Ejecución

Para ejecutar la aplicación en modo de pruebas localmente:

```bash
# Para desarrollo
python app.py

# O con variables de entorno
FLASK_ENV=development python app.py
```

### Entorno de Producción (Contenedores)
Siguiendo los principios de DevOps y preparación para el futuro escenario contenerizado de Innovatech:

```bash
# Construir y levantar con Docker Compose
docker-compose up -d --build
```
## Persistencia de Datos

Para el componente Frontend, se ha determinado el siguiente esquema de persistencia:

- **Naturaleza Stateless**: Al ser una interfaz web que consume servicios de una API externa, el frontend es mayormente "sin estado" (stateless).

- **Volúmenes (Named Volumes)**: Se utilizan volúmenes de Docker únicamente para la persistencia de los logs de acceso y errores en la ruta /app/logs.

- **Justificación**: Se optó por Named Volumes en lugar de bind mounts para asegurar que la gestión del almacenamiento sea delegada a Docker, facilitando la portabilidad entre diferentes instancias EC2 de AWS sin depender de rutas específicas del sistema de archivos local.

## Seguridad y Mínimo Privilegio

Siguiendo los estándares de seguridad solicitados, la contenedorización del frontend aplica las siguientes buenas prácticas:

- **Usuario No-Root**: El Dockerfile está configurado para ejecutar la aplicación bajo un usuario con privilegios limitados. Esto evita que, en caso de una vulnerabilidad, un atacante obtenga acceso total al contenedor o al host.

- **Gestión de Secretos**: No se almacenan credenciales ni llaves SSH en el repositorio. Se utilizan GitHub Secrets para inyectar variables sensibles durante el pipeline de despliegue.

- **Imagen Optimizada**: Uso de multi-stage builds para asegurar que la imagen final solo contenga el binario y las dependencias necesarias, reduciendo la superficie de ataque.

## Pipeline de Despliegue Continuo (CI/CD)

El proyecto utiliza **GitHub Actions** para automatizar el ciclo de vida del software. El flujo se activa ante cada `push` en la rama `deploy`:

1.  **Integración Continua (CI)**: Se construye la imagen Docker basada en el `Dockerfile` multi-stage para verificar que el código sea empaquetable.
2.  **Entrega Continua (CD)**:
    *   La imagen se publica en el registro (Docker Hub/ECR).
    *   Se realiza una conexión segura vía SSH a la instancia EC2 de AWS.
    *   Se ejecuta un script de despliegue que realiza el `pull` de la nueva imagen y reinicia el contenedor con la versión actualizada.

## Estructura del Proyecto

La organización del código sigue una estructura modular para facilitar la mantenibilidad y el escalamiento hacia microservicios en la Fase 2:

```
frontend/
├── .github/workflows/    # Pipeline CI/CD (GitHub Actions)
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── .env.example          # Ejemplo de variables de entorno
├── .env                  # Variables de entorno (crear manualmente)
├── Dockerfile            # Configuración de imagen multi-stage
├── docker-compose.yml    # Orquestación del servicio Frontend
├── templates/            # Plantillas HTML
│   ├── base.html         # Layout base y componentes comunes
│   ├── index.html        # Dashboard principal y lista de usuarios
│   ├── crear_usuario.html # Vista de registro
│   ├── editar_usuario.html # Vista de modificación
│   ├── 404.html          # # Manejo de error: Recurso no encontrado
│   └── 500.html          # Manejo de error: Fallo interno del servidor
├── static/               # Archivos estáticos (CSS, JS, imágenes)
└── README.md             # Documentación técnica del sistema
```

## Funcionalidades

### Páginas Disponibles
- **Página Principal (`/`)**: Visualización dinámica de la base de datos de usuarios con opciones de gestión.
- **Crear Usuario (`/crear`)**: Formulario interactivo para el alta de nuevos registros.
- **Editar Usuario (`/editar/<id>`)**: Interfaz para la actualización de datos existentes.
- **Eliminar Usuario**: Acción directa para la remoción de registros desde la vista principal.

### Características Técnicas
- **Responsive Design**: Interfaz optimizada para múltiples dispositivos mediante Bootstrap 5.
- **Bootstrap 5**: Framework CSS para estilos modernos
- **Font Awesome**: Iconos profesionales
- **Validación**: Validación en cliente y servidor
- **Mensajes Flash**: Notificaciones al usuario
- **Manejo de Errores**: Páginas personalizadas para errores 404 y 500

## Comunicación con Backend

La capa de Frontend actúa como un cliente de la API Backend ubicada en la subred privada de AWS. La comunicación se realiza estrictamente a través de peticiones HTTP:

```python
# Ejemplo de petición GET para obtener usuarios
response = requests.get(f'{BACKEND_URL}/api/usuarios')
usuarios = response.json()

# Ejemplo de petición POST para crear usuario
response = requests.post(f'{BACKEND_URL}/api/usuarios', json=datos_usuario)
```

## Puertos Requeridos

Para asegurar la conectividad en el ecosistema de Innovatech Chile, se han definido los siguientes puertos tanto para la ejecución local como para el despliegue en contenedores:

### Para funcionamiento en contenedor:
- **Puerto 5000**: Puerto del servidor frontend Flask (HTTP)
- **Puerto 8000**: Puerto de comunicación con la API Backend (Subred Privada).

### Explicación de puertos:
- **5000**: Es el puerto donde el servidor Flask escucha para servir la aplicación web. En el despliegue de AWS, este se mapea al puerto 80 de la instancia pública para permitir el acceso vía HTTP.
- **8000**: Representa el puerto de escucha del Backend API al que el Frontend se conecta para el intercambio de datos.

## Variables de Entorno

El uso de variables de entorno permite que la aplicación sea portable entre diferentes entornos (desarrollo, pruebas y producción) sin modificar el código fuente.

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `PORT` | Puerto interno donde corre el servidor Flask. | 5000 |
| `DEBUG` | Activa/Desactiva el modo de depuración. | False |
| `BACKEND_URL` | URL del backend API | http://localhost:8000 |
| `SECRET_KEY` | Clave para el cifrado de cookies y sesiones de usuario. | clave_secreta_por_defecto |
