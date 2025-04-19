# coding=utf-8
import pygame
import configparser
import math
import random
import Batalla

# Constantes de color y tamaños
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
tamCuadro = 32       # Tamaño de cada cuadro (tile) en píxeles
tamPantalla = [527, 398]  # Resolución de la ventana de juego
tamJugador = 48      # Tamaño del sprite del jugador (cada frame es 48x48)

# ---------------------------------------------------------------------------
# CLASES
# ---------------------------------------------------------------------------

class Mapa(object):
    def __init__(self, filename):
        self.filename = filename
        # Cargar y parsear el archivo de mapa (.map)
        self.parser = configparser.ConfigParser()
        self.parser.read(filename)
        # Leer el texto del mapa y crear lista de filas
        self.map = self.parser.get("level", "map").split("\n")
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.tileset = self.parser.get("level", "tileset")
        # Cargar la imagen del tileset
        try:
            self.image = pygame.image.load(self.tileset)
        except Exception as e:
            print(f"Error cargando la imagen del tileset: {e}")
            raise
        # Escala del tileset desde el archivo (.map)
        self.scale = int(self.parser.get("level", "scale"))
        if self.scale != 1:
            orig_w, orig_h = self.image.get_size()
            self.image = pygame.transform.scale(
                self.image, (orig_w * self.scale, orig_h * self.scale)
            )
        # Verificar alineación del tileset a la cuadrícula de 32px
        tileset_width, tileset_height = self.image.get_size()
        if tileset_width % tamCuadro != 0 or tileset_height % tamCuadro != 0:
            print(f"Advertencia: Las dimensiones del tileset ({tileset_width}x{tileset_height}) pueden no alinearse con cuadros de {tamCuadro}px.")
        else:
            print(f"Tileset '{self.tileset}' alineado a una cuadrícula de {tamCuadro}px.")
        print(f"Dimensiones del tileset: {tileset_width}x{tileset_height}")

        # Crear matriz de superficies para cada tile del mapa
        self.matrizMap = []
        for x in range(self.width):
            columna = []
            for y in range(self.height):
                letra = self.map[y][x]
                imagen_tile = self.obtener_imagen_tile(letra)
                columna.append(imagen_tile)
            self.matrizMap.append(columna)

    def obtener_imagen_tile(self, letra):
        # Determinar las coordenadas del tile dentro del tileset según la letra
        if letra == "A":      # Árbol (usado en exteriores)
            column, row = 0, 0
        elif letra == "#":    # Pared (muros interiores)
            column, row = 0, 1
        elif letra == "P":    # Hierba alta / Pokémon salvaje (exteriores)
            column, row = 2, 0
        elif letra == ".":    # Suelo vacío / camino
            column, row = 0, 3
        elif letra == "I":    # Punto de inicio (entrada de jugador)
            column, row = 4, 0
        elif letra == "p":    # Objeto interior (p.ej., alfombra o mesa)
            column, row = 3, 0
        else:
            return None  # Tile desconocido (espacio vacío o sin gráfico)
        # Extraer el tile correspondiente del tileset
        try:
            tile_surface = self.image.subsurface(pygame.Rect(column * tamCuadro, row * tamCuadro, tamCuadro, tamCuadro))
        except ValueError:
            print(f"Error: coordenadas de tile fuera de rango para '{letra}' -> ({column},{row})")
            return None
        return tile_surface

    def dibujar(self, pantalla):
        # Dibujar todos los tiles del mapa sobre la superficie 'pantalla'
        for y in range(self.height):
            for x in range(self.width):
                imagen_tile = self.matrizMap[x][y]
                if imagen_tile:
                    pantalla.blit(imagen_tile, (x * tamCuadro, y * tamCuadro))

