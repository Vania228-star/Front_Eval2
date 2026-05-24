# Importar librerías necesarias
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear instancia de la aplicación Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev_key_12345')

# Habilitar CORS
CORS(app)

# Configuración de la URL del backend API
# Asegúrate de que esta URL sea accesible desde el contenedor de Flask
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:3000')

# --- RUTAS ---

@app.route('/')
def index():
    """Página principal que obtiene la lista de usuarios del backend"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/usuarios', timeout=5)
        if response.status_code == 200:
            return render_template('index.html', usuarios=response.json())
        else:
            flash(f'Error del servidor: {response.status_code}', 'error')
            return render_template('index.html', usuarios=[])
    except requests.exceptions.RequestException as e:
        print(f'Error de conexión: {e}')
        flash('No se pudo conectar con el servidor backend', 'error')
        return render_template('index.html', usuarios=[])

@app.route('/crear', methods=['GET', 'POST'])
def crear_usuario():
    """Maneja la visualización y creación de usuarios"""
    if request.method == 'POST':
        try:
            datos = {
                'nombre': request.form.get('nombre'),
                'email': request.form.get('email'),
                'edad': int(request.form.get('edad')) if request.form.get('edad') else None
            }
            
            response = requests.post(f'{BACKEND_URL}/api/usuarios', json=datos, timeout=5)
            
            if response.status_code == 201:
                flash('Usuario creado exitosamente', 'success')
                return redirect(url_for('index'))
            else:
                flash('Error al crear usuario en el servidor', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            
    return render_template('crear_usuario.html')

@app.route('/editar/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    """Maneja la visualización y actualización de un usuario existente"""
    if request.method == 'POST':
        try:
            datos = {
                'nombre': request.form.get('nombre'),
                'email': request.form.get('email'),
                'edad': int(request.form.get('edad')) if request.form.get('edad') else None
            }
            response = requests.put(f'{BACKEND_URL}/api/usuarios/{usuario_id}', json=datos, timeout=5)
            
            if response.status_code == 200:
                flash('Usuario actualizado', 'success')
                return redirect(url_for('index'))
            else:
                flash('Error al actualizar', 'error')
        except Exception as e:
            flash(f'Error de conexión: {str(e)}', 'error')
        return redirect(url_for('editar_usuario', usuario_id=usuario_id))

    # Método GET: Obtener datos para el formulario
    try:
        response = requests.get(f'{BACKEND_URL}/api/usuarios', timeout=5)
        usuarios = response.json()
        usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
        if usuario:
            return render_template('editar_usuario.html', usuario=usuario)
        flash('Usuario no encontrado', 'error')
    except:
        flash('Error al conectar con el backend', 'error')
    return redirect(url_for('index'))

@app.route('/eliminar/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    """Elimina un usuario mediante petición DELETE"""
    try:
        response = requests.delete(f'{BACKEND_URL}/api/usuarios/{usuario_id}', timeout=5)
        if response.status_code == 200:
            flash('Usuario eliminado', 'success')
        else:
            flash('Error al eliminar', 'error')
    except:
        flash('Fallo de comunicación con el backend', 'error')
    return redirect(url_for('index'))

# --- MANEJO DE ERRORES ---

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_servidor(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)