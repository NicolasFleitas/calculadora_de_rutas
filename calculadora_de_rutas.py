from enum import Enum
import heapq

class TipoCelda(Enum):
    CAMINO = 0
    EDIFICIO = 1
    AGUA = 2
    BLOQUEO = 3

# Diccionario de COSTOS
COSTOS = {
    TipoCelda.CAMINO.value: 1,
    TipoCelda.AGUA.value: 3,    
}

# Diccionario de SIMBOLOS - EMOJIS 
SIMBOLOS_MAPA = {
    TipoCelda.CAMINO.value: "⬛",
    TipoCelda.EDIFICIO.value: "🏢",
    TipoCelda.AGUA.value: "💧",
    TipoCelda.BLOQUEO.value: "🚧",
}

# Creo una matriz de tamaño (filas x cols) llena de ceros
def crear_mapa(filas, cols):
    return [[0 for _ in range(cols)] for _ in range(filas)]       

def generar_ciudad(mapa, tamanho_bloque):
    filas = len(mapa)
    cols = len(mapa[0])

    for i in range(filas):
        for j in range(cols):
            # Cada "tamanho_bloque" (fila,columna) serán CAMINO
            if i % tamanho_bloque == 0 or j % tamanho_bloque == 0:
                mapa[i][j] = TipoCelda.CAMINO.value
            else:
                mapa[i][j] = TipoCelda.EDIFICIO.value
 
def mostrar_mapa(mapa, ruta=None, inicio=None, fin=None):
    # Convierte la lista 'ruta' a un set. Si está vacía o es None
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
                linea += SIMBOLOS_MAPA[celda] + " "
        print(linea)
    print()

def pedir_coordenada(mapa, mensaje):
    filas = len(mapa)
    cols = len(mapa[0])

    while True:
        try: 
            entrada = input(f"{mensaje} (fila,col): ")
            fila, col = map(int, entrada.split(","))

            if 0 <= fila < filas and 0 <= col < cols:
                if mapa[fila][col] == 0:  # Si la celda es CAMINO
                    return (fila, col)
                else:
                    print("❌ Esa celda es un obstáculo, elige otra.")
            else:
                print("❌ Coordenadas fuera del mapa.")

        except ValueError:
            print("⚠️ Ingresa en el formato correcto: fila,col (ej: 2,3)")

def dijkstra(mapa, inicio, fin):
   
    filas, cols = len(mapa), len(mapa[0])
    distancias = { (f,c): float('inf') for f in range(filas) for c in range(cols) }      
    distancias[inicio] = 0 
    padres = {inicio: None} # Indicamos que el nodo de inicio no tiene predecesor

    
    cola_prioridad = [(0, inicio)] # Cola de prioridad: Costo, posición

    while cola_prioridad: # Mientras la cola de prioridad no este vacía, iteramos.

        costo_actual, nodo_actual = heapq.heappop(cola_prioridad) # obtenemos el costo y nodo_actual de la cola

        if nodo_actual == fin: # Cuando lleguemos al nodo destino empezamos a reconstruir la ruta
            ruta = []             
            while nodo_actual is not None: # Mientras que el nodo_actual no sea None.
                ruta.append(nodo_actual) # Agregamos a la lista de rutas el nodo_actual
                nodo_actual = padres.get(nodo_actual) # obtenemos el padre del nodo_actual                           
            return ruta[::-1] # Retornar ruta de forma inversa
        
        f, c = nodo_actual # obtengo la coordenada en f(fila) y c(columna) del nodo actual

        movimientos = [(-1,0), (1,0), (0,-1), (0,1)] # Lista de movimientos posibles Up,Down,Left,Right
    
        for df, dc in movimientos:
            nf, nc = f + df, c + dc # calculo el valor de nf(nueva fila) y nc(nueva columna) 
            vecino = (nf, nc) # Inicializo una tupla con nombre vecino, con los nuevos valores de las coordenadas nf y nc

            if 0 <= nf < filas and 0 <= nc < cols: # valido que la nueva posicion no se salga de los limites de la matriz
                costo_movimiento = get_costo(mapa[nf][nc]) # obtenemos el valor de esa celda. Ej. Camino = 0 Agua = 2
                if costo_movimiento == float('inf'): # Si el costo es infinito, es un obstáculo
                    continue # No se puede mover a un obstáculo
                
                # Calcula el costo total para llegar al vecino a través del camino actual.
                costo_total = costo_actual + costo_movimiento 
                # Si el costo_total es menor al VALOR correspondiente del diccionario distancias con clave del VECINO.
                if costo_total < distancias[vecino]: 
                    costo_total = costo_actual + costo_movimiento # Acumulamos el costo
                    distancias[vecino] = costo_total 
                    padres[vecino] = nodo_actual 
                    heapq.heappush(cola_prioridad, (costo_total, vecino))     
    return None # No se encontró ruta

# Devuelve el costo de moverse a una celda según su tipo
# Si la clave (el valor entero) no existe, devuelve float('inf')
def get_costo(celda_valor):
   return COSTOS.get(celda_valor, float('inf')) # Si no existe, retorna infinito

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

                    # Recalcular ruta
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
                print("⚠️ Formato incorrecto, usa fila,col (ej: 3,4)")
        else:
            print("⚠️ Opción inválida")       

def validar_entrada_entero(mensaje):
    while True:
        entrada = input(mensaje)
        try:           
            numero_entero = int(entrada)           
            return numero_entero
        except ValueError:           
            print("❌ Entrada no válida. Por favor, ingrese un número entero.")

def main():
    print("🚗🚗 Bienvenido a la calculadora de rutas 🚗🚗")
    filas = validar_entrada_entero("Ingrese el alto del mapa: ")
    cols = validar_entrada_entero("Ingrese el ancho del mapa: ")
    
    mapa = crear_mapa(filas,cols)    
    generar_ciudad(mapa, tamanho_bloque=3)
    mostrar_mapa(mapa)
    
    inicio = pedir_coordenada(mapa, "Ingrese coordenadas de INICIO 🏁")
    while True:
        fin = pedir_coordenada(mapa, "Ingrese coordenadas de DESTINO 📍")
        if fin == inicio:
            print("El fin no puede ser igual al inicio")
        else:
            break

    ruta = dijkstra(mapa, inicio, fin)

    if ruta:
        print("Ruta encontrada ✅")
        mostrar_mapa(mapa, ruta, inicio, fin)
    else: 
        print("No hay ruta posible")
        
    agregar_obstaculos_usuario(mapa, inicio, fin)    



if __name__ == "__main__":
    main()
    