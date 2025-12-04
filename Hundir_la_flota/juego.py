import random
import time
import json # <-- Nuevo: Necesario para guardar y cargar la partida

# --- Constantes del Juego ---
DIMENSION = 10
AGUA = "~"      
BARCO = "#"     
TOCADO = "X"    
FALLADO = "O"   

LETRAS_A_NUMEROS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
NUMEROS_A_LETRAS = "ABCDEFGHIJ" 


# -----------------------------------------------------------------
# --- 1. LÓGICA BÁSICA DEL TABLERO (Sin cambios) ---
# -----------------------------------------------------------------

def crear_tablero(dimension):
    """Crea una matriz de NxN llena de agua."""
    return [[AGUA for _ in range(dimension)] for _ in range(dimension)]

def imprimir_tablero(tablero):
    """Muestra el tablero con coordenadas en la consola."""
    print("\n   " + " ".join([str(i) for i in range(DIMENSION)])) 
    print("  +" + "—" * (DIMENSION * 2)) 
    
    for i, fila in enumerate(tablero):
        print(f"{NUMEROS_A_LETRAS[i]} | {' '.join(fila)}") 

def validar_coordenadas(fila, col, longitud, orientacion, tablero):
    # ... (código existente para validar coordenadas)
    if orientacion == 'H':
        if col + longitud > DIMENSION: return False
        for i in range(longitud):
            if tablero[fila][col + i] != AGUA: return False
    else:
        if fila + longitud > DIMENSION: return False
        for i in range(longitud):
            if tablero[fila + i][col] != AGUA: return False
    return True

def colocar_barcos_aleatorios(tablero, flota):
    # ... (código existente para colocar barcos)
    for longitud in flota:
        colocado = False
        while not colocado:
            fila = random.randint(0, DIMENSION - 1)
            col = random.randint(0, DIMENSION - 1)
            orientacion = random.choice(['H', 'V'])
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
# --- 2. LÓGICA DE COORDENADAS E INTERACCIÓN (Sin cambios) ---
# -----------------------------------------------------------------

def traducir_coordenada(coordenada):
    # ... (código existente para traducir coordenadas)
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
    # ... (código existente para pedir y validar disparo)
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
    imprimir_tablero(tablero_pc_disparos)
    
    f_disp, c_disp = pedir_disparo(tablero_pc_disparos)
    
    if tablero_pc_barcos[f_disp][c_disp] == BARCO:
        print("\n🎉 ¡TOCADO! Excelente puntería.")
        tablero_pc_disparos[f_disp][c_disp] = TOCADO
        tablero_pc_barcos[f_disp][c_disp] = TOCADO
    else:
        print("\n💧 ¡AGUA! Has fallado el tiro.")
        tablero_pc_disparos[f_disp][c_disp] = FALLADO
        
    time.sleep(1.5)


# -----------------------------------------------------------------
# --- 3. FUNCIONALIDAD DE GUARDADO (NUEVO) ---
# -----------------------------------------------------------------

def guardar_partida(tablero_pc_barcos, tablero_pc_disparos, nombre_archivo="partida_guardada.json"):
    """Guarda el estado actual de la partida en un archivo JSON."""
    
    # Empaquetamos el estado del juego en un diccionario
    estado_partida = {
        "tablero_pc_barcos": tablero_pc_barcos,
        "tablero_pc_disparos": tablero_pc_disparos,
        "turno_actual": 1 # (Futuro: se puede guardar el turno actual o quien tiene el turno)
    }
    
    try:
        # Abrimos el archivo en modo escritura ('w') y usamos json.dump
        with open(nombre_archivo, 'w') as f:
            json.dump(estado_partida, f, indent=4) # indent=4 para que sea legible
        print(f"\n💾 Partida guardada con éxito en '{nombre_archivo}'.")
    except Exception as e:
        print(f"\n❌ Error al guardar la partida: {e}")


# -----------------------------------------------------------------
# --- 4. FUNCIÓN CONTROLADORA DEL JUEGO CON SUBMENÚ (ACTUALIZADO) ---
# -----------------------------------------------------------------

def iniciar_juego():
    """Configura el juego y gestiona el bucle de la partida con el submenú."""
    print("\n>> Generando el campo de batalla de la IA...")
    time.sleep(1)
    
    tablero_pc_barcos = crear_tablero(DIMENSION)     
    tablero_pc_disparos = crear_tablero(DIMENSION)   
    flota_estandar = [4, 3, 3, 2, 2]
    colocar_barcos_aleatorios(tablero_pc_barcos, flota_estandar)
    
    print("\n--- ¡FLOTA ENEMIGA LISTA! COMIENZA LA BATALLA ---")
    
    # --- Bucle Principal de Partida con Submenú ---
    while True:
        # 1. Mostrar el submenú de partida (con la nueva opción)
        print("\n" + "="*25)
        print("  MENÚ DE PARTIDA ACTUAL")
        print("="*25)
        print("  [1] Atacar")
        print("  [2] Ver mapa") # <-- NUEVA OPCIÓN
        print("  [3] Salir al menú principal (Guardar)") # <-- OPCIÓN ACTUALIZADA
        
        eleccion = input("\n> Selecciona una opción: ").strip()

        if eleccion == '1':
            realizar_ataque(tablero_pc_barcos, tablero_pc_disparos)
            
        elif eleccion == '2': # <-- IMPLEMENTACIÓN DE 'VER MAPA'
            print("\n--- TU MAPA DE DISPAROS DEL ENEMIGO ---")
            imprimir_tablero(tablero_pc_disparos)
            input("\nPresiona ENTER para volver al menú de partida...")
            
        elif eleccion == '3': 
            guardar_partida(tablero_pc_barcos, tablero_pc_disparos) # <-- GUARDAR PARTIDA
            break 
        
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")
            time.sleep(1)