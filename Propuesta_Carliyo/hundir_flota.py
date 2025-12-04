"""
HUNDIR LA FLOTA (Battleship) - Juego Clásico Naval
===================================================

Este módulo implementa el juego Hundir la Flota con múltiples modos:
- Jugador vs Jugador (local)
- Jugador vs Computadora (3 niveles de IA)

Configuración del juego:
- Tablero: 10×10 para cada jugador
- Flota: 1 Portaaviones (5), 1 Acorazado (4), 2 Cruceros (3), 1 Lancha (2)

Funcionalidades principales:
- Colocación manual o aleatoria de barcos
- IA con 3 niveles de dificultad (Fácil, Intermedio, Difícil)
- Sistema de disparos con resultados (Agua/Tocado/Hundido)
- Visualización de dos tableros (propio y enemigo)

Autor: Proyecto Grupal ASIR - Python
Fecha: Diciembre 2025
"""

import random
import os


def limpiar_pantalla():
    """
    Limpia la pantalla de la terminal para mejorar la visualización.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def crear_tablero():
    """
    Crea un tablero 10×10 vacío representado con agua ('~').
    
    Returns:
        list: Tablero 10×10 inicializado con agua
    """
    return [['~' for _ in range(10)] for _ in range(10)]


def mostrar_tableros(tablero_propio, tablero_disparos, nombre_jugador, turno_actual=True):
    """
    Muestra los dos tableros del jugador: el propio con sus barcos y el de disparos.
    
    Args:
        tablero_propio (list): Tablero con los barcos del jugador
        tablero_disparos (list): Tablero con los disparos que ha hecho el jugador
        nombre_jugador (str): Nombre del jugador
        turno_actual (bool): Si es el turno de este jugador
    """
    print(f"\n{'='*60}")
    if turno_actual:
        print(f"  TURNO DE: {nombre_jugador.upper()}")
    else:
        print(f"  TABLEROS DE: {nombre_jugador.upper()}")
    print(f"{'='*60}\n")
    
    # Encabezados
    print("     TU FLOTA                      TUS DISPAROS")
    print("   A B C D E F G H I J           A B C D E F G H I J")
    
    # Mostrar ambos tableros lado a lado
    for i in range(10):
        # Tablero propio
        print(f"{i+1:2} ", end="")
        for casilla in tablero_propio[i]:
            print(casilla, end=" ")
        
        # Espacio entre tableros
        print("      ", end="")
        
        # Tablero de disparos
        print(f"{i+1:2} ", end="")
        for casilla in tablero_disparos[i]:
            print(casilla, end=" ")
        
        print()
    
    print("\nLeyenda:")
    print("  ~ = Agua  |  B = Barco  |  X = Tocado  |  O = Agua (disparo fallado)")
    print(f"{'='*60}\n")


def validar_posicion(tablero, fila, columna, longitud, orientacion):
    """
    Valida si un barco se puede colocar en una posición específica.
    
    Los barcos no pueden:
    - Salirse del tablero
    - Solaparse con otros barcos
    - Estar adyacentes a otros barcos (debe haber al menos 1 casilla de separación)
    
    Args:
        tablero (list): Tablero donde se colocará el barco
        fila (int): Fila inicial
        columna (int): Columna inicial
        longitud (int): Longitud del barco
        orientacion (str): 'H' para horizontal, 'V' para vertical
    
    Returns:
        bool: True si la posición es válida, False si no
    """
    # Verificar límites del tablero
    if orientacion == 'H':
        if columna + longitud > 10:
            return False
    else:  # Vertical
        if fila + longitud > 10:
            return False
    
    # Verificar cada casilla del barco y sus adyacentes
    for i in range(longitud):
        if orientacion == 'H':
            f, c = fila, columna + i
        else:
            f, c = fila + i, columna
        
        # Verificar la casilla misma
        if tablero[f][c] != '~':
            return False
        
        # Verificar las 8 casillas adyacentes (para que no se toquen)
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nf, nc = f + df, c + dc
                # Si está dentro del tablero y no es agua, hay un barco cerca
                if 0 <= nf < 10 and 0 <= nc < 10:
                    if tablero[nf][nc] != '~' and (nf, nc) != (f, c):
                        return False
    
    return True


def colocar_barco(tablero, fila, columna, longitud, orientacion):
    """
    Coloca un barco en el tablero en la posición especificada.
    
    Args:
        tablero (list): Tablero donde colocar el barco
        fila (int): Fila inicial
        columna (int): Columna inicial
        longitud (int): Longitud del barco
        orientacion (str): 'H' horizontal o 'V' vertical
    """
    for i in range(longitud):
        if orientacion == 'H':
            tablero[fila][columna + i] = 'B'
        else:
            tablero[fila + i][columna] = 'B'


def colocar_barco_aleatorio(tablero, longitud):
    """
    Intenta colocar un barco de forma aleatoria en el tablero.
    
    Args:
        tablero (list): Tablero donde colocar el barco
        longitud (int): Longitud del barco
    
    Returns:
        bool: True si se pudo colocar, False si no
    """
    intentos = 0
    max_intentos = 100  # Evitar bucle infinito
    
    while intentos < max_intentos:
        fila = random.randint(0, 9)
        columna = random.randint(0, 9)
        orientacion = random.choice(['H', 'V'])
        
        if validar_posicion(tablero, fila, columna, longitud, orientacion):
            colocar_barco(tablero, fila, columna, longitud, orientacion)
            return True
        
        intentos += 1
    
    return False


def colocar_barco_manual(tablero, nombre_barco, longitud):
    """
    Permite al jugador colocar un barco manualmente.
    
    Args:
        tablero (list): Tablero donde colocar el barco
        nombre_barco (str): Nombre del barco
        longitud (int): Longitud del barco
    
    Returns:
        bool: True si colocó manualmente, False si eligió aleatorio
    """
    while True:
        limpiar_pantalla()
        print(f"{'='*60}")
        print(f"  COLOCANDO: {nombre_barco.upper()} (Longitud: {longitud})")
        print(f"{'='*60}\n")
        
        # Mostrar tablero actual
        print("   A B C D E F G H I J")
        for i in range(10):
            print(f"{i+1:2} ", end="")
            for casilla in tablero[i]:
                print(casilla, end=" ")
            print()
        
        print(f"\n{'='*60}")
        print("Opciones:")
        print("  1. Colocar manualmente")
        print("  2. Colocar aleatoriamente")
        print(f"{'='*60}")
        
        opcion = input("\n¿Qué quieres hacer? (1/2): ").strip()
        
        if opcion == '2':
            if colocar_barco_aleatorio(tablero, longitud):
                print(f"\n✓ {nombre_barco} colocado aleatoriamente.")
                input("Presiona Enter para continuar...")
                return False
            else:
                print(f"\n❌ No se pudo colocar el barco aleatoriamente. Intenta manualmente.")
                input("Presiona Enter para continuar...")
                continue
        
        elif opcion == '1':
            try:
                columna_input = input("Columna inicial (A-J): ").strip().upper()
                fila_input = input("Fila inicial (1-10): ").strip()
                orientacion = input("Orientación (H=horizontal, V=vertical): ").strip().upper()
                
                # Validar entrada
                if len(columna_input) != 1 or columna_input not in 'ABCDEFGHIJ':
                    print("\n❌ Columna inválida. Usa A-J.")
                    input("Presiona Enter para continuar...")
                    continue
                
                columna = ord(columna_input) - ord('A')
                fila = int(fila_input) - 1
                
                if fila < 0 or fila > 9:
                    print("\n❌ Fila inválida. Usa 1-10.")
                    input("Presiona Enter para continuar...")
                    continue
                
                if orientacion not in ['H', 'V']:
                    print("\n❌ Orientación inválida. Usa H o V.")
                    input("Presiona Enter para continuar...")
                    continue
                
                # Validar posición
                if not validar_posicion(tablero, fila, columna, longitud, orientacion):
                    print("\n❌ No se puede colocar el barco ahí (fuera del tablero, solapado o muy cerca de otro).")
                    input("Presiona Enter para continuar...")
                    continue
                
                # Colocar el barco
                colocar_barco(tablero, fila, columna, longitud, orientacion)
                print(f"\n✓ {nombre_barco} colocado correctamente.")
                input("Presiona Enter para continuar...")
                return True
                
            except ValueError:
                print("\n❌ Entrada inválida. Intenta de nuevo.")
                input("Presiona Enter para continuar...")
                continue
        else:
            print("\n❌ Opción inválida.")
            input("Presiona Enter para continuar...")


def colocar_flota(tablero, nombre_jugador):
    """
    Permite al jugador colocar toda su flota.
    
    Args:
        tablero (list): Tablero del jugador
        nombre_jugador (str): Nombre del jugador
    """
    flota = [
        ("Portaaviones", 5),
        ("Acorazado", 4),
        ("Crucero 1", 3),
        ("Crucero 2", 3),
        ("Lancha de Reconocimiento", 2)
    ]
    
    limpiar_pantalla()
    print(f"{'='*60}")
    print(f"  {nombre_jugador.upper()}: COLOCA TU FLOTA")
    print(f"{'='*60}")
    print("\nTu flota consiste en:")
    for nombre, longitud in flota:
        print(f"  - {nombre}: {longitud} casillas")
    print(f"\n{'='*60}")
    input("\nPresiona Enter para comenzar...")
    
    for nombre_barco, longitud in flota:
        colocar_barco_manual(tablero, nombre_barco, longitud)


def convertir_coordenada(columna_letra, fila_num):
    """
    Convierte coordenadas de letra-número a índices.
    
    Args:
        columna_letra (str): Letra de columna (A-J)
        fila_num (str): Número de fila (1-10)
    
    Returns:
        tuple: (fila, columna) como índices o (None, None) si inválido
    """
    try:
        columna_letra = columna_letra.upper()
        if len(columna_letra) != 1 or columna_letra not in 'ABCDEFGHIJ':
            return None, None
        
        columna = ord(columna_letra) - ord('A')
        fila = int(fila_num) - 1
        
        if fila < 0 or fila > 9:
            return None, None
        
        return fila, columna
    except:
        return None, None


def realizar_disparo(tablero_enemigo, tablero_disparos, fila, columna):
    """
    Realiza un disparo en el tablero enemigo.
    
    Args:
        tablero_enemigo (list): Tablero del enemigo (con sus barcos reales)
        tablero_disparos (list): Tablero de disparos del jugador que dispara
        fila (int): Fila del disparo
        columna (int): Columna del disparo
    
    Returns:
        str: 'repetido', 'agua', 'tocado', o 'hundido'
    """
    # Verificar si ya disparó ahí
    if tablero_disparos[fila][columna] != '~':
        return 'repetido'
    
    # Verificar si hay barco
    if tablero_enemigo[fila][columna] == 'B':
        # Tocado
        tablero_enemigo[fila][columna] = 'X'
        tablero_disparos[fila][columna] = 'X'
        
        # Verificar si hundió el barco
        if verificar_barco_hundido(tablero_enemigo, fila, columna):
            return 'hundido'
        else:
            return 'tocado'
    else:
        # Agua
        tablero_disparos[fila][columna] = 'O'
        return 'agua'


def verificar_barco_hundido(tablero, fila, columna):
    """
    Verifica si el barco tocado en (fila, columna) está completamente hundido.
    
    Args:
        tablero (list): Tablero con los barcos
        fila (int): Fila del último impacto
        columna (int): Columna del último impacto
    
    Returns:
        bool: True si el barco está hundido, False si no
    """
    # Buscar todas las partes del barco (conectadas horizontal o verticalmente)
    partes_barco = []
    visitados = set()
    
    def buscar_partes(f, c):
        """Función recursiva para encontrar todas las partes del barco"""
        if (f, c) in visitados or f < 0 or f >= 10 or c < 0 or c >= 10:
            return
        
        visitados.add((f, c))
        
        if tablero[f][c] in ['B', 'X']:
            partes_barco.append((f, c, tablero[f][c]))
            # Buscar en las 4 direcciones (no diagonales)
            buscar_partes(f-1, c)
            buscar_partes(f+1, c)
            buscar_partes(f, c-1)
            buscar_partes(f, c+1)
    
    buscar_partes(fila, columna)
    
    # El barco está hundido si todas sus partes son 'X'
    return all(estado == 'X' for _, _, estado in partes_barco)


def verificar_victoria(tablero):
    """
    Verifica si todos los barcos en el tablero han sido hundidos.
    
    Args:
        tablero (list): Tablero a verificar
    
    Returns:
        bool: True si todos los barcos están hundidos, False si no
    """
    for fila in tablero:
        for casilla in fila:
            if casilla == 'B':  # Si queda alguna parte de barco sin tocar
                return False
    return True


def turno_jugador(nombre_jugador, tablero_propio, tablero_enemigo, tablero_disparos):
    """
    Gestiona el turno de un jugador humano.
    
    Args:
        nombre_jugador (str): Nombre del jugador
        tablero_propio (list): Tablero del jugador
        tablero_enemigo (list): Tablero del enemigo
        tablero_disparos (list): Tablero de disparos del jugador
    
    Returns:
        bool: True si ganó, False si no
    """
    while True:
        limpiar_pantalla()
        mostrar_tableros(tablero_propio, tablero_disparos, nombre_jugador, turno_actual=True)
        
        columna_input = input("Columna para disparar (A-J): ").strip()
        fila_input = input("Fila para disparar (1-10): ").strip()
        
        fila, columna = convertir_coordenada(columna_input, fila_input)
        
        if fila is None:
            print("\n❌ Coordenadas inválidas. Intenta de nuevo.")
            input("Presiona Enter para continuar...")
            continue
        
        resultado = realizar_disparo(tablero_enemigo, tablero_disparos, fila, columna)
        
        if resultado == 'repetido':
            print("\n❌ Ya disparaste ahí. Elige otra casilla.")
            input("Presiona Enter para continuar...")
            continue
        
        limpiar_pantalla()
        mostrar_tableros(tablero_propio, tablero_disparos, nombre_jugador, turno_actual=True)
        
        if resultado == 'agua':
            print("\n[~] AGUA! No hay nada ahi.")
        elif resultado == 'tocado':
            print("\n[X] TOCADO! Le diste a un barco.")
        elif resultado == 'hundido':
            print("\n[XXX] HUNDIDO! Has hundido un barco enemigo.")
        
        input("\nPresiona Enter para continuar...")
        
        # Verificar victoria
        if verificar_victoria(tablero_enemigo):
            return True
        
        return False


def ia_disparar_facil(tablero_disparos):
    """
    IA de nivel fácil: dispara completamente al azar.
    
    Args:
        tablero_disparos (list): Tablero de disparos de la IA
    
    Returns:
        tuple: (fila, columna) donde disparar
    """
    while True:
        fila = random.randint(0, 9)
        columna = random.randint(0, 9)
        
        if tablero_disparos[fila][columna] == '~':
            return fila, columna


def ia_disparar_intermedio(tablero_disparos, ultimo_tocado):
    """
    IA de nivel intermedio: si tocó un barco, dispara alrededor.
    
    Args:
        tablero_disparos (list): Tablero de disparos de la IA
        ultimo_tocado (list): Lista de posiciones tocadas pendientes de explorar
    
    Returns:
        tuple: (fila, columna) donde disparar
    """
    # Si tiene barcos tocados, disparar adyacente
    if ultimo_tocado:
        f, c = ultimo_tocado[-1]
        
        # Intentar las 4 direcciones adyacentes
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(direcciones)
        
        for df, dc in direcciones:
            nf, nc = f + df, c + dc
            if 0 <= nf < 10 and 0 <= nc < 10 and tablero_disparos[nf][nc] == '~':
                return nf, nc
        
        # Si no hay casillas adyacentes libres, quitar de la lista
        ultimo_tocado.pop()
        return ia_disparar_intermedio(tablero_disparos, ultimo_tocado)
    
    # Si no hay barcos tocados, disparar al azar
    return ia_disparar_facil(tablero_disparos)


def ia_disparar_dificil(tablero_disparos, ultimo_tocado, patron):
    """
    IA de nivel difícil: usa patrón de tablero de ajedrez y búsqueda inteligente.
    
    Args:
        tablero_disparos (list): Tablero de disparos de la IA
        ultimo_tocado (list): Lista de posiciones tocadas
        patron (list): Lista de casillas en patrón de tablero de ajedrez
    
    Returns:
        tuple: (fila, columna) donde disparar
    """
    # Si tiene barcos tocados, usar estrategia inteligente
    if ultimo_tocado:
        return ia_disparar_intermedio(tablero_disparos, ultimo_tocado)
    
    # Si no, usar patrón de tablero de ajedrez
    if patron:
        while patron:
            fila, columna = patron.pop(0)
            if tablero_disparos[fila][columna] == '~':
                return fila, columna
    
    # Si se acabó el patrón, disparar al azar
    return ia_disparar_facil(tablero_disparos)


def turno_ia(nivel, tablero_ia, tablero_jugador, tablero_disparos_ia, ultimo_tocado, patron=None):
    """
    Gestiona el turno de la IA según su nivel de dificultad.
    
    Args:
        nivel (str): 'facil', 'intermedio' o 'dificil'
        tablero_ia (list): Tablero de la IA
        tablero_jugador (list): Tablero del jugador
        tablero_disparos_ia (list): Tablero de disparos de la IA
        ultimo_tocado (list): Lista de tocados para IA intermedia/difícil
        patron (list): Patrón para IA difícil
    
    Returns:
        bool: True si la IA ganó, False si no
    """
    print("\n[IA] Turno de la COMPUTADORA...")
    import time
    time.sleep(1.5)  # Pausa para dramatismo
    
    # Decidir dónde disparar según el nivel
    if nivel == 'facil':
        fila, columna = ia_disparar_facil(tablero_disparos_ia)
    elif nivel == 'intermedio':
        fila, columna = ia_disparar_intermedio(tablero_disparos_ia, ultimo_tocado)
    else:  # difícil
        fila, columna = ia_disparar_dificil(tablero_disparos_ia, ultimo_tocado, patron)
    
    # Realizar el disparo
    resultado = realizar_disparo(tablero_jugador, tablero_disparos_ia, fila, columna)
    
    # Convertir coordenadas para mostrar
    columna_letra = chr(ord('A') + columna)
    fila_num = fila + 1
    
    print(f"\nLa computadora dispara en: {columna_letra}{fila_num}")
    
    if resultado == 'agua':
        print("[~] AGUA!")
    elif resultado == 'tocado':
        print("[X] TOCADO! La computadora le dio a uno de tus barcos.")
        # Añadir a la lista de tocados para IA intermedia/difícil
        if nivel in ['intermedio', 'dificil']:
            ultimo_tocado.append((fila, columna))
    elif resultado == 'hundido':
        print("[XXX] HUNDIDO! La computadora hundio uno de tus barcos.")
        # Si hundió, limpiar la lista de tocados para este barco
        if nivel in ['intermedio', 'dificil'] and (fila, columna) in ultimo_tocado:
            ultimo_tocado.remove((fila, columna))
    
    input("\nPresiona Enter para continuar...")
    
    # Verificar victoria
    return verificar_victoria(tablero_jugador)


def menu_modo_juego():
    """
    Menú para seleccionar el modo de juego.
    
    Returns:
        str: 'pvp', 'pvc', o None para cancelar
    """
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("         HUNDIR LA FLOTA - MODO DE JUEGO")
        print("=" * 60)
        print("\n1. Jugador vs Jugador")
        print("2. Jugador vs Computadora")
        print("3. Volver al menú principal")
        print("=" * 60)
        
        opcion = input("\nElige el modo de juego (1-3): ").strip()
        
        if opcion == '1':
            return 'pvp'
        elif opcion == '2':
            return 'pvc'
        elif opcion == '3':
            return None
        else:
            print("\n❌ Opción inválida.")
            input("Presiona Enter para continuar...")


def menu_dificultad_ia():
    """
    Menú para seleccionar la dificultad de la IA.
    
    Returns:
        str: 'facil', 'intermedio', o 'dificil'
    """
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("         DIFICULTAD DE LA COMPUTADORA")
        print("=" * 60)
        print("\n1. Fácil      (Disparos aleatorios)")
        print("2. Intermedio (Busca alrededor al tocar)")
        print("3. Difícil    (Estrategia avanzada)")
        print("=" * 60)
        
        opcion = input("\nElige la dificultad (1-3): ").strip()
        
        if opcion == '1':
            return 'facil'
        elif opcion == '2':
            return 'intermedio'
        elif opcion == '3':
            return 'dificil'
        else:
            print("\n❌ Opción inválida.")
            input("Presiona Enter para continuar...")


def jugar_hundir_flota():
    """
    Función principal del juego Hundir la Flota.
    """
    # Seleccionar modo de juego
    modo = menu_modo_juego()
    
    if modo is None:
        return  # Volver al menú principal
    
    # Crear tableros
    tablero_j1 = crear_tablero()
    tablero_j2 = crear_tablero()
    tablero_disparos_j1 = crear_tablero()
    tablero_disparos_j2 = crear_tablero()
    
    if modo == 'pvp':
        # Modo Jugador vs Jugador
        nombre_j1 = input("\nNombre del Jugador 1: ").strip() or "Jugador 1"
        nombre_j2 = input("Nombre del Jugador 2: ").strip() or "Jugador 2"
        
        # Colocar flotas
        colocar_flota(tablero_j1, nombre_j1)
        input(f"\n{nombre_j1} ha colocado su flota. {nombre_j2}, aparta la vista...")
        colocar_flota(tablero_j2, nombre_j2)
        
        # Juego por turnos
        turno = 1  # 1 = Jugador 1, 2 = Jugador 2
        
        while True:
            if turno == 1:
                if turno_jugador(nombre_j1, tablero_j1, tablero_j2, tablero_disparos_j1):
                    limpiar_pantalla()
                    print("=" * 60)
                    print(f"  *** {nombre_j1.upper()} HA GANADO! ***")
                    print("=" * 60)
                    input("\nPresiona Enter para volver al menú principal...")
                    break
                turno = 2
            else:
                if turno_jugador(nombre_j2, tablero_j2, tablero_j1, tablero_disparos_j2):
                    limpiar_pantalla()
                    print("=" * 60)
                    print(f"  *** {nombre_j2.upper()} HA GANADO! ***")
                    print("=" * 60)
                    input("\nPresiona Enter para volver al menú principal...")
                    break
                turno = 1
    
    else:  # modo == 'pvc'
        # Modo Jugador vs Computadora
        nivel_ia = menu_dificultad_ia()
        nombre_j1 = input("\nTu nombre: ").strip() or "Jugador"
        
        # Colocar flota del jugador
        colocar_flota(tablero_j1, nombre_j1)
        
        # Colocar flota de la IA aleatoriamente
        print("\n[IA] La computadora esta colocando su flota...")
        for longitud in [5, 4, 3, 3, 2]:
            colocar_barco_aleatorio(tablero_j2, longitud)
        print("[OK] Flota de la computadora lista.")
        input("Presiona Enter para comenzar...")
        
        # Variables para la IA
        ultimo_tocado_ia = []  # Para IA intermedia y difícil
        patron_ia = []  # Para IA difícil
        
        # Crear patrón de tablero de ajedrez para IA difícil
        if nivel_ia == 'dificil':
            for i in range(10):
                for j in range(10):
                    if (i + j) % 2 == 0:
                        patron_ia.append((i, j))
            random.shuffle(patron_ia)
        
        # Juego por turnos
        turno = 1  # 1 = Jugador, 2 = IA
        
        while True:
            if turno == 1:
                if turno_jugador(nombre_j1, tablero_j1, tablero_j2, tablero_disparos_j1):
                    limpiar_pantalla()
                    print("=" * 60)
                    print(f"  *** {nombre_j1.upper()} HA GANADO! ***")
                    print("=" * 60)
                    input("\nPresiona Enter para volver al menú principal...")
                    break
                turno = 2
            else:
                if turno_ia(nivel_ia, tablero_j2, tablero_j1, tablero_disparos_j2, ultimo_tocado_ia, patron_ia):
                    limpiar_pantalla()
                    print("=" * 60)
                    print("  *** LA COMPUTADORA HA GANADO ***")
                    print("=" * 60)
                    input("\nPresiona Enter para volver al menú principal...")
                    break
                turno = 1


# Punto de entrada para pruebas del módulo
if __name__ == "__main__":
    jugar_hundir_flota()
