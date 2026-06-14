
nombres_productos = ["Arroz", "Azucar", "Leche"]
precios_productos = [4.5, 5.0, 4.0]
stock_productos = [30, 20, 15]

historial_ventas = []
historial_montos = []
historial_deudores = []
def ver_stock(nombres, precios, stock):
    print("\n--- CONSULTA DE STOCK ---")
    for i in range(len(nombres)):
        print("Producto:", nombres[i], " | Precio: S/.", precios[i], " | Stock:", stock[i])
    print("Consulta correcta")


def agregar_producto(nombres, precios, stock):
    print("\n--- AGREGAR PRODUCTO ---")
    if len(nombres) < 50:
        nuevo_nombre = input("Ingrese nombre del nuevo producto: ")
        while nuevo_nombre == "":
            print("Error: El nombre no puede estar vacío.")
            nuevo_nombre = input("Ingrese nombre del nuevo producto: ")
            # ACTUALIZACIÓN 1:
        # Eliminar espacios innecesarios al inicio y final del nombre.
        nuevo_nombre = input("Ingrese nombre del nuevo producto: ").strip()

        while nuevo_nombre == "":
            print("Error: El nombre no puede estar vacío.")
            nuevo_nombre = input("Ingrese nombre del nuevo producto: ").strip()
            # ACTUALIZACIÓN 2:
        # Estandarizar el nombre del producto para mantener uniformidad.
        nuevo_nombre = nuevo_nombre.title()

        precio_texto = input("Ingrese precio del producto: ")
        while not precio_texto.replace(".", "", 1).isdigit() or float(precio_texto) <= 0:
            print("Error: Ingrese un precio válido mayor a 0.")
            precio_texto = input("Ingrese precio del producto: ")
        nuevo_precio = float(precio_texto)

        stock_texto = input("Ingrese stock inicial: ")
        while not stock_texto.isdigit() or int(stock_texto) < 0:
            print("Error: Ingrese un stock válido (entero mayor o igual a 0).")
            stock_texto = input("Ingrese stock inicial: ")
        nuevo_stock = int(stock_texto)
        # ACTUALIZACIÓN 3:
        # Solicitar confirmación antes de registrar el producto.
        confirmar = input("¿Desea guardar el producto? (S/N): ").upper()
        if confirmar == "S":

         nombres.append(nuevo_nombre)
         precios.append(nuevo_precio)
         stock.append(nuevo_stock)
        print("Registro válido: Producto agregado correctamente.")
    else:
        print("Error: Capacidad máxima de almacén alcanzada.")