# Creación del tablero vacío

tablero = []
for i in range(10):
    fila = ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]
    tablero.append(fila)

# Definimos la flota y las letras
barcos_a_colocar = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
letras = "ABCDEFGHIJ"

# Bucles para colocar cada uno de los barcos
for longitud in barcos_a_colocar:
    colocado = False
    
    while colocado == False:
        # Mostramos el tablero por pantalla
        print("\n    1 2 3 4 5 6 7 8 9 10")
        print("   ---------------------")
        indice_letra = 0
        for fila_print in tablero:
            print(letras[indice_letra], "|", end=" ")
            for celda in fila_print:
                print(celda, end=" ")
            print()
            indice_letra = indice_letra + 1

        print(f"\nColocando barco de tamaño: {longitud}")
        
        # Pedimos los datos al usuario por pantalla
        letra_input = input("Introduce la letra de la fila (A-J): ").upper()
        if letra_input not in letras or letra_input == "":
            print("¡Letra no válida!")
            continue
            
        columna = int(input("Introduce el número de la columna (1-10): ")) - 1
        orientacion = input("Orientación: Horizontal (H) o Vertical (V): ").upper()

        # Convertimos la letra en índice (A=0, B=1, etc.)
        fila_index = 0
        for i in range(len(letras)):
            if letras[i] == letra_input:
                fila_index = i
        error = False
        
        # Compobamos si el barco se sale del tablero
        if orientacion == "H":
            if columna < 0 or columna + longitud > 10:
                error = True
                print("¡Error! El barco se sale del tablero horizontalmente.")
        elif orientacion == "V":
            if fila_index < 0 or fila_index + longitud > 10:
                error = True
                print("¡Error! El barco se sale del tablero verticalmente.")
        else:
            error = True
            print("¡Error! Orientación no válida.")

        # Comprobamos si hay barcos cerca o se posiciona encima
        if error == False:
            # Revisamos cada celda que ocuparía el barco
            for n in range(longitud):
                if orientacion == "H":
                    f_actual = fila_index
                    c_actual = columna + n
                else:
                    f_actual = fila_index + n
                    c_actual = columna
                
                # Revisamos el bloque 3x3 alrededor de esa celda
                for df in range(-1, 2):
                    for dc in range(-1, 2):
                        f_revisar = f_actual + df
                        c_revisar = c_actual + dc
                        
                        # Comprobamos si la casilla adyacente está dentro de la matriz
                        if 0 <= f_revisar < 10 and 0 <= c_revisar < 10:
                            if tablero[f_revisar][c_revisar] == "1":
                                error = True

            if error == True:
                print("¡Error! No puedes colocarlo aquí (hay un barco cerca o encima).")

        # Estructura para colocar el barco en caso de que no haya errores
        if error == False:
            for n in range(longitud):
                if orientacion == "H":
                    tablero[fila_index][columna + n] = "1"
                else:
                    tablero[fila_index + n][columna] = "1"
            colocado = True
            print("¡Barco colocado con éxito!")

print("\n¡TODOS LOS BARCOS HAN SIDO COLOCADOS!")