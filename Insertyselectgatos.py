from flask import Flask, request
import psycopg2

app = Flask(__name__)

# Configuración de la conexión a PostgreSQL
DB_CONFIG = {
    "dbname": "animal",
    "user": "faztadmin",      # Cambiá esto si usás otro usuario
    "password": "faztadmin",  # La contraseña que elegiste al instalar PostgreSQL
    "host": "localhost",
    "port": "5432"           # Puerto por defecto de PostgreSQL
}

# Función para conectar a la base de datos
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

class Gato:
    def __init__(self, nombre, color, velocidad):
        self.nombre = nombre
        self.color = color
        self.velocidad = velocidad
    
    def maullar(self):
        return f"¡Miau! Soy {self.nombre}, el gato {self.color}"

# Ruta para mostrar el formulario y la lista de gatos
@app.route('/')
def formulario_gato():
    # Conectamos a la base de datos
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtenemos todos los gatos
    cur.execute("SELECT id, nombre, color, velocidad FROM gatos")
    gatos = cur.fetchall()
    
    # Cerramos la conexión
    cur.close()
    conn.close()
    
    # Creamos una lista HTML con los gatos
    lista_gatos = "".join([f"<li>{gato[1]} ({gato[2]}, {gato[3]} km/h)</li>" for gato in gatos])
    
    return f"""
    <h1>Crear un Gato</h1>
    <form method="POST" action="/crear_gato">
        <p>Nombre: <input type="text" name="nombre"></p>
        <p>Color: <input type="text" name="color"></p>
        <p>Velocidad (km/h): <input type="number" name="velocidad"></p>
        <input type="submit" value="Crear Gato">
    </form>
    <h2>Gatos Guardados</h2>
    <ul>{lista_gatos}</ul>
    """

# Ruta para procesar el formulario y guardar en la base de datos
@app.route('/crear_gato', methods=['POST'])
def crear_gato():
    nombre = request.form['nombre']
    color = request.form['color']
    velocidad = int(request.form['velocidad'])
    
    # Conectamos a la base de datos
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Insertamos el nuevo gato
    cur.execute(
        "INSERT INTO gatos (nombre, color, velocidad) VALUES (%s, %s, %s)",
        (nombre, color, velocidad)
    )
    conn.commit()  # Guardamos los cambios
    
    # Cerramos la conexión
    cur.close()
    conn.close()
    
    # Creamos el objeto Gato para mostrarlo
    nuevo_gato = Gato(nombre, color, velocidad)
    
    return f"""
    <h1>Gato Creado</h1>
    <p>Nombre: {nuevo_gato.nombre}</p>
    <p>Color: {nuevo_gato.color}</p>
    <p>Velocidad: {nuevo_gato.velocidad} km/h</p>
    <p>{nuevo_gato.maullar()}</p>
    <a href="/">Volver</a>
    """

if __name__ == '__main__':
    app.run(debug=True)