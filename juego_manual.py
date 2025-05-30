# FlowFree/juego_manual.py

import os
try:
    import readchar
    READCHAR_DISPONIBLE = True
    # print("DEBUG: readchar importado exitosamente.") # Para depuración
except ImportError:
    READCHAR_DISPONIBLE = False
    print("ADVERTENCIA: La biblioteca 'readchar' no está instalada (pip install readchar).")
    print("Se usará input() estándar (requiere presionar Enter y mostrará la tecla).")

from tablero_juego import cargar_nivel_desde_archivo 

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def seleccionar_color_activo_manual(tablero_actual, estado_partida_manual):
    """
    Permite al usuario seleccionar qué color dibujar o cambiar.
    Usa readchar si está disponible para entrada directa de números.
    """
    # El tablero ya se mostró antes de llamar esta función
    print("\n--- SELECCIONAR COLOR ---")
    colores_info = tablero_actual.obtener_colores_estado() 
    colores_listado = list(colores_info.items())

    for i, (color_char, info) in enumerate(colores_listado):
        estado_str = "Completado" if info['completado'] else "Pendiente"
        print(f"{i+1}. Color {color_char} (Inicio: {info['inicio']}, Fin: {info['fin']}) - {estado_str}")

    prompt_general = f"Elige el número del color (1-{len(colores_listado)}), o '0' para cancelar"
    if READCHAR_DISPONIBLE:
        print(prompt_general + ": (presiona la tecla numérica)")
    else:
        print(prompt_general + ": ")


    while True:
        num_eleccion = -1 # Valor por defecto
        try:
            if READCHAR_DISPONIBLE:
                tecla = readchar.readkey()
                if tecla == readchar.key.CTRL_C: raise KeyboardInterrupt
                if tecla.isdigit():
                    num_eleccion = int(tecla)
                    # Aquí no se limpia pantalla ni se imprime la tecla
                else:
                    # print(f"DEBUG: Tecla no numérica '{tecla}' para selección de color.") # Opcional
                    # No hacer nada, esperar una tecla numérica válida
                    continue # Vuelve al inicio del bucle while para leer otra tecla
            else: # Usar input() estándar
                entrada_str = input() # El prompt ya se imprimió
                if not entrada_str.strip(): continue # Ignorar Enter vacío
                num_eleccion = int(entrada_str)
        
        except KeyboardInterrupt:
            print("\nSelección cancelada (Ctrl+C).")
            estado_partida_manual['color_activo'] = None
            return False # Indica cancelación
        except ValueError: # Para int(entrada_str) si no es número
            print("Entrada no válida. Introduce un número.")
            continue
        except Exception as e: 
            print(f"Error inesperado en selección de color: {e}")
            continue

        # Lógica de validación de num_eleccion
        if num_eleccion == 0:
            estado_partida_manual['color_activo'] = None
            # No imprimir "Ningún color seleccionado" aquí, el bucle principal lo manejará
            return False # Indica cancelación o ninguna selección
        elif 1 <= num_eleccion <= len(colores_listado):
            color_seleccionado_char, info_color_seleccionado = colores_listado[num_eleccion - 1]
            if info_color_seleccionado['completado']:
                # Este mensaje se mostrará brevemente antes de limpiar y volver a pedir
                print(f"El color {color_seleccionado_char} ya está completado. Elige otro.")
                if READCHAR_DISPONIBLE:
                    # Pequeña pausa para que el usuario vea el mensaje si se usa readchar
                    # ya que la pantalla se limpiará rápidamente.
                    # Alternativamente, este mensaje se podría pasar al bucle principal.
                    try: readchar.readkey(timeout=0.5) # Espera medio segundo o una tecla
                    except: pass
                else:
                    input("Presiona Enter para continuar...")
                return "REINTENTAR_SELECCION" # Señal para que el bucle principal limpie y reintente
            
            estado_partida_manual['color_activo'] = color_seleccionado_char
            # No imprimir "Color activo", se hará en el bucle principal
            return True # Selección exitosa
        else:
            if num_eleccion != -1: # Si no fue un 'continue' por tecla no numérica con readchar
                print(f"Número '{num_eleccion}' fuera de rango. Intenta de nuevo.")
                if not READCHAR_DISPONIBLE: input("Presiona Enter para continuar...")
            # Si es -1, fue una tecla no numérica con readchar, ya se manejó con 'continue'


