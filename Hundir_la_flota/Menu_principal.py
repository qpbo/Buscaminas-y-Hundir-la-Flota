import os
import time

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

def continuar_partida():
    print("\n>> Buscando partida guardada... (Funcionalidad pendiente)")
    time.sleep(2)

def nueva_partida():
    print("\n>> Iniciando una nueva batalla... ¡Prepara los barcos!")
    time.sleep(2)
    # Aquí iría la llamada a tu función principal del juego
    # ej: iniciar_juego()

def opciones():
    print("\n>> Abriendo configuración...")
    print("   - Dificultad: Normal")
    print("   - Sonido: On")
    input("\nPresiona ENTER para volver...")

def menu_principal():
    while True:
        limpiar_pantalla()
        mostrar_titulo()
        
        print("  [1] Continuar partida")
        print("  [2] Nueva partida")
        print("  [3] Opciones")
        print("  [4] Salir")
        
        eleccion = input("\n> Selecciona una opción: ")

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