
from flask import Flask, render_template, redirect, url_for
import mysql.connector
app = Flask(__name__,template_folder='templates') 

# Configurar la conexión
config = {
    'user': 'CandelaSalcedo',
    'password': 'Candela1234',
    'host': 'CandelaSalcedo.mysql.pythonanywhere-services.com',  # Cambiar si tu base de datos está en un servidor remoto
    'database': 'CandelaSalcedo$default',
    'raise_on_warnings': True  # Esto es opcional, para recibir advertencias como excepciones
}

# Establecer la conexión
try:
    conn = mysql.connector.connect(**config)

    if conn.is_connected():
        print('Conexión establecida correctamente.')

        # Aquí puedes realizar operaciones en la base de datos

except mysql.connector.Error as e:
    print(f'Error al conectar a la base de datos: {e}')

finally:
    # Asegúrate de cerrar la conexión cuando hayas terminado
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print('Conexión cerrada.')





# Clase para manejar el carrito
class Carrito:
    def __init__(self):
        self.items = {}

    def agregar_producto(self, producto_id):
        if producto_id in self.items:
            self.items[producto_id] += 1
        else:
            self.items[producto_id] = 1

    def quitar_producto(self, producto_id):
        if producto_id in self.items:
            if self.items[producto_id] > 1:
                self.items[producto_id] -= 1
            else:
                del self.items[producto_id]

    def vaciar_carrito(self):
        self.items = {}

    def obtener_cantidad_total(self):
        return sum(self.items.values())

carrito = Carrito()


# Rutas
@app.route('/')
def index():
    # Calcula la cantidad total de productos en el carrito
    cantidad_total = carrito.obtener_cantidad_total()
    return render_template('templates/index.html', carrito=carrito, cantidad_total=cantidad_total)

@app.route('/agregar/<int:producto_id>', methods=['POST'])
def agregar_producto(producto_id):
    carrito.agregar_producto(producto_id)
    return redirect(url_for('index'))

@app.route('/quitar/<int:producto_id>', methods=['POST'])
def quitar_producto(producto_id):
    carrito.quitar_producto(producto_id)
    return redirect(url_for('index'))

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    carrito.vaciar_carrito()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
