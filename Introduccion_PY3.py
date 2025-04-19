import pygame
import configparser
import modonormal

NEGRO  = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE  = (0, 255, 0)
ROJO   = (255, 0, 0)

tamPantalla = [527, 398]
pantalla = pygame.display.set_mode(tamPantalla)
pygame.display.set_caption("POKEMON")

def pokemon_init():
    matrizPokemon = []
    parser = configparser.ConfigParser()
    parser.read("pokemon/pokemon.cfg")
    # Cargar pokémon de la sección Generacion1
    data = parser.get("Generacion1", "pokemones").split("\n")
    for pokemon in data:
        fila = []
        cadena = ""
        # Separar campos por espacios (maneja múltiples espacios)
        for i in range(len(pokemon)):
            if pokemon[i] != " ":
                cadena += pokemon[i]
                if i + 1 == len(pokemon):
                    fila.append(cadena)
                    cadena = ""
            else:
                if len(cadena):
                    fila.append(cadena)
                cadena = ""
        # Convertir estadísticas numéricas a enteros
        if len(fila) >= 6:
            fila[1] = int(fila[1]); fila[2] = int(fila[2]); fila[3] = int(fila[3])
            fila[4] = int(fila[4]); fila[5] = int(fila[5])
            fila.append(int(fila[5]))  # PS actuales iniciales
        matrizPokemon.append(fila)
    # Calcular experiencia inicial
    for poke in matrizPokemon:
        poke[3] = (4 * (poke[1] ** 3)) // 5
    # Cargar sprites de cada Pokémon (suponiendo 65x65 por sprite en fila)
    for i, poke in enumerate(matrizPokemon):
        filename = f"img/pokemones/{i+1}.png"
        image = pygame.image.load(filename)
        imagen_ancho, imagen_alto = image.get_size()
        alto, ancho = 65, 65
        # Dividir la tira de sprites en cuadros individuales
        for x in range(imagen_ancho // ancho):
            cuadro = (x * ancho, 0, ancho, alto)
            poke.append(image.subsurface(cuadro))
        print(f"Cargando Pokémon: {poke[0]} ... Ok")
    return matrizPokemon

def imagenes(tamano, posicion, ruta):
    imagen = pygame.image.load(ruta)
    imagen = pygame.transform.scale(imagen, tamano)
    pantalla.blit(imagen, posicion)
    pygame.display.flip()

def Presentacion():
    reloj = pygame.time.Clock()
    pag, ver_pag, terminar = 1, True, False
    while not terminar and ver_pag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
                return terminar
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pantalla.fill(NEGRO)
                    ver_pag = False
        if pag == 1:
            imagenes(tamPantalla, [0, 0], "img/Pinicial/inicial1.jpg")
            reloj.tick(0.5)
        if pag == 2:
            imagenes(tamPantalla, [0, 0], "img/Pinicial/inicial2.jpg")
            reloj.tick(0.7)
        if pag == 3:
            imagenes([260, 80], [133, 310], "img/Pinicial/barespa.png")
        pag += 1
    return False

def Introduccion(terminar):
    reloj = pygame.time.Clock()
    pag, ver_pag = 1, True
    while not terminar and ver_pag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
                return terminar
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pag += 1
                    pantalla.fill(NEGRO)
        if pag == 1:
            imagenes([527, 308], [0, 0], "img/Introduccion/Oak1.png")
            imagenes([400, 80], [60, 310], "img/Introduccion/Introduccion1.png")
            reloj.tick(0.7)
        if pag == 2:
            imagenes([527, 308], [0, 0], "img/Introduccion/OakLab.png")
            imagenes([400, 80], [60, 310], "img/Introduccion/Introduccion2.png")
            reloj.tick(0.7)
        if pag == 3:
            imagenes([527, 308], [0, 0], "img/Introduccion/Oak2.png")
            imagenes([400, 80], [60, 310], "img/Introduccion/Introduccion3.png")
            reloj.tick(0.7)
        if pag == 4:
            imagenes([527, 308], [0, 0], "img/Introduccion/Oak3.png")
            imagenes([400, 80], [60, 310], "img/Introduccion/Introduccion4.png")
            reloj.tick(0.7)
        if pag == 5:
            imagenes([527, 308], [0, 0], "img/Introduccion/Nieto.png")
            imagenes([400, 80], [60, 310], "img/Introduccion/Introduccion5.png")
            reloj.tick(0.7)
        if pag == 6:
            imagenes([527, 308], [0, 0], "img/Introduccion/Blue.png")
            imagenes([400, 80], [60, 310], "img/Introduccion/Introduccion6.png")
            reloj.tick(0.7)
        if pag == 7:
            imagenes([527, 308], [0, 0], "img/Introduccion/Vs.png")
            imagenes([400, 80], [60, 310], "img/Introduccion/Introduccion7.png")
            reloj.tick(0.7)
        if pag == 8:
            ver_pag = False
        # Indicador de tecla (tecla A para avanzar)
        imagenes([20, 20], [480, 330], "img/Teclado/A.png")
    return terminar

def Controles(terminar):
    reloj = pygame.time.Clock()
    pag, ver_pag = 1, True
    while not terminar and ver_pag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
                return terminar
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pag += 1
                    pantalla.fill(NEGRO)
        if pag == 1:
            imagenes([527, 398], [0, 0], "img/Controles/Controles.jpg")
            reloj.tick(0.7)
        if pag == 2:
            ver_pag = False
        imagenes([20, 20], [480, 330], "img/Teclado/A.png")
    return terminar

if __name__ == '__main__':
    pokemones = pokemon_init()
    pygame.init()
    pygame.mixer.music.load("sound/introduccion.ogg")
    pygame.mixer.music.play(-1)

    presentacion = Presentacion()
    introduccion = Introduccion(presentacion)
    controles = Controles(introduccion)

    pygame.mixer.music.stop()
    # Iniciar modo de juego normal con el mapa interior inicial
    modonormal.main("maps/interior.map", introduccion, pokemones, False, False, False)
