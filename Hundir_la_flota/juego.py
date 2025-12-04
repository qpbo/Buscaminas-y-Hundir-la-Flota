import random
import time

# --- Constantes del Juego ---
DIMENSION = 10
AGUA = "~"      # Símbolo para agua
BARCO = "#"     # Símbolo para barco intacto
TOCADO = "X"    # Símbolo para barco impactado
FALLADO = "O"   # Símbolo para disparo al agua

# Diccionarios y listas para la traducción de coordenadas (A->0, B->1, etc.)
LETRAS_A_NUMEROS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
NUMEROS_A_LETRAS = "ABCDEFGHIJ" 


# -----------------------------------------------------------------
# --- 1. LÓGICA BÁSICA DEL TABLERO ---
# -----------------------------------------------------------------

def crear_tablero(dimension):
    """Crea una matriz de NxN llena de agua."""
    return [[AGUA for _ in range(dimension)] for _ in range(dimension)]

def imprimir_tablero(tablero):
    """Muestra el tablero con coordenadas en la consola."""
    # Números de columna (0 a 9)
    print("\n   " + " ".join([str(i) for i in range(DIMENSION)])) 
    print("  +" + "—" * (DIMENSION * 2)) # Línea separadora
    
    for i, fila in enumerate(tablero):
        # Letra de fila + Contenido de la fila
        print(f"{NUMEROS_A_LETRAS[i]} | {' '.join(fila)}") 

def validar_coordenadas(fila, col, longitud, orientacion, tablero):
    """Comprueba si el barco cabe y no choca con otro."""
    if orientacion == 'H': # Horizontal
        if col + longitud > DIMENSION: return False
        for i in range(longitud):
            if tablero[fila][col + i] != AGUA: return False
    else: # Vertical
        if fila + longitud > DIMENSION: return False
        for i in range(longitud):
            if tablero[fila + i][col] != AGUA: return False
            
    return True

def colocar_barcos_aleatorios(tablero, flota):
    """Coloca una lista de barcos (longitudes) aleatoriamente."""
    for longitud in flota:
        colocado = False
        while not colocado:
            # Elegir posición y orientación al azar
            fila = random.randint(0, DIMENSION - 1)
            col = random.randint(0, DIMENSION - 1)
            orientacion = random.choice(['H', 'V'])
            
            # Si es válido, colocamos el barco
            if validar_coordenadas(fila, col, longitud, orientacion, tablero):
                if orientacion == 'H':
                    for i in range(longitud):
                        tablero[fila][col + i] = BARCO
                else:
                    for i in range(longitud):
                        tablero[fila + i][col] = BARCO
                colocado = True
    return tablero


# -----------------------------------------------------------------
# --- 2. LÓGICA DE COORDENADAS E INTERACCIÓN ---
# -----------------------------------------------------------------

def traducir_coordenada(coordenada):
    """
    Traduce una coordenada tipo "A5" a índices de matriz (0, 5).
    """
    if len(coordenada) < 2 or len(coordenada) > 3:
        return None, None
    
    letra_fila = coordenada[0].upper()
    try:
        num_columna = int(coordenada[1:])
    except ValueError:
        return None, None 

    if letra_fila in LETRAS_A_NUMEROS:
        fila = LETRAS_A_NUMEROS[letra_fila]
    else:
        return None, None

    columna = num_columna 
    
    if 0 <= fila < DIMENSION and 0 <= columna < DIMENSION:
        return fila, columna
    else:
        return None, None


def pedir_disparo(tablero_enemigo_disparos):
    """
    Pide y valida la coordenada de disparo.
    """
    while True:
        coordenada_str = input("🎯 ¿Dónde disparas? (Ej: A5, J0): ").strip()
        
        fila, columna = traducir_coordenada(coordenada_str)
        
        if fila is None:
            print("❌ Formato de coordenada inválido. Usa una letra (A-J) y un número (0-9).")
            continue
        
        if tablero_enemigo_disparos[fila][columna] != AGUA:
            print("❌ Ya has disparado a esa casilla. Elige otra.")
            continue
            
        return fila, columna

def realizar_ataque(tablero_pc_barcos, tablero_pc_disparos):
    """
    Gestiona la secuencia de ataque del jugador: pide coordenada, comprueba impacto
    y actualiza ambos tableros.
    """
    print("\n--- INICIANDO ATAQUE ---")
    print("Tu mapa de disparos (IA):")
    imprimir_tablero(tablero_pc_disparos) # Muestra solo los hits/misses
    
    f_disp, c_disp = pedir_disparo(tablero_pc_disparos)
    
    # Comprobar resultado del disparo en el tablero oculto
    if tablero_pc_barcos[f_disp][c_disp] == BARCO:
        print("\n🎉 ¡TOCADO! Excelente puntería.")
        tablero_pc_disparos[f_disp][c_disp] = TOCADO
        tablero_pc_barcos[f_disp][c_disp] = TOCADO # Marcar en el tablero real
        # Aquí se podría añadir la lógica de 'Hundido'
    else:
        print("\n💧 ¡AGUA! Has fallado el tiro.")
        tablero_pc_disparos[f_disp][c_disp] = FALLADO
        
    time.sleep(1.5)


# -----------------------------------------------------------------
# --- 3. FUNCIÓN CONTROLADORA DEL JUEGO CON SUBMENÚ ---
# -----------------------------------------------------------------

def iniciar_juego():
    """Configura el juego y gestiona el bucle de la partida con el submenú."""
    print("\n>> Generando el campo de batalla de la IA...")
    time.sleep(1)
    
    # 1. Inicialización de los tableros
    tablero_pc_barcos = crear_tablero(DIMENSION)     # Dónde están los barcos (oculto)
    tablero_pc_disparos = crear_tablero(DIMENSION)   # Lo que el jugador ve (hits/misses)
    
    # 2. Colocar la flota de la IA
    flota_estandar = [4, 3, 3, 2, 2]
    colocar_barcos_aleatorios(tablero_pc_barcos, flota_estandar)
    
    print("\n--- ¡FLOTA ENEMIGA LISTA! COMIENZA LA BATALLA ---")
    
    # --- Bucle Principal de Partida con Submenú ---
    while True:
        # Aquí puedes añadir la lógica para limpiar la pantalla si quieres
        # limpiar_pantalla() 
        
        # 1. Mostrar el submenú de partida
        print("\n" + "="*25)
        print("  MENÚ DE PARTIDA ACTUAL")
        print("="*25)
        print("  [1] Atacar")
        print("  [2] Salir al menú principal")
        
        eleccion = input("\n> Selecciona una opción: ").strip()

        if eleccion == '1':
            realizar_ataque(tablero_pc_barcos, tablero_pc_disparos)
            # Faltaría añadir el turno de la IA y la comprobación de victoria aquí
            
        elif eleccion == '2':
            print("\nVolviendo al menú principal. La partida no está guardada.")
            time.sleep(1)
            break # Sale del bucle de partida y vuelve al Menu_principal.py
        
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")
            time.sleep(1)