# PYOKEMON-2.0-game
Taller de universdad
# pokemon-game
este es un juego basico y perfecto para practica en el github.

# 🕹️ Pyokemon 2.0

**Pyokemon 2.0** es un juego de Pokémon por consola hecho en Python. Está diseñado como una práctica educativa para aprender estructuras de datos, modularidad y trabajo con archivos. Inspirado en el universo Pokémon, cuenta con combates, exploración, efectos sonoros y almacenamiento en la nube.

---

## 📦 Requisitos

- Python 3.10 o superior
- windows(recomendado)
- Git (opcional, para clonar el repositorio)
- Conexión a internet 

---

## 📥 Instalación

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/Arturo2023-byte/pokemon-game.git
   cd pokemon-game
   
Ejecuta el juego con:

            python Introduccion_PY3.py

              
🎮 Características del juego: 

✅ Menú interactivo por consola

✅ Batallas contra pokémon salvajes

✅ Recolección y almacenamiento de pokémon

✅ Módulo de música de fondo y efectos de sonido

✅ Colores y animaciones en texto gracias a conversion de datos originales del juego con us debida licencia

Estructura del proyecto:

PYOKEMON 2.0/
│
├── Introduccion_PY3.py              # 🟡 Archivo principal que inicia el juego (menú e intro)
├── modonormal.py                    # 🟠 Modo de exploración del mundo (carga de mapas, movimiento)
├── Batalla.py                       # 🔴 Módulo que maneja las batallas Pokémon
├── config.py                        # ⚙️  (Opcional) Configuraciones generales
│
├── maps/                            # 🗺️ Carpeta con todos los mapas y tilesets
│   ├── interior.map                 # Casa inicial
│   ├── pueblopaleta.map            # Pueblo exterior
│   ├── centropokemon.map           # Centro Pokémon
│   ├── ciudadverde.map             # Ciudad Verde
│   ├── gimnasio.map                # Gimnasio Pokémon
│   ├── lab.map                     # Laboratorio
│   ├── tienda.map                  # Tienda
│   ├── ruta1.map                   # Ruta
│   ├── interior.png                # Tileset para interiores (160x128 px, tiles de 32x32)
│   ├── pueblopaleta.png            # Tileset para exteriores (160x128 px)
│   ├── ...                         # Otros tilesets en resolución 160x128, alineados a 32x32
│
├── sprites/                         # 👤 Carpeta con sprites de personajes
│   ├── red.png                     # Personaje jugable (tamaño 32x48 px recomendado)
│   ├── npcs/                       # Otros personajes
│
├── audio/                           # 🔊 Carpeta con música y efectos de sonido
│   ├── intro.mp3                   # Música de introducción
│   ├── batalla.mp3                 # Música de batalla
│   ├── ...
│
├── saves/                           # 💾 Carpeta donde guardar progreso (opcional)
│
└── README.md                        # 📘 Instrucciones del proyecto

📄 Licencia
Proyecto académico sin fines comerciales. Basado en el universo Pokémon, propiedad de Nintendo/GameFreak.

✨ Autor
Desarrollado por Arturo2023-byte
Colaboración y asistencia: ChatGPT
