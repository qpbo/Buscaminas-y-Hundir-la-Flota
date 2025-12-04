import random
import time
import json 

# --- Constantes del Juego ---
DIMENSION = 10
AGUA = "~"      # Símbolo para agua
BARCO = "#"     # Símbolo para barco intacto
TOCADO = "X"    # Símbolo para barco impactado
FALLADO = "O"   # Símbolo para disparo al agua

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
## 2. Lógica de Coordenadas y Ataque del Jugador
# -----------------------------------------------------------------

def traducir_coordenada(coordenada):
    """Traduce una coordenada tipo 'A5' a índices de matriz (0, 5)."""
    if len(coordenada) < 2 or len(coordenada) > 3: return None, None
    letra_fila = coordenada[0].upper()
    try:
        num_columna = int(coordenada[1:])
    except ValueError: return None, None 

    if letra_fila in LETRAS_A_NUMEROS: fila = LETRAS_A_NUMEROS[letra_fila]
    else: return None, None

    columna = num_columna 
    
    if 0 <= fila < DIMENSION and 0 <= columna < DIMENSION:
        return fila, columna
    else: return None, None

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
    """Gestiona la secuencia de ataque del jugador y devuelve si hubo impacto."""
    print("\n--- INICIANDO ATAQUE DEL JUGADOR ---")
    
    f_disp, c_disp = pedir_disparo(tablero_pc_disparos)
    
    impacto = False
    if tablero_pc_barcos[f_disp][c_disp] == BARCO:
        print("\n🎉 ¡TOCADO! Excelente puntería.")
        tablero_pc_disparos[f_disp][c_disp] = TOCADO
        tablero_pc_barcos[f_disp][c_disp] = TOCADO
        impacto = True
    else:
        print("\n💧 ¡AGUA! Has fallado el tiro.")
        tablero_pc_disparos[f_disp][c_disp] = FALLADO
        
    time.sleep(1.5)
    return impacto 


# -----------------------------------------------------------------
## 3. Lógica de la IA
# -----------------------------------------------------------------

def generar_disparo_ia(tablero_jugador_barcos):
    """Genera coordenadas aleatorias, asegurando que no se dispare dos veces."""
    # La IA solo dispara a casillas que no sean TOCADO ('X') o FALLADO ('O')
    while True:
        fila = random.randint(0, DIMENSION - 1)
        col = random.randint(0, DIMENSION - 1)
        
        if tablero_jugador_barcos[fila][col] not in [TOCADO, FALLADO]:
            return fila, col

def realizar_ataque_ia(tablero_jugador_barcos, tablero_jugador_disparos):
    """Lógica de un solo disparo de la IA y devuelve si hubo impacto."""
    
    # La IA dispara contra el tablero del jugador, no contra su propio tablero de disparos.
    f_disp, c_disp = generar_disparo_ia(tablero_jugador_barcos)
    coordenada_str = f"{NUMEROS_A_LETRAS[f_disp]}{c_disp}"
    
    print(f"\nLa IA dispara a la coordenada: {coordenada_str}...")
    time.sleep(1)

    impacto = False
    if tablero_jugador_barcos[f_disp][c_disp] == BARCO:
        print("💥 ¡HAN DADO EN TU FLOTA! Tocado.")
        # La IA marca el impacto en tu tablero de barcos
        tablero_jugador_barcos[f_disp][c_disp] = TOCADO 
        impacto = True
    else:
        print("💦 La IA ha disparado al agua. Falló.")
        # La IA marca el fallo en tu tablero de barcos
        tablero_jugador_barcos[f_disp][c_disp] = FALLADO 
    
    time.sleep(1.5)
    return impacto

def turno_ia(tablero_jugador_barcos, tablero_jugador_disparos, dificultad):
    """Controla el número de disparos de la IA según la dificultad."""
    print("\n--- TURNO DE LA IA ---")
    
    # Primer ataque (siempre se ejecuta)
    impacto_anterior = realizar_ataque_ia(tablero_jugador_barcos, tablero_jugador_disparos)
    
    # Manejar ataques adicionales
    if dificultad == "Medio" and impacto_anterior:
        print("\n--- ¡IMPACTO! La IA ataca de nuevo (Nivel Medio) ---")
        realizar_ataque_ia(tablero_jugador_barcos, tablero_jugador_disparos)
        
    elif dificultad == "Dificil":
        print("\n--- La IA ataca de nuevo (Nivel Difícil) ---")
        realizar_ataque_ia(tablero_jugador_barcos, tablero_jugador_disparos)


# -----------------------------------------------------------------
## 4. Funcionalidad de Guardado y Carga
# -----------------------------------------------------------------

