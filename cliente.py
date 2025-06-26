import requests
import sys

class ConsoleClient:
    def __init__(self, api_url='http://127.0.0.1:5000'):
        self.api_url = api_url
        self.user_id = None

    def registrar(self):
        nombre = input("Nombre de usuario: ")
        contrasena = input("Contraseña: ")
        r = requests.post(f'{self.api_url}/registro', json={'nombre': nombre, 'contrasena': contrasena})
        print(r.json())
        if r.status_code == 201:
            self.user_id = r.json()['id']

    def login(self):
        nombre = input("Nombre de usuario: ")
        contrasena = input("Contraseña: ")
        r = requests.post(f'{self.api_url}/login', json={'nombre': nombre, 'contrasena': contrasena})
        print(r.json())
        if r.status_code == 200:
            self.user_id = r.json()['id']

    def agregar_tarea(self):
        if not self.user_id:
            print("Primero debes iniciar sesión.")
            return
        titulo = input("Título de la tarea: ")
        r = requests.post(f'{self.api_url}/tareas', json={'titulo': titulo, 'id_usuario': self.user_id})
        print(r.json())

    def listar_tareas(self):
        if not self.user_id:
            print("Primero debes iniciar sesión.")
            return
        r = requests.get(f'{self.api_url}/tareas/{self.user_id}')
        if r.status_code == 200:
            tareas = r.json()
            if tareas:
                for tarea in tareas:
                    print(f"- {tarea['titulo']} (ID: {tarea['id']})")
            else:
                print("No hay tareas.")
        else:
            print(r.json().get('mensaje', 'Error al obtener tareas.'))

    def run(self):
        print('''Comandos: 
              registrar -> Registrar un nuevo usuario
              login -> Iniciar o cambiar sesión
              agregar -> Agregar una nueva tarea
              listar -> Mostrar las tareas del usuario
              salir -> Finalizar sesión
            ''')
        
        while True:
            cmd = input("> ").strip().lower()
            if cmd == 'registrar':
                self.registrar()
            elif cmd == 'login':
                self.login()
            elif cmd == 'agregar':
                self.agregar_tarea()
            elif cmd == 'listar':
                self.listar_tareas()
            elif cmd == 'salir':
                break
            else:
                print("Comando no reconocido.")

if __name__ == '__main__':
    # Obtener la url de la API x parametros
    api_url = 'http://127.0.0.1:5000'
    if len(sys.argv) > 1:
        api_url = sys.argv[1]

    cliente = ConsoleClient(api_url)
    cliente.run()