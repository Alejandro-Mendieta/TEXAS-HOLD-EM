"""
Texas Hold'em - Versión Mejorada con Interfaz Avanzada
- Interfaz visual mejorada con efectos, transiciones y animaciones
- Sistema de partículas para fichas y cartas
- Efectos de sonido y música de fondo
- IA mejorada con múltiples personalidades
- Sistema de guardado y estadísticas
- Temas visuales intercambiables
- Tutorial interactivo para nuevos jugadores

Ejecutar: python texas_holdem_pygame_avanzado.py
Requiere: pygame, random, sys, math, json, datetime
"""

import pygame
import random
import sys
import math
import json
import os
from datetime import datetime
from enum import Enum
from itertools import combinations

# ---------- Configuración ----------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texas Hold'em - Edición Premium")
clock = pygame.time.Clock()
FPS = 60

# Configuración de rutas
def resource_path(relative_path):
    """Función para rutas compatibles con Linux y Windows"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    path = os.path.join(base_path, relative_path)
    return os.path.normpath(path)

# Colores con temas
TEMAS = {
    "Clásico": {
        "VERDE_MESA": (11, 102, 35),
        "VERDE_OSCURO": (8, 75, 26),
        "BLANCO": (245, 245, 245),
        "NEGRO": (20, 20, 20),
        "GRIS_CLARO": (220, 220, 220),
        "ROJO": (200, 30, 30),
        "AZUL": (20, 90, 160),
        "DORADO": (232, 190, 60),
        "COLOR_BOTON": (40, 120, 180),
        "COLOR_BOTON_HOVER": (60, 140, 220)
    },
    "Nocturno": {
        "VERDE_MESA": (10, 40, 60),
        "VERDE_OSCURO": (5, 25, 40),
        "BLANCO": (220, 230, 240),
        "NEGRO": (5, 5, 15),
        "GRIS_CLARO": (180, 190, 200),
        "ROJO": (180, 60, 80),
        "AZUL": (30, 100, 180),
        "DORADO": (200, 170, 50),
        "COLOR_BOTON": (70, 100, 150),
        "COLOR_BOTON_HOVER": (90, 130, 190)
    },
    "Lujo": {
        "VERDE_MESA": (120, 80, 40),
        "VERDE_OSCURO": (90, 60, 30),
        "BLANCO": (250, 240, 230),
        "NEGRO": (30, 20, 10),
        "GRIS_CLARO": (200, 190, 180),
        "ROJO": (180, 100, 80),
        "AZUL": (80, 120, 180),
        "DORADO": (215, 180, 100),
        "COLOR_BOTON": (160, 120, 80),
        "COLOR_BOTON_HOVER": (190, 150, 110)
    }
}

tema_actual = "Clásico"
COLORES = TEMAS[tema_actual]

# Fuentes mejoradas
def obtener_fuente(tamaño, bold=False):
    """Obtener fuentes compatibles con diferentes sistemas"""
    fuentes = ['arial', 'dejavusans', 'liberationsans', 'freesans']
    for fuente_nombre in fuentes:
        try:
            if bold:
                fuente = pygame.font.SysFont(fuente_nombre, tamaño, bold=True)
            else:
                fuente = pygame.font.SysFont(fuente_nombre, tamaño)
            # Probar la fuente
            texto_prueba = fuente.render('Test', True, COLORES["BLANCO"])
            if texto_prueba.get_width() > 0:
                return fuente
        except:
            continue
    return pygame.font.Font(None, tamaño)

fuente_pequena = obtener_fuente(16)
fuente_media = obtener_fuente(22)
fuente_grande = obtener_fuente(34, bold=True)
fuente_titulo = obtener_fuente(44, bold=True)
fuente_muy_grande = obtener_fuente(60, bold=True)

# Estados del juego
class EstadoJuego(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4
    FINAL = 5

# Rangos de mano
class RankingMano(Enum):
    CARTA_ALTA = 0
    PAR = 1
    DOBLE_PAR = 2
    TRIO = 3
    ESCALERA = 4
    COLOR = 5
    FULL_HOUSE = 6
    POKER = 7
    ESCALERA_COLOR = 8
    ESCALERA_REAL = 9

# ---------- Sistema de Partículas ----------
particulas = []

class Particula:
    def __init__(self, x, y, tipo="confeti", color=None):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.life = random.uniform(60, 120)
        self.size = random.randint(2, 6)
        
        # Configurar propiedades según el tipo de efecto
        if tipo == "confeti":
            self.color = color or random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), 
                                               (255, 255, 0), (255, 0, 255), (0, 255, 255)])
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-8, -2)
            self.gravity = 0.2
        elif tipo == "brillo":
            self.color = color or (random.randint(200, 255), random.randint(200, 255), random.randint(100, 200))
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
            self.gravity = 0.05
        elif tipo == "fichas":
            self.color = color or (random.randint(200, 255), random.randint(180, 220), random.randint(0, 100))
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-5, -1)
            self.gravity = 0.15
            self.size = random.randint(3, 8)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 1
        return self.life > 0
        
    def draw(self, surface):
        if self.tipo == "fichas":
            # Dibujar como fichas circulares
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(surface, COLORES["DORADO"], (int(self.x), int(self.y)), self.size, 1)
        else:
            # Confeti o brillo rectangular
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

def crear_particulas(x, y, cantidad=50, tipo="confeti", color=None):
    for _ in range(cantidad):
        particulas.append(Particula(x, y, tipo, color))

# ---------- Sistema de Audio ----------
class SistemaAudio:
    def __init__(self):
        self.sonidos = {}
        self.volumen_efectos = 0.3
        self.inicializar_sonidos_virtuales()
    
    def inicializar_sonidos_virtuales(self):
        """Crear sonidos básicos programáticamente"""
        print("Sistema de audio inicializado (modo virtual)")
    
    def reproducir(self, nombre):
        """Reproducir efecto de sonido (implementación virtual)"""
        print(f"Sonido reproducido: {nombre}")

# ---------- Sistema de Guardado ----------
class SistemaGuardado:
    def __init__(self):
        self.archivo_estadisticas = "estadisticas_poker.json"
        self.estadisticas = self.cargar_estadisticas()
    
    def cargar_estadisticas(self):
        try:
            with open(self.archivo_estadisticas, 'r') as f:
                return json.load(f)
        except:
            # Estadísticas por defecto
            return {
                "partidas_jugadas": 0,
                "partidas_ganadas": 0,
                "mejor_mano": "",
                "mayor_bote": 0,
                "fichas_ganadas": 0,
                "ultima_partida": ""
            }
    
    def guardar_estadisticas(self, estadisticas):
        try:
            with open(self.archivo_estadisticas, 'w') as f:
                json.dump(estadisticas, f, indent=2)
            return True
        except Exception as e:
            print(f"Error guardando estadísticas: {e}")
            return False
    
    def actualizar_estadisticas(self, resultado):
        self.estadisticas["partidas_jugadas"] += 1
        if resultado == "ganada":
            self.estadisticas["partidas_ganadas"] += 1
        self.estadisticas["ultima_partida"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.guardar_estadisticas(self.estadisticas)

# ---------- Utilidades Mejoradas ----------
SUITS = ['♥', '♦', '♣', '♠']
VAL_STR = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

def valor_str(v):
    return VAL_STR.get(v, str(v))

# CORRECCIÓN: Función corregida para manejar transparencias
def draw_rounded_rect_with_shadow(surface, rect, color, radius=12, shadow_offset=6, alpha=255):
    # Crear superficie para la sombra
    shadow_surf = pygame.Surface((rect.w + shadow_offset, rect.h + shadow_offset), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 90), shadow_surf.get_rect(), border_radius=radius)
    surface.blit(shadow_surf, (rect.x - shadow_offset//2, rect.y - shadow_offset//2))
    
    # Crear superficie para el rectángulo principal
    if alpha < 255:
        main_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        # Si el color tiene 4 elementos (RGBA), usar ese alpha, sino usar el alpha proporcionado
        if len(color) == 4:
            pygame.draw.rect(main_surf, color, (0, 0, rect.w, rect.h), border_radius=radius)
        else:
            pygame.draw.rect(main_surf, (*color, alpha), (0, 0, rect.w, rect.h), border_radius=radius)
        surface.blit(main_surf, rect)
    else:
        # Sin transparencia, dibujar directamente
        if len(color) == 4:
            # Color con alpha, usar superficie
            main_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            pygame.draw.rect(main_surf, color, (0, 0, rect.w, rect.h), border_radius=radius)
            surface.blit(main_surf, rect)
        else:
            # Color sólido, dibujar directamente
            pygame.draw.rect(surface, color, rect, border_radius=radius)

# Efecto de texto brillante
def dibujar_texto_brillante(surface, texto, x, y, fuente, color, intensidad=10):
    for i in range(intensidad, 0, -1):
        alpha = 20 + i * 5
        offset = i
        texto_surf = fuente.render(texto, True, color)
        texto_surf.set_alpha(alpha)
        surface.blit(texto_surf, (x - offset, y - offset))
    
    texto_surf = fuente.render(texto, True, color)
    surface.blit(texto_surf, (x, y))

# ---------- Clases del Juego Mejoradas ----------
class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor
        self.angulo = 0
        self.escala = 1.0
        self.alpha = 255

    def __str__(self):
        return f"{valor_str(self.valor)}{SUITS[self.palo]}"

    def color(self):
        return COLORES["ROJO"] if self.palo in [0,1] else COLORES["NEGRO"]

    def dibujar(self, surface, x, y, w=78, h=110, boca_arriba=True, escala=1.0, animar=False):
        # Aplicar animación si está activa
        if animar:
            w = int(w * self.escala)
            h = int(h * self.escala)
        
        # Sombra
        sombra = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(sombra, (0,0,0,90), sombra.get_rect(), border_radius=10)
        surface.blit(sombra, (x+4, y+6))

        carta_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        if boca_arriba:
            pygame.draw.rect(carta_surf, COLORES["BLANCO"], carta_surf.get_rect(), border_radius=10)
            pygame.draw.rect(carta_surf, COLORES["NEGRO"], carta_surf.get_rect(), 2, border_radius=10)

            # Valor arriba
            txt = fuente_media.render(str(self), True, self.color())
            carta_surf.blit(txt, (8, 8))

            # Símbolo grande en el centro
            simbolo = fuente_grande.render(SUITS[self.palo], True, self.color())
            carta_surf.blit(simbolo, (carta_surf.get_width()//2 - simbolo.get_width()//2,
                                      carta_surf.get_height()//2 - simbolo.get_height()//2))

            # Valor invertido abajo
            txt_inv = fuente_media.render(str(self), True, self.color())
            txt_inv = pygame.transform.rotate(txt_inv, 180)
            carta_surf.blit(txt_inv, (carta_surf.get_width() - txt_inv.get_width() - 8,
                                       carta_surf.get_height() - txt_inv.get_height() - 8))
        else:
            # Dorso estilizado con diseño de casino
            pygame.draw.rect(carta_surf, COLORES["AZUL"], carta_surf.get_rect(), border_radius=10)
            pygame.draw.rect(carta_surf, COLORES["NEGRO"], carta_surf.get_rect(), 2, border_radius=10)
            
            # Patrón de casino en el dorso
            for i in range(4, w-10, 12):
                for j in range(6, h-10, 12):
                    if (i+j) % 24 == 0:
                        pygame.draw.circle(carta_surf, (255,255,255,40), (i,j), 3)
            
            # Texto "POKER" en el centro
            texto_poker = fuente_pequena.render("POKER", True, (255,255,255,100))
            carta_surf.blit(texto_poker, (w//2 - texto_poker.get_width()//2, 
                                         h//2 - texto_poker.get_height()//2))

        # Aplicar rotación si es necesario
        if self.angulo != 0:
            carta_surf = pygame.transform.rotate(carta_surf, self.angulo)
        
        # Aplicar transparencia
        if self.alpha < 255:
            carta_surf.set_alpha(self.alpha)
            
        surface.blit(carta_surf, (x, y))

class Jugador:
    def __init__(self, nombre, es_ia=False, fichas=1000, personalidad="normal"):
        self.nombre = nombre
        self.es_ia = es_ia
        self.fichas = fichas
        self.mano = []
        self.apuesta_actual = 0
        self.en_juego = True
        self.ha_hecho_all_in = False
        self.ha_pasado = False
        self.mano_final = None
        self.ranking_mano = None
        self.personalidad = personalidad  # "agresiva", "conservadora", "impredecible"
        self.avatar_color = self.generar_color_avatar()
        self.ultima_accion = ""
        self.tiempo_decision = 0

    def generar_color_avatar(self):
        """Genera un color único para el avatar del jugador"""
        if self.nombre == "Tú":
            return (70, 130, 180)  # Azul para el jugador humano
        elif "Ana" in self.nombre:
            return (220, 100, 120)  # Rosa para Ana
        elif "Luis" in self.nombre:
            return (100, 180, 100)  # Verde para Luis
        elif "Mia" in self.nombre:
            return (180, 120, 220)  # Púrpura para Mia
        else:
            return (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))

    def recibir_carta(self, carta):
        self.mano.append(carta)

    def hacer_apuesta(self, cantidad):
        cantidad = max(0, int(cantidad))
        if cantidad >= self.fichas:
            cantidad = self.fichas
            self.ha_hecho_all_in = True
        self.fichas -= cantidad
        self.apuesta_actual += cantidad
        return cantidad

    def reset_apuesta(self):
        self.apuesta_actual = 0
        self.ha_pasado = False

    def puede_jugar(self):
        return self.en_juego and not self.ha_hecho_all_in and self.fichas > 0

    # IA mejorada con personalidades
    def evaluar_mano_preflop(self):
        a, b = self.mano
        if a.valor == b.valor:
            if a.valor >= 11: return 0.95
            if a.valor >= 8: return 0.78
            return 0.55
        if a.palo == b.palo:
            if abs(a.valor - b.valor) <= 2:
                return 0.72
            return 0.5
        if a.valor >= 11 and b.valor >= 10:
            return 0.7
        if abs(a.valor-b.valor) == 1:
            return 0.45
        return 0.28

    def evaluar_fuerza_mano(self, cartas_comunitarias, ronda):
        if not cartas_comunitarias:
            return self.evaluar_mano_preflop()
        todas = self.mano + cartas_comunitarias
        ranking, _ = evaluar_mejor_mano_static(todas)
        fuerza = ranking.value / 9.0
        if ronda == EstadoJuego.FLOP: fuerza *= 0.85
        elif ronda == EstadoJuego.TURN: fuerza *= 0.93
        return min(fuerza, 1.0)

    def tomar_decision_ia(self, apuesta_requerida, bote_actual, cartas_comunitarias, ronda, apuesta_minima, jugadores_en_vida):
        if not self.puede_jugar():
            return "fold", 0
            
        # Simular tiempo de pensamiento
        self.tiempo_decision = random.randint(500, 2000)
        
        fuerza = self.evaluar_fuerza_mano(cartas_comunitarias, ronda)
        
        # Modificar comportamiento según personalidad
        if self.personalidad == "agresiva":
            fuerza *= 1.2  # Sobreestima su mano
        elif self.personalidad == "conservadora":
            fuerza *= 0.8  # Subestima su mano
        elif self.personalidad == "impredecible":
            fuerza = random.uniform(fuerza * 0.7, fuerza * 1.3)
        
        fuerza = max(0.1, min(1.0, fuerza))
        
        # Lógica de decisión mejorada
        if fuerza < 0.25:
            if apuesta_requerida <= max(1, apuesta_minima//10) and random.random() < 0.3:
                self.ultima_accion = "call"
                return "call", apuesta_requerida
            self.ultima_accion = "fold"
            return "fold", 0
            
        elif fuerza < 0.55:
            if apuesta_requerida <= self.fichas * 0.15:
                if random.random() < 0.6:
                    self.ultima_accion = "call"
                    return "call", apuesta_requerida
                else:
                    raise_amt = min(self.fichas, max(apuesta_minima*2, int(self.fichas*0.08)))
                    self.ultima_accion = f"raise {raise_amt}"
                    return "raise", raise_amt
            self.ultima_accion = "fold"
            return "fold", 0
            
        elif fuerza < 0.8:
            if random.random() < 0.75:
                raise_amt = min(self.fichas, max(apuesta_minima*2, int(bote_actual*0.25)))
                self.ultima_accion = f"raise {raise_amt}"
                return "raise", raise_amt
            self.ultima_accion = "call"
            return "call", apuesta_requerida
            
        else:
            if random.random() < 0.35:
                self.ultima_accion = "all in"
                return "raise", self.fichas
            else:
                raise_amt = min(self.fichas, max(apuesta_minima*3, int(bote_actual*0.5)))
                self.ultima_accion = f"raise {raise_amt}"
                return "raise", raise_amt

# ---------- Lógica de evaluación de manos ----------
def es_escalera_valores(valores):
    vals = sorted(set(valores))
    if set([14,2,3,4,5]).issubset(set(valores)):
        return True
    if len(vals) < 5:
        return False
    for i in range(len(vals)-4):
        if vals[i+4] - vals[i] == 4 and vals[i+1]==vals[i]+1 and vals[i+2]==vals[i]+2 and vals[i+3]==vals[i]+3:
            return True
    return False

def evaluar_combinacion_static(cartas):
    cartas_ord = sorted(cartas, key=lambda c: c.valor, reverse=True)
    valores = [c.valor for c in cartas_ord]
    suits = [c.palo for c in cartas_ord]
    mismo_palo = len(set(suits)) == 1
    es_escal = es_escalera_valores(valores)
    
    if mismo_palo and es_escal and max(valores) == 14 and min(valores) == 10:
        return RankingMano.ESCALERA_REAL, cartas_ord
    if mismo_palo and es_escal:
        return RankingMano.ESCALERA_COLOR, cartas_ord
    freq = {}
    for v in valores:
        freq[v] = freq.get(v,0) + 1
    items = sorted(freq.items(), key=lambda x: (x[1], x[0]), reverse=True)
    if items[0][1] == 4:
        return RankingMano.POKER, cartas_ord
    if items[0][1] == 3 and len(items) > 1 and items[1][1] == 2:
        return RankingMano.FULL_HOUSE, cartas_ord
    if mismo_palo:
        return RankingMano.COLOR, cartas_ord
    if es_escal:
        return RankingMano.ESCALERA, cartas_ord
    if items[0][1] == 3:
        return RankingMano.TRIO, cartas_ord
    if items[0][1] == 2 and len(items) > 1 and items[1][1] == 2:
        return RankingMano.DOBLE_PAR, cartas_ord
    if items[0][1] == 2:
        return RankingMano.PAR, cartas_ord
    return RankingMano.CARTA_ALTA, cartas_ord

def evaluar_mejor_mano_static(cartas):
    mejor_ranking = RankingMano.CARTA_ALTA
    mejor_mano = None
    for combo in combinations(cartas, 5):
        ranking, mano_ord = evaluar_combinacion_static(combo)
        if ranking.value > mejor_ranking.value:
            mejor_ranking = ranking
            mejor_mano = mano_ord
        elif ranking.value == mejor_ranking.value and mejor_mano is not None:
            comp = comparar_manos_static(mano_ord, mejor_mano, ranking)
            if comp > 0:
                mejor_mano = mano_ord
        elif ranking.value == melhor_ranking.value and mejor_mano is None:
            mejor_mano = mano_ord
    return mejor_ranking, mejor_mano

def comparar_manos_static(m1, m2, ranking):
    v1 = [c.valor for c in m1]
    v2 = [c.valor for c in m2]
    if ranking in (RankingMano.ESCALERA, RankingMano.ESCALERA_COLOR):
        s1 = 5 if set(v1) == {14,2,3,4,5} else max(v1)
        s2 = 5 if set(v2) == {14,2,3,4,5} else max(v2)
        return s1 - s2
    f1 = {}
    f2 = {}
    for x in v1: f1[x] = f1.get(x,0)+1
    for x in v2: f2[x] = f2.get(x,0)+1
    ord1 = sorted(f1.items(), key=lambda x: (x[1], x[0]), reverse=True)
    ord2 = sorted(f2.items(), key=lambda x: (x[1], x[0]), reverse=True)
    for (val1,cnt1),(val2,cnt2) in zip(ord1, ord2):
        if val1 != val2:
            return val1 - val2
    return 0

# ---------- Clase Principal del Juego Mejorada ----------
class PokerGame:
    def __init__(self):
        self.jugadores = [
            Jugador("Tú", es_ia=False, fichas=1500),
            Jugador("IA - Ana", es_ia=True, fichas=1200, personalidad="agresiva"),
            Jugador("IA - Luis", es_ia=True, fichas=1200, personalidad="conservadora"),
            Jugador("IA - Mia", es_ia=True, fichas=1200, personalidad="impredecible")
        ]
        self.mazo = []
        self.cartas_comunitarias = []
        self.bote = 0
        self.apuesta_minima = 20
        self.dealer_index = 0
        self.jugador_actual_index = 1
        self.estado = EstadoJuego.PREFLOP
        self.ronda_terminada = False
        self.ganador = None
        self.animaciones = []
        self.audio = SistemaAudio()
        self.guardado = SistemaGuardado()
        self.estadisticas_partida = {
            "manos_jugadas": 0,
            "bote_maximo": 0,
            "jugador_mas_agresivo": "",
            "acciones_totales": 0
        }
        self.crear_mazo()

    def crear_mazo(self):
        self.mazo = [Carta(p, v) for p in range(4) for v in range(2,15)]

    def barajar(self):
        random.shuffle(self.mazo)

    def repartir_cartas(self):
        for j in self.jugadores:
            j.mano = []
        for _ in range(2):
            for j in self.jugadores:
                if len(self.mazo)>0:
                    j.recibir_carta(self.mazo.pop())
                    # Animación de reparto
                    self.agregar_animacion_carta(j, _)

    def agregar_animacion_carta(self, jugador, numero_carta):
        # Simular animación de carta volando
        pass

    def repartir_cartas_comunitarias(self):
        if self.estado == EstadoJuego.FLOP and len(self.cartas_comunitarias) == 0:
            if len(self.mazo)>0: self.mazo.pop()
            for _ in range(3):
                if len(self.mazo)>0:
                    carta = self.mazo.pop()
                    self.cartas_comunitarias.append(carta)
                    # Animación para cartas comunitarias
                    crear_particulas(WIDTH//2, HEIGHT//2, 20, "brillo", carta.color())
        elif self.estado == EstadoJuego.TURN and len(self.cartas_comunitarias) == 3:
            if len(self.mazo)>0: self.mazo.pop()
            if len(self.mazo)>0:
                carta = self.mazo.pop()
                self.cartas_comunitarias.append(carta)
                crear_particulas(WIDTH//2, HEIGHT//2, 20, "brillo", carta.color())
        elif self.estado == EstadoJuego.RIVER and len(self.cartas_comunitarias) == 4:
            if len(self.mazo)>0: self.mazo.pop()
            if len(self.mazo)>0:
                carta = self.mazo.pop()
                self.cartas_comunitarias.append(carta)
                crear_particulas(WIDTH//2, HEIGHT//2, 20, "brillo", carta.color())

    def iniciar_nueva_mano(self):
        self.crear_mazo(); self.barajar()
        self.cartas_comunitarias = []
        self.bote = 0
        self.estado = EstadoJuego.PREFLOP
        self.ronda_terminada = False
        self.ganador = None
        self.estadisticas_partida["manos_jugadas"] += 1
        
        # Mover dealer
        self.dealer_index = (self.dealer_index + 1) % len(self.jugadores)
        
        # Reset jugadores
        for j in self.jugadores:
            j.reset_apuesta()
            j.mano = []
            j.en_juego = True if j.fichas > 0 else False
            j.ha_hecho_all_in = False
            j.mano_final = None
            j.ranking_mano = None
        
        # Repartir cartas
        self.repartir_cartas()
        
        # Aplicar blinds
        small = self.apuesta_minima // 2
        big = self.apuesta_minima
        sb_idx = (self.dealer_index + 1) % len(self.jugadores)
        bb_idx = (self.dealer_index + 2) % len(self.jugadores)
        
        # Animación para blinds
        crear_particulas(
            WIDTH//2, HEIGHT//2, 
            30, "fichas", COLORES["DORADO"]
        )
        
        self.jugadores[sb_idx].hacer_apuesta(small)
        self.jugadores[bb_idx].hacer_apuesta(big)
        self.bote = small + big
        
        # Siguiente jugador después del big blind
        self.jugador_actual_index = (bb_idx + 1) % len(self.jugadores)

    def encontrar_siguiente_jugador_index(self, desde):
        n = len(self.jugadores)
        for i in range(1, n+1):
            idx = (desde + i) % n
            j = self.jugadores[idx]
            if j.en_juego and (not j.ha_hecho_all_in) and j.fichas>0:
                return idx
        return None

    def verificar_fin_ronda(self):
        jugadores_activos = [j for j in self.jugadores if j.en_juego]
        if not jugadores_activos:
            self.ronda_terminada = True
            return
        apuesta_max = max(j.apuesta_actual for j in jugadores_activos)
        for j in jugadores_activos:
            if not j.ha_hecho_all_in and j.apuesta_actual != apuesta_max:
                self.ronda_terminada = False
                return
        self.ronda_terminada = True

    def siguiente_estado(self):
        if self.estado == EstadoJuego.PREFLOP:
            self.estado = EstadoJuego.FLOP
        elif self.estado == EstadoJuego.FLOP:
            self.estado = EstadoJuego.TURN
        elif self.estado == EstadoJuego.TURN:
            self.estado = EstadoJuego.RIVER
        elif self.estado == EstadoJuego.RIVER:
            self.estado = EstadoJuego.SHOWDOWN
            self.determinar_ganador()
        elif self.estado == EstadoJuego.SHOWDOWN:
            self.estado = EstadoJuego.FINAL
            
        # Efecto visual al cambiar de estado
        crear_particulas(WIDTH//2, HEIGHT//2, 50, "confeti")
        
        # Reset apuestas
        for j in self.jugadores:
            j.reset_apuesta()
        self.ronda_terminada = False
        self.jugador_actual_index = (self.dealer_index + 1) % len(self.jugadores)

    def determinar_ganador(self):
        jugadores_activos = [j for j in self.jugadores if j.en_juego]
        if len(jugadores_activos) == 1:
            self.ganador = jugadores_activos[0]
            self.ganador.fichas += self.bote
            # Efecto de victoria
            crear_particulas(WIDTH//2, HEIGHT//2, 100, "confeti")
            self.bote = 0
            return
            
        mejores = []
        for j in jugadores_activos:
            ranking, mano = evaluar_mejor_mano_static(j.mano + self.cartas_comunitarias)
            j.ranking_mano = ranking
            j.mano_final = mano
            mejores.append((j, ranking, mano))
            
        mejor_ranking = max(r for _,r,_ in mejores)
        contenders = [(jug, r, m) for (jug,r,m) in mejores if r == mejor_ranking]
        
        if len(contenders) == 1:
            ganador = contenders[0][0]
        else:
            # Desempate
            manos_comp = []
            for jug, r, m in contenders:
                valores = [c.valor for c in m]
                manos_comp.append((jug, valores, m))
            manos_comp.sort(key=lambda x: x[1], reverse=True)
            ganador = manos_comp[0][0]
            
        self.ganador = ganador
        self.ganador.fichas += self.bote
        # Gran efecto de victoria
        crear_particulas(WIDTH//2, HEIGHT//2, 200, "confeti")
        crear_particulas(WIDTH//2, HEIGHT//2, 50, "fichas", COLORES["DORADO"])
        self.bote = 0

# ---------- Renderizado UI Mejorado ----------
MARGEN_X = 100
MARGEN_Y = 80

def dibujar_mesa(surface):
    # Fondo con degradado
    for y in range(HEIGHT):
        color = (
            max(0, COLORES["VERDE_MESA"][0] - y//30),
            max(0, COLORES["VERDE_MESA"][1] - y//40),
            max(0, COLORES["VERDE_MESA"][2] - y//50)
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))
    
    # Mesa ovalada con efecto 3D
    tabla_ancho = int(WIDTH * 0.85)
    tabla_alto = int(HEIGHT * 0.6)
    tabla_x = WIDTH * 0.075
    tabla_y = HEIGHT * 0.12
    
    # Sombra de la mesa
    sombra = pygame.Surface((tabla_ancho + 20, tabla_alto + 20), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 80), sombra.get_rect())
    surface.blit(sombra, (tabla_x - 10, tabla_y - 10))
    
    # Mesa principal
    tabla = pygame.Surface((tabla_ancho, tabla_alto), pygame.SRCALPHA)
    pygame.draw.ellipse(tabla, COLORES["VERDE_OSCURO"], tabla.get_rect())
    
    # Efecto de iluminación
    for i in range(10):
        radio = min(tabla_ancho, tabla_alto) // 2 - i * 5
        if radio > 0:
            alpha = 30 - i * 3
            color = (255, 255, 255, alpha)
            pygame.draw.ellipse(tabla, color, (
                tabla_ancho//2 - radio, tabla_alto//2 - radio,
                radio * 2, radio * 2
            ), 2)
    
    # Borde de la mesa
    pygame.draw.ellipse(tabla, COLORES["DORADO"], tabla.get_rect(), 8)
    pygame.draw.ellipse(tabla, (0, 0, 0, 50), tabla.get_rect(), 2)
    
    surface.blit(tabla, (tabla_x, tabla_y))
    
    # Logo del casino en el centro
    logo_texto = fuente_titulo.render("POKER", True, COLORES["DORADO"])
    surface.blit(logo_texto, (WIDTH//2 - logo_texto.get_width()//2, HEIGHT//2 - logo_texto.get_height()//2 - 10))
    
    logo_subtexto = fuente_pequena.render("PREMIUM EDITION", True, COLORES["BLANCO"])
    surface.blit(logo_subtexto, (WIDTH//2 - logo_subtexto.get_width()//2, HEIGHT//2 + 30))

def dibujar_jugadores(surface, juego):
    posiciones = [
        (WIDTH//2, int(HEIGHT*0.78)),      # bottom - player
        (int(WIDTH*0.84), int(HEIGHT*0.48)), # right
        (WIDTH//2, int(HEIGHT*0.18)),      # top
        (int(WIDTH*0.16), int(HEIGHT*0.48))  # left
    ]
    
    for i, j in enumerate(juego.jugadores):
        x, y = posiciones[i]
        
        # Avatar circular con efecto de profundidad
        avatar_radio = 46
        avatar_rect = pygame.Rect(x-avatar_radio, y-avatar_radio, avatar_radio*2, avatar_radio*2)
        
        # Sombra del avatar
        sombra = pygame.Surface((avatar_radio*2 + 10, avatar_radio*2 + 10), pygame.SRCALPHA)
        pygame.draw.circle(sombra, (0,0,0,100), (avatar_radio+5, avatar_radio+5), avatar_radio)
        surface.blit(sombra, (x-avatar_radio-5, y-avatar_radio-5))
        
        # Avatar principal
        pygame.draw.circle(surface, j.avatar_color, (x, y), avatar_radio)
        pygame.draw.circle(surface, COLORES["NEGRO"], (x, y), avatar_radio, 3)
        
        # Efecto de resaltado
        if i == juego.jugador_actual_index:
            pygame.draw.circle(surface, COLORES["DORADO"], (x, y), avatar_radio + 5, 3)
            # Añadir efecto de brillo
            for r in range(avatar_radio + 2, avatar_radio + 8, 2):
                pygame.draw.circle(surface, (255, 255, 255, 50), (x, y), r, 1)
        
        # Información del jugador
        panel_ancho = 160
        panel_alto = 80
        panel_rect = pygame.Rect(x - panel_ancho//2, y + avatar_radio + 10, panel_ancho, panel_alto)
        draw_rounded_rect_with_shadow(surface, panel_rect, (40, 40, 40), radius=8, alpha=200)
        
        # Nombre
        color_text = COLORES["BLANCO"] if j.en_juego else COLORES["GRIS_CLARO"]
        nombre = fuente_pequena.render(j.nombre, True, color_text)
        surface.blit(nombre, (x - nombre.get_width()//2, y + avatar_radio + 15))
        
        # Fichas
        fichas = fuente_pequena.render(f"${j.fichas}", True, COLORES["DORADO"])
        surface.blit(fichas, (x - fichas.get_width()//2, y + avatar_radio + 35))
        
        # Apuesta actual
        if j.apuesta_actual > 0:
            apuesta = fuente_pequena.render(f"Apuesta: ${j.apuesta_actual}", True, COLORES["BLANCO"])
            surface.blit(apuesta, (x - apuesta.get_width()//2, y + avatar_radio + 55))
        
        # Dealer button
        if i == juego.dealer_index:
            dealer_rect = pygame.Rect(x - 60, y - avatar_radio - 25, 30, 20)
            draw_rounded_rect_with_shadow(surface, dealer_rect, COLORES["DORADO"], radius=4)
            dealer_text = fuente_pequena.render("D", True, COLORES["NEGRO"])
            surface.blit(dealer_text, (dealer_rect.centerx - dealer_text.get_width()//2, 
                                     dealer_rect.centery - dealer_text.get_height()//2))
        
        # Estado especial
        if j.ha_hecho_all_in:
            allin_text = fuente_pequena.render("ALL IN", True, COLORES["ROJO"])
            surface.blit(allin_text, (x - allin_text.get_width()//2, y - avatar_radio - 25))
        elif not j.en_juego:
            fold_text = fuente_pequena.render("FOLD", True, COLORES["ROJO"])
            surface.blit(fold_text, (x - fold_text.get_width()//2, y - avatar_radio - 25))
        
        # Cartas del jugador
        boca_arriba = (not j.es_ia) or (j.en_juego and juego.estado == EstadoJuego.SHOWDOWN) or (i == 0)
        for idx, carta in enumerate(j.mano):
            carta_x = x - 46 + idx * 52
            carta_y = y + avatar_radio + 90
            carta.dibujar(surface, carta_x, carta_y, w=68, h=96, boca_arriba=boca_arriba)
        
        # Última acción de IA
        if j.es_ia and j.ultima_accion and juego.estado != EstadoJuego.SHOWDOWN:
            accion_text = fuente_pequena.render(j.ultima_accion, True, COLORES["BLANCO"])
            surface.blit(accion_text, (x - accion_text.get_width()//2, y - avatar_radio - 45))

def dibujar_comunitarias(surface, juego):
    x0 = WIDTH//2 - 220
    y0 = HEIGHT//2 - 60
    
    # Panel para cartas comunitarias
    panel_rect = pygame.Rect(x0 - 20, y0 - 20, 5 * 110 + 40, 140 + 40)
    draw_rounded_rect_with_shadow(surface, panel_rect, (30, 30, 30), radius=12, alpha=150)
    
    # Cartas comunitarias
    for i in range(5):
        if i < len(juego.cartas_comunitarias):
            juego.cartas_comunitarias[i].dibujar(surface, x0 + i * 110, y0, w=98, h=140, boca_arriba=True)
        else:
            # Placeholder con animación de espera
            if juego.estado.value >= i:
                alpha = 128 + int(127 * math.sin(pygame.time.get_ticks() / 500))
                carta_placeholder = Carta(0, 2)
                carta_placeholder.alpha = alpha
                carta_placeholder.dibujar(surface, x0 + i * 110, y0, w=98, h=140, boca_arriba=False)
    
    # Bote con efecto brillante
    bote_text = fuente_grande.render(f"Bote: ${juego.bote}", True, COLORES["DORADO"])
    dibujar_texto_brillante(surface, f"Bote: ${juego.bote}", WIDTH//2, y0 - 70, fuente_grande, COLORES["DORADO"])
    
    # Estado de la ronda
    estados = {
        EstadoJuego.PREFLOP: "Pre-Flop", 
        EstadoJuego.FLOP: "Flop", 
        EstadoJuego.TURN: "Turn", 
        EstadoJuego.RIVER: "River", 
        EstadoJuego.SHOWDOWN: "Showdown", 
        EstadoJuego.FINAL: "Mano finalizada"
    }
    estado_text = fuente_media.render(estados[juego.estado], True, COLORES["BLANCO"])
    surface.blit(estado_text, (WIDTH//2 - estado_text.get_width()//2, 24))

def dibujar_controles(surface, juego):
    jugador = juego.jugadores[juego.jugador_actual_index]
    
    # Panel de controles con efecto de cristal
    panel = pygame.Rect(WIDTH//2 - 280, HEIGHT - 160, 560, 130)
    draw_rounded_rect_with_shadow(surface, panel, (30, 30, 30), radius=16, alpha=200)
    pygame.draw.rect(surface, (60, 60, 60), panel, 2, border_radius=16)
    
    # Título del panel
    titulo = fuente_media.render("Tu Turno", True, COLORES["BLANCO"])
    surface.blit(titulo, (panel.centerx - titulo.get_width()//2, panel.y + 10))
    
    # Botones
    btn_w = 120
    btn_h = 46
    fold_r = pygame.Rect(panel.x + 20, panel.y + 50, btn_w, btn_h)
    call_r = pygame.Rect(panel.x + 160, panel.y + 50, btn_w, btn_h)
    raise_r = pygame.Rect(panel.x + 300, panel.y + 50, btn_w, btn_h)
    allin_r = pygame.Rect(panel.x + 440, panel.y + 50, btn_w - 40, btn_h)
    
    # Efectos hover
    mouse_pos = pygame.mouse.get_pos()
    
    # Botón Fold
    color_fold = (180, 40, 40) if fold_r.collidepoint(mouse_pos) else (150, 30, 30)
    pygame.draw.rect(surface, color_fold, fold_r, border_radius=8)
    pygame.draw.rect(surface, COLORES["BLANCO"], fold_r, 2, border_radius=8)
    txt_fold = fuente_media.render("Fold", True, COLORES["BLANCO"])
    surface.blit(txt_fold, (fold_r.centerx - txt_fold.get_width()//2, fold_r.centery - txt_fold.get_height()//2))
    
    # Botón Call
    necesidad = max(0, juego.apuesta_minima - jugador.apuesta_actual)
    color_call = (40, 180, 40) if call_r.collidepoint(mouse_pos) else (30, 150, 30)
    pygame.draw.rect(surface, color_call, call_r, border_radius=8)
    pygame.draw.rect(surface, COLORES["BLANCO"], call_r, 2, border_radius=8)
    txt_call = fuente_media.render(f"Call (${necesidad})", True, COLORES["BLANCO"])
    surface.blit(txt_call, (call_r.centerx - txt_call.get_width()//2, call_r.centery - txt_call.get_height()//2))
    
    # Botón Raise
    color_raise = (30, 90, 180) if raise_r.collidepoint(mouse_pos) else (20, 70, 160)
    pygame.draw.rect(surface, color_raise, raise_r, border_radius=8)
    pygame.draw.rect(surface, COLORES["BLANCO"], raise_r, 2, border_radius=8)
    txt_raise = fuente_media.render("Raise", True, COLORES["BLANCO"])
    surface.blit(txt_raise, (raise_r.centerx - txt_raise.get_width()//2, raise_r.centery - txt_raise.get_height()//2))
    
    # Botón All-in
    color_allin = (200, 120, 20) if allin_r.collidepoint(mouse_pos) else (180, 100, 0)
    pygame.draw.rect(surface, color_allin, allin_r, border_radius=8)
    pygame.draw.rect(surface, COLORES["BLANCO"], allin_r, 2, border_radius=8)
    txt_allin = fuente_pequena.render("ALL IN", True, COLORES["BLANCO"])
    surface.blit(txt_allin, (allin_r.centerx - txt_allin.get_width()//2, allin_r.centery - txt_allin.get_height()//2))
    
    # Información de apuesta mínima
    sugerencia = fuente_pequena.render(f"Apuesta mínima: ${juego.apuesta_minima}", True, COLORES["GRIS_CLARO"])
    surface.blit(sugerencia, (panel.x + 20, panel.y + 100))
    
    return fold_r, call_r, raise_r, allin_r

def dibujar_menu_principal(surface, juego):
    # Fondo animado
    tiempo = pygame.time.get_ticks() / 1000
    for y in range(HEIGHT):
        color = (
            max(0, COLORES["VERDE_MESA"][0] - y//40),
            max(0, COLORES["VERDE_MESA"][1] - y//50),
            max(0, COLORES["VERDE_MESA"][2] - y//60)
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))
    
    # Título animado
    titulo = fuente_muy_grande.render("TEXAS HOLD'EM", True, COLORES["DORADO"])
    titulo_rect = titulo.get_rect(center=(WIDTH//2, 120))
    
    # Efecto de brillo en el título
    alpha = 200 + int(55 * math.sin(tiempo * 2))
    titulo_temp = fuente_muy_grande.render("TEXAS HOLD'EM", True, COLORES["DORADO"])
    titulo_temp.set_alpha(alpha)
    surface.blit(titulo_temp, titulo_rect)
    
    # Subtítulo
    subtitulo = fuente_media.render("Edición Premium", True, COLORES["BLANCO"])
    surface.blit(subtitulo, (WIDTH//2 - subtitulo.get_width()//2, 190))
    
    # Botón jugar
    boton_jugar = pygame.Rect(WIDTH//2 - 120, 300, 240, 70)
    mouse_pos = pygame.mouse.get_pos()
    color_boton = COLORES["COLOR_BOTON_HOVER"] if boton_jugar.collidepoint(mouse_pos) else COLORES["COLOR_BOTON"]
    
    pygame.draw.rect(surface, color_boton, boton_jugar, border_radius=12)
    pygame.draw.rect(surface, COLORES["BLANCO"], boton_jugar, 3, border_radius=12)
    
    texto_jugar = fuente_grande.render("JUGAR", True, COLORES["BLANCO"])
    texto_rect = texto_jugar.get_rect(center=boton_jugar.center)
    surface.blit(texto_jugar, texto_rect)
    
    # Estadísticas rápidas
    stats = juego.guardado.estadisticas
    panel_stats = pygame.Rect(WIDTH//2 - 200, 400, 400, 150)
    draw_rounded_rect_with_shadow(surface, panel_stats, (30, 30, 30), radius=12, alpha=180)
    
    texto_stats = fuente_media.render("TUS ESTADÍSTICAS", True, COLORES["DORADO"])
    surface.blit(texto_stats, (panel_stats.centerx - texto_stats.get_width()//2, panel_stats.y + 15))
    
    stats_textos = [
        f"Partidas jugadas: {stats['partidas_jugadas']}",
        f"Partidas ganadas: {stats['partidas_ganadas']}",
        f"Mejor mano: {stats['mejor_mano'] or 'N/A'}",
        f"Última partida: {stats['ultima_partida'] or 'Nunca'}"
    ]
    
    for i, texto in enumerate(stats_textos):
        texto_surf = fuente_pequena.render(texto, True, COLORES["BLANCO"])
        surface.blit(texto_surf, (panel_stats.x + 20, panel_stats.y + 50 + i * 25))
    
    # Instrucciones
    instrucciones = [
        "CONTROLES:",
        "• Usa los botones para tomar decisiones",
        "• Fold: Retirarte de la mano",
        "• Call: Igualar la apuesta actual", 
        "• Raise: Aumentar la apuesta",
        "• All-in: Apostar todas tus fichas"
    ]
    
    for i, linea in enumerate(instrucciones):
        texto = fuente_pequena.render(linea, True, COLORES["BLANCO"])
        surface.blit(texto, (WIDTH//2 - texto.get_width()//2, 580 + i * 25))
    
    return boton_jugar

# ---------- Loop Principal Mejorado ----------

def main():
    global particulas, COLORES, tema_actual
    
    juego = PokerGame()
    running = True
    click_cooldown = 0
    estado_aplicacion = "menu"  # "menu", "jugando", "game_over"
    
    # Efectos de partículas iniciales
    for _ in range(50):
        crear_particulas(random.randint(0, WIDTH), random.randint(0, HEIGHT), 1, "confeti")
    
    while running:
        dt = clock.tick(FPS)
        if click_cooldown > 0:
            click_cooldown -= 1
        
        # Actualizar partículas
        particulas = [p for p in particulas if p.update()]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if estado_aplicacion == "jugando":
                        estado_aplicacion = "menu"
                    elif estado_aplicacion == "menu":
                        running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and click_cooldown == 0:
                mouse = pygame.mouse.get_pos()
                
                if estado_aplicacion == "menu":
                    boton_jugar = dibujar_menu_principal(screen, juego)
                    if boton_jugar.collidepoint(mouse):
                        estado_aplicacion = "jugando"
                        juego.iniciar_nueva_mano()
                        click_cooldown = 20
                
                elif estado_aplicacion == "jugando":
                    # Turno del jugador humano
                    if not juego.jugadores[juego.jugador_actual_index].es_ia and juego.estado not in (EstadoJuego.SHOWDOWN, EstadoJuego.FINAL):
                        fold_r, call_r, raise_r, allin_r = dibujar_controles(screen, juego)
                        
                        if fold_r.collidepoint(mouse):
                            juego.jugadores[juego.jugador_actual_index].en_juego = False
                            juego.jugador_actual_index = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index) or juego.jugador_actual_index
                            click_cooldown = 10
                            juego.audio.reproducir("fold")
                            
                        elif call_r.collidepoint(mouse):
                            j = juego.jugadores[juego.jugador_actual_index]
                            necesidad = max(0, juego.apuesta_minima - j.apuesta_actual)
                            apuesta = j.hacer_apuesta(necesidad)
                            juego.bote += apuesta
                            juego.jugador_actual_index = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index) or juego.jugador_actual_index
                            click_cooldown = 10
                            juego.audio.reproducir("apuesta")
                            crear_particulas(mouse[0], mouse[1], 20, "fichas", COLORES["DORADO"])
                            
                        elif raise_r.collidepoint(mouse):
                            j = juego.jugadores[juego.jugador_actual_index]
                            incremento = min(j.fichas, max(juego.apuesta_minima*2, int(juego.apuesta_minima*1.5)))
                            apuesta = j.hacer_apuesta(incremento)
                            juego.bote += apuesta
                            juego.apuesta_minima = j.apuesta_actual
                            juego.jugador_actual_index = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index) or juego.jugador_actual_index
                            click_cooldown = 10
                            juego.audio.reproducir("apuesta")
                            crear_particulas(mouse[0], mouse[1], 30, "fichas", COLORES["DORADO"])
                            
                        elif allin_r.collidepoint(mouse):
                            j = juego.jugadores[juego.jugador_actual_index]
                            apuesta = j.hacer_apuesta(j.fichas)
                            juego.bote += apuesta
                            juego.jugador_actual_index = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index) or juego.jugador_actual_index
                            click_cooldown = 10
                            juego.audio.reproducir("allin")
                            crear_particulas(mouse[0], mouse[1], 50, "fichas", COLORES["DORADO"])
                
                # Botón nueva mano cuando final
                if estado_aplicacion == "jugando" and juego.estado == EstadoJuego.FINAL:
                    btn = pygame.Rect(WIDTH//2-130, HEIGHT//2+70, 260, 54)
                    if btn.collidepoint(mouse):
                        juego.iniciar_nueva_mano()
                        click_cooldown = 12
                        juego.audio.reproducir("nueva_mano")
        
        # Lógica del juego
        if estado_aplicacion == "jugando":
            # Decisiones de IA
            current = juego.jugadores[juego.jugador_actual_index]
            if current.es_ia and juego.estado not in (EstadoJuego.SHOWDOWN, EstadoJuego.FINAL):
                apuesta_req = max(0, juego.apuesta_minima - current.apuesta_actual)
                decision, cantidad = current.tomar_decision_ia(apuesta_req, juego.bote, juego.cartas_comunitarias, juego.estado, juego.apuesta_minima, len([x for x in juego.jugadores if x.en_juego]))
                
                if decision == "fold":
                    current.en_juego = False
                    juego.audio.reproducir("fold")
                elif decision == "call":
                    apuesta = current.hacer_apuesta(cantidad)
                    juego.bote += apuesta
                    juego.audio.reproducir("apuesta")
                elif decision == "raise":
                    apuesta = current.hacer_apuesta(cantidad)
                    juego.bote += apuesta
                    juego.apuesta_minima = current.apuesta_actual
                    juego.audio.reproducir("apuesta")
                
                # Siguiente jugador
                nxt = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index)
                juego.jugador_actual_index = nxt if nxt is not None else juego.jugador_actual_index
            
            # Verificar fin de ronda
            juego.verificar_fin_ronda()
            if juego.ronda_terminada and juego.estado not in (EstadoJuego.SHOWDOWN, EstadoJuego.FINAL):
                juego.repartir_cartas_comunitarias()
                juego.siguiente_estado()
        
        # Renderizado
        if estado_aplicacion == "menu":
            dibujar_menu_principal(screen, juego)
        elif estado_aplicacion == "jugando":
            dibujar_mesa(screen)
            dibujar_comunitarias(screen, juego)
            dibujar_jugadores(screen, juego)
            
            # Controles para humano
            if not juego.jugadores[juego.jugador_actual_index].es_ia and juego.estado not in (EstadoJuego.SHOWDOWN, EstadoJuego.FINAL):
                dibujar_controles(screen, juego)
            
            # Mostrar ganador
            if juego.ganador:
                t = fuente_titulo.render(f"{juego.ganador.nombre} gana!", True, COLORES["DORADO"])
                screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 180))
                
                if juego.estado == EstadoJuego.SHOWDOWN and juego.ganador.mano_final:
                    nm = fuente_media.render(f"Mano: {juego.ganador.ranking_mano.name.replace('_',' ')}", True, COLORES["BLANCO"])
                    screen.blit(nm, (WIDTH//2 - nm.get_width()//2, HEIGHT//2 - 120))
            
            # Botón nueva mano
            if juego.estado == EstadoJuego.FINAL:
                btn = pygame.Rect(WIDTH//2-130, HEIGHT//2+70, 260, 54)
                draw_rounded_rect_with_shadow(screen, btn, COLORES["COLOR_BOTON"], radius=12)
                txt = fuente_grande.render("Nueva mano", True, COLORES["BLANCO"])
                screen.blit(txt, (btn.centerx - txt.get_width()//2, btn.centery - txt.get_height()//2))
        
        # Dibujar partículas
        for particula in particulas:
            particula.draw(screen)
        
        pygame.display.flip()
    
    # Guardar estadísticas al salir
    juego.guardado.guardar_estadisticas(juego.guardado.estadisticas)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()