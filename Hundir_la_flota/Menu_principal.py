import os
import time
import juego

# Variable global para almacenar la dificultad, accesible en todo el menú
DIFICULTAD_ACTUAL = "Medio" 

def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    if os.name == 'nt': # Para Windows
        os.system('cls')
    else: # Para Mac y Linux
        os.system('clear')

def mostrar_titulo():
    """Imprime el arte ASCII del título."""
    titulo = r"""
  _   _                 _ _         _          __ _       _        
 | | | |               | (_)       | |        / _| |     | |       
 | |_| |_   _ _ __   __| |_ _ __   | | __ _  | |_| | ___ | |_ __ _ 
 |  _  | | | | '_ \ / _` | | '__|  | |/ _` | |  _| |/ _ \| __/ _` |
 | | | | |_| | | | | (_| | | |     | | (_| | | | | | (_) | || (_| |
 \_| |_/\__,_|_| |_|\__,_|_|_|     |_|\__,_| |_| |_|\___/ \__\__,_|
    """
    print(titulo)
    print("\n" + "="*60 + "\n")

# -----------------------------------------------------------------
## Funciones de Acción del Menú
# -----------------------------------------------------------------

def continuar_partida():
    """Carga una partida guardada y la inicia, pasando la dificultad actual."""
    
    # 🌟 CORRECCIÓN CRÍTICA: Desempaquetamos los 4 tableros que devuelve juego.cargar_partida()
    tableros_pc_barcos, tableros_pc_disparos, tableros_jugador_barcos, tableros_jugador_disparos = juego.cargar_partida()
    
    # Verificamos si la carga falló (si el primer valor es None)
    if tableros_pc_barcos is None:
        print("\n>> ❌ No se encontró ninguna partida guardada para continuar.")
        time.sleep(2)
    else:
        # Iniciamos el juego pasándole los 4 tableros cargados y la dificultad
        juego.iniciar_juego(
            tableros_pc_barcos, 
            tableros_pc_disparos, 
            tableros_jugador_barcos, 
            tableros_jugador_disparos,
            DIFICULTAD_ACTUAL
        )


def nueva_partida():
    """Inicia una partida nueva, pasando la dificultad actual."""
    # Al no pasar tableros, juego.iniciar_juego los crea
    juego.iniciar_juego(dificultad=DIFICULTAD_ACTUAL)


def opciones():
    """Permite al usuario cambiar la dificultad del juego."""
    global DIFICULTAD_ACTUAL 
    while True:
        limpiar_pantalla()
        mostrar_titulo()
        print("  [—] MENÚ DE OPCIONES")
        print(f"  [—] Dificultad actual: **{DIFICULTAD_ACTUAL}**\n")
        print("  [1] Fácil (IA ataca 1 vez)")
        print("  [2] Medio (IA ataca 1 vez, 2 si acierta)")
        print("  [3] Difícil (IA ataca 2 veces)")
        print("  [4] Volver al menú principal")
        
        eleccion = input("\n> Selecciona una opción: ").strip()

        if eleccion == '1':
            DIFICULTAD_ACTUAL = "Facil"
        elif eleccion == '2':
            DIFICULTAD_ACTUAL = "Medio"
        elif eleccion == '3':
            DIFICULTAD_ACTUAL = "Dificil"
        elif eleccion == '4':
            break
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")
            time.sleep(1)
        
        if eleccion in ['1', '2', '3']:
            print(f"\n✅ Dificultad cambiada a: {DIFICULTAD_ACTUAL}")
            time.sleep(1)


# -----------------------------------------------------------------
## Bucle Principal del Menú
# -----------------------------------------------------------------

def menu_principal():
    """Gestiona el bucle y la interacción del menú principal."""
    while True:
        limpiar_pantalla()
        mostrar_titulo()
        
        print("  [1] Continuar partida")
        print("  [2] Nueva partida")
        print(f"  [3] Opciones (Dificultad: {DIFICULTAD_ACTUAL})") 
        print("  [4] Salir")
        
        eleccion = input("\n> Selecciona una opción: ").strip()

        if eleccion == '1':
            continuar_partida() 
        elif eleccion == '2':
            nueva_partida()
        elif eleccion == '3':
            opciones()
        elif eleccion == '4':
            print("\n¡Gracias por jugar! Cerrando el sistema...")
            break
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")
            time.sleep(1)

if __name__ == "__main__":
    menu_principal()