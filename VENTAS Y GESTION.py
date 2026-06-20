# ============================================================
# SISTEMA DE VENTAS Y GESTION DE BODEGA
# Curso: Fundamentos de Programacion - CIIN1205P
# ============================================================

import os

# --- DATOS INICIALES DEL INVENTARIO ---
nombres_productos = ["Arroz", "Azucar", "Leche"]
precios_productos = [4.5, 5.0, 4.0]
stock_productos   = [30, 20, 15]

# --- HISTORIAL DE VENTAS ---
historial_ventas   = []
historial_montos   = []
historial_deudores = []


# ============================================================
# FUNCION 1: Registrar venta (RQ-01, RQ-02, RQ-03, RQ-06)
# ============================================================
def registrar_venta(nombres, precios, stock, h_ventas, h_montos, h_deudores):
    print("\n--- REGISTRAR NUEVA VENTA ---")

    # Validacion: limite de 50 ventas
    if len(h_ventas) >= 50:
        print("Error: Se ha alcanzado el limite de 50 ventas.")
        return

    # Validacion: nombre del producto no vacio
    producto = ""
    while producto == "":
        producto = input("Ingrese nombre del producto: ").strip()
        if producto == "":
            print("Error: El nombre no puede estar vacio.")

    # Buscar producto en inventario
    indice = -1
    for i in range(len(nombres)):
        if nombres[i].lower() == producto.lower():
            indice = i

    if indice == -1:
        print("Error: El producto no existe en el inventario.")
        return

    # Validacion: cantidad entera mayor a 0
    cantidad_texto = ""
    while True:
        cantidad_texto = input("Ingrese cantidad: ").strip()
        if cantidad_texto.isdigit() and int(cantidad_texto) > 0:
            break
        print("Error: Debe ingresar un numero entero mayor a 0.")
    cantidad = int(cantidad_texto)

    # Verificar stock suficiente
    if stock[indice] < cantidad:
        print("Error: No hay suficiente stock. Stock disponible:", stock[indice])
        return

    total = precios[indice] * cantidad
    print("Total de la venta: S/.", round(total, 2))

    # Seleccion tipo de pago con validacion
    print("Tipo de pago:")
    print("1. Efectivo")
    print("2. Fiado")
    tipo_pago = ""
    while tipo_pago not in ["1", "2"]:
        tipo_pago = input("Seleccione una opcion (1 o 2): ").strip()
        if tipo_pago not in ["1", "2"]:
            print("Error: Opcion no valida. Ingrese 1 o 2.")

    if tipo_pago == "1":
        # RQ-02: calcular_vuelto()
        dinero_texto = ""
        while True:
            dinero_texto = input("Ingrese dinero recibido: ").strip()
            try:
                dinero = float(dinero_texto)
                if dinero < total:
                    print("Error: Dinero insuficiente. El total es S/.", round(total, 2))
                else:
                    break
            except ValueError:
                print("Error: Ingrese un monto numerico valido.")
        vuelto = dinero - total
        print("Vuelto correcto: S/.", round(vuelto, 2))
        print("Venta registrada correctamente.")
        estado_pago = "Efectivo"

    else:
        # RQ-06: registrar_fiado()
        cliente = ""
        while cliente == "":
            cliente = input("Ingrese nombre del cliente que debe: ").strip()
            if cliente == "":
                print("Error: El nombre del cliente no puede estar vacio.")
        print("Fiado registrado. Deuda de S/.", round(total, 2), "guardada para el cliente:", cliente)
        estado_pago = cliente

    # RQ-03: actualizar_stock()
    stock[indice] -= cantidad
    print("Stock actualizado:", stock[indice], "unidades restantes.")

    # Guardar en historial
    h_ventas.append(nombres[indice])
    h_montos.append(round(total, 2))
    h_deudores.append(estado_pago)

    # Guardar en archivo ventas.txt
    guardar_venta_archivo(nombres[indice], round(total, 2), estado_pago)


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
# - Guarda reporte en archivo reporte.txt
# ============================================================
def generar_reporte(h_ventas, h_montos, h_deudores):
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
        with open("reporte.txt", "w", encoding="utf-8") as archivo:
            archivo.writelines(lineas_reporte)

        print("\nReporte guardado correctamente en 'reporte.txt'")

    except Exception as e:
        print("\nNo se pudo guardar el reporte:", e)

    print("Reporte completado correctamente.")


# ============================================================
# FUNCION 5: Salir MEJORADA (RQ-08)
# - Pide confirmacion antes de salir
# - Guarda inventario en archivo inventario.txt
# ============================================================
def salir(nombres, precios, stock):
    print("\n--- SALIR DEL SISTEMA ---")

    # Confirmacion antes de cerrar
    confirmacion = ""
    while confirmacion not in ["s", "n"]:
        confirmacion = input("¿Esta seguro que desea salir? (S/N): ").strip().lower()
        if confirmacion not in ["s", "n"]:
            print("Error: Ingrese S para confirmar o N para cancelar.")

    if confirmacion == "n":
        print("Operacion cancelada. Regresando al menu...")
        return False  # No salir

    # Guardar inventario actual en archivo
    try:
        with open("inventario.txt", "w", encoding="utf-8") as f:
            f.write("=== INVENTARIO FINAL DEL DIA ===\n")
            for i in range(len(nombres)):
                f.write(f"Producto: {nombres[i]} | Precio: S/. {precios[i]} | Stock: {stock[i]}\n")
        print("Inventario guardado correctamente en 'inventario.txt'")
    except Exception as e:
        print("Advertencia: No se pudo guardar el inventario.", e)

    print("Cierre correcto. Saliendo del sistema...")
    return True  # Confirmar salida.


# ============================================================
# FUNCION AUXILIAR: Guardar venta individual en archivo
# ============================================================
def guardar_venta_archivo(producto, monto, estado):
    try:
        with open("ventas.txt", "a", encoding="utf-8") as f:
            f.write(f"Producto: {producto} | Monto: S/. {monto} | Estado: {estado}\n")
    except Exception as e:
        print("Advertencia: No se pudo registrar en archivo.", e)


# ============================================================
# MENU PRINCIPAL
# ============================================================
def menu_principal():
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
            registrar_venta(nombres_productos, precios_productos, stock_productos,
                            historial_ventas, historial_montos, historial_deudores)
        elif opcion == "2":
            ver_stock(nombres_productos, precios_productos, stock_productos)
        elif opcion == "3":
            agregar_producto(nombres_productos, precios_productos, stock_productos)
        elif opcion == "4":
            generar_reporte(historial_ventas, historial_montos, historial_deudores)
        elif opcion == "5":
            cerrar = salir(nombres_productos, precios_productos, stock_productos)
            if not cerrar:
                opcion = "0"  # Cancelar salida, volver al menu
        else:
            print("Opcion no valida, intente de nuevo.")


# --- PUNTO DE ENTRADA ---
menu_principal()
