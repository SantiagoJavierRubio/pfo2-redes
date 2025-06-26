from flask import Flask, request, jsonify
from db import DB
import bcrypt

class ServidorAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = DB('pfo2.redes.db')
        self.db.iniciar()
        self.definir_rutas()
        
    def hashear_contrasena(self, contrasena):
        # Genera un hash de la contraseña 
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(contrasena.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def validar_contrasena(self, contrasena, hashed):
        # Verifica la contraseña contra el hash guardado en la db
        return bcrypt.checkpw(contrasena.encode('utf-8'), hashed.encode('utf-8'))

    def definir_rutas(self):
        @self.app.route('/registro', methods=['POST'])
        def registro_usuario():
            data = request.get_json()
            nombre = data.get('nombre')
            contrasena = data.get('contrasena')
            if not nombre or not contrasena:
                return jsonify({'error': 'Nombre y contraseña son requeridos'}), 400
            
            # Validar que no exista ya un usuario con el mismo nombre
            existe = self.db.get_usuario(nombre)
            if existe:
                return jsonify({'error': 'El usuario ya existe'}), 400
            
            hashed = self.hashear_contrasena(contrasena)
            # Agregar el usuario a la base de datos
            idusuario = self.db.agregar_usuario(nombre, hashed)
            if not idusuario:
                return jsonify({'error': 'Error al registrar el usuario'}), 500
            
            return jsonify({'mensaje': 'Usuario registrado exitosamente', 'id': idusuario }), 201

        @self.app.route('/login', methods=['POST'])
        def login_usuario():
            data = request.get_json()
            nombre = data.get('nombre')
            contrasena = data.get('contrasena')
            if not nombre or not contrasena:
                return jsonify({'error': 'Nombre y contraseña son requeridos'}), 400
            
            usuario = self.db.get_usuario(nombre)
            if not usuario or not self.validar_contrasena(contrasena, usuario.contrasena):
                return jsonify({'error': 'Nombre de usuario o contraseña incorrectos'}), 401
            
            return jsonify({'mensaje': 'Inicio de sesión exitoso', 'id': usuario.id}), 200
        
        @self.app.route('/tareas', methods=['POST'])
        def agregar_tarea():
            data = request.get_json()
            titulo = data.get('titulo')
            id_usuario = data.get('id_usuario')
            if not titulo or not id_usuario:
                return jsonify({'error': 'Título y ID de usuario son requeridos'}), 400
            
            usuario = self.db.get_usuario_id(id_usuario)
            if not usuario:
                return jsonify({'error': 'El id de usuario no corresponde a un usuario registrado'}), 401

            # Agregar la tarea a la base de datos
            id_tarea = self.db.agregar_tarea(titulo, id_usuario)
            if not id_tarea:
                return jsonify({'error': 'Error al agregar la tarea'}), 500
            
            return jsonify({'mensaje': 'Tarea agregada exitosamente' }), 201
        
        @self.app.route('/tareas/<id_usuario>', methods=['GET'])
        def obtener_tareas(id_usuario):
            if not id_usuario:
                return jsonify({'error': 'ID de usuario es requerido'}), 400
            
            usuario = self.db.get_usuario_id(id_usuario)
            if not usuario:
                return jsonify({'error': 'El id de usuario no corresponde a un usuario registrado'}), 401

            # Obtener las tareas del usuario
            tareas = self.db.obtener_tareas(id_usuario)
            if not tareas:
                return jsonify({'mensaje': 'No hay tareas para este usuario'}), 404
            
            return jsonify([{'id': tarea.id, 'titulo': tarea.titulo} for tarea in tareas]), 200
        
        @self.app.route('/tareas', methods=['GET'])
        def html_bienvenida():
            return '''
            <html>
                <head>
                    <title>Bienvenido a la API de Tareas</title>
                </head>
                <body>
                    <h1>API de Tareas</h1>
                    <p>Utiliza los endpoints /registro, /login, /tareas para interactuar con la API.</p>
                </body>
            </html>
            '''

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    servidor = ServidorAPI()
    servidor.run()