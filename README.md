# 🎮 Texas Hold'em - Edición Premium Oro

<img width="901" height="636" alt="image" src="https://github.com/Alejandro-Mendieta/TEXAS-HOLD-EM/blob/main/ASSETS/FOTOS/FOTO.png?raw=true" />
<img width="901" height="636" alt="image" src="https://github.com/Alejandro-Mendieta/TEXAS-HOLD-EM/blob/main/ASSETS/FOTOS/FOTO1.png?raw=true" />

![Estado](https://img.shields.io/badge/Estado-Completado%20✅-brightgreen?style=for-the-badge&logo=rocket)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg?style=for-the-badge)
![License](https://img.shields.io/badge/Licencia-MIT-yellow.svg?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0%20Premium-cyan?style=for-the-badge)
![Multiplayer](https://img.shields.io/badge/Multijugador-4%20Jugadores-orange?style=for-the-badge)

Un juego de Poker Texas Hold'em premium con diseño de lujo en oro y negro, sistema de login completo e inteligencia artificial avanzada. Desarrollado en Python con Pygame.

## ✨ Características Premium

### 🎯 Jugabilidad Mejorada
- **Texas Hold'em completo** con todas las rondas: Pre-flop, Flop, Turn, River y Showdown
- **Sistema de apuestas avanzado** con blinds automáticos, calls, raises y all-ins
- **Evaluación automática** de manos según las reglas oficiales del poker
- **4 jugadores** (1 humano + 3 IA) con personalidades únicas
- **Sistema de dealer** rotativo y blinds progresivos

### 🔐 Sistema de Usuarios
- **Registro y login** seguro con base de datos JSON
- **Perfiles persistentes** con estadísticas individuales
- **Sistema de fichas** que se mantiene entre sesiones
- **Historial de partidas** y progreso guardado automáticamente

### 🎨 Interfaz de Lujo
- **Tema Premium Oro y Negro** con diseño de casino exclusivo
- **Efectos de partículas** doradas para victorias y acciones
- **Cartas premium** con detalles dorados y plateados
- **Animaciones fluidas** y transiciones suaves
- **Mesa ovalada** con patrones geométricos dorados
- **Tipografía elegante** con fuentes premium

### 🤖 Inteligencia Artificial Avanzada
- **Tres personalidades distintas**:
  - **🤝 Ana (Agresiva)**: Apuesta frecuentemente y toma riesgos calculados
  - **🛡️ Luis (Conservador)**: Juego seguro y estratégico
  - **🎭 Mia (Impredecible)**: Comportamiento variable y sorpresivo
- **Toma de decisiones** basada en fuerza de mano y contexto de juego
- **Tiempos de reacción** realistas que simulan pensamiento humano

## 🚀 Instalación y Ejecución

### Requisitos del Sistema
- **Python 3.8** o superior
- **Pygame 2.5.2** o superior
- **Sistema operativo**: Windows, Linux o macOS

### Instalación Rápida

```bash
# Clonar el repositorio (si está en GitHub)
git clone https://github.com/Alejandro-Mendieta/TEXAS-HOLD-EM.git
cd TEXAS-HOLD-EM

# Instalar Pygame
pip install pygame

# Ejecutar el juego
python POKER.py
```

### Verificación de Instalación

```bash
# Verificar versión de Python
python --version

# Verificar instalación de Pygame
python -c "import pygame; print(pygame.version.ver)"
```

## 🎮 Controles del Juego

### Durante el Juego
- **FOLD** 🚫: Retirarse de la mano actual
- **CALL** ✅: Igualar la apuesta actual
- **RAISE** ⬆️: Aumentar la apuesta
- **ALL-IN** 🎯: Apostar todas las fichas disponibles
- **ESC** ↩️: Volver al menú principal

### Navegación General
- **Clic izquierdo** 🖱️: Seleccionar opciones y botones
- **TAB** ↹: Cambiar entre campos en el login
- **ENTER** ⏎: Confirmar en formularios
- **ESC** 🚪: Salir del juego o volver atrás

## 🃏 Reglas del Texas Hold'em

### Desarrollo de la Partida
1. **PRE-FLOP** 📦: Cada jugador recibe 2 cartas privadas
2. **FLOP** 🌊: Se revelan 3 cartas comunitarias
3. **TURN** 🔄: Se revela la 4ª carta comunitaria  
4. **RIVER** 🏞️: Se revela la 5ª carta comunitaria
5. **SHOWDOWN** 🃏: Los jugadores muestran sus manos

### Sistema de Apuestas
- **Small Blind**: 50% de la apuesta mínima
- **Big Blind**: Apuesta mínima completa
- **Ronda de apuestas** después de cada revelación de cartas
- **All-in**: Cuando un jugador apuesta todas sus fichas

### Jerarquía de Manos
1. **🃏 Escalera Real** (A-K-Q-J-10 del mismo palo)
2. **🌟 Escalera de Color** (5 cartas consecutivas del mismo palo)
3. **🎯 Póker** (4 cartas del mismo valor)
4. **🏠 Full House** (trío + par)
5. **💎 Color** (5 cartas del mismo palo)
6. **📈 Escalera** (5 cartas consecutivas)
7. **🎲 Trío** (3 cartas del mismo valor)
8. **👥 Doble Par** (2 pares de cartas)
9. **📊 Par** (2 cartas del mismo valor)
10. **🔼 Carta Alta** (ninguna de las anteriores)

## 🎨 Características Visuales Premium

### Diseño Oro y Negro
- **Paleta de colores** exclusiva con tonos dorados y negros de lujo
- **Cartas personalizadas** con fondos dorados para figuras y plateados para números
- **Avatares circulares** con efectos de brillo y bordes dorados
- **Mesa de juego** con patrones geométricos concéntricos

### Efectos Visuales
- **Sistema de partículas** con efectos de oro, diamantes y brillos
- **Animaciones de cartas** con sombras y reflejos
- **Efectos de hover** en botones con degradados dorados
- **Paneles transparentes** con efecto cristal
- **Texto con brillo** dinámico en títulos importantes

## 🤖 Sistema de IA Mejorado

### Personalidades Detalladas

#### 🤝 Ana - Estrategia Agresiva
- **Fuerza base**: +30% sobre cálculo normal
- **Frecuencia de raises**: Alta
- **Tolerancia al riesgo**: Elevada
- **Ideal para**: Jugadores que buscan acción rápida

#### 🛡️ Luis - Estrategia Conservadora  
- **Fuerza base**: -30% sobre cálculo normal
- **Frecuencia de folds**: Moderada-Alta
- **Tolerancia al riesgo**: Baja
- **Ideal para**: Partidas estratégicas y calculadas

#### 🎭 Mia - Estrategia Impredecible
- **Fuerza base**: Variable (50% - 150%)
- **Comportamiento**: Aleatorio controlado
- **Factor sorpresa**: Alto
- **Ideal para**: Mantener la partida interesante

### Toma de Decisiones
```python
# Algoritmo de decisión basado en:
1. Fuerza de mano actual
2. Cartas comunitarias visibles
3. Comportamiento de otros jugadores
4. Tamaño del bote
5. Fichas restantes
6. Personalidad asignada
```

## 💾 Sistema de Progreso

### Estadísticas Guardadas
- **📊 Partidas jugadas** totales
- **🏆 Partidas ganadas** y ratio de victorias
- **💰 Fichas acumuladas** en el perfil
- **🕐 Fecha de registro** y última conexión
- **📈 Progreso individual** por usuario

### Archivos de Datos
```
TEXAS-HOLD-EM/
├── 📁 ASSETS/                 # Recursos gráficos
├── 📄 POKER.py               # Juego principal
├── 📊 usuarios_poker.json    # Base de datos de usuarios
├── 📋 requirements.txt       # Dependencias
└── 📖 README.md             # Documentación
```

## 🛠️ Estructura del Código

### Arquitectura Principal
```python
PokerGame()                    # Clase principal del juego
├── Jugador()                 # Sistema de jugadores
├── Carta()                   # Sistema de cartas premium  
├── EstadoJuego               # Máquina de estados
└── SistemaParticulas()       # Efectos visuales

SistemaLogin()                # Autenticación de usuarios
├── cargar_usuarios()         # Gestión de base de datos
├── registrar_usuario()       # Registro nuevo
└── login_usuario()          # Autenticación
```

### Módulos Importantes
- **🎨 Renderizado UI**: Interfaz premium con efectos
- **🎯 Lógica de Juego**: Reglas y mecánicas del poker
- **🤖 IA**: Comportamiento de jugadores artificiales
- **💾 Persistencia**: Guardado y carga de datos
- **✨ Efectos**: Sistema de partículas y animaciones

## 🐛 Solución de Problemas

### Errores Comunes y Soluciones

#### ❌ "invalid color argument"
```python
# Solución: Usar superficies con alpha correctamente
brillo_surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
color_correcto = (255, 255, 255, alpha)  # RGBA con alpha al final
```

#### ❌ "ModuleNotFoundError: No module named 'pygame'"
```bash
# Solución: Reinstalar Pygame
pip uninstall pygame
pip install pygame==2.5.2
```

#### ❌ El juego se cierra al hacer clic en "Jugar"
```python
# Solución: Verificar que todos los jugadores estén inicializados
# El código actual incluye protecciones contra este error
```

### Optimización de Rendimiento

#### Para sistemas con recursos limitados:
```python
# En el código, reducir:
FPS = 30  # En lugar de 60
particulas = 20  # Reducir cantidad de efectos
```

#### Mejoras de rendimiento incluidas:
- ✅ Lazy loading de recursos
- ✅ Pool de partículas reutilizable
- ✅ Verificación de nulidad en renderizado
- ✅ Optimización de colisiones y detección

## 🎨 Personalización Avanzada

### Modificar Dificultad IA
```python
# En la clase Jugador, método tomar_decision_ia()
if self.personalidad == "agresiva":
    fuerza *= 1.3  # Aumentar para mayor dificultad
```

### Añadir Nuevos Efectos
```python
# En el sistema de partículas
crear_particulas(x, y, cantidad=50, tipo="nuevo_efecto")
```

### Personalizar Apariencia
```python
# En el diccionario COLORES
COLORES["MI_ORO"] = (255, 200, 0)  # Color personalizado
```

## 🔄 Flujo del Juego

```
LOGIN → MENÚ PRINCIPAL → PARTIDA
     ├── NUEVA MANO → PRE-FLOP → FLOP → TURN → RIVER → SHOWDOWN
     ├── ESTADÍSTICAS (Ver progreso)
     └── SALIR (Guardado automático)
```

## 🤝 Contribuciones

### 🎯 Áreas de Mejora Bienvenidas
1. **🎵 Sistema de Sonido**: Efectos de audio y música ambiental
2. **🌐 Multijugador Online**: Conexión en red para partidas remotas
3. **📱 Interfaz Táctil**: Optimización para dispositivos táctiles
4. **🎨 Más Temas**: Nuevos esquemas de color y diseños
5. **🤖 IA Avanzada**: Algoritmos más complejos de toma de decisiones

### Proceso de Contribución
1. 🍴 Hacer fork del proyecto
2. 🌿 Crear una rama para la feature (`git checkout -b feature/AmazingFeature`)
3. 💾 Hacer commit de los cambios (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push a la rama (`git push origin feature/AmazingFeature`)
5. 🔄 Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para más detalles.

**Permisos incluyen**:
- ✅ Uso comercial
- ✅ Distribución
- ✅ Modificación
- ✅ Uso privado

## 👨‍💻 Desarrollo

**Desarrollado por Alejandro Mendieta**

Creado con ❤️ usando Python y Pygame. Este proyecto implementa las mejores prácticas modernas de desarrollo de juegos con una arquitectura escalable para futuras expansiones.

### Características Técnicas Destacadas
- **🏗️ Arquitectura modular** y fácil de mantener
- **🎨 Sistema de renderizado** optimizado
- **💾 Persistencia de datos** robusta
- **🎯 IA configurable** y expansible
- **📱 Interfaz responsive** y accesible

---

## 🚀 Próximas Características Planeadas

### 🎮 Mejoras de Jugabilidad
- [ ] **🏆 Sistema de torneos** con eliminatorias
- [ ] **📊 Estadísticas avanzadas** y gráficos de progreso
- [ ] **🎯 Modo desafío** con objetivos específicos
- [ ] **👥 Más jugadores IA** con personalidades adicionales

### 🌐 Funcionalidades Online
- [ ] **🔗 Multijugador en red** para partidas online
- [ ] **📱 Versión web** usando Pygame Web
- [ ] **☁️ Sincronización en la nube** de progreso

### 🎨 Mejoras Visuales
- [ ] **🎞️ Animaciones 3D** para cartas y fichas
- [ ] **🎨 Temas dinámicos** que cambian automáticamente
- [ ] **✨ Más efectos de partículas** y transiciones

### 🤖 IA Avanzada
- [ ] **🧠 Machine Learning** para IA adaptativa
- [ ] **📈 Análisis de estrategia** en tiempo real
- [ ] **🎭 Personalidades dinámicas** que evolucionan

---

**¿Listo para jugar?** 🎯 ¡Inicia el juego y experimenta el Texas Hold'em más premium en Python!

```bash
python POKER.py
```

**¡Que comiencen las apuestas!** ♠️♥️♦️♣️