def obtener_entrada_accion_manual_directa():
    """
    Obtiene una sola tecla de acción W,A,S,D,C,Z,Q directamente.
    No imprime la tecla ni espera Enter si readchar está disponible.
    """
    # El prompt de acción se muestra en el bucle principal
    if READCHAR_DISPONIBLE:
        try:
            tecla = readchar.readkey()
            if hasattr(tecla, 'upper'): # Si es un string (W, A, S, D, etc.)
                accion = tecla.upper()
            elif tecla == readchar.key.CTRL_C: # Manejar Ctrl+C
                raise KeyboardInterrupt
            else: # Otras teclas especiales de readchar (flechas, etc.) no mapeadas
                accion = None 
            
            if accion in ['W', 'A', 'S', 'D', 'C', 'Z', 'Q']:
                return accion
            return None # Tecla no reconocida o no mapeada
        except KeyboardInterrupt:
            return 'Q' # Tratar Ctrl+C como salir
        except Exception: # Cualquier otro error con readchar
            return None
    else: # Fallback a input() estándar
        entrada = input("Tu acción (W,A,S,D,C,Z,Q) + Enter: ").upper()
        if entrada in ['W', 'A', 'S', 'D', 'C', 'Z', 'Q']:
            return entrada
        else:
            print("Acción no válida.")
            return None