def guardar_partida(tablero_pc_barcos, tablero_pc_disparos, tablero_jugador_barcos, tablero_jugador_disparos, nombre_archivo="partida_guardada.json"):
    """Guarda el estado completo de la partida (4 tableros)."""
    
    estado_partida = {
        "tablero_pc_barcos": tablero_pc_barcos,
        "tablero_pc_disparos": tablero_pc_disparos,
        "tablero_jugador_barcos": tablero_jugador_barcos,
        "tablero_jugador_disparos": tablero_jugador_disparos,
    }
    
    try:
        with open(nombre_archivo, 'w') as f:
            json.dump(estado_partida, f, indent=4)
        print(f"\n💾 Partida guardada con éxito en '{nombre_archivo}'.")
    except Exception as e:
        print(f"\n❌ Error al guardar la partida: {e}")

def cargar_partida(nombre_archivo="partida_guardada.json"):
    """Carga el estado completo de la partida desde un archivo JSON (4 tableros)."""
    try:
        with open(nombre_archivo, 'r') as f:
            estado_partida = json.load(f)
        
        print(f"\n✅ Partida cargada desde '{nombre_archivo}'.")
        
        # Devolvemos los 4 tableros
        return (estado_partida["tablero_pc_barcos"], 
                estado_partida["tablero_pc_disparos"],
                estado_partida["tablero_jugador_barcos"],
                estado_partida["tablero_jugador_disparos"])
        
    except FileNotFoundError:
        return None, None, None, None
    except Exception as e:
        print(f"\n❌ Error al cargar la partida. El archivo podría estar corrupto: {e}")
        return None, None, None, None


# -----------------------------------------------------------------
## 5. Función Controladora del Juego (CON MENÚ DE PARTIDA CORREGIDO)
# -----------------------------------------------------------------

def iniciar_juego(tablero_pc_barcos=None, tablero_pc_disparos=None, tablero_jugador_barcos=None, tablero_jugador_disparos=None, dificultad="Medio"):
    """
    Configura y gestiona el bucle de la partida. 
    Recibe los 4 tableros si se está cargando la partida, o los inicializa si es nueva.
    """
    flota_estandar = [4, 3, 3, 2, 2]

    if tablero_pc_barcos is None:
        # Lógica de "Nueva Partida" (Crea los 4 tableros)
        print("\n>> Generando el campo de batalla...")
        time.sleep(1)
        
        # Tableros del PC
        tablero_pc_barcos = crear_tablero(DIMENSION)     
        tablero_pc_disparos = crear_tablero(DIMENSION)   
        colocar_barcos_aleatorios(tablero_pc_barcos, flota_estandar)
        
        # Tableros del Jugador
        tablero_jugador_barcos = crear_tablero(DIMENSION) # Donde están tus barcos y la IA dispara
        tablero_jugador_disparos = crear_tablero(DIMENSION) # Tu mapa de disparos (no se usa, pero se mantiene por simetría)
        colocar_barcos_aleatorios(tablero_jugador_barcos, flota_estandar)
        
        print("\n--- ¡FLOTAS LISTAS! COMIENZA LA BATALLA ---")
    
    else:
        # Lógica de "Continuar Partida" (Los 4 tableros ya fueron pasados y desempaquetados)
        print("\n--- Partida cargada con éxito. Continuamos la batalla. ---")
        
    print(f"Dificultad de la IA: {dificultad}")
        
    # --- Bucle Principal de Partida con Submenú ---
    while True:
        # 1. Mostrar el submenú de partida
        print("\n" + "="*25)
        print("  MENÚ DE PARTIDA ACTUAL")
        print("="*25)
        print("  [1] Atacar")
        print("  [2] Ver mapa (Mi Flota)") # Muestra dónde están tus barcos y los ataques de la IA
        print("  [3] Ver mapa (IA)")      # Muestra tus disparos al enemigo
        print("  [4] Salir al menú principal (Guardar)") 
        
        eleccion = input("\n> Selecciona una opción: ").strip()

        if eleccion == '1':
            realizar_ataque(tablero_pc_barcos, tablero_pc_disparos)
            
            # --- TURNO DE LA IA ---
            turno_ia(tablero_jugador_barcos, tablero_jugador_disparos, dificultad)
            
        elif eleccion == '2': 
            # 🌟 CORRECCIÓN APLICADA: Muestra el tablero de TUS BARCOS (donde la IA ha disparado)
            print("\n--- MI FLOTA ---")
            imprimir_tablero(tablero_jugador_barcos) 
            input("\nPresiona ENTER para volver al menú de partida...")

        elif eleccion == '3': 
            # Muestra el mapa de la IA (Mis Disparos)
            print("\n--- TU MAPA DE DISPAROS DEL ENEMIGO ---")
            imprimir_tablero(tablero_pc_disparos)
            input("\nPresiona ENTER para volver al menú de partida...")
            
        elif eleccion == '4': 
            guardar_partida(tablero_pc_barcos, tablero_pc_disparos, tablero_jugador_barcos, tablero_jugador_disparos)
            break 
        
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")
            time.sleep(1)