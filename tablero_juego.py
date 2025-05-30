# FlowFree/tablero_juego.py

import copy

class TableroJuego:
    """
    Representa el tablero del juego Flow Free.
    Almacena la cuadrícula, las dimensiones, y la información de los colores
    (puntos de inicio y fin, y los caminos actuales).
    Las celdas pueden ser:
    - Letra de color (ej: 'R'): Punto de inicio/fin o parte de un camino.
    - '.' (punto): Celda vacía transitable.
    - '#' (almohadilla): Pared, no transitable.
    """
    CARACTER_VACIO = '.'
    CARACTER_PARED = '#'

    def __init__(self, filas_cuadricula, pares_colores_originales=None, caminos_actuales=None):
        if not filas_cuadricula:
            raise ValueError("Las filas de la cuadrícula no pueden estar vacías.")

        self.alto = len(filas_cuadricula)
        self.ancho = len(filas_cuadricula[0])
        self.cuadricula_base_con_paredes = [list(fila) for fila in filas_cuadricula]
        self.cuadricula = [list(fila) for fila in filas_cuadricula] 

        if pares_colores_originales is None:
            self.pares_colores = self._encontrar_pares_colores(self.cuadricula_base_con_paredes)
        else:
            self.pares_colores = pares_colores_originales

        if caminos_actuales is None:
            self.caminos = {
                color: [detalles['inicio']] for color, detalles in self.pares_colores.items()
            }
        else:
            self.caminos = caminos_actuales
            self._actualizar_cuadricula_de_trabajo_desde_caminos()


    def _actualizar_cuadricula_de_trabajo_desde_caminos(self):
        self.cuadricula = [list(fila) for fila in self.cuadricula_base_con_paredes]
        for color, ruta in self.caminos.items():
            if not ruta: continue
            for f, c in ruta:
                celda_base = self.cuadricula_base_con_paredes[f][c]
                if celda_base == self.CARACTER_VACIO or celda_base == color:
                    self.cuadricula[f][c] = color
                elif celda_base == self.CARACTER_PARED:
                     # Esto solo debería ser una advertencia si la lógica de movimiento es incorrecta
                    pass # print(f"ADVERTENCIA: Camino de {color} intenta dibujar sobre pared en ({f},{c}) al actualizar cuadrícula.")


    def _encontrar_pares_colores(self, cuadricula_para_analisis):
        puntos_extremos = {}
        for f in range(self.alto):
            for c in range(self.ancho):
                caracter = cuadricula_para_analisis[f][c]
                if caracter != self.CARACTER_VACIO and caracter != self.CARACTER_PARED:
                    if caracter not in puntos_extremos:
                        puntos_extremos[caracter] = []
                    puntos_extremos[caracter].append((f, c))

        info_pares_colores = {}
        for color, puntos in puntos_extremos.items():
            if len(puntos) != 2:
                raise ValueError(f"El color '{color}' no tiene exactamente dos puntos. Encontrados: {puntos}")
            puntos.sort()
            info_pares_colores[color] = {'inicio': puntos[0], 'fin': puntos[1]}
        return info_pares_colores

    def obtener_colores(self):
        return list(self.pares_colores.keys())

    def obtener_colores_estado(self):
        estado_colores = {}
        for color_char, detalles in self.pares_colores.items():
            estado_colores[color_char] = {
                'inicio': detalles['inicio'],
                'fin': detalles['fin'],
                'completado': self.camino_esta_completo(color_char)
            }
        return estado_colores

    def mostrar_tablero_consola(self):
        print("\n" + "-" * (self.ancho * 2 + 3))
        for f in range(self.alto):
            fila_str = "| "
            for c in range(self.ancho):
                fila_str += str(self.cuadricula[f][c]) + " "
            fila_str += "|"
            print(fila_str)
        print("-" * (self.ancho * 2 + 3))

    def es_posicion_valida(self, f, c):
        return 0 <= f < self.alto and 0 <= c < self.ancho

    def camino_esta_completo(self, color_char):
        if color_char not in self.pares_colores: return False
        punto_final_esperado = self.pares_colores[color_char]['fin']
        camino_actual = self.caminos.get(color_char, [])
        return camino_actual and camino_actual[-1] == punto_final_esperado

    def todos_los_caminos_completos(self):
        for color_char in self.obtener_colores():
            if not self.camino_esta_completo(color_char):
                return False
        return True

    def tablero_esta_lleno(self):
        for f in range(self.alto):
            for c in range(self.ancho):
                if self.cuadricula[f][c] == self.CARACTER_VACIO:
                    return False
        return True

    def intentar_extender_camino(self, color_char, direccion):
        if self.camino_esta_completo(color_char):
            return False, f"El camino del color {color_char} ya está completo."

        camino_actual = self.caminos[color_char]
        if not camino_actual: # No debería pasar si se inicializa con el punto de inicio
            return False, f"Error interno: Camino para {color_char} está vacío."
            
        cabeza_f, cabeza_c = camino_actual[-1]

        nf, nc = cabeza_f, cabeza_c
        if direccion == 'arriba':   nf -= 1
        elif direccion == 'abajo':  nf += 1
        elif direccion == 'izquierda': nc -= 1
        elif direccion == 'derecha':  nc += 1
        else:
            return False, "Dirección no válida."

        if not self.es_posicion_valida(nf, nc):
            return False, "Movimiento fuera del tablero."

        valor_celda_destino = self.cuadricula[nf][nc]
        punto_final_color_actual = self.pares_colores[color_char]['fin']

        if valor_celda_destino == self.CARACTER_PARED:
            return False, "No se puede mover hacia una pared ('#')."
        
        if valor_celda_destino == self.CARACTER_VACIO:
            pass
        elif (nf, nc) == punto_final_color_actual:
            if self.cuadricula_base_con_paredes[nf][nc] != color_char:
                return False, f"Error interno: El punto final esperado {nf},{nc} para {color_char} no es {color_char} en la base."
            pass
        elif valor_celda_destino == color_char:
            if (nf,nc) in camino_actual: # Evita pisarse a sí mismo
                 return False, f"El camino de {color_char} no puede cruzarse a sí mismo."
            # Si no está en el camino actual pero es del mismo color (y no es el final), es un error o un estado inválido.
            return False, f"Celda ya ocupada por el mismo color {color_char} (pero no es el final ni parte del camino actual)."
        else: 
            return False, f"Celda ({nf},{nc}) ocupada por '{valor_celda_destino}' (otro color o camino)."

        self.cuadricula[nf][nc] = color_char
        self.caminos[color_char].append((nf, nc))

        if (nf, nc) == punto_final_color_actual:
            return True, f"¡Color {color_char} completado!"
        return True, "Movimiento exitoso."


    def deshacer_ultimo_paso(self, color_char):
        camino = self.caminos.get(color_char)
        if not camino or len(camino) <= 1:
            return False, "No hay suficientes pasos para deshacer en este color."

        pos_a_borrar_f, pos_a_borrar_c = camino.pop()
        caracter_base_en_pos = self.cuadricula_base_con_paredes[pos_a_borrar_f][pos_a_borrar_c]

        if caracter_base_en_pos == self.CARACTER_VACIO:
            self.cuadricula[pos_a_borrar_f][pos_a_borrar_c] = self.CARACTER_VACIO
        elif caracter_base_en_pos == color_char: 
            self.cuadricula[pos_a_borrar_f][pos_a_borrar_c] = color_char 
        else:
            # Si la base era una pared u otro color, y se dibujó encima,
            # al deshacer debería volver a ser '.' si el camino pasó por ahí.
            # La lógica actual asume que solo se dibuja sobre '.' o el propio endpoint.
            # Si la celda base no era '.' ni el propio color, es un caso anómalo para deshacer.
            # Lo más seguro es volverla '.' si no es un endpoint del color actual.
             if (pos_a_borrar_f, pos_a_borrar_c) != self.pares_colores[color_char]['inicio'] and \
                (pos_a_borrar_f, pos_a_borrar_c) != self.pares_colores[color_char]['fin']:
                 self.cuadricula[pos_a_borrar_f][pos_a_borrar_c] = self.CARACTER_VACIO
             # Si era un endpoint, ya se maneja arriba.

        return True, f"Último paso de {color_char} deshecho."


    def __eq__(self, otro):
        if not isinstance(otro, TableroJuego): return False
        return self.cuadricula == otro.cuadricula and self.caminos == otro.caminos

    def __hash__(self):
        cuadricula_tupla = tuple(map(tuple, self.cuadricula))
        caminos_items_ordenados = sorted(self.caminos.items())
        caminos_tupla_final = []
        for color, ruta_lista in caminos_items_ordenados:
            caminos_tupla_final.append((color, tuple(ruta_lista)))
        return hash((cuadricula_tupla, tuple(caminos_tupla_final)))

    def generar_copia_profunda(self):
        filas_cuadricula_base_str = ["".join(fila) for fila in self.cuadricula_base_con_paredes]
        caminos_copiados = copy.deepcopy(self.caminos)
        nuevo_tablero = TableroJuego(
            filas_cuadricula_base_str,
            pares_colores_originales=self.pares_colores, 
            caminos_actuales=caminos_copiados
        )
        return nuevo_tablero

