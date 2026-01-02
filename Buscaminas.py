import random

#Creaccion del tablero

def tablero_logico(filas, columnas, num_minas):
    tablero = []
    #Crear tablero vacio
    for _ in range(filas):
        tablero.append([0] * columnas)
    
    #Colocacion de minas
    minas_plantadas = 0
    while minas_plantadas < num_minas:
        f = random.randint(0, filas -1)
        c = random.randint(0, columnas -1)

        #si no hay mina se planta (representado con el -1)
        if tablero[f][c] != -1:
            tablero[f][c] = -1
            minas_plantadas += 1

            #Recorremos el cuadrado de 3x3 alrededor de la mina
            for i in range(max(0, f-1), min(filas, f+2)):
                for j in range(max(0, c-1), min(columnas, c+2)):
                    if tablero[i][j] != -1:
                        tablero[i][j] += 1
    return tablero


