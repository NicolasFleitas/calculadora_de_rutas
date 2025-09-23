# MVP: 
# Primera versión con datos estáticos y simulación de obstáculos fijos (con el mismo valor)
# Resolución utilizando bfs.

# 0 -> CAMINO LIBRE
# 1 -> edificio (no se puede pasar)
# 2 -> agua (obstáculo, pero podría tener un costo mayor en lugar de ser bloqueado)
# 3 -> zona bloqueada temporalmente

from collections import deque
import random

def crear_mapa(filas, cols):
    return [[0 for _ in range(cols)] for _ in range(filas)]

# Funcion para visualizar datos en consola
def mostrar_mapa(mapa, ruta=None, inicio=None, fin=None):
    simbolos = {0: ".", 1: "X", 2: "X", 3: "X"}
    ruta_set = set(ruta) if ruta else set()

    for i, fila in enumerate(mapa):
        linea = ""
        for j, celda in enumerate(fila):
            pos = (i, j)

            if pos == inicio:
                linea += "S "
            elif pos == fin:
                linea += "D "
            elif pos in ruta_set:
                linea += "* "
            else:
                linea += simbolos[celda] + " "
        print(linea)
    print()

# Validar posiciones
def es_valido(mapa, fila, col):
    # Valida que una coordenada esté dentro del mapa y sea transitable.
    return (
        0 <= fila < len(mapa)
        and 0 <= col < len(mapa[0])
        and mapa[fila][col] == 0
    )

# bfs para rutas
def bfs(mapa, inicio, fin):

    if not es_valido(mapa, inicio[0], inicio[1]) or not es_valido(mapa, fin[0], fin[1]):
        return None

    # retorna la lista de coordenadas que forman la ruta o None si no existe
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # N, S, O, E
    visitados = set([inicio])
    padres = {inicio: None} # Guarda de dónde vino cada nodo
    cola = deque([inicio]) # La cola solo guarda posiciones

    while cola:
        actual = cola.popleft() # Extrae el 1° elemento de la cola, es el Nodo a explorar en el paso actual

        if actual == fin: # Si nodo actual es el destino, la búsqueda terminó con éxito.
            # reconstruir ruta desde fin -> inicio
            ruta = []
            while actual is not None:
                ruta.append(actual)
                actual = padres[actual]
            return ruta[::-1]  # invertimos para inicio -> fin
        
        fila, col = actual

        for df, dc in movimientos:
            nf, nc = fila + df, col + dc
            vecino = (nf, nc)

            if es_valido(mapa, nf, nc) and vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                cola.append(vecino)    
    return None # No se encontró ruta

def generar_ciudad(mapa, tamanho_bloque, inicio, fin):
    filas = len(mapa)
    cols = len(mapa[0])

    for i in range(filas):
        for j in range(cols):
            # Cada "tamaho_bloque" filas o columnas serán calles
            if i % tamanho_bloque == 0 or j % tamanho_bloque == 0:
                mapa[i][j] = 0 # calle
            else:
                mapa[i][j] = 1 # edificio

    # Asegurar inicio y fin libres    
    mapa[inicio[0]][inicio[1]] = 0
    mapa[fin[0]][fin[1]] = 0
              
def pedir_coordenada(mapa, mensaje):
    filas = len(mapa)
    cols = len(mapa[0])

    while True:
        try: 
            entrada = input(f"{mensaje} (fila,col): ")
            fila, col = map(int, entrada.split(","))

            if 0 <= fila < filas and 0 <= col < cols:
                if mapa[fila][col] == 0:
                    return (fila, col)
                else:
                    print("❌ Esa celda es un obstáculo, elige otra.")
            else:
                print("❌ Coordenadas fuera del mapa.")
        except ValueError:
            print("⚠️ Ingresa en el formato correcto: fila,col (ej: 2,3)")

def agregar_obstaculos_usuario(mapa, inicio, fin):
    while True:
        print("\n--- Menú de obstáculos ---")
        print("1: Agregar edificio (bloqueo permanente)")
        print("2: Agregar agua (obstáculo con ruta alternativa)")
        print("3: Agregar zona bloqueada temporalmente")
        print("0: Terminar")

        opcion = input("Elige una opción: ")

        if opcion == "0":
            break
        elif opcion in["1","2","3"]:
            try:
                entrada = input("Ingrese coordenadas del obstáculo (fila,col): ")
                fila,col = map(int, entrada.split(","))

                if (fila, col) == inicio or (fila, col) == fin:
                    print("❌ No puedes bloquear el inicio ni el destino.")
                elif 0 <= fila < len(mapa) and 0 <= col < len(mapa[0]):
                    mapa[fila][col] = int(opcion)
                    print(f"✅ Obstáculo agregado en ({fila}, {col})")

                    # Recalcular ruta automáticamente
                    ruta = bfs(mapa, inicio, fin)
                    if ruta:
                        print("Ruta recalculada ✅")
                        mostrar_mapa(mapa, ruta, inicio, fin)
                    else: 
                        print("No hay ruta posible 😥")
                        mostrar_mapa(mapa, None, inicio, fin)

                else: 
                    print("❌ Coordenadas fuera del mapa.")
            except ValueError:
                print("⚠️ Formato incorrecto, usa fila,col (ej: 2,3)")
        else:
            print("⚠️ Opción inválida")
            
            

if __name__ == "__main__":

    print("🚗🚗 Bienvenido a la calculadora de rutas 🚗🚗")
    filas = int(input("Ingrese un número para el números de filas: "))
    cols = int(input("Ingrese un número para el números de columnas: "))
    
    mapa = crear_mapa(filas,cols)    
    
    inicio = (0,0)
    fin = (filas-1,cols-1)

    generar_ciudad(mapa, tamanho_bloque=3, inicio=inicio, fin=fin)

    inicio = pedir_coordenada(mapa, "Ingrese coordenadas de INICIO")
    fin = pedir_coordenada(mapa, "Ingrese coordenadas de DESTINO")

    agregar_obstaculos_usuario(mapa, inicio, fin)
    
    ruta = bfs(mapa, inicio, fin)

    if ruta:
        print("Ruta encontrada ✅")
        mostrar_mapa(mapa, ruta, inicio, fin)
    else: 
        print("No hay ruta posible")