# --- Funciones auxiliares ---
def cargar_nivel_desde_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()

        # Quitar solo saltos de línea/retorno de carro, preservar espacios internos
        filas_cuadricula_str = []
        for linea_raw in lineas:
            linea_procesada = linea_raw.rstrip('\n\r')
            if linea_procesada: # Solo añadir si no está completamente vacía después de quitar saltos
                filas_cuadricula_str.append(linea_procesada)
        
        if not filas_cuadricula_str: # Si todas las líneas estaban vacías o solo eran saltos
            print(f"Error: El archivo '{ruta_archivo}' está vacío o no contiene filas de datos válidas.")
            return None

        longitud_primera_fila = len(filas_cuadricula_str[0])
        for i, fila in enumerate(filas_cuadricula_str):
            if len(fila) != longitud_primera_fila:
                print(f"Error: La fila {i+1} ('{fila}') en '{ruta_archivo}' tiene longitud {len(fila)}, se esperaba {longitud_primera_fila}.")
                return None
        return TableroJuego(filas_cuadricula_str)
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado '{ruta_archivo}'")
        return None
    except ValueError as ve:
        print(f"Error al procesar el contenido del nivel '{ruta_archivo}': {ve}")
        return None
    except Exception as e:
        print(f"Error inesperado al cargar el nivel '{ruta_archivo}': {e}")
        return None