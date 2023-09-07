import sys
import pygame
from pygame.locals import *
from copy import deepcopy

# Constantes
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (60, 179, 113)
AZUL = (253, 221, 202)
TAMANO_CASILLA = 50
MARGEN = 5

# Inicializar Pygame
pygame.init()

def iniciar_juego(tamaño_tablero):
    ANCHO = tamaño_tablero * (TAMANO_CASILLA + MARGEN) + MARGEN
    ALTO = ANCHO

    # Establecer la altura y el ancho de la pantalla
    dimensiones_pantalla = [ANCHO, ALTO]
    pantalla = pygame.display.set_mode(dimensiones_pantalla)

    # Establecer título de la pantalla
    pygame.display.set_caption("Reversi")

    # Inicializar tablero
    tablero = [[0 for x in range(tamaño_tablero)] for y in range(tamaño_tablero)]
    tablero[tamaño_tablero//2-1][tamaño_tablero//2-1] = 1
    tablero[tamaño_tablero//2][tamaño_tablero//2] = 1
    tablero[tamaño_tablero//2-1][tamaño_tablero//2] = -1
    tablero[tamaño_tablero//2][tamaño_tablero//2-1] = -1
    
    jugar(tablero, pantalla, tamaño_tablero)

def menu_inicio():
    fuente = pygame.font.Font(None, 36)
    fuente_grande = pygame.font.Font(None, 72)
    texto_titulo = fuente_grande.render("Reversi", True, BLANCO)
    rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 4))
    texto_jugar = fuente.render("Jugar", True, BLANCO)
    rect_jugar = texto_jugar.get_rect(center=(ANCHO // 2, ALTO // 2))
    texto_salir = fuente.render("Salir", True, BLANCO)
    rect_salir = texto_salir.get_rect(center=(ANCHO // 2, ALTO * 3 // 4))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if rect_jugar.collidepoint(event.pos):
                    seleccionar_tamaño()
                elif rect_salir.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pantalla.fill(VERDE)
        pantalla.blit(texto_titulo, rect_titulo)
        pantalla.blit(texto_jugar, rect_jugar)
        pantalla.blit(texto_salir, rect_salir)
        pygame.display.flip()

def seleccionar_tamaño():
    fuente = pygame.font.Font(None, 36)
    fuente_grande = pygame.font.Font(None, 38)
    texto_titulo = fuente_grande.render("Seleccione el tamaño del tablero", True, BLANCO)
    rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 4))
    texto_6x6 = fuente.render("6x6", True, BLANCO)
    rect_6x6 = texto_6x6.get_rect(center=(ANCHO // 2, ALTO // 2))
    texto_8x8 = fuente.render("8x8", True, BLANCO)
    rect_8x8 = texto_8x8.get_rect(center=(ANCHO // 2, ALTO * 3 // 4))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if rect_6x6.collidepoint(event.pos):
                    iniciar_juego(6)
                elif rect_8x8.collidepoint(event.pos):
                    iniciar_juego(8)
        pantalla.fill(VERDE)
        pantalla.blit(texto_titulo, rect_titulo)
        pantalla.blit(texto_6x6, rect_6x6)
        pantalla.blit(texto_8x8, rect_8x8)
        pygame.display.flip()

def dibujar_tablero(tablero, pantalla, tamaño_tablero, posiciones_validas):
    pantalla.fill(VERDE)

    for fila in range(tamaño_tablero):
        for columna in range(tamaño_tablero):
            color = AZUL
            pygame.draw.rect(pantalla,
                             color,
                             [(MARGEN + TAMANO_CASILLA) * columna + MARGEN,
                              (MARGEN + TAMANO_CASILLA) * fila + MARGEN,
                              TAMANO_CASILLA,
                              TAMANO_CASILLA])

            if tablero[fila][columna] == 1:
                pygame.draw.ellipse(pantalla, NEGRO, [(MARGEN + TAMANO_CASILLA) * columna + MARGEN,
                                                      (MARGEN + TAMANO_CASILLA) * fila + MARGEN,
                                                      TAMANO_CASILLA,
                                                      TAMANO_CASILLA])
            elif tablero[fila][columna] == -1:
                pygame.draw.ellipse(pantalla, BLANCO, [(MARGEN + TAMANO_CASILLA) * columna + MARGEN,
                                                       (MARGEN + TAMANO_CASILLA) * fila + MARGEN,
                                                       TAMANO_CASILLA,
                                                       TAMANO_CASILLA])

            if (fila, columna) in posiciones_validas:
                pygame.draw.circle(pantalla, NEGRO, ((TAMANO_CASILLA + MARGEN) * columna + TAMANO_CASILLA // 2,
                                                     (TAMANO_CASILLA + MARGEN) * fila + TAMANO_CASILLA // 2),
                                   TAMANO_CASILLA // 4)

    pygame.display.flip()

def jugar(tablero, pantalla, tamaño_tablero):
    turno_jugador = 1
    juego_terminado = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if not juego_terminado:
            posiciones_validas = obtener_posiciones_validas(tablero, turno_jugador)
            dibujar_tablero(tablero, pantalla, tamaño_tablero, posiciones_validas)

            if not posiciones_validas and not obtener_posiciones_validas(tablero, -turno_jugador):
                puntaje_jugador_humano = evaluar_tablero(tablero, 1)
                puntaje_IA = evaluar_tablero(tablero, -1)

                print("Juego terminado!")
                print("Puntaje Jugador Humano:", puntaje_jugador_humano)
                print("Puntaje IA:", puntaje_IA)

                if puntaje_jugador_humano > puntaje_IA:
                    print("Ganó el Jugador Humano!")
                elif puntaje_jugador_humano < puntaje_IA:
                    print("Ganó la IA!")
                else:
                    print("Empate!")

                juego_terminado = True

            if turno_jugador == 1:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        columna = event.pos[0] // (TAMANO_CASILLA + MARGEN)
                        fila = event.pos[1] // (TAMANO_CASILLA + MARGEN)

                        if (fila, columna) in posiciones_validas:
                            realizar_movimiento(tablero, fila, columna, turno_jugador)
                            turno_jugador = -turno_jugador
            else:
                mejor_jugada = obtener_mejor_jugada_IA(tablero, turno_jugador)
                if mejor_jugada is not None:
                    realizar_movimiento(tablero, mejor_jugada[0], mejor_jugada[1], turno_jugador)
                    turno_jugador = -turno_jugador
                else:
                    turno_jugador = -turno_jugador

def obtener_posiciones_validas(tablero, jugador):
    posiciones_validas = []
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            if es_posicion_valida(tablero, fila, columna, jugador):
                posiciones_validas.append((fila, columna))
    return posiciones_validas

def es_posicion_valida(tablero, fila, columna, jugador):
    if tablero[fila][columna] != 0:
        return False

    direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for direccion in direcciones:
        fila_temp = fila + direccion[0]
        columna_temp = columna + direccion[1]
        hay_ficha_oponente = False

        while 0 <= fila_temp < len(tablero) and 0 <= columna_temp < len(tablero[0]):
            if tablero[fila_temp][columna_temp] == -jugador:
                hay_ficha_oponente = True
            elif (tablero[fila_temp][columna_temp] == jugador) and hay_ficha_oponente:
                return True
            else:
                break

            fila_temp += direccion[0]
            columna_temp += direccion[1]

    return False

def realizar_movimiento(tablero, fila, columna, jugador):
    tablero[fila][columna] = jugador
    direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for direccion in direcciones:
        fila_temp = fila + direccion[0]
        columna_temp = columna + direccion[1]
        hay_ficha_oponente = False
        fichas_a_voltear = []

        while 0 <= fila_temp < len(tablero) and 0 <= columna_temp < len(tablero[0]):
            if tablero[fila_temp][columna_temp] == -jugador:
                hay_ficha_oponente = True
                fichas_a_voltear.append((fila_temp, columna_temp))
            elif (tablero[fila_temp][columna_temp] == jugador) and hay_ficha_oponente:
                for ficha in fichas_a_voltear:
                    tablero[ficha[0]][ficha[1]] = jugador
                break
            else:
                break

            fila_temp += direccion[0]
            columna_temp += direccion[1]

def evaluar_tablero(tablero, jugador):
    puntaje = 0
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            if tablero[fila][columna] == jugador:
                puntaje += 1
            elif tablero[fila][columna] == -jugador:
                puntaje -= 1
    return puntaje

def minimax(tablero, profundidad, alfa, beta, jugador):
    if profundidad == 0:
        return evaluar_tablero(tablero, jugador)

    posiciones_validas = obtener_posiciones_validas(tablero, jugador)
    if not posiciones_validas:
        return evaluar_tablero(tablero, jugador)

    if jugador == 1:
        mejor_valor = -float('inf')
        for posicion in posiciones_validas:
            tablero_temp = deepcopy(tablero)
            realizar_movimiento(tablero_temp, posicion[0], posicion[1], jugador)
            valor = minimax(tablero_temp, profundidad - 1, alfa, beta, -jugador)
            mejor_valor = max(mejor_valor, valor)
            alfa = max(alfa, valor)
            if beta <= alfa:
                break
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for posicion in posiciones_validas:
            tablero_temp = deepcopy(tablero)
            realizar_movimiento(tablero_temp, posicion[0], posicion[1], jugador)
            valor = minimax(tablero_temp, profundidad - 1, alfa, beta, -jugador)
            mejor_valor = min(mejor_valor, valor)
            beta = min(beta, valor)
            if beta <= alfa:
                break
        return mejor_valor

def obtener_mejor_jugada_IA(tablero, jugador):
    posiciones_validas = obtener_posiciones_validas(tablero, jugador)
    mejor_valor = float('-inf')
    mejor_jugada = None

    for posicion in posiciones_validas:
        tablero_temp = deepcopy(tablero)
        realizar_movimiento(tablero_temp, posicion[0], posicion[1], jugador)
        valor = minimax(tablero_temp, 3, float('-inf'), float('inf'), -jugador)

        if valor > mejor_valor:
            mejor_valor = valor
            mejor_jugada = posicion

    return mejor_jugada

if __name__ == "__main__":
    ANCHO = 8 * (TAMANO_CASILLA + MARGEN) + MARGEN
    ALTO = ANCHO
    pantalla = pygame.display.set_mode((ANCHO, ALTO))

    menu_inicio()

