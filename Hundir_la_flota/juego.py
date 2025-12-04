import random
import time
import json # Necesario para guardar y cargar la partida en formato JSON

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
## 1. Lógica Básica del Tablero y Barcos
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
    """Comprueba si el barco cabe y no choca con otro."""
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
    """Coloca una lista de barcos (longitudes) aleatoriamente."""
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
## 2. Lógica de Coordenadas y Ataque
# -----------------------------------------------------------------

def traducir_coordenada(coordenada):
    """Traduce una coordenada tipo 'A5' a índices de matriz (0, 5)."""
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
    """Pide y valida la coordenada de disparo."""
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
    """Gestiona la secuencia de ataque del jugador."""
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
## 3. Funcionalidad de Guardado y Carga
# -----------------------------------------------------------------

def guardar_partida(tablero_pc_barcos, tablero_pc_disparos, nombre_archivo="partida_guardada.json"):
    """Guarda el estado actual de la partida en un archivo JSON."""
    
    estado_partida = {
        "tablero_pc_barcos": tablero_pc_barcos,
        "tablero_pc_disparos": tablero_pc_disparos,
    }
    
    try:
        with open(nombre_archivo, 'w') as f:
            json.dump(estado_partida, f, indent=4)
        print(f"\n💾 Partida guardada con éxito en '{nombre_archivo}'.")
    except Exception as e:
        print(f"\n❌ Error al guardar la partida: {e}")

def cargar_partida(nombre_archivo="partida_guardada.json"):
    """Carga el estado de la partida desde un archivo JSON."""
    try:
        with open(nombre_archivo, 'r') as f:
            estado_partida = json.load(f)
        
        print(f"\n✅ Partida cargada desde '{nombre_archivo}'.")
        
        return estado_partida["tablero_pc_barcos"], estado_partida["tablero_pc_disparos"]
        
    except FileNotFoundError:
        return None, None # Indicamos que no hay archivo guardado
    except Exception as e:
        print(f"\n❌ Error al cargar la partida. El archivo podría estar corrupto: {e}")
        return None, None


# -----------------------------------------------------------------
## 4. Función Controladora del Juego (con Submenú)
# -----------------------------------------------------------------

def iniciar_juego(tablero_pc_barcos=None, tablero_pc_disparos=None):
    """
    Configura y gestiona el bucle de la partida. 
    Inicia desde cero si no se pasan tableros (Nueva Partida) o continúa si se pasan.
    """
    
    if tablero_pc_barcos is None:
        # Lógica de "Nueva Partida"
        print("\n>> Generando el campo de batalla de la IA...")
        time.sleep(1)
        
        tablero_pc_barcos = crear_tablero(DIMENSION)     
        tablero_pc_disparos = crear_tablero(DIMENSION)   
        flota_estandar = [4, 3, 3, 2, 2]
        colocar_barcos_aleatorios(tablero_pc_barcos, flota_estandar)
        
        print("\n--- ¡FLOTA ENEMIGA LISTA! COMIENZA LA BATALLA ---")
    
    else:
        # Lógica de "Continuar Partida"
        print("\n--- Partida cargada con éxito. Continuamos la batalla. ---")
        
    # --- Bucle Principal de Partida con Submenú ---
    while True:
        # 1. Mostrar el submenú de partida
        print("\n" + "="*25)
        print("  MENÚ DE PARTIDA ACTUAL")
        print("="*25)
        print("  [1] Atacar")
        print("  [2] Ver mapa") 
        print("  [3] Salir al menú principal (Guardar)") 
        
        eleccion = input("\n> Selecciona una opción: ").strip()

        if eleccion == '1':
            realizar_ataque(tablero_pc_barcos, tablero_pc_disparos)
            
        elif eleccion == '2': 
            print("\n--- TU MAPA DE DISPAROS DEL ENEMIGO ---")
            imprimir_tablero(tablero_pc_disparos)
            input("\nPresiona ENTER para volver al menú de partida...")
            
        elif eleccion == '3': 
            guardar_partida(tablero_pc_barcos, tablero_pc_disparos)
            break 
        
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")
            time.sleep(1)