class Jugador(object):
    def __init__(self, imagen):
        # Cargar spritesheet del jugador y dividirla en matriz [frame][dirección]
        self.image = pygame.image.load(imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tamJugador * 3, tamJugador * 4))
        imagen_ancho, imagen_alto = self.image.get_size()
        self.matrizJugador = []
        for frame in range(3):  # 3 cuadros de animación por dirección
            fila = []
            for dir in range(4):  # 4 direcciones (0=Up,1=Down,2=Left,3=Right)
                cuadro = (frame * tamJugador, dir * tamJugador, tamJugador, tamJugador)
                fila.append(self.image.subsurface(cuadro))
            self.matrizJugador.append(fila)
        # Posición en píxeles del jugador
        self.pos = [0, 0]
        self.sprite = self.matrizJugador[1][1]  # Sprite inicial (mirando hacia abajo)
        # Atributos del jugador
        self.pokemones = []
        self.seleccionar_pokemon = True
        self.aviso_sin_pokemon = False
        self.city = False
        self.ultima_batalla = []   # Posición del último encuentro Pokémon (para no repetir inmediato)
        # Flags de historia / misiones
        self.oak_conversacion = True
        self.duelo_Blue = True
        self.duelo_Brock = False

    def ubicar(self, city):
        # Posicionar al jugador en el punto de inicio 'I' del mapa dado (city)
        pos_tile = [0, 0]
        try:
            # Buscar coordenadas del tile 'I' en el mapa
            for idx, fila in enumerate(city.map):
                if "I" in fila:
                    pos_tile[0] = fila.index("I")
                    pos_tile[1] = idx
                    break
        except ValueError:
            pos_tile = [0, 0]
        # Convertir coordenadas del tile de inicio a píxeles en la pantalla
        pixel_unit = tamCuadro // city.scale
        self.pos[0] = (pos_tile[0] * city.scale - city.parser.getint("level", "iniciox")) * pixel_unit
        self.pos[1] = (pos_tile[1] * city.scale - city.parser.getint("level", "inicioy")) * pixel_unit - (tamJugador - tamCuadro)
        # Ajustar sprite inicial (mirando hacia abajo)
        self.sprite = self.matrizJugador[1][1]

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, (int(self.pos[0]), int(self.pos[1])))

    def transfM(self, city):
        # Convertir la posición del jugador en píxeles a coordenadas de la matriz del mapa (tile x,y)
        tile_x = int((((self.pos[0] * city.scale) // tamCuadro) + city.parser.getint("level", "iniciox")) // city.scale)
        tile_y = int(((((self.pos[1] + (tamJugador - tamCuadro)) * city.scale) // tamCuadro) + city.parser.getint("level", "inicioy")) // city.scale)
        return tile_x, tile_y

    def is_a_wall(self, city, direc):
        # Determinar si en la dirección dada hay un obstáculo (muro/árbol/agua)
        posx, posy = self.transfM(city)
        try:
            if direc == "left" and city.map[posy][posx - 1] in ["#", "A", "c", "W"]:
                return True
            if direc == "right" and city.map[posy][posx + 1] in ["#", "A", "c", "W"]:
                return True
            if direc == "up" and city.map[posy - 1][posx] in ["#", "A", "c", "W"]:
                return True
            if direc == "down" and city.map[posy + 1][posx] in ["#", "A", "c", "W"]:
                return True
        except IndexError:
            # Fuera de los límites del mapa se considera obstáculo (borde)
            return True
        return False

# ---------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL DEL MODO "NORMAL" (EXPLORACIÓN)
# ---------------------------------------------------------------------------

def main(archivo_mapa, terminar, pokemones, jugador_inicial, ciudad_inicial, ciudades_iniciales):
    pygame.init()
    pantalla = pygame.display.set_mode(tamPantalla)
    pantalla.fill(NEGRO)
    # Permitir pulsación continua de teclas (para movimiento fluido)
    pygame.key.set_repeat(200, 100)

    # Cargar el mapa inicial
    mapa = Mapa(archivo_mapa)
    print(f"Cargando mapa: {archivo_mapa}")

    # Crear jugador si no existe y ubicarlo en el mapa
    if not jugador_inicial:
        jugador_inicial = {"pokemones": pokemones}
    jugador = Jugador("red.png")
    jugador.pokemones = pokemones  # Asignar la lista de pokémon cargados al jugador
    jugador.ubicar(mapa)

    # Mensaje de bienvenida (simple)
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render('¡Bienvenido al juego!', True, BLANCO)
    pantalla.blit(texto, (tamPantalla[0] // 2 - texto.get_width() // 2,
                           tamPantalla[1] // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

    # Bucle principal del juego (exploración)
    reloj = pygame.time.Clock()
    while not terminar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminar = True

                elif event.key == pygame.K_UP:
                    tx, ty = jugador.transfM(mapa)
                    # Salir por la parte superior del mapa (p.ej., de Pueblo Paleta a Ruta 1)
                    if ty == 0 and mapa.map[ty][tx] not in ["#", "A", "c", "W"]:
                        next_map_file = None
                        if "pueblopaleta.map" in mapa.filename:
                            next_map_file = "maps/ruta1.map"
                        elif "ruta1.map" in mapa.filename:
                            next_map_file = "maps/ciudadverde.map"
                        if next_map_file:
                            mapa = Mapa(next_map_file)
                            print(f"Cambiando al mapa: {next_map_file}")
                            # Ubicar jugador en la entrada inferior del nuevo mapa
                            ex, ey = tx, mapa.height - 1
                            jugador.pos[0] = (ex * mapa.scale - mapa.parser.getint("level", "iniciox")) * (tamCuadro // mapa.scale)
                            jugador.pos[1] = (ey * mapa.scale - mapa.parser.getint("level", "inicioy")) * (tamCuadro // mapa.scale) - (tamJugador - tamCuadro)
                            jugador.ultima_batalla = []
                            continue
                    if not jugador.is_a_wall(mapa, "up"):
                        jugador.pos[1] -= tamCuadro
                        jugador.sprite = jugador.matrizJugador[1][0]  # mirar hacia arriba
                        tx, ty = jugador.transfM(mapa)
                        # Entrar a un edificio (puerta) desde afuera
                        if mapa.map[ty][tx] == "E":
                            next_map_file = None
                            if "pueblopaleta.map" in mapa.filename:
                                next_map_file = "maps/lab.map"
                            elif "ciudadverde.map" in mapa.filename:
                                next_map_file = "maps/centropokemon.map"
                            if next_map_file:
                                mapa = Mapa(next_map_file)
                                print(f"Entrando al mapa: {next_map_file}")
                                # Ubicar jugador justo dentro de la puerta del nuevo mapa
                                ex, ey = 0, 0
                                for j, line in enumerate(mapa.map):
                                    if "I" in line:
                                        ex, ey = line.index("I"), j
                                        break
                                jugador.pos[0] = (ex * mapa.scale - mapa.parser.getint("level", "iniciox")) * (tamCuadro // mapa.scale)
                                jugador.pos[1] = (ey * mapa.scale - mapa.parser.getint("level", "inicioy")) * (tamCuadro // mapa.scale) - (tamJugador - tamCuadro)
                                jugador.ultima_batalla = []
                                continue
                        # Posible encuentro Pokémon salvaje al moverse
                        if mapa.map[ty][tx] == "P":
                            if (ty, tx) != tuple(jugador.ultima_batalla) and random.random() < 0.25:
                                jugador.ultima_batalla = [ty, tx]
                                pokemon_enemigo = random.choice(pokemones)
                                print(f"¡Un {pokemon_enemigo[0]} salvaje apareció!")
                                Batalla.main(jugador, [pokemon_enemigo], 0, True, pokemones, [])

                elif event.key == pygame.K_DOWN:
                    tx, ty = jugador.transfM(mapa)
                    # Salir por la parte inferior del mapa (p.ej., de un edificio al exterior)
                    if ty == mapa.height - 1 and mapa.map[ty][tx] not in ["#", "A", "c", "W"]:
                        next_map_file = None
                        if "ruta1.map" in mapa.filename:
                            next_map_file = "maps/pueblopaleta.map"
                        elif "ciudadverde.map" in mapa.filename:
                            next_map_file = "maps/ruta1.map"
                        elif "lab.map" in mapa.filename or "interior.map" in mapa.filename:
                            next_map_file = "maps/pueblopaleta.map"
                        elif "centropokemon.map" in mapa.filename or "tienda.map" in mapa.filename or "gimnasio.map" in mapa.filename:
                            next_map_file = "maps/ciudadverde.map"
                        if next_map_file:
                            mapa = Mapa(next_map_file)
                            print(f"Saliendo al mapa: {next_map_file}")
                            # Ubicar jugador en la entrada superior del nuevo mapa
                            ex, ey = tx, 0
                            jugador.pos[0] = (ex * mapa.scale - mapa.parser.getint("level", "iniciox")) * (tamCuadro // mapa.scale)
                            jugador.pos[1] = (ey * mapa.scale - mapa.parser.getint("level", "inicioy")) * (tamCuadro // mapa.scale) - (tamJugador - tamCuadro)
                            jugador.ultima_batalla = []
                            continue
                    if not jugador.is_a_wall(mapa, "down"):
                        jugador.pos[1] += tamCuadro
                        jugador.sprite = jugador.matrizJugador[1][1]  # mirar hacia abajo
                        tx, ty = jugador.transfM(mapa)
                        # (No hay entrada de edificio hacia abajo en este juego)
                        if mapa.map[ty][tx] == "P":
                            if (ty, tx) != tuple(jugador.ultima_batalla) and random.random() < 0.25:
                                jugador.ultima_batalla = [ty, tx]
                                pokemon_enemigo = random.choice(pokemones)
                                print(f"¡Un {pokemon_enemigo[0]} salvaje apareció!")
                                Batalla.main(jugador, [pokemon_enemigo], 0, True, pokemones, [])

                elif event.key == pygame.K_LEFT:
                    tx, ty = jugador.transfM(mapa)
                    if not jugador.is_a_wall(mapa, "left"):
                        jugador.pos[0] -= tamCuadro
                        jugador.sprite = jugador.matrizJugador[1][2]  # mirar hacia la izquierda
                        tx, ty = jugador.transfM(mapa)
                        if mapa.map[ty][tx] == "P":
                            if (ty, tx) != tuple(jugador.ultima_batalla) and random.random() < 0.25:
                                jugador.ultima_batalla = [ty, tx]
                                pokemon_enemigo = random.choice(pokemones)
                                print(f"¡Un {pokemon_enemigo[0]} salvaje apareció!")
                                Batalla.main(jugador, [pokemon_enemigo], 0, True, pokemones, [])

                elif event.key == pygame.K_RIGHT:
                    tx, ty = jugador.transfM(mapa)
                    if not jugador.is_a_wall(mapa, "right"):
                        jugador.pos[0] += tamCuadro
                        jugador.sprite = jugador.matrizJugador[1][3]  # mirar hacia la derecha
                        tx, ty = jugador.transfM(mapa)
                        if mapa.map[ty][tx] == "P":
                            if (ty, tx) != tuple(jugador.ultima_batalla) and random.random() < 0.25:
                                jugador.ultima_batalla = [ty, tx]
                                pokemon_enemigo = random.choice(pokemones)
                                print(f"¡Un {pokemon_enemigo[0]} salvaje apareció!")
                                Batalla.main(jugador, [pokemon_enemigo], 0, True, pokemones, [])

        # Dibujar escena: fondo negro, luego mapa y jugador
        pantalla.fill(NEGRO)
        mapa.dibujar(pantalla)
        jugador.dibujar(pantalla)
        pygame.display.flip()
        reloj.tick(60)
    return terminar
