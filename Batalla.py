# coding=utf-8
import pygame
import configparser  # Cambié ConfigParser a configparser para Python 3
import modonormal
import random

# Constantes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
tamPantalla = [527, 398]

# Convertir Letra a una Imagen:
def convertLI(letra):
    return "img/Batalla/" + letra + ".png"

class Estado(object):
    # Pokemon -> Objeto Pokemon
    # posM -> Posicion del marco
    # posN -> Posicion del nombre
    # posL -> Posicion del nivel (level)
    # posB -> Posicion de la barra de vida
    def __init__(self, pokemon, posM, posN, posL, posB):
        # Marco
        self.marco = pygame.image.load("img/Batalla/estado_pokemon.png")
        self.marco_pos = posM
        # Datos del pokemon
        self.pokemon = pokemon
        # Nombre del pokemon:
        self.nombre = list(self.pokemon[0].upper())
        self.posi_nombre = posN
        for i in range(len(self.nombre)):  # Convertir cadena en vector de imagenes:
            self.nombre[i] = [convertLI(self.nombre[i]), (self.posi_nombre[0] + i * 10, self.posi_nombre[1])]
        # Nivel del pokemon:
        self.nivel = list(str(self.pokemon[1]))
        self.posi_nivel = posL
        for i in range(len(self.nivel)):  # Convertir cadena en vector de imagenes:
            self.nivel[i] = [convertLI(self.nivel[i]), (self.posi_nivel[0] + i * 6, self.posi_nivel[1])]

        # Barra de salud
        self.ps_barra = pygame.image.load("img/Batalla/ps_barra.png")
        self.ps_vacio = pygame.image.load("img/Batalla/ps_vacio.png")
        self.status = []
        for i in range(10):  # La barra se divide en 10 secciones:
            self.status.append([self.ps_barra, (posB[0] + i * 9, posB[1])])

    # Mostrar por pantalla el marco y la barra de vida:
    def mostrar(self, pantalla):
        pantalla.blit(self.marco, self.marco_pos)
        for barrita in self.status:
            pantalla.blit(barrita[0], barrita[1])
        for letra in self.nombre:
            img = pygame.image.load(letra[0])
            pantalla.blit(img, letra[1])
        for numero in self.nivel:
            img = pygame.image.load(numero[0])
            pantalla.blit(img, numero[1])

    # Actualizar PS, Nombre y Nivel
    def calc_ps(self):
        # PS
        vida = self.pokemon[5]
        limvida = self.pokemon[6]
        porcion = limvida / 10.0
        for i in range(len(self.status)):
            if vida > porcion * (i):
                self.status[i][0] = self.ps_barra
            else:
                self.status[i][0] = self.ps_vacio
        # Nombre:
        self.nombre = list(self.pokemon[0].upper())
        for i in range(len(self.nombre)):  # Convertir cadena en vector de imagenes:
            self.nombre[i] = [convertLI(self.nombre[i]), (self.posi_nombre[0] + i * 10, self.posi_nombre[1])]
        # Nivel:
        self.nivel = list(str(self.pokemon[1]))
        for i in range(len(self.nivel)):  # Convertir cadena en vector de imagenes:
            self.nivel[i] = [convertLI(self.nivel[i]), (self.posi_nivel[0] + i * 6, self.posi_nivel[1])]


class Cursor(object):
    def __init__(self):
        self.image = pygame.image.load("img/Batalla/cursor.png")
        # Dominio de posiciones validas en las que puede estar el cursor
        self.posicion_validas = {}
        self.posicion_validas["Capturar"] = (388, 304)
        self.posicion_validas["Huir"] = (440, 345)
        self.posicion_validas["Lucha"] = (308, 304)
        self.posicion_validas["Pokemon"] = (308, 345)
        self.posicion_validas["Placaje"] = (10, 302)
        self.posicion = self.posicion_validas["Lucha"]  # Posicion inicial (actual)

    def cambiar_pos(self, item):
        try:
            self.posicion = self.posicion_validas[item]
        except KeyError:
            pass

    def mostrar(self, pantalla):
        pantalla.blit(self.image, self.posicion)


