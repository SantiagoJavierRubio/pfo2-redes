import sqlite3
from uuid import uuid4

class Usuario:
    def __init__(self, id, nombre, contrasena):
        self.id = id
        self.nombre = nombre
        self.contrasena = contrasena

    def __str__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}')"
    
class Tarea:
    def __init__(self, id, titulo, id_usuario):
        self.id = id
        self.titulo = titulo
        self.id_usuario = id_usuario

    def __str__(self):
        return f"Tarea(id={self.id}, titulo='{self.titulo}', id_usuario={self.id_usuario})"

class DB:
    def __init__(self, nombre):
        self.nombre = nombre

    def iniciar(self):
        with sqlite3.connect(self.nombre) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS usuarios (id TEXT PRIMARY KEY, nombre TEXT, contrasena TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS tareas (id TEXT PRIMARY KEY, titulo TEXT, id_usuario TEXT, FOREIGN KEY (id_usuario) REFERENCES usuarios(id))')
            conn.commit()

    def get_usuario(self, nombre):
        with sqlite3.connect(self.nombre) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM usuarios WHERE nombre = ?', (nombre,))
            res = c.fetchone()
            if res:
                return Usuario(*res)
            return None
     
    def get_usuario_id(self, id):
        with sqlite3.connect(self.nombre) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
            res = c.fetchone()
            if res:
                return Usuario(*res)
            return None
    
    def agregar_usuario(self, nombre, contrasena):
        with sqlite3.connect(self.nombre) as conn:
            c = conn.cursor()
            id = uuid4()
            c.execute('INSERT INTO usuarios (id, nombre, contrasena) VALUES (?, ?, ?)', (str(id), nombre, contrasena))
            conn.commit()
            return str(id)
    
    def agregar_tarea(self, titulo, id_usuario):
        with sqlite3.connect(self.nombre) as conn:
            c = conn.cursor()
            id = uuid4()
            c.execute('INSERT INTO tareas (id, titulo, id_usuario) VALUES (?, ?, ?)', (str(id), titulo, id_usuario))
            conn.commit()
            return str(id)

    def obtener_tareas(self, id_usuario):
        with sqlite3.connect(self.nombre) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM tareas WHERE id_usuario = ?', (id_usuario,))
            res = c.fetchall()
            if res:
                return [Tarea(*row) for row in res]
            return None
