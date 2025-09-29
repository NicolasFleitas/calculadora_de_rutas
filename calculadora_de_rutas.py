# Resolución de rutas más corta (menor peso) utilizando el algoritmo de Dijkstra.

from enum import Enum
import heapq # Importamos heapq para la cola de prioridad de Dijkstra

class TipoCelda(Enum):
    CAMINO = 0
    EDIFICIO = 1
    AGUA = 2
    BLOQUEO = 3

COSTOS = {
    TipoCelda.CAMINO: 1,
    TipoCelda.AGUA: 5,
    # Edificio y bloqueo no hace falta definir acá, porque su costo es infinito
}

SIMBOLOS_MAPA = {
    TipoCelda.CAMINO: "⬛",
    TipoCelda.EDIFICIO: "🏢",
    TipoCelda.AGUA: "💧",
    TipoCelda.BLOQUEO: "🚧",
}

def crear_mapa(filas, cols):
    return [[0 for _ in range(cols)] for _ in range(filas)]

# Funcion para visualizar datos en consola
def mostrar_mapa(mapa, ruta=None, inicio=None, fin=None):
    simbolos = {0: "⬛", 1: "🏢", 2: "💧", 3: "🚧"}
    ruta_set = set(ruta) if ruta else set()

    for i, fila in enumerate(mapa):
        linea = ""
        for j, celda in enumerate(fila):
            pos = (i, j)

            if pos == inicio:
                linea += "🏁 "
            elif pos == fin:
                linea += "📍 "
            elif pos in ruta_set:
                linea += "🚗 "
            else:
                linea += simbolos[celda] + " "
        print(linea)
    print()

# Devuelve el costo de moverse a una celda según su tipo
def get_costo(celda_valor):
    # Devuelve el costo de moverse a una celda según su tipo."""
    # Busca el valor en el diccionario de costos. Si no encuentra,
    # significa que es un obstáculo infranqueable (costo infinito).
   return COSTOS.get(TipoCelda(celda_valor), float('inf'))

def dijkstra(mapa, inicio, fin):
    filas, cols = len(mapa), len(mapa[0])

    # Verifica si el inicio o el fin están en un obstáculo infranqueable
    if get_costo(mapa[inicio[0]][inicio[1]]) == float('inf') or get_costo(mapa[fin[0]][fin[1]]) == float('inf'):
        return None
    
    distancias = {} 

    for f in range(filas):
        for c in range(cols):
            distancias[(f,c)] = float('inf')
    
    distancias[inicio] = 0
    padres = {inicio: None}

    # Cola de prioridad: (costo, posición)
    colap = [(0, inicio)]

    while colap:
        costo_actual, actual = heapq.heappop(colap) 

        if actual == fin:
            # Reconstruir ruta
            ruta = []
            while actual is not None:
                ruta.append(actual)
                actual = padres.get(actual)
            
            return ruta[::-1]
        
        fila, col = actual
        movimientos = [(-1,0), (1,0), (0,-1), (0,1)]
        # OJO: Nombres de variables: fila-col
        for df, dc in movimientos:
            nf, nc = fila + df, col + dc
            vecino = (nf, nc)

            if 0 <= nf < filas and 0 <= nc < cols:
                costo_movimiento = get_costo(mapa[nf][nc])
                if costo_movimiento == float('inf'):
                    continue # No se puede mover a un obstáculo
                
                nuevo_costo = costo_actual + costo_movimiento
                if nuevo_costo < distancias[vecino]:
                    distancias[vecino] = nuevo_costo
                    padres[vecino] = actual
                    heapq.heappush(colap, (nuevo_costo, vecino))
    
    return None # No se encontró ruta

def generar_ciudad(mapa, tamanho_bloque):
    filas = len(mapa)
    cols = len(mapa[0])

    for i in range(filas):
        for j in range(cols):
            # Cada "tamanho_bloque" filas o columnas serán calles
            if i % tamanho_bloque == 0 or j % tamanho_bloque == 0:
                mapa[i][j] = TipoCelda.CAMINO.value
            else:
                mapa[i][j] = TipoCelda.EDIFICIO.value
              
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
        print("1: Agregar edificio 🏢")
        print("2: Agregar agua 💧")
        print("3: Agregar zona bloqueada 🚧")
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
                    ruta = dijkstra(mapa, inicio, fin)
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
            
def main():
    print("🚗🚗 Bienvenido a la calculadora de rutas 🚗🚗")
    filas = int(input("Ingrese un número para el números de filas: "))
    cols = int(input("Ingrese un número para el números de columnas: "))
    
    mapa = crear_mapa(filas,cols)    
    generar_ciudad(mapa, tamanho_bloque=3)
    mostrar_mapa(mapa)
    
    inicio = pedir_coordenada(mapa, "Ingrese coordenadas de INICIO 🏁")
    fin = pedir_coordenada(mapa, "Ingrese coordenadas de DESTINO 📍")

    ruta = dijkstra(mapa, inicio, fin)

    if ruta:
        print("Ruta encontrada ✅")
        mostrar_mapa(mapa, ruta, inicio, fin)
    else: 
        print("No hay ruta posible")
        
    agregar_obstaculos_usuario(mapa, inicio, fin)    

if __name__ == "__main__":
    main()