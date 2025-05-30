

from juego_manual import iniciar_partida_manual # <--- IMPORTACIÓN AQUÍ ARRIBA
# Cuando implementemos algoritmos, importaremos desde aquí también.
# from resolucion_automatica import menu_algoritmos 

def menu_principal():
    """Muestra el menú principal y maneja la selección del usuario."""
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Jugar manualmente")
        print("2. Resolver por algoritmos (No implementado)")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            print("\nIniciando modo de juego manual...")
            iniciar_partida_manual() # <--- LLAMAR A LA FUNCIÓN DIRECTAMENTE
                                     
        elif opcion == '2':
            print("\nResolver por algoritmos (función aún no implementada).")
            # Aquí llamarías a la función o menú para los algoritmos.
            # Ejemplo: menu_algoritmos()
        elif opcion == '3':
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    print("¡Bienvenido al juego Flow Free!")
    menu_principal()