# MVP: 
# Primera versión con datos estáticos y simulación de obstáculos fijos (con el mismo valor)
# Resolución utilizando bfs.

# 0 -> CAMINO LIBRE
# 1 -> edificio (no se puede pasar)
# 2 -> agua (obstáculo, pero podría tener un costo mayor en lugar de ser bloqueado)
# 3 -> zona bloqueada temporalmente

from collections import deque

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
        actual = cola.popleft()

        if actual == fin:
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
               

if __name__ == "__main__":

    print("Bienvenido a la calculadora de rutas")
    filas = int(input("Ingrese un número para el números de filas: "))
    cols = int(input("Ingrese un número para el números de columnas: "))
    
    mapa = crear_mapa(filas,cols)

    # Ejemplo de obstaculos fijos
    mapa[1][2] = 1
    mapa[2][2] = 1
    mapa[3][2] = 1
    mapa[4][3] = 1
  
    # TODO: Pedir al usuario coordenadas de inicio y fin.
    # Validar que:
    # * Esten dentro de los limites de la matriz
    # * Que sea un camino transitable, libre de obstáculos.

    inicio = (0,0)
    fin = (4,4)

    ruta = bfs(mapa, inicio, fin)

    if ruta:
        print("Ruta encontrada")
        mostrar_mapa(mapa, ruta, inicio, fin)
    else: 
        print("No hay ruta posible")