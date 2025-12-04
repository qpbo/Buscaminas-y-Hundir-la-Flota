# 🎮 Buscaminas y Hundir la Flota - Proyecto Python

Proyecto grupal de Python desarrollado por el **Dream Team** que implementa dos juegos clásicos de terminal: **Buscaminas** y **Hundir la Flota**.

---

## 📋 Descripción

Este programa ofrece dos juegos completos jugables desde la terminal:

### 💣 Buscaminas
Un juego de lógica donde debes descubrir todas las casillas sin pisar ninguna mina.

**Características:**
- 3 niveles de dificultad (Fácil, Intermedio, Difícil)
- Sistema de banderas para marcar minas sospechosas
- Expansión automática cuando encuentras casillas vacías
- Interfaz de terminal clara y fácil de usar

### ⚓ Hundir la Flota (Battleship)
El clásico juego naval donde debes hundir toda la flota enemiga antes de que hundan la tuya.

**Características:**
- Modo Jugador vs Jugador (local)
- Modo Jugador vs Computadora con 3 niveles de IA
- Colocación manual o aleatoria de barcos
- Sistema de detección Agua/Tocado/Hundido

---

## 🚀 Requisitos

- **Python 3.6 o superior**
- Sistema operativo: Windows, Linux o macOS
- Terminal/Consola con soporte para caracteres Unicode (para los emojis y símbolos)

---

## 📥 Instalación

1. **Clona o descarga este repositorio:**
   ```bash
   git clone https://github.com/qpbo/Buscaminas-y-Hundir-la-Flota.git
   cd Propuesta_Carliyo
   ```

