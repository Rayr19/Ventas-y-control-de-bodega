# ============================================================
# SISTEMA DE VENTAS Y GESTION DE BODEGA
# Curso: Fundamentos de Programacion - CIIN1205P
# ============================================================
import csv
import os

# --- DATOS INICIALES DEL INVENTARIO ---
nombres_productos = ["Arroz", "Azucar", "Leche"]
precios_productos = [4.5, 5.0, 4.0]
stock_productos   = [30, 20, 15]
secciones_productos = [] #Ruben - Nueva mejora, agregar seccion a cada producto para mejor organizacion y consulta
# --- HISTORIAL DE VENTAS ---
historial_ventas   = []
historial_montos   = []
historial_deudores = []


# ============================================================
# FUNCION 1: Registrar venta (RQ-01, RQ-02, RQ-03, RQ-06)
# ============================================================
def registrar_venta(nombres, precios, stock, secciones, h_ventas, h_montos, h_deudores):

    #Ruben - Nueva mejora , mostrar como catalogo al registrar venta para facilitar seleccion y evitar errores de tipeo
    print("\n" + "="*80)
    print("                REGISTRAR NUEVA VENTA - SELECCIONE PRODUCTO")
    print("="*80)
    
    # para poder imprimir el Formato en tabla
    if not nombres:
        print("No hay productos disponibles.")
        return

    print(f"{'#':<3} | {'PRODUCTO':<25} | {'PRECIO':<8} | {'STOCK':<6} | {'SECCIÓN'}")
    print("-" * 80)
    for i in range(len(nombres)):
        print(f"{i + 1:<3} | {nombres[i]:<25} | S/. {precios[i]:<5} | {stock[i]:<6} | {secciones[i]}")
    print("-" * 80)

    # para poder seleccionar el producto por numero y evitar errores de tipeo.
    try:
        seleccion = int(input("\nIngrese el número del producto a vender: ")) - 1
        if seleccion < 0 or seleccion >= len(nombres):
            print("Error: Producto no encontrado.")
            return
    except ValueError:
        print("Error: Ingrese un número válido.")
        return

    # para validar la cantida y el stock disponible
    try:
        cantidad = int(input(f"Cantidad de {nombres[seleccion]}: "))
        if cantidad <= 0 or cantidad > stock[seleccion]:
            print("Error: Cantidad no válida o sin stock suficiente.")
            return

        #para calcular el total a pagar
        total = precios[seleccion] * cantidad
        print(f"\nTotal a pagar: S/. {total:.2f}")

        # para seleccionar el tipo de pago y registrar la venta
        tipo = input("¿1. Efectivo o 2. Fiado?: ")
        if tipo == "1":
            monto_recibido = float(input("Monto recibido: S/. "))
            if monto_recibido >= total:
                print(f"Vuelto: S/. {monto_recibido - total:.2f}")
                estado = "Efectivo"
            else:
                print("Error: Monto insuficiente.")
                return
        else:
            estado = input("Nombre del cliente: ")

        # Guardar después de cada venta
        stock[seleccion] -= cantidad
        h_ventas.append(nombres[seleccion])
        h_montos.append(total)
        h_deudores.append(estado)
        guardar_historial_ventas(h_ventas, h_montos, h_deudores) 
        print("¡Venta registrada con éxito!")
        
    except ValueError:
        print("Error: Entrada no válida.")

# ============================================================
# FUNCION 2: Ver stock (RQ-04)
# ============================================================
def ver_stock(nombres, precios, stock):
    print("\n--- CONSULTA DE STOCK ---")
    if len(nombres) == 0:
        print("No hay productos registrados.")
        return
    for i in range(len(nombres)):
        print("Producto:", nombres[i],
              " | Precio: S/.", precios[i],
              " | Stock:", stock[i])
    print("Consulta correcta")


