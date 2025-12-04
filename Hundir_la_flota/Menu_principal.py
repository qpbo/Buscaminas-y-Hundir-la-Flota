import os
import time
import juego  # Importamos el módulo de lógica del juego

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
# --- FUNCIONES DE ACCIÓN DEL MENÚ (Carga y Nueva Partida) ---
# -----------------------------------------------------------------

def continuar_partida():
    """Carga una partida guardada y la inicia."""
    
    # Intenta cargar la partida guardada en juego.py
    tableros_barcos, tableros_disparos = juego.cargar_partida()
    
    if tableros_barcos is None:
        # Si devuelve None, no hay archivo o está corrupto
        print("\n>> ❌ No se encontró ninguna partida guardada para continuar.")
        time.sleep(2)
    else:
        # Si la carga es exitosa, llama a iniciar_juego pasándole los tableros
        juego.iniciar_juego(tableros_barcos, tableros_disparos)


def nueva_partida():
    """Inicia una partida nueva llamando a juego.iniciar_juego sin argumentos."""
    # Al no pasar argumentos, juego.iniciar_juego crea tableros desde cero
    juego.iniciar_juego()


def opciones():
    """Función de demostración para Opciones."""
    print("\n>> Abriendo configuración... (Funcionalidad pendiente)")
    input("\nPresiona ENTER para volver...")


# -----------------------------------------------------------------
# --- BUCLE PRINCIPAL DEL MENÚ ---
# -----------------------------------------------------------------

def menu_principal():
    """Gestiona el bucle y la interacción del menú principal."""
    while True:
        limpiar_pantalla()
        mostrar_titulo()
        
        print("  [1] Continuar partida")
        print("  [2] Nueva partida")
        print("  [3] Opciones")
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