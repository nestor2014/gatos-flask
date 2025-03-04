from flask import Flask, request, redirect, url_for, render_template
import psycopg2

app = Flask(__name__)

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

@app.route('/')
def formulario_gato():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, color, velocidad FROM gatos")
    gatos = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('index.html', gatos=gatos)

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
    
    return render_template('crear.html', gato=nuevo_gato)

@app.route('/actualizar_gato/<int:gato_id>', methods=['GET'])
def mostrar_actualizar_gato(gato_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, color, velocidad FROM gatos WHERE id = %s", (gato_id,))
    gato = cur.fetchone()
    cur.close()
    conn.close()
    
    if gato:
        return render_template('actualizar.html', gato=gato)
    return "Gato no encontrado", 404

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

@app.route('/eliminar_gato/<int:gato_id>', methods=['GET'])
def confirmar_eliminar_gato(gato_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, color, velocidad FROM gatos WHERE id = %s", (gato_id,))
    gato = cur.fetchone()
    cur.close()
    conn.close()
    
    if gato:
        return render_template('eliminar.html', gato=gato)
    return "Gato no encontrado", 404

@app.route('/eliminar_gato/<int:gato_id>', methods=['POST'])
def eliminar_gato(gato_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM gatos WHERE id = %s", (gato_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('formulario_gato'))

@app.route('/historias_clinicas')
def historias_clinicas():
    return render_template('base.html', content="Página de Historias Clínicas en desarrollo")

@app.route('/contacto')
def contacto():
    return render_template('base.html', content="Página de Contacto en desarrollo")

if __name__ == '__main__':
    app.run(debug=True)