class Pokemon(object):
    def __init__(self, pokemones, sentido=True):
        self.pokemones = pokemones  # Matriz de Pokemones
        # Buscar Pokemon inicial (Primer pokemon con PS > 0)
        for poke in self.pokemones:
            if poke[5] > 0:
                self.pokemon = poke
                break
        self.contPok = 0  # Contador Pokemon
        image_ancho, imagen_alto = self.pokemon[7].get_size()
        # Imagen frontal
        self.imageF = pygame.transform.scale(self.pokemon[7], (image_ancho * 2, imagen_alto * 2))
        self.posF = [319, 36]
        # Imagen Trasera
        self.imageP = pygame.transform.scale(self.pokemon[8], (image_ancho * 2, imagen_alto * 2))
        self.posP = [76, 133]
        self.sentido = sentido
        if self.sentido:
            self.image = self.imageP
            self.pos = self.posP
        else:
            self.image = self.imageF
            self.pos = self.posF
        self.terminar_duelo = False

    def mostrar(self, pantalla):
        pantalla.blit(self.image, self.pos)

    def cambiar_Pokemon(self):
        image_ancho, imagen_alto = self.pokemon[7].get_size()
        # Imagen frontal
        self.imageF = pygame.transform.scale(self.pokemon[7], (image_ancho * 2, imagen_alto * 2))
        # Imagen Trasera
        self.imageP = pygame.transform.scale(self.pokemon[8], (image_ancho * 2, imagen_alto * 2))
        if self.sentido:
            self.image = self.imageP
        else:
            self.image = self.imageF

    def subir_nivel(self):
        # Calcular nivel en función de la experiencia:
        n = ((self.pokemon[3] * 5.0) / 4) ** (1.0 / 3)
        self.pokemon[1] = int(n)

    def atacar(self, enemigo, pantalla, tipo_combate):  # Atacar Pokemon Enemigo
        e = [0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 4]  # Dominio de efectividad
        # Variables para el calculo del daño
        E = e[random.randrange(0, 10)]  # Efectividad del ataque
        V = random.randrange(85, 101)  # Variacion del daño
        P = 50  # Potencia del Placaje
        N = self.pokemon[1]  # Nivel del pokemon atacante
        # DAÑO CAUSADO AL OPONENTE:
        reloj = pygame.time.Clock()
        self.pos[0] += 20
        self.mostrar(pantalla)
        pygame.display.flip()
        reloj.tick(20)
        self.pos[0] -= 40
        self.mostrar(pantalla)
        pygame.display.flip()
        reloj.tick(20)
        self.pos[0] += 20
        self.mostrar(pantalla)
        pygame.display.flip()
        reloj.tick(20)

        D = 0.01 * E * V * (2 + ((0.2 * N + 1) * P) / 25)
        enemigo.pokemon[5] -= D

        # Calcular Experiencia ganada (Cuando el pokemon enemigo es derrotado)
        if enemigo.pokemon[5] <= 0:
            if not tipo_combate:
                C = 1  # Pokemon Salvaje
            else:
                C = 1.5  # Entrenador Pokemon
            exp = (enemigo.pokemon[3] * enemigo.pokemon[1] * C) / 7
            self.pokemon[3] += exp  # Subir experiencia
            self.subir_nivel()  # Verificar si aumenta de nivel

            # Si el contador pokemon es igual a la longitud de los pokemones enemigos
            # enemigos, quiere decir que fue completamente derrotado
            if enemigo.contPok == len(enemigo.pokemones) - 1:
                self.terminar_duelo = True
            # Enemigo cambia de pokemon
            if len(enemigo.pokemones) > 1 and not self.terminar_duelo:
                enemigo.contPok += 1
                enemigo.pokemon = enemigo.pokemones[enemigo.contPok]
                enemigo.cambiar_Pokemon()


# Función principal:
def main(jugador, enemigo, tipo_combate, terminar, matrizPokemon, Ciudades_INIT):
    # Parametros iniciales:
    pygame.init()
    pantalla = pygame.display.set_mode(tamPantalla)
    pantalla.fill(NEGRO)
    reloj = pygame.time.Clock()
    turno_enemigo = False
    pygame.mixer.music.load("sound/batalla.ogg")
    pygame.mixer.music.play(-1)

    # Código para la animación y la lógica de combate...

    while not terminar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
            # Aquí manejamos las teclas y las opciones del combate...
            
            # Ejemplo de uso de print corregido:
            print("¡GANAS LA BATALLA!")
            
        pygame.display.flip()
