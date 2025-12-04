"""
BUSCAMINAS - Juego Clásico de Minas
====================================

Este módulo implementa el juego del Buscaminas con tres niveles de dificultad:
- Fácil: 8 filas × 10 columnas con 10 minas
- Intermedio: 16 filas × 16 columnas con 40 minas  
- Difícil: 30 filas × 16 columnas con 99 minas

Funcionalidades principales:
- Colocación aleatoria de minas
- Cálculo automático de minas vecinas
- Expansión automática cuando se encuentra un 0
- Sistema de banderas para marcar minas sospechosas
- Detección de victoria/derrota

Autor: Proyecto Grupal ASIR - Python
Fecha: Diciembre 2025
"""

import random
import os


def limpiar_pantalla():
    """
    Limpia la pantalla de la terminal para mejorar la visualización.
    Funciona en Windows (cls) y Linux/Mac (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def crear_tablero(filas, columnas):
    """
    Crea dos tableros vacíos: uno para el estado real y otro para lo que ve el jugador.
    
    Args:
        filas (int): Número de filas del tablero
        columnas (int): Número de columnas del tablero
    
    Returns:
        tuple: (tablero_real, tablero_visible)
            - tablero_real: Contiene las minas ('*') y números
            - tablero_visible: Lo que el jugador ve ('#' = oculto, número/bandera visible)
    """
    # Tablero real: inicializado con 0 en todas las posiciones
    tablero_real = [[0 for _ in range(columnas)] for _ in range(filas)]
    
    # Tablero visible: inicializado con '#' (casilla oculta)
    tablero_visible = [['#' for _ in range(columnas)] for _ in range(filas)]
    
    return tablero_real, tablero_visible


def colocar_minas(tablero_real, num_minas):
    """
    Coloca las minas de forma aleatoria en el tablero sin repetir posiciones.
    
    Args:
        tablero_real (list): El tablero donde se colocarán las minas
        num_minas (int): Cantidad de minas a colocar
    """
    filas = len(tablero_real)
    columnas = len(tablero_real[0])
    minas_colocadas = 0
    
    while minas_colocadas < num_minas:
        # Generar posición aleatoria
        fila = random.randint(0, filas - 1)
        columna = random.randint(0, columnas - 1)
        
        # Si la posición no tiene mina, colocar una
        if tablero_real[fila][columna] != '*':
            tablero_real[fila][columna] = '*'
            minas_colocadas += 1


def calcular_vecinos(tablero_real):
    """
    Calcula cuántas minas hay alrededor de cada casilla que no es mina.
    Se comprueban las 8 direcciones: arriba, abajo, izquierda, derecha y diagonales.
    
    Args:
        tablero_real (list): El tablero con las minas ya colocadas
    """
    filas = len(tablero_real)
    columnas = len(tablero_real[0])
    
    # Direcciones: arriba, abajo, izq, der, y las 4 diagonales
    direcciones = [
        (-1, -1), (-1, 0), (-1, 1),  # Arriba-izq, arriba, arriba-der
        (0, -1),           (0, 1),    # Izquierda, derecha
        (1, -1),  (1, 0),  (1, 1)     # Abajo-izq, abajo, abajo-der
    ]
    
    # Recorrer cada casilla del tablero
    for fila in range(filas):
        for columna in range(columnas):
            # Solo calcular para casillas que no son minas
            if tablero_real[fila][columna] != '*':
                minas_vecinas = 0
                
                # Revisar las 8 direcciones
                for df, dc in direcciones:
                    nueva_fila = fila + df
                    nueva_columna = columna + dc
                    
                    # Verificar que la posición esté dentro del tablero
                    if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
                        if tablero_real[nueva_fila][nueva_columna] == '*':
                            minas_vecinas += 1
                
                # Asignar el número de minas vecinas
                tablero_real[fila][columna] = minas_vecinas


def mostrar_tablero(tablero_visible, mostrar_coordenadas=True):
    """
    Muestra el tablero en la terminal de forma visual y clara.
    
    Args:
        tablero_visible (list): El tablero que ve el jugador
        mostrar_coordenadas (bool): Si mostrar las letras de columnas y números de filas
    """
    filas = len(tablero_visible)
    columnas = len(tablero_visible[0])
    
    # Mostrar letras de columnas (A, B, C, ...)
    if mostrar_coordenadas:
        print("\n    ", end="")
        for i in range(columnas):
            # Usar letras A-Z, luego AA, AB, etc. si hay más de 26 columnas
            if i < 26:
                print(chr(65 + i), end=" ")
            else:
                print(chr(65 + i // 26 - 1) + chr(65 + i % 26), end="")
        print()
    
    # Mostrar cada fila con su número
    for i, fila in enumerate(tablero_visible):
        if mostrar_coordenadas:
            print(f"{i + 1:3} ", end="")  # Número de fila alineado a la derecha
        
        for casilla in fila:
            # Colorear o formatear según el contenido
            if casilla == '#':
                print('#', end=" ")  # Casilla oculta
            elif casilla == 'F':
                print('F', end=" ")  # Bandera
            elif casilla == 0:
                print('.', end=" ")  # Casilla vacía (sin minas vecinas)
            else:
                print(casilla, end=" ")  # Número de minas vecinas
        print()
    print()


def revelar_casilla(tablero_real, tablero_visible, fila, columna):
    """
    Revela una casilla. Si es 0, expande automáticamente a las casillas vecinas.
    Esta función usa recursividad para la expansión automática.
    
    IMPORTANTE: Cuando se expande un área de ceros, también se revelan las casillas
    con números (1-8) que están en el borde de esa expansión. Esto es fundamental
    para que el juego sea jugable y siga las reglas clásicas del Buscaminas.
    
    Args:
        tablero_real (list): Tablero con las minas y números
        tablero_visible (list): Tablero que ve el jugador
        fila (int): Fila de la casilla a revelar
        columna (int): Columna de la casilla a revelar
    
    Returns:
        bool: True si pisó una mina, False si es seguro
    """
    # Verificar límites del tablero
    if fila < 0 or fila >= len(tablero_real) or columna < 0 or columna >= len(tablero_real[0]):
        return False
    
    # Si ya está revelada o tiene bandera, no hacer nada
    if tablero_visible[fila][columna] != '#':
        return False
    
    # Revelar la casilla actual
    tablero_visible[fila][columna] = tablero_real[fila][columna]
    
    # Si es mina, retornar True (perdió)
    if tablero_real[fila][columna] == '*':
        return True
    
    # Si es 0, expandir automáticamente a TODAS las casillas vecinas
    # Esto revelará tanto los ceros como los números (1-8) en el borde
    if tablero_real[fila][columna] == 0:
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),  # Arriba-izq, arriba, arriba-der
            (0, -1),           (0, 1),    # Izquierda, derecha
            (1, -1),  (1, 0),  (1, 1)     # Abajo-izq, abajo, abajo-der
        ]
        
        for df, dc in direcciones:
            nueva_fila = fila + df
            nueva_columna = columna + dc
            
            # Recursión: revelar todas las casillas vecinas
            # Si la vecina es 0, continuará expandiendo
            # Si la vecina es un número (1-8), se revelará pero no expandirá más
            revelar_casilla(tablero_real, tablero_visible, nueva_fila, nueva_columna)
    
    return False


def marcar_bandera(tablero_visible, fila, columna):
    """
    Marca o desmarca una bandera en una casilla.
    Las banderas se usan para indicar dónde el jugador cree que hay una mina.
    
    Args:
        tablero_visible (list): Tablero visible del jugador
        fila (int): Fila de la casilla
        columna (int): Columna de la casilla
    
    Returns:
        bool: True si se pudo marcar/desmarcar, False si no
    """
    # Solo se puede marcar/desmarcar casillas ocultas o con bandera
    if tablero_visible[fila][columna] == '#':
        tablero_visible[fila][columna] = 'F'
        return True
    elif tablero_visible[fila][columna] == 'F':
        tablero_visible[fila][columna] = '#'
        return True
    
    return False


def verificar_victoria(tablero_real, tablero_visible):
    """
    Verifica si el jugador ha ganado.
    Gana cuando todas las casillas sin minas están reveladas.
    
    Args:
        tablero_real (list): Tablero con minas y números
        tablero_visible (list): Tablero que ve el jugador
    
    Returns:
        bool: True si ganó, False si no
    """
    filas = len(tablero_real)
    columnas = len(tablero_real[0])
    
    for fila in range(filas):
        for columna in range(columnas):
            # Si hay una casilla sin mina que no está revelada, no ha ganado
            if tablero_real[fila][columna] != '*' and tablero_visible[fila][columna] == '#':
                return False
    
    return True


def convertir_coordenada_columna(letra):
    """
    Convierte una letra de columna (A, B, C...) a índice numérico (0, 1, 2...).
    
    Args:
        letra (str): Letra o letras de la columna (ej: 'A', 'B', 'AA')
    
    Returns:
        int: Índice de columna o -1 si es inválido
    """
    letra = letra.upper()
    
    # Si es una sola letra (A-Z)
    if len(letra) == 1:
        return ord(letra) - ord('A')
    # Si son dos letras (AA, AB, etc.)
    elif len(letra) == 2:
        return (ord(letra[0]) - ord('A') + 1) * 26 + (ord(letra[1]) - ord('A'))
    
    return -1


def revelar_todo(tablero_real, tablero_visible):
    """
    Revela todo el tablero (usado cuando el jugador pierde).
    
    Args:
        tablero_real (list): Tablero real con minas
        tablero_visible (list): Tablero visible del jugador
    """
    filas = len(tablero_real)
    columnas = len(tablero_real[0])
    
    for fila in range(filas):
        for columna in range(columnas):
            tablero_visible[fila][columna] = tablero_real[fila][columna]


def menu_dificultad():
    """
    Muestra el menú de selección de dificultad y retorna la configuración elegida.
    
    Returns:
        tuple: (filas, columnas, minas) o None si cancela
    """
    while True:
        limpiar_pantalla()
        print("=" * 50)
        print("         BUSCAMINAS - NIVEL DE DIFICULTAD")
        print("=" * 50)
        print("\n1. Fácil      (8 × 10 con 10 minas)")
        print("2. Intermedio (16 × 16 con 40 minas)")
        print("3. Difícil    (30 × 16 con 99 minas)")
        print("4. Volver al menú principal")
        print("=" * 50)
        
        opcion = input("\nElige tu nivel de dificultad (1-4): ").strip()
        
        if opcion == '1':
            return (8, 10, 10)
        elif opcion == '2':
            return (16, 16, 40)
        elif opcion == '3':
            return (30, 16, 99)
        elif opcion == '4':
            return None
        else:
            print("\n❌ Opción inválida. Presiona Enter para intentar de nuevo...")
            input()


def jugar_buscaminas():
    """
    Función principal del juego Buscaminas.
    Controla todo el flujo del juego desde la selección de dificultad hasta el final.
    """
    # Seleccionar dificultad
    config = menu_dificultad()
    
    if config is None:
        return  # Volver al menú principal
    
    filas, columnas, num_minas = config
    
    # Crear el tablero
    tablero_real, tablero_visible = crear_tablero(filas, columnas)
    
    # Colocar minas
    colocar_minas(tablero_real, num_minas)
    
    # Calcular números de vecinos
    calcular_vecinos(tablero_real)
    
    # Variables del juego
    juego_activo = True
    
    # Bucle principal del juego
    while juego_activo:
        limpiar_pantalla()
        
        print("=" * 50)
        print("                   BUSCAMINAS")
        print("=" * 50)
        print(f"Tablero: {filas}×{columnas} | Minas: {num_minas}")
        print("=" * 50)
        print("\nLeyenda:")
        print("  # = Casilla oculta")
        print("  F = Bandera (mina sospechosa)")
        print("  . = Casilla vacia (0 minas vecinas)")
        print("  1-8 = Numero de minas vecinas")
        print("=" * 50)
        
        # Mostrar tablero
        mostrar_tablero(tablero_visible)
        
        print("\nOpciones:")
        print("  R = Revelar casilla  |  F = Marcar/desmarcar bandera  |  S = Salir")
        print("=" * 50)
        
        # Pedir acción al jugador
        accion = input("\n¿Qué quieres hacer? (R/F/S): ").strip().upper()
        
        if accion == 'S':
            print("\nSaliendo del juego...")
            input("Presiona Enter para continuar...")
            break
        
        if accion not in ['R', 'F']:
            print("\n❌ Acción inválida. Usa R (revelar), F (bandera) o S (salir).")
            input("Presiona Enter para continuar...")
            continue
        
        # Pedir coordenadas
        try:
            columna_input = input("Columna (letra, ej: A): ").strip()
            fila_input = input("Fila (número, ej: 1): ").strip()
            
            columna = convertir_coordenada_columna(columna_input)
            fila = int(fila_input) - 1  # Convertir a índice (comenzando en 0)
            
            # Verificar que las coordenadas sean válidas
            if columna < 0 or columna >= columnas or fila < 0 or fila >= filas:
                print(f"\n❌ Coordenadas fuera del tablero. Debe ser entre A-{chr(65 + columnas - 1)} y 1-{filas}.")
                input("Presiona Enter para continuar...")
                continue
            
        except ValueError:
            print("\n❌ Coordenadas inválidas. Asegúrate de usar letra para columna y número para fila.")
            input("Presiona Enter para continuar...")
            continue
        
        # Ejecutar la acción
        if accion == 'R':
            # Revelar casilla
            piso_mina = revelar_casilla(tablero_real, tablero_visible, fila, columna)
            
            if piso_mina:
                # Perdió - revelar todo el tablero
                limpiar_pantalla()
                print("=" * 50)
                print("                *** BOOM ***")
                print("=" * 50)
                print("\nPisaste una mina! Has perdido.")
                print("\nTablero completo:")
                revelar_todo(tablero_real, tablero_visible)
                mostrar_tablero(tablero_visible)
                print("=" * 50)
                input("\nPresiona Enter para volver al menú principal...")
                juego_activo = False
            else:
                # Verificar victoria
                if verificar_victoria(tablero_real, tablero_visible):
                    limpiar_pantalla()
                    print("=" * 50)
                    print("              *** VICTORIA ***")
                    print("=" * 50)
                    print("\nFelicidades! Has descubierto todas las casillas seguras.")
                    print("\nTablero completo:")
                    revelar_todo(tablero_real, tablero_visible)
                    mostrar_tablero(tablero_visible)
                    print("=" * 50)
                    input("\nPresiona Enter para volver al menú principal...")
                    juego_activo = False
        
        elif accion == 'F':
            # Marcar/desmarcar bandera
            if not marcar_bandera(tablero_visible, fila, columna):
                print("\n[X] No puedes poner una bandera en una casilla ya revelada.")
                input("Presiona Enter para continuar...")


# Punto de entrada para pruebas del módulo
if __name__ == "__main__":
    jugar_buscaminas()
