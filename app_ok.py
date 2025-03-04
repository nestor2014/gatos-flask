from flask import Flask, request, redirect, url_for

app = Flask(__name__)

import psycopg2

# Configuración de la conexión a PostgreSQL
DB_CONFIG = {
    "dbname": "animal",
    "user": "faztadmin",
    "password": "faztadmin",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

class Gato:
    def __init__(self, nombre, color, velocidad):
        self.nombre = nombre
        self.color = color
        self.velocidad = velocidad
    
    def maullar(self):
        return f"¡Miau! Soy {self.nombre}, el gato {self.color}"

# Página principal con lista de gatos y botones
@app.route('/')
def formulario_gato():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, color, velocidad FROM gatos")
    gatos = cur.fetchall()
    cur.close()
    conn.close()
    
    lista_gatos = "".join([
        f"<li>ID: {gato[0]} - {gato[1]} ({gato[2]}, {gato[3]} km/h) "
        f'<form style="display:inline;" action="/actualizar_gato/{gato[0]}" method="GET">'
        f'<input type="submit" value="Actualizar"></form> '
        f'<form style="display:inline;" action="/eliminar_gato/{gato[0]}" method="GET">'
        f'<input type="submit" value="Eliminar"></form></li>'
        for gato in gatos
    ])
    
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

# Crear un gato
@app.route('/crear_gato', methods=['POST'])
def crear_gato():
    nombre = request.form['nombre']
    color = request.form['color']
    velocidad = int(request.form['velocidad'])
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO gatos (nombre, color, velocidad) VALUES (%s, %s, %s)",
        (nombre, color, velocidad)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    nuevo_gato = Gato(nombre, color, velocidad)
    
    return f"""
    <h1>Gato Creado</h1>
    <p>Nombre: {nuevo_gato.nombre}</p>
    <p>Color: {nuevo_gato.color}</p>
    <p>Velocidad: {nuevo_gato.velocidad} km/h</p>
    <p>{nuevo_gato.maullar()}</p>
    <a href="/">Volver</a>
    """

# Formulario para actualizar un gato
@app.route('/actualizar_gato/<int:gato_id>', methods=['GET'])
def mostrar_actualizar_gato(gato_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, color, velocidad FROM gatos WHERE id = %s", (gato_id,))
    gato = cur.fetchone()
    cur.close()
    conn.close()
    
    if gato:
        return f"""
        <h1>Actualizar Gato ID: {gato[0]}</h1>
        <form method="POST" action="/actualizar_gato/{gato[0]}">
            <p>Nombre: <input type="text" name="nombre" value="{gato[1]}"></p>
            <p>Color: <input type="text" name="color" value="{gato[2]}"></p>
            <p>Velocidad (km/h): <input type="number" name="velocidad" value="{gato[3]}"></p>
            <input type="submit" value="Guardar Cambios">
            <a href="/">Cancelar</a>
        </form>
        """
    return "Gato no encontrado", 404

# Procesar la actualización
@app.route('/actualizar_gato/<int:gato_id>', methods=['POST'])
def actualizar_gato(gato_id):
    nombre = request.form['nombre']
    color = request.form['color']
    velocidad = int(request.form['velocidad'])
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE gatos SET nombre = %s, color = %s, velocidad = %s WHERE id = %s",
        (nombre, color, velocidad, gato_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('formulario_gato'))

# Confirmación para eliminar un gato
@app.route('/eliminar_gato/<int:gato_id>', methods=['GET'])
def confirmar_eliminar_gato(gato_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, color, velocidad FROM gatos WHERE id = %s", (gato_id,))
    gato = cur.fetchone()
    cur.close()
    conn.close()
    
    if gato:
        return f"""
        <h1>Eliminar Gato ID: {gato[0]}</h1>
        <p>¿Estás seguro de eliminar a {gato[1]} ({gato[2]}, {gato[3]} km/h)?</p>
        <form method="POST" action="/eliminar_gato/{gato[0]}">
            <input type="submit" value="Sí, eliminar">
            <a href="/">No, volver</a>
        </form>
        """
    return "Gato no encontrado", 404

# Procesar la eliminación
@app.route('/eliminar_gato/<int:gato_id>', methods=['POST'])
def eliminar_gato(gato_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM gatos WHERE id = %s", (gato_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('formulario_gato'))

if __name__ == '__main__':
    app.run(debug=True)