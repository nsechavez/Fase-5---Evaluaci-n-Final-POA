import pandas as pd
import numpy as np

# 1. Matriz de inventario con al menos 5 artículos
inventario = [
    {"Código Artículo": "A001", "Nombre": "Tornillos", "Stock Actual": 50, "Stock Mínimo Requerido": 100},
    {"Código Artículo": "A002", "Nombre": "Martillos", "Stock Actual": 10, "Stock Mínimo Requerido": 20},
    {"Código Artículo": "A003", "Nombre": "Clavos", "Stock Actual": 200, "Stock Mínimo Requerido": 150},
    {"Código Artículo": "A004", "Nombre": "Destornilladores", "Stock Actual": 15, "Stock Mínimo Requerido": 30},
    {"Código Artículo": "A005", "Nombre": "Cintas métricas", "Stock Actual": 5, "Stock Mínimo Requerido": 10},
    {"Código Artículo": "A006", "Nombre": "Llaves inglesas", "Stock Actual": 25, "Stock Mínimo Requerido": 25}
]

# Convertir la lista de diccionarios a un DataFrame de Pandas para una mejor manipulación
df_inventario = pd.DataFrame(inventario)

# 2. Módulo (función) para determinar la cantidad exacta a pedir para un artículo
def calcular_cantidad_a_pedir(stock_actual, stock_minimo_requerido):
    """
    Calcula la cantidad a pedir para un artículo.
    
    Args:
        stock_actual (int): El stock actual del artículo.
        stock_minimo_requerido (int): El stock mínimo requerido para el artículo.
        
    Returns:
        int: La cantidad a pedir (cero si el stock es suficiente).
    """
    if stock_actual < stock_minimo_requerido:
        return stock_minimo_requerido - stock_actual
    else:
        return 0

# 3. Lógica de Negocio y Salida: Imprimir una lista de pedidos inicial
print("-- Lista de Pedidos de Inventario Inicial ---")
lista_pedidos_inicial = []

for index, row in df_inventario.iterrows():
    nombre_articulo = row["Nombre"]
    stock_actual = row["Stock Actual"]
    stock_minimo = row["Stock Mínimo Requerido"]
    
    cantidad_a_pedir = calcular_cantidad_a_pedir(stock_actual, stock_minimo)
    
    if cantidad_a_pedir > 0:
        lista_pedidos_inicial.append({"Artículo": nombre_articulo, "Cantidad a Pedir": cantidad_a_pedir})

if lista_pedidos_inicial:
    for pedido in lista_pedidos_inicial:
        print(f"Artículo: {pedido['Artículo']}, Cantidad a Pedir: {pedido['Cantidad a Pedir']}")
else:
    print("No se necesitan pedidos en este momento. El inventario es suficiente para todos los artículos.")

print("---------------------------------------------")

# Función para consultar el stock de un artículo
def consultar_stock(nombre_articulo):
    item = df_inventario[df_inventario['Nombre'].str.lower() == nombre_articulo.lower()]
    if not item.empty:
        print(f"\n--- Información de Stock para {item['Nombre'].values[0]} ---")
        print(f"Stock Actual: {item['Stock Actual'].values[0]}")
        print(f"Stock Mínimo Requerido: {item['Stock Mínimo Requerido'].values[0]}")
        cantidad_a_pedir_actual = calcular_cantidad_a_pedir(item['Stock Actual'].values[0], item['Stock Mínimo Requerido'].values[0])
        if cantidad_a_pedir_actual > 0:
            print(f"Cantidad sugerida a pedir: {cantidad_a_pedir_actual}")
        else:
            print("Stock suficiente. No se necesita pedir.")
        print("------------------------------------------")
    else:
        print(f"\nArtículo '{nombre_articulo}' no encontrado en el inventario.")

# Función para realizar un pedido (simulación: actualiza el Stock Actual)
def realizar_pedido(nombre_articulo, cantidad_pedida):
    global df_inventario # Para modificar el DataFrame globalmente
    
    idx = df_inventario[df_inventario['Nombre'].str.lower() == nombre_articulo.lower()].index
    if not idx.empty:
        # Convertir cantidad_pedida a entero, ya que input() devuelve string
        try:
            cantidad_pedida = int(cantidad_pedida)
            if cantidad_pedida < 0:
                print("La cantidad a pedir no puede ser negativa.")
                return
        except ValueError:
            print("La cantidad debe ser un número entero.")
            return
            
        df_inventario.loc[idx, 'Stock Actual'] += cantidad_pedida
        print(f"\nSe han añadido {cantidad_pedida} unidades de '{df_inventario.loc[idx, 'Nombre'].values[0]}'.")
        print(f"Nuevo Stock Actual: {df_inventario.loc[idx, 'Stock Actual'].values[0]}")
        
        # Re-evaluar si el artículo sigue necesitando ser reabastecido
        stock_actual = df_inventario.loc[idx, 'Stock Actual'].values[0]
        stock_minimo = df_inventario.loc[idx, 'Stock Mínimo Requerido'].values[0]
        cantidad_sugerida = calcular_cantidad_a_pedir(stock_actual, stock_minimo)
        if cantidad_sugerida > 0:
            print(f"Aún se sugieren pedir {cantidad_sugerida} unidades más para alcanzar el mínimo.")
        else:
            print("El stock ahora es suficiente.")
            
    else:
        print(f"\nArtículo '{nombre_articulo}' no encontrado en el inventario.")

# Interfaz interactiva simple
while True:
    print("\n--- Menú de Inventario ---")
    print("1. Consultar stock de un artículo")
    print("2. Realizar un pedido (actualizar stock)")
    print("3. Mostrar todo el inventario")
    print("4. Salir")
    
    opcion = input("Ingrese su opción: ")
    
    if opcion == '1':
        nombre = input("Ingrese el nombre del artículo a consultar: ")
        consultar_stock(nombre)
    elif opcion == '2':
        nombre = input("Ingrese el nombre del artículo para el pedido: ")
        cantidad = input("Ingrese la cantidad a pedir: ")
        realizar_pedido(nombre, cantidad)
    elif opcion == '3':
        print("\n--- Inventario Completo ---")
        print(df_inventario)
        print("---------------------------")
    elif opcion == '4':
        print("Saliendo del programa de inventario.")
        break
    else:
        print("Opción no válida. Por favor, intente de nuevo.")
