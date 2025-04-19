import pygame

# Asume que ya has cargado la imagen
image = pygame.image.load('maps/interior.png')
tile_width = 32  # Tamaño de cada tile
tile_height = 32

# Verifica la dimensión de la imagen cargada
print(f"Imagen cargada con dimensiones: {image.get_width()}x{image.get_height()}")

# Prueba para ver si se están extrayendo bien los tiles
tile_rect = pygame.Rect(0, 0, tile_width, tile_height)  # Aquí tomamos el primer tile (columna 0, fila 0)
tile_image = image.subsurface(tile_rect)

# Muestra el tile extraído
pygame.init()
screen = pygame.display.set_mode((tile_width, tile_height))
screen.blit(tile_image, (0, 0))
pygame.display.flip()

# Espera hasta que el jugador cierre la ventana para comprobar si el tile está bien cargado
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