2. **Verifica que tienes Python instalado:**
   ```bash
   python --version
   ```
   
   Si no tienes Python, descárgalo desde [python.org](https://www.python.org/downloads/)

---

## ▶️ Cómo Ejecutar

### Método 1: Ejecutar el programa principal
```bash
python main.py
```

### Método 2: Ejecutar cada juego individualmente

**Para jugar solo al Buscaminas:**
```bash
python buscaminas.py
```

**Para jugar solo a Hundir la Flota:**
```bash
python hundir_flota.py
```

---

## 🎯 Cómo Jugar

### Buscaminas

1. Selecciona el nivel de dificultad:
   - **Fácil:** Tablero 8×10 con 10 minas
   - **Intermedio:** Tablero 16×16 con 40 minas
   - **Difícil:** Tablero 30×16 con 99 minas

2. En cada turno puedes:
   - **R (Revelar):** Descubrir una casilla
   - **F (Flag/Bandera):** Marcar una casilla como sospechosa
   - **S (Salir):** Abandonar el juego

3. Introduce las coordenadas:
   - **Columna:** Letra (A, B, C, ...)
   - **Fila:** Número (1, 2, 3, ...)

4. **Objetivo:** Descubre todas las casillas sin minas
   - Si pisas una mina: **¡Pierdes!** 💥
   - Si descubres todas las casillas seguras: **¡Ganas!** 🎉

**Leyenda del tablero:**
- `▢` = Casilla oculta
- `⚑` = Bandera (mina sospechosa)
- `·` = Casilla vacía (0 minas vecinas)
- `1-8` = Número de minas en casillas adyacentes

---

### Hundir la Flota

1. **Elige el modo de juego:**
   - **Jugador vs Jugador:** Dos personas juegan localmente
   - **Jugador vs Computadora:** Juega contra la IA

2. **Si juegas contra la computadora, elige la dificultad:**
   - **Fácil:** Disparos completamente aleatorios
   - **Intermedio:** Al tocar un barco, busca alrededor
   - **Difícil:** Usa estrategia avanzada con patrones

3. **Coloca tu flota** (5 barcos en total):
   - 1 Portaaviones (5 casillas)
   - 1 Acorazado (4 casillas)
   - 2 Cruceros (3 casillas cada uno)
   - 1 Lancha de Reconocimiento (2 casillas)

   Para cada barco puedes:
   - **Opción 1:** Colocarlo manualmente (elige posición y orientación)
   - **Opción 2:** Colocación aleatoria

4. **Juega por turnos:**
   - Introduce coordenadas para disparar (ej: columna A, fila 5)
   - El juego te dirá si fue:
     - 💧 **Agua:** No hay nada
     - 💥 **Tocado:** Le diste a un barco
     - 🔥 **Hundido:** Barco completamente destruido

5. **Objetivo:** Hundir todos los barcos enemigos antes de que hundan los tuyos

**Leyenda del tablero:**
- `~` = Agua
- `B` = Tu barco
- `X` = Parte de barco tocada
- `O` = Disparo fallado (agua)

---

## 📁 Estructura del Proyecto

```
Propuesta_Carliyo/
│
├── main.py              # Menú principal - Punto de entrada del programa
├── buscaminas.py        # Lógica completa del juego Buscaminas
├── hundir_flota.py      # Lógica completa del juego Hundir la Flota
├── README.md            # Este archivo - Documentación
└── CONTEXTO_PROYECTO.txt # Documentación técnica completa del proyecto
```

### Descripción de cada archivo:

- **`main.py`:** 
  - Menu principal con opciones para elegir juego
  - Importa y ejecuta los módulos de los juegos
  - Manejo de errores y salida elegante

- **`buscaminas.py`:**
  - Creación y gestión del tablero
  - Colocación aleatoria de minas
  - Cálculo de minas vecinas
  - Sistema de revelado y expansión automática
  - Marcado de banderas
  - Detección de victoria/derrota

- **`hundir_flota.py`:**
  - Creación de tableros para ambos jugadores
  - Colocación de barcos (manual/aleatoria)
  - Sistema de turnos
  - Inteligencia Artificial con 3 niveles
  - Detección de impactos y hundimientos
  - Modo PvP y PvC

---

## 👥 Equipo de Desarrollo

Este es un proyecto grupal desarrollado por el **Dream Team**:
- **ASIR (Administración de Sistemas Informáticos en Red)**
- **Asignatura:** Optativa - Introducción a Python
- **Fecha:** Diciembre 2025

---

## 🔧 Características Técnicas

### Buscaminas
- Tableros dinámicos de diferentes tamaños
- Algoritmo recursivo para expansión automática
- Generación aleatoria de minas sin repetición
- Validación de coordenadas del usuario
- Sistema de banderas independiente

### Hundir la Flota
- Validación de posiciones de barcos (sin solapamiento ni adyacencia)
- IA con 3 niveles:
  - **Fácil:** Random puro
  - **Intermedio:** Búsqueda inteligente tras impacto
  - **Difícil:** Patrón de tablero de ajedrez + búsqueda inteligente
- Detección automática de barcos hundidos
- Gestión de turnos alternados
- Dos tableros por jugador (propio y de disparos)

---

## 🐛 Solución de Problemas

### El programa no arranca
- Verifica que tienes Python 3.6 o superior: `python --version`
- Asegúrate de estar en la carpeta correcta: `cd Propuesta_Carliyo`
- Intenta ejecutar con: `python3 main.py` (en Linux/Mac)

### Los símbolos se ven mal
- Tu terminal necesita soporte para Unicode/UTF-8
- En Windows: Usa PowerShell o Windows Terminal
- Actualiza la terminal a una versión más reciente

### Error "ModuleNotFoundError"
- Asegúrate de que todos los archivos estén en la misma carpeta
- Ejecuta desde la carpeta `Propuesta_Carliyo`: `cd Propuesta_Carliyo && python main.py`

---

## 📝 Notas para el Desarrollo

Este código está ampliamente comentado para facilitar:
- La comprensión de todos los miembros del equipo
- El trabajo colaborativo en GitHub
- La presentación del proyecto
- Futuras modificaciones y mejoras

Cada función tiene:
- **Docstring** explicando qué hace
- **Comentarios** sobre la lógica importante
- **Nombres descriptivos** de variables y funciones

---

## 🎓 Aprendizajes del Proyecto

Este proyecto cubre:
- ✅ Estructuras de datos (listas, listas bidimensionales)
- ✅ Funciones y modularización
- ✅ Bucles y condicionales
- ✅ Recursividad (expansión en Buscaminas)
- ✅ Generación de números aleatorios
- ✅ Validación de entrada del usuario
- ✅ Algoritmos de búsqueda (IA en Hundir la Flota)
- ✅ Importación de módulos
- ✅ Manejo de excepciones
- ✅ Documentación de código

---

## 📜 Licencia

Este proyecto es solo para fines educativos.

---

## 📞 Contacto

Para preguntas sobre este proyecto, contacta a cualquier miembro del equipo.

---

**¡Disfruta jugando!** 🎮🎉