def iniciar_partida_manual():
    ruta_predeterminada = "niveles/ejemplo_con_pared.txt"
    entrada_ruta = input(f"Ruta del nivel (Enter para '{ruta_predeterminada}'): ")
    ruta_archivo_a_cargar = entrada_ruta.strip() if entrada_ruta.strip() else ruta_predeterminada
    if not entrada_ruta.strip() and ruta_archivo_a_cargar == ruta_predeterminada:
         print(f"Usando nivel por defecto: {ruta_predeterminada}")

    tablero_actual = cargar_nivel_desde_archivo(ruta_archivo_a_cargar)

    if not tablero_actual:
        print(f"No se pudo cargar el nivel desde '{ruta_archivo_a_cargar}'.")
        if not READCHAR_DISPONIBLE: input("Presiona Enter para volver al menú...")
        return 

    estado_partida_manual = {'color_activo': None}
    partida_en_curso = True
    mensaje_interfaz = "¡Nivel cargado! Comienza el juego." 

    while partida_en_curso:
        limpiar_pantalla()
        print(f"--- Flow Free --- Nivel: {os.path.basename(ruta_archivo_a_cargar)} ---")
        
        info_color_str = "Ninguno"
        if estado_partida_manual['color_activo']:
            ca = estado_partida_manual['color_activo']
            if tablero_actual.caminos.get(ca): # Asegurarse de que el color y su camino existen
                cabeza = tablero_actual.caminos[ca][-1]
                info_color_str = f"{ca} (Cabeza en: {cabeza})"
            else:
                info_color_str = f"{ca} (Error: sin camino)"
        print(f"Color Activo: {info_color_str}")
        
        tablero_actual.mostrar_tablero_consola()
        print(f"\n{mensaje_interfaz}") # Mensaje de la última acción/estado
        print("Mov: [W]Arriba [A]Izq [S]Abajo [D]Der | Acc: [C]Color [Z]Deshacer [Q]Salir")

        if not estado_partida_manual['color_activo']:
            # print("\nDebes seleccionar un color para dibujar.") # Ya se infiere por "Color Activo: Ninguno"
            resultado_seleccion = seleccionar_color_activo_manual(tablero_actual, estado_partida_manual)
            if resultado_seleccion == True: # Color seleccionado
                mensaje_interfaz = f"Color {estado_partida_manual['color_activo']} seleccionado. Elige una acción."
            elif resultado_seleccion == "REINTENTAR_SELECCION":
                mensaje_interfaz = "Ese color ya está completo o hubo un error. Elige otro."
            else: # False, cancelación
                accion_post = input("No se seleccionó color. ¿[S]alir del nivel o [R]eintentar selección? ").upper()
                if accion_post == 'S':
                    partida_en_curso = False
                    mensaje_interfaz = "Saliendo del nivel..."
                else:
                    mensaje_interfaz = "Reintentando selección de color."
            continue # Vuelve al inicio del bucle para limpiar y redibujar

        # --- Si hay color activo ---
        color_actual = estado_partida_manual['color_activo']
        
        if tablero_actual.camino_esta_completo(color_actual):
            mensaje_interfaz = f"El color {color_actual} ya está completo. Elige otro."
            estado_partida_manual['color_activo'] = None 
            continue 

        # print(f"--- Dibujando con color: {color_actual} ---") # Ya se muestra arriba
        # if tablero_actual.caminos[color_actual]: 
        #      cabeza_actual_camino = tablero_actual.caminos[color_actual][-1]
        #      print(f"Cabeza actual en: {cabeza_actual_camino}") # Ya se muestra arriba

        accion = obtener_entrada_accion_manual_directa()

        if accion is None: # Tecla no reconocida
            mensaje_interfaz = "Tecla no válida. Usa W,A,S,D,C,Z,Q."
            continue

        if accion == 'Q':
            mensaje_interfaz = "Saliendo del nivel..."
            partida_en_curso = False
        elif accion == 'C':
            estado_partida_manual['color_activo'] = None
            mensaje_interfaz = "Cambiando de color... Selecciona uno nuevo."
        elif accion == 'Z': 
            exito_deshacer, msg_deshacer = tablero_actual.deshacer_ultimo_paso(color_actual)
            mensaje_interfaz = msg_deshacer 
        
        elif accion in ['W', 'A', 'S', 'D']: 
            direccion_map = {'W': 'arriba', 'A': 'izquierda', 'S': 'abajo', 'D': 'derecha'}
            direccion = direccion_map[accion]
            exito_movimiento, msg_movimiento = tablero_actual.intentar_extender_camino(color_actual, direccion)
            mensaje_interfaz = msg_movimiento

            if exito_movimiento: 
                if tablero_actual.todos_los_caminos_completos():
                    limpiar_pantalla() # Limpiar antes del mensaje final de victoria
                    print(f"--- Flow Free --- Nivel: {os.path.basename(ruta_archivo_a_cargar)} ---")
                    print(f"Color Activo: {info_color_str}") # Mostrar el último estado
                    tablero_actual.mostrar_tablero_consola()
                    if tablero_actual.tablero_esta_lleno():
                        mensaje_interfaz = "¡FELICIDADES! ¡Has resuelto el rompecabezas perfectamente!"
                    else:
                        mensaje_interfaz = "¡Todos los flujos conectados! Pero el tablero no está completamente lleno."
                    print(f"\n{mensaje_interfaz}")
                    partida_en_curso = False 
    
    # --- Fin del bucle while partida_en_curso ---
    if READCHAR_DISPONIBLE and partida_en_curso == False : # Si salió por victoria y readchar está activo
        pass # El mensaje ya se imprimió, solo esperar el input de abajo
    else: # Si salió por 'Q' o si readchar no está activo, limpiar e imprimir mensaje final
        limpiar_pantalla()
    
    print(f"\n--- Fin de la partida manual. ({mensaje_interfaz}) ---")
    input("Presiona Enter para volver al menú principal...")


if __name__ == "__main__":
    print("Este módulo está diseñado para ser importado por main.py")