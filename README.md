# PFO2 - Redes - API Tareas

### Pasos iniciales
Clonar el repositorio
```bash
git clone ...
```
Acceder al codigo
```bash
cd pfo2-redes
```
Instalar dependencias
```bash
pip install -r requirements.txt
```

# Servidor
API con Flask y persistencia en SQLite
Inicia un servidor que permite manejar autenticacion y tareas.

## Funcionalidades
### Registrar usuario
Guardar un nuevo usuario en la base de datos
- Si ya existe o no se proporcionan los datos minimos se devolvera un error

### Inciar sesion
Autenticar un usuario y devolver el id para autorizar el acceso a las tareas
- Si los datos no coinciden con los guardados en la base de datos o no se proporcionan los datos minimos se devolvera un error

> [!NOTE]
> Las contraseñas de guardan hasheadas para seguridad!

### Crear tarea
Agregar una nueva tarea asociada al usuario a la base de datos
- Si no se pasa un id de usuario valido o los datos minimos se devolvera un error

### Listar tareas
Mostrar todas las tareas guardadas para un usuario.
- Si no se pasa un id de usuario valido se devolvera un error

## Cómo usar:
correr en la terminal:
```bash
python servidor.py
```


# Cliente
Aplicación de consola para consumir los endpoints del servidor.

#### Proporciona una serie de comandos y maneja el estado de la autenticación para los requests.

## Cómo usar:
**{{api_url}}** --> la ubicación del servidor. En local el default es http://localhost:5000 (si no se pasa ningun valor se usará éste)

Correr en la terminal:
```bash
python cliente.py {{api_url}}
```