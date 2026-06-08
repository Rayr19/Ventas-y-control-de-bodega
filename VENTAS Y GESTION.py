
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

        nombres.append(nuevo_nombre)
        precios.append(nuevo_precio)
        stock.append(nuevo_stock)
        print("Registro válido: Producto agregado correctamente.")
    else:
        print("Error: Capacidad máxima de almacén alcanzada.")

def generar_reporte(h_ventas, h_montos, h_deudores):
    print("\n--- REPORTE DE HISTORICOS (Ventas y Cuentas por Cobrar) ---")
    if len(h_ventas) == 0:
        print("No hay ventas registradas en el sistema.")
    else:
        for i in range(len(h_ventas)):
            if h_deudores[i] == "Efectivo":
                print("Venta N", i + 1, " -> Producto:", h_ventas[i], " | Monto: S/.", h_montos[i], " | Estado: PAGADO (Efectivo)")
            else:
                print("Venta N", i + 1, " -> Producto:", h_ventas[i], " | Monto: S/.", h_montos[i], " | Estado: POR COBRAR a [", h_deudores[i], "]")
        print("Reporte correcto")

def menu_principal():
    opcion = "0"
    while opcion != "5":
        print("\n=== SISTEMA DE VENTAS DE LA BODEGA ===")
        print("1. Registrar venta")
        print("2. Ver stock")
        print("3. Agregar producto")
        print("4. Generar reporte")
        print("5. Salir")
        
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            registrar_venta(nombres_productos, precios_productos, stock_productos, historial_ventas, historial_montos, historial_deudores)
        elif opcion == "2":
            ver_stock(nombres_productos, precios_productos, stock_productos)
        elif opcion == "3":
            agregar_producto(nombres_productos, precios_productos, stock_productos)
        elif opcion == "4":
            generar_reporte(historial_ventas, historial_montos, historial_deudores)
        elif opcion == "5":

            print("Cierre correcto. Saliendo del sistema...")
        else:
            print("Opcion no valida, intente de nuevo.")

menu_principal()        
             
