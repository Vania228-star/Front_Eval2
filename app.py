from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = os.getenv('SECRET_KEY', 'dev_key_12345')

CORS(app)

BACKEND_URL = 'http://localhost:3000'

@app.route('/')
def index():
    try:
        response = requests.get(f'{BACKEND_URL}/api/usuarios', timeout=5)
        if response.status_code == 200:
            return render_template('index.html', usuarios=response.json())
        else:
            flash(f'Error del servidor: {response.status_code}', 'error')
            return render_template('index.html', usuarios=[])
    except Exception as e:
        print(f"--- ERROR DE CONEXIÓN ---: {e}")
        flash('No se pudo conectar con el servidor backend', 'error')
        return render_template('index.html', usuarios=[])

@app.route('/crear', methods=['GET', 'POST'])
def crear_usuario():
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
                flash('Error al crear usuario', 'error')
        except Exception as e:
            print(f"--- ERROR CREAR ---: {e}")
            flash('Error al conectar con el servidor', 'error')
    return render_template('crear_usuario.html')

@app.route('/eliminar/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    try:
        response = requests.delete(f'{BACKEND_URL}/api/usuarios/{usuario_id}', timeout=5)
        if response.status_code == 200:
            flash('Usuario eliminado', 'success')
        else:
            flash('Error al eliminar', 'error')
    except Exception as e:
        print(f"--- ERROR ELIMINAR ---: {e}")
        flash('Fallo de comunicación con el backend', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)