# ============================================================
# FUNCION 3: Agregar producto (RQ-05)
# ============================================================
def agregar_producto(nombres, precios, stock):
    print("\n--- GESTION DE PRODUCTOS ---")
    print("1. Agregar nuevo producto")
    print("2. Actualizar producto existente")

    opcion = input("Seleccione una opcion: ").strip()

    # ============================================================
    # MEJORA GENERAL:
    # Se convierte una sola funcion en un modulo de gestion
    # permitiendo AGREGAR y ACTUALIZAR sin cambiar el menu principal
    # ============================================================

    # ============================================================
    # OPCION 1: AGREGAR PRODUCTO (MEJORADO)
    # ============================================================
    if opcion == "1":

        # MEJORA: control de capacidad
        if len(nombres) >= 50:
            print("Error: Capacidad maxima de almacen alcanzada.")
            return

        # MEJORA: limpieza de datos
        nuevo_nombre = input("Ingrese nombre del nuevo producto: ").strip()

        while nuevo_nombre == "":
            print("Error: El nombre no puede estar vacio.")
            nuevo_nombre = input("Ingrese nombre del nuevo producto: ").strip()

        # MEJORA: estandarizacion
        nuevo_nombre = nuevo_nombre.title()

        # MEJORA: evitar duplicados
        for producto in nombres:
            if producto.lower() == nuevo_nombre.lower():
                print("Error: El producto ya existe en el inventario.")
                return

        # MEJORA: validacion de precio
        while True:
            try:
                nuevo_precio = float(input("Ingrese precio del producto: "))
                if nuevo_precio > 0:
                    break
                print("Error: El precio debe ser mayor a 0.")
            except ValueError:
                print("Error: Ingrese un numero valido.")

        # MEJORA: validacion de stock
        while True:
            stock_texto = input("Ingrese stock inicial: ")
            if stock_texto.isdigit() and int(stock_texto) >= 0:
                nuevo_stock = int(stock_texto)
                break
            print("Error: Ingrese un stock valido.")

        # MEJORA: confirmacion
        confirmar = input("¿Desea guardar el producto? (S/N): ").strip().upper()

        if confirmar == "S":

            nombres.append(nuevo_nombre)
            precios.append(nuevo_precio)
            stock.append(nuevo_stock)

            # MEJORA: resumen
            print("\n--- RESUMEN DEL PRODUCTO ---")
            print("Nombre:", nuevo_nombre)
            print("Precio: S/.", nuevo_precio)
            print("Stock:", nuevo_stock)

            # MEJORA: contador
            print("Total de productos registrados:", len(nombres))

            # MEJORA: mensaje final
            print(f"Producto '{nuevo_nombre}' agregado correctamente.")

        else:
            print("Operacion cancelada.")

    # ============================================================
    # OPCION 2: ACTUALIZAR PRODUCTO (NUEVA MEJORA)
    # ============================================================
    elif opcion == "2":

        # MEJORA: validacion de entrada
        producto = input("Ingrese nombre del producto a actualizar: ").strip()

        while producto == "":
            print("Error: El nombre no puede estar vacio.")
            producto = input("Ingrese nombre del producto a actualizar: ").strip()

        producto = producto.title()

        # MEJORA: busqueda segura
        indice = -1
        for i in range(len(nombres)):
            if nombres[i].lower() == producto.lower():
                indice = i
                break

        # MEJORA: validacion existencia
        if indice == -1:
            print("Error: Producto no encontrado.")
            return

        print("\n--- PRODUCTO ENCONTRADO ---")
        print("Nombre:", nombres[indice])
        print("Precio actual: S/.", precios[indice])
        print("Stock actual:", stock[indice])

        # MEJORA: nuevo precio validado
        while True:
            try:
                nuevo_precio = float(input("Ingrese nuevo precio: "))
                if nuevo_precio > 0:
                    break
                print("Error: Precio invalido.")
            except ValueError:
                print("Error: Ingrese un numero valido.")

        # MEJORA: nuevo stock validado
        while True:
            stock_texto = input("Ingrese nuevo stock: ")
            if stock_texto.isdigit() and int(stock_texto) >= 0:
                nuevo_stock = int(stock_texto)
                break
            print("Error: Stock invalido.")

        # MEJORA: confirmacion
        confirmar = input("¿Desea actualizar el producto? (S/N): ").strip().upper()

        if confirmar == "S":

            precios[indice] = nuevo_precio
            stock[indice] = nuevo_stock

            # MEJORA: resumen final
            print("\n--- PRODUCTO ACTUALIZADO ---")
            print("Nombre:", nombres[indice])
            print("Nuevo precio: S/.", precios[indice])
            print("Nuevo stock:", stock[indice])

            print("Producto actualizado correctamente.")

        else:
            print("Actualizacion cancelada.")

    else:
        print("Opcion no valida.")


