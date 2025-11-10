# 🎮 Texas Hold'em

<img width="901" height="636" alt="image" src="https://github.com/Alejandro-Mendieta/TEXAS-HOLD-EM/blob/main/ASSETS/FOTOS/FOTO.png?raw=true" />

![Estado](https://img.shields.io/badge/Estado-En%20Proceso-brightgreen?style=for-the-badge&logo=rocket)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/Licencia-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-1.0-cyan)

Un juego de Poker Texas Hold'em completamente funcional con interfaz moderna, efectos visuales avanzados e inteligencia artificial mejorada. Desarrollado en Python con Pygame.

## ✨ Características Principales

### 🎯 Jugabilidad
- **Texas Hold'em completo** con todas las rondas: Pre-flop, Flop, Turn y River
- **Sistema de apuestas** realista con blinds, calls, raises y all-ins
- **Evaluación automática** de manos según las reglas oficiales del poker
- **Múltiples jugadores IA** con diferentes personalidades

### 🎨 Interfaz Visual
- **Temas intercambiables** (Clásico, Nocturno, Lujo)
- **Efectos de partículas** para victorias, apuestas y transiciones
- **Animaciones suaves** para cartas y fichas
- **Texto con efectos** de brillo y resplandor
- **Mesa ovalada** con diseño profesional de casino

### 🤖 Inteligencia Artificial
- **Tres personalidades distintas**:
  - **Agresiva**: Apuesta frecuentemente y toma riesgos
  - **Conservadora**: Juego seguro y calculado
  - **Impredecible**: Comportamiento variable y sorpresivo
- **Tiempo de decisión** realista que simula pensamiento humano
- **Evaluación de fuerza** de mano adaptativa por ronda

### 💾 Sistema de Progreso
- **Estadísticas persistentes** (partidas jugadas, ganadas, mejores manos)
- **Guardado automático** de progreso
- **Récords personales** y historial de juego
- **Sistema de puntuación** detallado

## 🚀 Instalación y Ejecución

### Requisitos del Sistema
- **Python 3.8** o superior
- **Pygame 2.5** o superior
- **Sistema operativo**: Windows, Linux o macOS

### Instalación de Dependencias

```bash
# Instalar Pygame
pip install pygame

# O instalar desde requirements.txt
pip install -r requirements.txt
```

### Ejecutar el Juego

```bash
# Ejecutar directamente
python POKER.py

# O si está en un entorno virtual
python3 POKER.py
```

## 🎮 Controles del Juego

### Durante el Juego
- **Fold**: Retirarse de la mano actual
- **Call**: Igualar la apuesta actual
- **Raise**: Aumentar la apuesta
- **All-in**: Apostar todas las fichas disponibles
- **ESC**: Volver al menú principal

### Navegación
- **Clic izquierdo**: Seleccionar opciones y botones
- **ESC**: Salir del juego o volver atrás

## 🃏 Reglas del Texas Hold'em

### Desarrollo de la Partida
1. **Pre-flop**: Cada jugador recibe 2 cartas privadas
2. **Flop**: Se revelan 3 cartas comunitarias
3. **Turn**: Se revela la 4ª carta comunitaria
4. **River**: Se revela la 5ª carta comunitaria
5. **Showdown**: Los jugadores muestran sus manos

### Jerarquía de Manos
1. **Escalera Real** (A-K-Q-J-10 del mismo palo)
2. **Escalera de Color** (5 cartas consecutivas del mismo palo)
3. **Póker** (4 cartas del mismo valor)
4. **Full House** (trío + par)
5. **Color** (5 cartas del mismo palo)
6. **Escalera** (5 cartas consecutivas)
7. **Trío** (3 cartas del mismo valor)
8. **Doble Par** (2 pares de cartas)
9. **Par** (2 cartas del mismo valor)
10. **Carta Alta** (ninguna de las anteriores)

## 🎨 Personalización

### Temas Disponibles
- **Clásico**: Verde tradicional de casino
- **Nocturno**: Azul oscuro elegante
- **Lujo**: Tono marrón premium

### Efectos Visuales
- Partículas de confeti en victorias
- Efectos de fichas al apostar
- Brillos en cartas comunitarias
- Animaciones de hover en botones

## 🏆 Sistema de Estadísticas

El juego guarda automáticamente:
- **Partidas totales** jugadas
- **Partidas ganadas**
- **Mejor mano** conseguida
- **Mayor bote** ganado
- **Fichas totales** acumuladas
- **Fecha** de la última partida

## 🛠️ Estructura del Proyecto

```
POKER/
├── POKER.py                 # Archivo principal del juego
├── estadisticas_poker.json  # Datos guardados (se crea automáticamente)
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🐛 Solución de Problemas

### Error común: "invalid color argument"
```python
# Si aparece este error, asegurarse de usar:
pygame.Surface((ancho, alto), pygame.SRCALPHA)
# Para superficies con transparencia
```

### Rendimiento en sistemas lentos
- Reducir `FPS` en la línea 25 del código
- Disminuir la cantidad de partículas en efectos
- Usar el tema "Clásico" que requiere menos recursos

## 📝 Personalización Avanzada

### Modificar personalidades IA
En la clase `Jugador`, ajustar los multiplicadores:
```python
if self.personalidad == "agresiva":
    fuerza *= 1.2  # Aumentar para más agresividad
```

### Añadir nuevos temas
En el diccionario `TEMAS`, agregar nueva configuración:
```python
"NuevoTema": {
    "VERDE_MESA": (R, G, B),
    "VERDE_OSCURO": (R, G, B),
    # ... más colores
}
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:

1. Reportar bugs o problemas
2. Sugerir nuevas características
3. Mejorar la inteligencia artificial
4. Añadir nuevos temas visuales
5. Optimizar el rendimiento

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👨‍💻 Desarrollo
Por Alejandro Mendieta

creado con ❤️ usando Python y Pygame. Incluye las mejores prácticas modernas de desarrollo de juegos y una arquitectura escalable para futuras mejoras.

---

## 🎯 Próximas Características

- [ ] Modo torneo con eliminatorias
- [ ] Más personalidades de IA
- [ ] Efectos de sonido realistas
- [ ] Modo multijugador en red
- [ ] Sistema de logros y recompensas
- [ ] Tutorial interactivo para principiantes

---
