import os
import time
import juego  # <--- IMPORTANTE: Importamos el archivo que acabamos de crear

def limpiar_pantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_titulo():
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

def nueva_partida():
    # Llamamos a la función maestra que está dentro de juego.py
    juego.iniciar_juego()

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
            print("Pendiente...")
            time.sleep(1)
        elif eleccion == '2':
            nueva_partida()  # <--- Esto nos lleva al otro archivo
        elif eleccion == '3':
            print("Opciones...")
            time.sleep(1)
        elif eleccion == '4':
            print("\n¡Adiós!")
            break

if __name__ == "__main__":
    menu_principal()