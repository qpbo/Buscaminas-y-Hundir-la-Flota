"""
MENÚ PRINCIPAL - Buscaminas y Hundir la Flota
==============================================

Este es el punto de entrada principal del programa.
Permite al usuario elegir entre los dos juegos disponibles:
1. Buscaminas
2. Hundir la Flota

Autor: Proyecto Grupal ASIR - Python
Fecha: Diciembre 2025
"""

import os

# Importar los módulos de los juegos
import buscaminas
import hundir_flota


def limpiar_pantalla():
    """
    Limpia la pantalla de la terminal.
    Funciona en Windows (cls) y Linux/Mac (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_banner():
    """
    Muestra un banner de bienvenida ASCII art.
    """
    print("""
    ============================================================
    
              BUSCAMINAS Y HUNDIR LA FLOTA
                    Dream Team
              Proyecto Python - ASIR 2025
    
    ============================================================
    """)


def menu_principal():
    """
    Muestra el menú principal y gestiona la selección del usuario.
    Permite elegir entre Buscaminas, Hundir la Flota o Salir.
    """
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        print("\n" + "=" * 60)
        print("                    MENU PRINCIPAL")
        print("=" * 60)
        print("\n1. Jugar Buscaminas")
        print("2. Jugar Hundir la Flota")
        print("3. Salir")
        print("\n" + "=" * 60)
        
        opcion = input("\nElige una opción (1-3): ").strip()
        
        if opcion == '1':
            # Ejecutar Buscaminas
            buscaminas.jugar_buscaminas()
        
        elif opcion == '2':
            # Ejecutar Hundir la Flota
            hundir_flota.jugar_hundir_flota()
        
        elif opcion == '3':
            # Salir del programa
            limpiar_pantalla()
            print("\n" + "=" * 60)
            print("       Gracias por jugar! Hasta la proxima")
            print("=" * 60 + "\n")
            break
        
        else:
            # Opción inválida
            print("\n[X] Opcion invalida. Por favor, elige 1, 2 o 3.")
            input("\nPresiona Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    """
    Este bloque se ejecuta cuando se inicia el programa directamente.
    Llama a la función menu_principal() que controla todo el flujo.
    """
    try:
        menu_principal()
    except KeyboardInterrupt:
        # Manejo de Ctrl+C para salir elegantemente
        limpiar_pantalla()
        print("\n\n" + "=" * 60)
        print("       Programa interrumpido. Hasta luego!")
        print("=" * 60 + "\n")
    except Exception as e:
        # Manejo de errores inesperados
        print(f"\n[ERROR] Error inesperado: {e}")
        print("Por favor, contacta al equipo de desarrollo.")
        input("\nPresiona Enter para salir...")
