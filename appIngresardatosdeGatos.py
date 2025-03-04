from flask import Flask, request

app = Flask(__name__)

class Gato:
    def __init__(self, nombre, color, velocidad):
        self.nombre = nombre
        self.color = color
        self.velocidad = velocidad
    
    def maullar(self):
        return f"¡Miau! Soy {self.nombre}, el gato {self.color}"

# Ruta para mostrar el formulario
@app.route('/')
def formulario_gato():
    return """
    <h1>Crear un Gato</h1>
    <form method="POST" action="/crear_gato">
        <p>Nombre: <input type="text" name="nombre"></p>
        <p>Color: <input type="text" name="color"></p>
        <p>Velocidad (km/h): <input type="number" name="velocidad"></p>
        <input type="submit" value="Crear Gato">
    </form>
    """

# Ruta para procesar el formulario
@app.route('/crear_gato', methods=['POST'])
def crear_gato():
    nombre = request.form['nombre']
    color = request.form['color']
    velocidad = int(request.form['velocidad'])
    
    nuevo_gato = Gato(nombre, color, velocidad)
    
    return f"""
    <h1>Gato Creado</h1>
    <p>Nombre: {nuevo_gato.nombre}</p>
    <p>Color: {nuevo_gato.color}</p>
    <p>Velocidad: {nuevo_gato.velocidad} km/h</p>
    <p>{nuevo_gato.maullar()}</p>
    """

if __name__ == '__main__':
    app.run(debug=True)