# ============================================================
# FUNCION 4: Generar reporte MEJORADO (RQ-07)
# - Muestra ventas, total acumulado y fiados pendientes
# - Guarda reporte en archivo reporte.csv
# ============================================================
def generar_reporte(h_ventas, h_montos, h_deudores):

    #Ruben - Cargar historial de ventas desde archivo 
    if os.path.exists("ventas.csv"):
        try:
            with open("ventas.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=';') #ruben , para que en el excel se separen las columnas correctamente
                next(reader, None)  
                
                
                h_ventas.clear()
                h_montos.clear()
                h_deudores.clear()
                
                for fila in reader:
                    if len(fila) == 3:
                        h_ventas.append(fila[0])
                        h_montos.append(float(fila[1]))
                        h_deudores.append(fila[2])
        except Exception as e:
            print(f"Error al leer el historial: {e}")

  

    print("\n--- REPORTE DE HISTORICOS (Ventas y Cuentas por Cobrar) ---")

    # MEJORA 1: Validar que las listas tengan la misma cantidad de elementos
    if len(h_ventas) != len(h_montos) or len(h_ventas) != len(h_deudores):
        print("Error: Las listas contienen diferentes cantidades de elementos.")
        return

    # MEJORA 2: Validar que los montos sean numéricos
    for monto in h_montos:
        if not isinstance(monto, (int, float)):
            print("Error: Existe un monto no numérico.")
            return

    if len(h_ventas) == 0:
        print("No hay ventas registradas en el sistema.")
        return

    total_vendido = 0
    ventas_pagadas = 0
    ventas_credito = 0

    # Lista para guardar el reporte en archivo
    lineas_reporte = []
    lineas_reporte.append("=== REPORTE DE VENTAS ===\n\n")

    # MEJORA 3: Mostrar detalle de ventas
    for i in range(len(h_ventas)):
        total_vendido += h_montos[i]

        if h_deudores[i] == "Efectivo":
            ventas_pagadas += 1

            linea = (
                f"Venta N {i+1} -> Producto: {h_ventas[i]}"
                f" | Monto: S/. {h_montos[i]}"
                f" | Estado: PAGADO (Efectivo)"
            )

        else:
            ventas_credito += 1

            linea = (
                f"Venta N {i+1} -> Producto: {h_ventas[i]}"
                f" | Monto: S/. {h_montos[i]}"
                f" | Estado: POR COBRAR a [{h_deudores[i]}]"
            )

        print(linea)
        lineas_reporte.append(linea + "\n")

    # MEJORA 4: Resumen del reporte
    print("\n--- RESUMEN ---")
    print("Total vendido: S/.", total_vendido)
    print("Ventas pagadas:", ventas_pagadas)
    print("Ventas por cobrar:", ventas_credito)

    lineas_reporte.append("\n--- RESUMEN ---\n")
    lineas_reporte.append(f"Total vendido: S/. {total_vendido}\n")
    lineas_reporte.append(f"Ventas pagadas: {ventas_pagadas}\n")
    lineas_reporte.append(f"Ventas por cobrar: {ventas_credito}\n")

    # MEJORA 5: Promedio por venta
    promedio = total_vendido / len(h_ventas)

    print("Promedio por venta: S/.", round(promedio, 2))

    lineas_reporte.append(
        f"Promedio por venta: S/. {round(promedio, 2)}\n"
    )

    # MEJORA 6: Ranking de productos más vendidos
    ranking = {}

    for producto in h_ventas:
        if producto in ranking:
            ranking[producto] += 1
        else:
            ranking[producto] = 1

    print("\n--- RANKING DE PRODUCTOS ---")

    lineas_reporte.append("\n--- RANKING DE PRODUCTOS ---\n")

    for producto, cantidad in sorted(ranking.items(),
                key=lambda x: x[1],
                  reverse=True):

        print(f"{producto}: {cantidad} unidades vendidas")

        lineas_reporte.append(
            f"{producto}: {cantidad} unidades vendidas\n"
        )

    # MEJORA 7: Guardar reporte en archivo
    try:
        with open("reporte.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo, delimiter=';') #ruben , para que en el excel se separen las columnas correctamente

           
            writer.writerow(["N° Venta", "Producto", "Monto", "Estado"])

           
            for i in range(len(h_ventas)):

                if h_deudores[i] == "Efectivo":
                    estado = "PAGADO"
                else:
                    estado = "POR COBRAR"

                writer.writerow([
                    i + 1,
                    h_ventas[i],
                    h_montos[i],
                    estado
                ])


        print("\nReporte guardado correctamente en 'reporte.csv'")
    except Exception as e:
        print("\nNo se pudo guardar el reporte:", e)


# ============================================================
# FUNCION 5: Salir MEJORADA (RQ-08)
# - Pide confirmacion antes de salir
# - Guarda inventario en archivo inventario.csv
# ============================================================

def salir(nombres, precios, stock, secciones):
    print("\n--- SALIR DEL SISTEMA ---")

    confirmacion = ""
    while confirmacion not in ["s", "n"]:
        confirmacion = input("¿Esta seguro que desea salir? (S/N): ").strip().lower()
        if confirmacion not in ["s", "n"]:
            print("Error: Ingrese S para confirmar o N para cancelar.")

    if confirmacion == "n":
        print("Operacion cancelada. Regresando al menu...")
        return False

    # Guardar inventario en CSV
    try:
        with open("inventario.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')

            
            writer.writerow(["Producto", "Precio", "Stock", "Seccion"])

           
            for i in range(len(nombres)):
                writer.writerow([
                    nombres[i],
                    precios[i],
                    stock[i],
                    secciones[i] 
                ])

        print("Inventario guardado correctamente en 'inventario.csv'")

    except Exception as e:
        print("Advertencia: No se pudo guardar el inventario.", e)

    print("Cierre correcto. Saliendo del sistema...")
    return True

# ============================================================
# FUNCION AUXILIAR: Guardar venta individual en archivo
# ============================================================

def guardar_venta_archivo(producto, monto, estado):
    try:
        archivo_existe = os.path.exists("ventas.csv")

        with open("ventas.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not archivo_existe:
                writer.writerow(["Producto", "Monto", "Estado"])

            writer.writerow([producto, monto, estado])

    except Exception as e:
        print("Advertencia:", e)
        



# ============================================================
# MENU PRINCIPAL
# ============================================================
def menu_principal():
    cargar_inventario()  # Cargar inventario al iniciar el programa(Ruben)
    cargar_ventas()  # Cargar historial de ventas al iniciar el programa(Ruben)
    opcion = "0"
    while opcion != "5":
        print("\n=== SISTEMA DE VENTAS DE LA BODEGA ===")
        print("1. Registrar venta")
        print("2. Ver stock")
        print("3. Agregar producto")
        print("4. Generar reporte")
        print("5. Salir")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":                                                           
            registrar_venta(nombres_productos, precios_productos, stock_productos, secciones_productos, historial_ventas, historial_montos, historial_deudores)
        elif opcion == "2":
            ver_stock(nombres_productos, precios_productos, stock_productos)
        elif opcion == "3":
            agregar_producto(nombres_productos, precios_productos, stock_productos)
        elif opcion == "4":
            generar_reporte(historial_ventas, historial_montos, historial_deudores)
        elif opcion == "5":
            cerrar = salir(nombres_productos,  precios_productos, stock_productos, secciones_productos)
            if not cerrar:
                opcion = "0"  # Cancelar salida, volver al menu
        else:
            print("Opcion no valida, intente de nuevo.")

#Ruben

def cargar_inventario():

    #ruben - Limpiar las listas antes de cargar para evitar duplicados en caso de múltiples cargas
    nombres_productos.clear()
    precios_productos.clear()
    stock_productos.clear()
    
    secciones_productos.clear()

    if os.path.exists("inventario.csv"):
     try:
        with open("inventario.csv", "r", encoding="utf-8") as f:
            lineas = f.readlines()
            for linea in lineas[1:]:
                linea = linea.strip()
                if linea:  
                    datos = linea.split(';') # Aquí se separan los datos por el punto y coma
                    if len(datos) == 4:
                        nombres_productos.append(datos[0])
                        precios_productos.append(float(datos[1]))
                        stock_productos.append(int(datos[2]))
                        secciones_productos.append(datos[3])
        print("Inventario cargado exitosamente.")
        
     except Exception as e:
            print(f"Error al cargar el inventario: {e}")
    else:
        print("No se encontró archivo de inventario previo. Iniciando con valores predeterminados.")

def cargar_ventas():
    if os.path.exists("ventas.csv"):
        try:
            with open("ventas.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=';')
                next(reader, None)  
                
                historial_ventas.clear()
                historial_montos.clear()
                historial_deudores.clear()
                
                for fila in reader:
                    if len(fila) == 3:
                        historial_ventas.append(fila[0])
                        historial_montos.append(float(fila[1]))
                        historial_deudores.append(fila[2])

            print("Historial de ventas y deudas cargado correctamente.")
        except Exception as e:
            print(f"Error al cargar historial: {e}")


def ver_stock(nombres, precios, stock):
    print("\n" + "="*70)
    print("                    CATÁLOGO DE LA TIENDA")
    print("="*70)
    
    if not nombres: 
        print("El inventario está vacío.")
        return

    print(f"{'PRODUCTO':<30} | {'PRECIO':<10} | {'STOCK':<8} | {'SECCIÓN'}")
    print("-" * 70)
    
    for i in range(len(nombres)):
        print(f"{nombres[i]:<30} | S/. {precios[i]:<6} | {stock[i]:<8} | {secciones_productos[i]}")
        
    print("="*70 + "\n")


def guardar_inventario(nombres, precios, stock, secciones):
    print(f"DEBUG: Voy a guardar {len(nombres)} productos.") 
    try:
        with open("inventario.csv", "w", encoding="utf-8") as f:
            f.write("Producto,Precio,Stock,Seccion\n")
            for i in range(len(nombres)):
                f.write(f"{nombres[i]},{precios[i]},{stock[i]},{secciones[i]}\n")
        print("Datos guardados con éxito.")
    except Exception as e:
        print(f"Error al guardar: {e}")

def guardar_historial_ventas(h_ventas, h_montos, h_deudores):
    try:
        with open("ventas.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';') 
            
            
            writer.writerow(["Producto", "Monto", "Estado"])
            
            for i in range(len(h_ventas)):
                writer.writerow([h_ventas[i], h_montos[i], h_deudores[i]])
                
    except Exception as e:
        print(f"Error al guardar historial: {e}")

# --- PUNTO DE ENTRADA ---
menu_principal()
