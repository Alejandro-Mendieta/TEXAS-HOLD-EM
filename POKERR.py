"""
Texas Hold'em - Versión Premium Oro y Negro
- Diseño de lujo con tema oro y negro
- Mesa premium con efectos de brillo y reflejos
- Cartas doradas y plateadas con detalles premium
- Animaciones y partículas de oro
- Efectos visuales de alta gama

Ejecutar: python texas_holdem_premium.py
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
pygame.display.set_caption("Texas Hold'em - Edición Premium Oro")
clock = pygame.time.Clock()
FPS = 60

# Tema Premium Oro y Negro
COLORES = {
    "ORO_PRINCIPAL": (212, 175, 55),
    "ORO_SECUNDARIO": (245, 200, 80),
    "ORO_CLARO": (255, 215, 0),
    "ORO_OSCURO": (180, 150, 40),
    "NEGRO_LUJO": (10, 10, 10),
    "NEGRO_SUAVE": (20, 20, 20),
    "NEGRO_CARTA": (5, 5, 5),
    "PLATA": (192, 192, 192),
    "PLATA_OSCURO": (150, 150, 150),
    "BLANCO_PREMIUM": (245, 245, 245),
    "ROJO_LUJO": (180, 40, 40),
    "VERDE_LUJO": (40, 140, 40),
    "TRANSPARENTE": (0, 0, 0, 0)
}

# Fuentes premium
def obtener_fuente(tamaño, bold=False, italic=False):
    """Obtener fuentes premium"""
    try:
        if bold and italic:
            return pygame.font.SysFont('timesnewroman', tamaño, bold=True, italic=True)
        elif bold:
            return pygame.font.SysFont('timesnewroman', tamaño, bold=True)
        else:
            return pygame.font.SysFont('garamond', tamaño)
    except:
        return pygame.font.Font(None, tamaño)

fuente_pequena = obtener_fuente(18)
fuente_media = obtener_fuente(24)
fuente_grande = obtener_fuente(36, bold=True)
fuente_titulo = obtener_fuente(48, bold=True)
fuente_muy_grande = obtener_fuente(72, bold=True)
fuente_elegante = obtener_fuente(28, italic=True)

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

# ---------- Sistema de Partículas Premium ----------
particulas = []

class Particula:
    def __init__(self, x, y, tipo="oro", color=None):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.life = random.uniform(80, 160)
        self.size = random.randint(3, 8)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        
        if tipo == "oro":
            self.color = color or random.choice([
                COLORES["ORO_PRINCIPAL"],
                COLORES["ORO_SECUNDARIO"], 
                COLORES["ORO_CLARO"],
                (255, 223, 0)
            ])
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-6, -3)
            self.gravity = 0.15
        elif tipo == "brillo_oro":
            self.color = (255, 255, 200)
            self.alpha = random.randint(100, 200)
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-0.5, 0.5)
            self.gravity = 0.02
            self.size = random.randint(2, 4)
        elif tipo == "diamante":
            self.color = (200, 230, 255)
            self.alpha = 200
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-4, -2)
            self.gravity = 0.1
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 1
        self.rotation += self.rotation_speed
        return self.life > 0
        
    def draw(self, surface):
        if self.tipo in ["brillo_oro", "diamante"]:
            # Crear superficie para partículas con alpha
            part_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            if self.tipo == "diamante":
                # Partícula con forma de diamante
                points = []
                for i in range(4):
                    angle = math.radians(self.rotation + i * 90)
                    px = self.size + math.cos(angle) * self.size
                    py = self.size + math.sin(angle) * self.size
                    points.append((px, py))
                pygame.draw.polygon(part_surf, (*self.color, self.alpha), points)
            else:
                # Partícula circular con brillo
                pygame.draw.circle(part_surf, (*self.color, self.alpha), 
                                 (self.size, self.size), self.size)
            
            surface.blit(part_surf, (int(self.x - self.size), int(self.y - self.size)))
        else:
            # Partículas normales sin transparencia
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
            if self.tipo == "oro":
                pygame.draw.circle(surface, COLORES["ORO_CLARO"], (int(self.x), int(self.y)), self.size, 1)

def crear_particulas(x, y, cantidad=50, tipo="oro", color=None):
    for _ in range(cantidad):
        particulas.append(Particula(x, y, tipo, color))

# ---------- Utilidades Premium ----------
SUITS = ['♥', '♦', '♣', '♠']
VAL_STR = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

def valor_str(v):
    return VAL_STR.get(v, str(v))

def crear_degradado_vertical(width, height, color_top, color_bottom):
    """Crear superficie con degradado vertical"""
    surface = pygame.Surface((width, height))
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    return surface

def dibujar_texto_brillante_premium(surface, texto, x, y, fuente, color_base, intensidad=15):
    """Efecto de texto brillante premium"""
    # Sombra suave
    texto_sombra = fuente.render(texto, True, (0, 0, 0))
    surface.blit(texto_sombra, (x + 3, y + 3))
    
    # Efecto de brillo exterior
    for i in range(intensidad, 0, -2):
        alpha = 30 + i * 3
        color_brillo = (
            min(255, color_base[0] + i * 2),
            min(255, color_base[1] + i * 2),
            min(255, color_base[2] + i * 1)
        )
        # Crear superficie para el efecto de brillo
        brillo_surf = pygame.Surface((fuente.size(texto)[0] + i*2, fuente.size(texto)[1] + i*2), pygame.SRCALPHA)
        texto_brillo = fuente.render(texto, True, (*color_brillo, alpha))
        brillo_surf.blit(texto_brillo, (i, i))
        surface.blit(brillo_surf, (x - i, y - i))
    
    # Texto principal
    texto_principal = fuente.render(texto, True, color_base)
    surface.blit(texto_principal, (x, y))

def dibujar_boton_premium(surface, rect, texto, hover=False, disabled=False):
    """Dibujar botón con estilo premium"""
    # Fondo con degradado
    if disabled:
        color_top = (80, 80, 80)
        color_bottom = (50, 50, 50)
        color_borde = (100, 100, 100)
    elif hover:
        color_top = COLORES["ORO_CLARO"]
        color_bottom = COLORES["ORO_OSCURO"]
        color_borde = COLORES["ORO_PRINCIPAL"]
    else:
        color_top = COLORES["ORO_PRINCIPAL"]
        color_bottom = COLORES["ORO_OSCURO"]
        color_borde = COLORES["ORO_SECUNDARIO"]
    
    # Superficie del botón con degradado
    boton_surf = crear_degradado_vertical(rect.width, rect.height, color_top, color_bottom)
    
    # Efecto de brillo en el borde superior
    pygame.draw.line(boton_surf, COLORES["ORO_CLARO"], (5, 5), (rect.width-5, 5), 2)
    
    # Borde exterior
    pygame.draw.rect(boton_surf, color_borde, boton_surf.get_rect(), 3, border_radius=12)
    
    # Borde interior dorado
    pygame.draw.rect(boton_surf, COLORES["ORO_CLARO"], 
                    (2, 2, rect.width-4, rect.height-4), 2, border_radius=10)
    
    surface.blit(boton_surf, rect)
    
    # Texto del botón
    color_texto = COLORES["NEGRO_LUJO"] if not disabled else COLORES["PLATA_OSCURO"]
    texto_surf = fuente_media.render(texto, True, color_texto)
    texto_rect = texto_surf.get_rect(center=rect.center)
    surface.blit(texto_surf, texto_rect)
    
    return boton_surf

def dibujar_rect_redondeado_alpha(surface, rect, color, radius=12, alpha=255):
    """Dibujar rectángulo redondeado con transparencia"""
    surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    if len(color) == 4:
        pygame.draw.rect(surf, color, surf.get_rect(), border_radius=radius)
    else:
        pygame.draw.rect(surf, (*color, alpha), surf.get_rect(), border_radius=radius)
    surface.blit(surf, rect)

# ---------- Clases del Juego Premium ----------
class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor
        self.angulo = 0
        self.escala = 1.0
        self.alpha = 255
        self.brillo = 0

    def __str__(self):
        return f"{valor_str(self.valor)}{SUITS[self.palo]}"

    def color_carta(self):
        """Color premium para las cartas"""
        if self.palo in [0, 1]:  # Corazones y Diamantes
            return COLORES["ROJO_LUJO"]
        else:  # Tréboles y Picas
            return COLORES["NEGRO_LUJO"]

    def fondo_carta(self):
        """Fondo premium dorado o plateado"""
        if self.valor >= 12:  # Rey, Reina, As - Dorado
            return COLORES["ORO_PRINCIPAL"]
        else:  # Plateado para cartas menores
            return COLORES["PLATA"]

    def dibujar_premium(self, surface, x, y, w=78, h=110, boca_arriba=True):
        # Sombra premium
        sombra_surf = pygame.Surface((w + 8, h + 8), pygame.SRCALPHA)
        pygame.draw.rect(sombra_surf, (0, 0, 0, 120), sombra_surf.get_rect(), border_radius=12)
        surface.blit(sombra_surf, (x - 4, y - 4))

        # Superficie de la carta
        carta_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        
        if boca_arriba:
            # Fondo con textura premium
            fondo_color = self.fondo_carta()
            pygame.draw.rect(carta_surf, fondo_color, carta_surf.get_rect(), border_radius=10)
            
            # Patrón de lujo en el fondo
            for i in range(0, w, 8):
                for j in range(0, h, 8):
                    if (i + j) % 16 == 0:
                        pygame.draw.circle(carta_surf, (255, 255, 255, 30), (i, j), 1)
            
            # Borde exterior negro
            pygame.draw.rect(carta_surf, COLORES["NEGRO_CARTA"], carta_surf.get_rect(), 2, border_radius=10)
            
            # Borde interior dorado/plateado
            borde_color = COLORES["ORO_SECUNDARIO"] if self.valor >= 12 else COLORES["PLATA_OSCURO"]
            pygame.draw.rect(carta_surf, borde_color, (3, 3, w-6, h-6), 2, border_radius=8)
            
            # Valor superior
            txt_color = self.color_carta()
            valor_txt = fuente_media.render(str(self), True, txt_color)
            carta_surf.blit(valor_txt, (10, 8))
            
            # Símbolo del palo en el centro (más grande y elegante)
            simbolo = fuente_grande.render(SUITS[self.palo], True, txt_color)
            carta_surf.blit(simbolo, (w//2 - simbolo.get_width()//2, h//2 - simbolo.get_height()//2))
            
            # Valor inferior (invertido)
            valor_inv = fuente_media.render(str(self), True, txt_color)
            valor_inv = pygame.transform.rotate(valor_inv, 180)
            carta_surf.blit(valor_inv, (w - valor_inv.get_width() - 10, h - valor_inv.get_height() - 8))
            
            # Efecto de brillo si está activo
            if self.brillo > 0:
                brillo_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                pygame.draw.rect(brillo_surf, (255, 255, 200, self.brillo), brillo_surf.get_rect(), border_radius=10)
                carta_surf.blit(brillo_surf, (0, 0))
                
        else:
            # Dorso de carta premium - Diseño de casino de lujo
            pygame.draw.rect(carta_surf, COLORES["NEGRO_LUJO"], carta_surf.get_rect(), border_radius=10)
            
            # Borde dorado en el dorso
            pygame.draw.rect(carta_surf, COLORES["ORO_PRINCIPAL"], carta_surf.get_rect(), 3, border_radius=10)
            
            # Patrón geométrico de lujo
            centro_x, centro_y = w//2, h//2
            radio = min(w, h) // 3
            
            # Diseño central
            for i in range(8):
                angulo = math.radians(i * 45)
                x1 = centro_x + math.cos(angulo) * radio * 0.3
                y1 = centro_y + math.sin(angulo) * radio * 0.3
                x2 = centro_x + math.cos(angulo) * radio
                y2 = centro_y + math.sin(angulo) * radio
                pygame.draw.line(carta_surf, COLORES["ORO_SECUNDARIO"], (x1, y1), (x2, y2), 2)
            
            # Círculo central
            pygame.draw.circle(carta_surf, COLORES["ORO_PRINCIPAL"], (centro_x, centro_y), radio//3, 2)
            
            # Texto "PREMIUM"
            premium_txt = fuente_pequena.render("PREMIUM", True, COLORES["ORO_CLARO"])
            carta_surf.blit(premium_txt, (centro_x - premium_txt.get_width()//2, centro_y - premium_txt.get_height()//2))

        # Aplicar rotación si es necesario
        if self.angulo != 0:
            carta_surf = pygame.transform.rotate(carta_surf, self.angulo)
            
        # Aplicar transparencia
        if self.alpha < 255:
            carta_surf.set_alpha(self.alpha)
            
        surface.blit(carta_surf, (x, y))

class Jugador:
    def __init__(self, nombre, es_ia=False, fichas=2000, personalidad="normal"):
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
        self.personalidad = personalidad
        self.avatar_color = self.generar_color_premium()
        self.ultima_accion = ""
        self.tiempo_decision = 0
        self.efecto_brillo = 0

    def generar_color_premium(self):
        """Colores de avatar premium"""
        if self.nombre == "Tú":
            return COLORES["ORO_PRINCIPAL"]
        elif "Ana" in self.nombre:
            return (180, 80, 120)  # Rosa oscuro premium
        elif "Luis" in self.nombre:
            return (80, 160, 120)  # Verde esmeralda
        elif "Mia" in self.nombre:
            return (160, 100, 200)  # Púrpura real
        else:
            return (random.randint(120, 180), random.randint(120, 180), random.randint(120, 180))

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

    # IA mejorada
    def evaluar_mano_preflop(self):
        if len(self.mano) < 2:
            return 0.5
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
        if len(todas) < 5:
            return 0.5
        ranking, _ = evaluar_mejor_mano_static(todas)
        fuerza = ranking.value / 9.0
        if ronda == EstadoJuego.FLOP: fuerza *= 0.85
        elif ronda == EstadoJuego.TURN: fuerza *= 0.93
        return min(fuerza, 1.0)

    def tomar_decision_ia(self, apuesta_requerida, bote_actual, cartas_comunitarias, ronda, apuesta_minima, jugadores_en_vida):
        if not self.puede_jugar():
            return "fold", 0
            
        self.tiempo_decision = random.randint(500, 2000)
        fuerza = self.evaluar_fuerza_mano(cartas_comunitarias, ronda)
        
        if self.personalidad == "agresiva":
            fuerza *= 1.2
        elif self.personalidad == "conservadora":
            fuerza *= 0.8
        elif self.personalidad == "impredecible":
            fuerza = random.uniform(fuerza * 0.7, fuerza * 1.3)
        
        fuerza = max(0.1, min(1.0, fuerza))
        
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
    if len(cartas) < 5:
        return RankingMano.CARTA_ALTA, cartas
        
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
    if len(cartas) < 5:
        return RankingMano.CARTA_ALTA, cartas
        
    mejor_ranking = RankingMano.CARTA_ALTA
    mejor_mano = None
    
    for combo in combinations(cartas, 5):
        ranking, mano_ord = evaluar_combinacion_static(list(combo))
        if ranking.value > mejor_ranking.value:
            mejor_ranking = ranking
            mejor_mano = mano_ord
        elif ranking.value == mejor_ranking.value and mejor_mano is not None:
            # Comparar manos del mismo ranking
            comp = comparar_manos_static(mano_ord, mejor_mano, ranking)
            if comp > 0:
                mejor_mano = mano_ord
        elif ranking.value == mejor_ranking.value and mejor_mano is None:
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

# ---------- Clase Principal del Juego Premium ----------
class PokerGame:
    def __init__(self):
        self.jugadores = [
            Jugador("Tú", es_ia=False, fichas=3000),
            Jugador("IA - Ana", es_ia=True, fichas=2500, personalidad="agresiva"),
            Jugador("IA - Luis", es_ia=True, fichas=2500, personalidad="conservadora"),
            Jugador("IA - Mia", es_ia=True, fichas=2500, personalidad="impredecible")
        ]
        self.mazo = []
        self.cartas_comunitarias = []
        self.bote = 0
        self.apuesta_minima = 50
        self.dealer_index = 0
        self.jugador_actual_index = 1
        self.estado = EstadoJuego.PREFLOP
        self.ronda_terminada = False
        self.ganador = None
        self.animaciones = []
        self.efecto_brillo_mesa = 0
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
                if len(self.mazo) > 0:
                    j.recibir_carta(self.mazo.pop())

    def repartir_cartas_comunitarias(self):
        if self.estado == EstadoJuego.FLOP and len(self.cartas_comunitarias) == 0:
            if len(self.mazo) > 0: 
                self.mazo.pop()  # Quemar carta
            for _ in range(3):
                if len(self.mazo) > 0:
                    carta = self.mazo.pop()
                    self.cartas_comunitarias.append(carta)
                    crear_particulas(WIDTH//2, HEIGHT//2, 30, "oro")
                    
        elif self.estado == EstadoJuego.TURN and len(self.cartas_comunitarias) == 3:
            if len(self.mazo) > 0: 
                self.mazo.pop()  # Quemar carta
            if len(self.mazo) > 0:
                carta = self.mazo.pop()
                self.cartas_comunitarias.append(carta)
                crear_particulas(WIDTH//2, HEIGHT//2, 20, "oro")
                
        elif self.estado == EstadoJuego.RIVER and len(self.cartas_comunitarias) == 4:
            if len(self.mazo) > 0: 
                self.mazo.pop()  # Quemar carta
            if len(self.mazo) > 0:
                carta = self.mazo.pop()
                self.cartas_comunitarias.append(carta)
                crear_particulas(WIDTH//2, HEIGHT//2, 20, "oro")

    def iniciar_nueva_mano(self):
        self.crear_mazo()
        self.barajar()
        self.cartas_comunitarias = []
        self.bote = 0
        self.estado = EstadoJuego.PREFLOP
        self.ronda_terminada = False
        self.ganador = None
        
        self.dealer_index = (self.dealer_index + 1) % len(self.jugadores)
        
        for j in self.jugadores:
            j.reset_apuesta()
            j.mano = []
            j.en_juego = True if j.fichas > 0 else False
            j.ha_hecho_all_in = False
            j.mano_final = None
            j.ranking_mano = None
        
        self.repartir_cartas()
        
        # Aplicar blinds
        small = self.apuesta_minima // 2
        big = self.apuesta_minima
        sb_idx = (self.dealer_index + 1) % len(self.jugadores)
        bb_idx = (self.dealer_index + 2) % len(self.jugadores)
        
        crear_particulas(WIDTH//2, HEIGHT//2, 40, "oro")
        
        self.jugadores[sb_idx].hacer_apuesta(small)
        self.jugadores[bb_idx].hacer_apuesta(big)
        self.bote = small + big
        
        self.jugador_actual_index = (bb_idx + 1) % len(self.jugadores)

    def encontrar_siguiente_jugador_index(self, desde):
        n = len(self.jugadores)
        for i in range(1, n+1):
            idx = (desde + i) % n
            j = self.jugadores[idx]
            if j.en_juego and (not j.ha_hecho_all_in) and j.fichas > 0:
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
            
        crear_particulas(WIDTH//2, HEIGHT//2, 60, "oro")
        
        for j in self.jugadores:
            j.reset_apuesta()
        self.ronda_terminada = False
        self.jugador_actual_index = (self.dealer_index + 1) % len(self.jugadores)

    def determinar_ganador(self):
        jugadores_activos = [j for j in self.jugadores if j.en_juego]
        if len(jugadores_activos) == 1:
            self.ganador = jugadores_activos[0]
            self.ganador.fichas += self.bote
            crear_particulas(WIDTH//2, HEIGHT//2, 150, "oro")
            crear_particulas(WIDTH//2, HEIGHT//2, 50, "diamante")
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
        crear_particulas(WIDTH//2, HEIGHT//2, 200, "oro")
        crear_particulas(WIDTH//2, HEIGHT//2, 80, "diamante")
        self.bote = 0

# ---------- Renderizado UI Premium ----------
def dibujar_mesa_premium(surface, juego):
    # Fondo con textura de terciopelo negro
    for y in range(HEIGHT):
        color = (
            max(0, COLORES["NEGRO_LUJO"][0] + (y // 100)),
            max(0, COLORES["NEGRO_LUJO"][1] + (y // 120)),
            max(0, COLORES["NEGRO_LUJO"][2] + (y // 140))
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))
    
    # Efecto de brillo pulsante en la mesa
    juego.efecto_brillo_mesa = (juego.efecto_brillo_mesa + 0.02) % (2 * math.pi)
    brillo_intensidad = int(30 + 15 * math.sin(juego.efecto_brillo_mesa))
    
    # Mesa ovalada premium
    tabla_ancho = int(WIDTH * 0.88)
    tabla_alto = int(HEIGHT * 0.65)
    tabla_x = (WIDTH - tabla_ancho) // 2
    tabla_y = (HEIGHT - tabla_alto) // 2
    
    # Sombra de lujo
    sombra_surf = pygame.Surface((tabla_ancho + 30, tabla_alto + 30), pygame.SRCALPHA)
    for i in range(15, 0, -2):
        alpha = 100 - i * 6
        pygame.draw.ellipse(sombra_surf, (0, 0, 0, alpha), 
                          (15-i, 15-i, tabla_ancho+2*i, tabla_alto+2*i))
    surface.blit(sombra_surf, (tabla_x-15, tabla_y-15))
    
    # Mesa principal con degradado dorado
    tabla = crear_degradado_vertical(tabla_ancho, tabla_alto, COLORES["NEGRO_SUAVE"], COLORES["NEGRO_LUJO"])
    
    # Patrón de diseño premium en la mesa
    centro_x, centro_y = tabla_ancho // 2, tabla_alto // 2
    radio_max = min(tabla_ancho, tabla_alto) // 2 - 20
    
    # Diseño circular concéntrico dorado
    for i in range(1, 6):
        radio = radio_max - i * 25
        if radio > 0:
            pygame.draw.ellipse(tabla, COLORES["ORO_PRINCIPAL"], 
                              (centro_x - radio, centro_y - radio, radio*2, radio*2), 3)
    
    # Líneas radiales doradas
    for i in range(8):
        angulo = math.radians(i * 45)
        x1 = centro_x + math.cos(angulo) * 50
        y1 = centro_y + math.sin(angulo) * 50
        x2 = centro_x + math.cos(angulo) * (radio_max - 10)
        y2 = centro_y + math.sin(angulo) * (radio_max - 10)
        pygame.draw.line(tabla, COLORES["ORO_SECUNDARIO"], (x1, y1), (x2, y2), 2)
    
    # Borde exterior de lujo
    pygame.draw.ellipse(tabla, COLORES["ORO_PRINCIPAL"], tabla.get_rect(), 8)
    pygame.draw.ellipse(tabla, COLORES["ORO_CLARO"], (4, 4, tabla_ancho-8, tabla_alto-8), 4)
    
    surface.blit(tabla, (tabla_x, tabla_y))
    
    # Logo premium centrado
    logo_texto = fuente_titulo.render("CASINO PREMIUM", True, COLORES["ORO_CLARO"])
    surface.blit(logo_texto, (WIDTH//2 - logo_texto.get_width()//2, HEIGHT//2 - logo_texto.get_height()//2))
    
    logo_subtexto = fuente_elegante.render("Texas Hold'em Edition", True, COLORES["PLATA"])
    surface.blit(logo_subtexto, (WIDTH//2 - logo_subtexto.get_width()//2, HEIGHT//2 + 40))

def dibujar_jugadores_premium(surface, juego):
    posiciones = [
        (WIDTH//2, int(HEIGHT*0.78)),      # bottom - player
        (int(WIDTH*0.84), int(HEIGHT*0.48)), # right
        (WIDTH//2, int(HEIGHT*0.18)),      # top
        (int(WIDTH*0.16), int(HEIGHT*0.48))  # left
    ]
    
    for i, j in enumerate(juego.jugadores):
        x, y = posiciones[i]
        
        # Avatar circular premium
        avatar_radio = 50
        
        # Sombra del avatar
        sombra_surf = pygame.Surface((avatar_radio*2 + 12, avatar_radio*2 + 12), pygame.SRCALPHA)
        pygame.draw.circle(sombra_surf, (0, 0, 0, 120), (avatar_radio+6, avatar_radio+6), avatar_radio)
        surface.blit(sombra_surf, (x-avatar_radio-6, y-avatar_radio-6))
        
        # Avatar con efecto de metal pulido
        pygame.draw.circle(surface, j.avatar_color, (x, y), avatar_radio)
        
        # Efecto de brillo en el avatar
        if i == juego.jugador_actual_index:
            for r in range(avatar_radio + 2, avatar_radio + 10, 2):
                brillo_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                alpha = 100 - (r - avatar_radio) * 15
                pygame.draw.circle(brillo_surf, (255, 255, 255, alpha), (r, r), r, 2)
                surface.blit(brillo_surf, (x - r, y - r))
        
        # Borde dorado del avatar
        pygame.draw.circle(surface, COLORES["ORO_PRINCIPAL"], (x, y), avatar_radio, 3)
        pygame.draw.circle(surface, COLORES["ORO_CLARO"], (x, y), avatar_radio-2, 1)
        
        # Panel de información del jugador
        panel_ancho = 180
        panel_alto = 90
        panel_rect = pygame.Rect(x - panel_ancho//2, y + avatar_radio + 15, panel_ancho, panel_alto)
        
        # Fondo del panel con efecto cristal
        panel_surf = pygame.Surface((panel_ancho, panel_alto), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (30, 30, 30, 220), panel_surf.get_rect(), border_radius=10)
        pygame.draw.rect(panel_surf, COLORES["ORO_SECUNDARIO"], panel_surf.get_rect(), 2, border_radius=10)
        surface.blit(panel_surf, panel_rect)
        
        # Nombre del jugador
        color_nombre = COLORES["BLANCO_PREMIUM"] if j.en_juego else COLORES["PLATA_OSCURO"]
        nombre = fuente_pequena.render(j.nombre, True, color_nombre)
        surface.blit(nombre, (x - nombre.get_width()//2, y + avatar_radio + 25))
        
        # Fichas
        fichas = fuente_pequena.render(f"${j.fichas:,}", True, COLORES["ORO_CLARO"])
        surface.blit(fichas, (x - fichas.get_width()//2, y + avatar_radio + 45))
        
        # Apuesta actual
        if j.apuesta_actual > 0:
            apuesta = fuente_pequena.render(f"Apuesta: ${j.apuesta_actual}", True, COLORES["BLANCO_PREMIUM"])
            surface.blit(apuesta, (x - apuesta.get_width()//2, y + avatar_radio + 65))
        
        # Botón dealer
        if i == juego.dealer_index:
            dealer_rect = pygame.Rect(x - 25, y - avatar_radio - 30, 50, 24)
            pygame.draw.rect(surface, COLORES["ORO_PRINCIPAL"], dealer_rect, border_radius=12)
            pygame.draw.rect(surface, COLORES["ORO_CLARO"], dealer_rect, 2, border_radius=12)
            dealer_text = fuente_pequena.render("D", True, COLORES["NEGRO_LUJO"])
            surface.blit(dealer_text, (dealer_rect.centerx - dealer_text.get_width()//2, 
                                     dealer_rect.centery - dealer_text.get_height()//2))
        
        # Estados especiales
        if j.ha_hecho_all_in:
            allin_rect = pygame.Rect(x - 40, y - avatar_radio - 60, 80, 24)
            pygame.draw.rect(surface, (180, 40, 40), allin_rect, border_radius=12)
            pygame.draw.rect(surface, COLORES["ORO_CLARO"], allin_rect, 2, border_radius=12)
            allin_text = fuente_pequena.render("ALL IN", True, COLORES["BLANCO_PREMIUM"])
            surface.blit(allin_text, (allin_rect.centerx - allin_text.get_width()//2, 
                                    allin_rect.centery - allin_text.get_height()//2))
        elif not j.en_juego:
            fold_rect = pygame.Rect(x - 35, y - avatar_radio - 60, 70, 24)
            pygame.draw.rect(surface, (80, 80, 80), fold_rect, border_radius=12)
            fold_text = fuente_pequena.render("FOLD", True, COLORES["BLANCO_PREMIUM"])
            surface.blit(fold_text, (fold_rect.centerx - fold_text.get_width()//2, 
                                   fold_rect.centery - fold_text.get_height()//2))
        
        # Cartas del jugador
        boca_arriba = (not j.es_ia) or (j.en_juego and juego.estado == EstadoJuego.SHOWDOWN) or (i == 0)
        for idx, carta in enumerate(j.mano):
            carta_x = x - 50 + idx * 60
            carta_y = y + avatar_radio + 110
            if idx < len(j.mano):  # Verificar que existe la carta
                carta.dibujar_premium(surface, carta_x, carta_y, w=72, h=100, boca_arriba=boca_arriba)
        
        # Última acción de IA
        if j.es_ia and j.ultima_accion and juego.estado != EstadoJuego.SHOWDOWN:
            accion_rect = pygame.Rect(x - 60, y - avatar_radio - 90, 120, 24)
            accion_surf = pygame.Surface((120, 24), pygame.SRCALPHA)
            pygame.draw.rect(accion_surf, (40, 40, 40, 200), accion_surf.get_rect(), border_radius=8)
            surface.blit(accion_surf, accion_rect)
            accion_text = fuente_pequena.render(j.ultima_accion, True, COLORES["ORO_CLARO"])
            surface.blit(accion_text, (accion_rect.centerx - accion_text.get_width()//2, 
                                     accion_rect.centery - accion_text.get_height()//2))

def dibujar_comunitarias_premium(surface, juego):
    x0 = WIDTH//2 - 240
    y0 = HEIGHT//2 - 70
    
    # Panel de cartas comunitarias con estilo lujo
    panel_ancho = 5 * 120 + 60
    panel_alto = 160
    panel_rect = pygame.Rect(x0 - 30, y0 - 30, panel_ancho, panel_alto)
    
    # Fondo del panel
    panel_surf = pygame.Surface((panel_ancho, panel_alto), pygame.SRCALPHA)
    pygame.draw.rect(panel_surf, (20, 20, 20, 200), panel_surf.get_rect(), border_radius=15)
    pygame.draw.rect(panel_surf, COLORES["ORO_PRINCIPAL"], panel_surf.get_rect(), 4, border_radius=15)
    pygame.draw.rect(panel_surf, COLORES["ORO_CLARO"], (2, 2, panel_ancho-4, panel_alto-4), 2, border_radius=13)
    surface.blit(panel_surf, panel_rect)
    
    # Cartas comunitarias
    for i in range(5):
        if i < len(juego.cartas_comunitarias):
            # Aplicar efecto de brillo a las cartas comunitarias
            if juego.estado.value >= i + 1:  # Solo brillar cuando se revelan
                juego.cartas_comunitarias[i].brillo = 50
            juego.cartas_comunitarias[i].dibujar_premium(surface, x0 + i * 120, y0, w=100, h=140, boca_arriba=True)
        else:
            # Placeholder con efecto de anticipación
            if juego.estado.value >= i:
                alpha = 150 + int(105 * math.sin(pygame.time.get_ticks() / 600))
                carta_placeholder = Carta(0, 2)
                carta_placeholder.alpha = alpha
                carta_placeholder.dibujar_premium(surface, x0 + i * 120, y0, w=100, h=140, boca_arriba=False)
    
    # Bote con estilo premium
    bote_text = f"BOTE: ${juego.bote:,}"
    bote_surf = fuente_grande.render(bote_text, True, COLORES["ORO_CLARO"])
    surface.blit(bote_surf, (WIDTH//2 - bote_surf.get_width()//2, y0 - 80))
    
    # Estado de la ronda
    estados = {
        EstadoJuego.PREFLOP: "PRE-FLOP", 
        EstadoJuego.FLOP: "FLOP", 
        EstadoJuego.TURN: "TURN", 
        EstadoJuego.RIVER: "RIVER", 
        EstadoJuego.SHOWDOWN: "SHOWDOWN", 
        EstadoJuego.FINAL: "MANO FINALIZADA"
    }
    estado_text = fuente_media.render(estados[juego.estado], True, COLORES["ORO_SECUNDARIO"])
    surface.blit(estado_text, (WIDTH//2 - estado_text.get_width()//2, 30))

def dibujar_controles_premium(surface, juego):
    if juego.jugador_actual_index >= len(juego.jugadores):
        return None, None, None, None
        
    jugador = juego.jugadores[juego.jugador_actual_index]
    
    # Panel de controles premium
    panel_ancho = 600
    panel_alto = 140
    panel_rect = pygame.Rect(WIDTH//2 - panel_ancho//2, HEIGHT - panel_alto - 20, panel_ancho, panel_alto)
    
    # Fondo del panel con efecto de cristal esmerilado
    panel_surf = pygame.Surface((panel_ancho, panel_alto), pygame.SRCALPHA)
    pygame.draw.rect(panel_surf, (30, 30, 30, 230), panel_surf.get_rect(), border_radius=20)
    pygame.draw.rect(panel_surf, COLORES["ORO_PRINCIPAL"], panel_surf.get_rect(), 4, border_radius=20)
    pygame.draw.rect(panel_surf, COLORES["ORO_CLARO"], (2, 2, panel_ancho-4, panel_alto-4), 2, border_radius=18)
    surface.blit(panel_surf, panel_rect)
    
    # Título del panel
    titulo = fuente_media.render("TU TURNO", True, COLORES["ORO_CLARO"])
    surface.blit(titulo, (panel_rect.centerx - titulo.get_width()//2, panel_rect.y + 15))
    
    # Botones de acción
    btn_ancho = 130
    btn_alto = 50
    espacio = 20
    
    fold_r = pygame.Rect(panel_rect.x + espacio, panel_rect.y + 60, btn_ancho, btn_alto)
    call_r = pygame.Rect(panel_rect.x + espacio*2 + btn_ancho, panel_rect.y + 60, btn_ancho, btn_alto)
    raise_r = pygame.Rect(panel_rect.x + espacio*3 + btn_ancho*2, panel_rect.y + 60, btn_ancho, btn_alto)
    allin_r = pygame.Rect(panel_rect.x + espacio*4 + btn_ancho*3, panel_rect.y + 60, btn_ancho, btn_alto)
    
    mouse_pos = pygame.mouse.get_pos()
    
    # Dibujar botones
    dibujar_boton_premium(surface, fold_r, "FOLD", fold_r.collidepoint(mouse_pos))
    
    necesidad = max(0, juego.apuesta_minima - jugador.apuesta_actual)
    dibujar_boton_premium(surface, call_r, f"CALL ${necesidad}", call_r.collidepoint(mouse_pos))
    
    dibujar_boton_premium(surface, raise_r, "RAISE", raise_r.collidepoint(mouse_pos))
    dibujar_boton_premium(surface, allin_r, "ALL IN", allin_r.collidepoint(mouse_pos))
    
    # Información de apuesta
    info_text = fuente_pequena.render(f"Apuesta mínima: ${juego.apuesta_minima}", True, COLORES["PLATA"])
    surface.blit(info_text, (panel_rect.x + 20, panel_rect.y + 115))
    
    return fold_r, call_r, raise_r, allin_r

def dibujar_menu_principal_premium(surface):
    # Fondo con textura de terciopelo negro
    for y in range(HEIGHT):
        base_color = COLORES["NEGRO_LUJO"]
        color = (
            max(0, min(255, base_color[0])),
            max(0, min(255, base_color[1])),
            max(0, min(255, base_color[2]))
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))
    
    # Título principal
    titulo_texto = "TEXAS HOLD'EM"
    titulo_surf = fuente_muy_grande.render(titulo_texto, True, COLORES["ORO_CLARO"])
    titulo_rect = titulo_surf.get_rect(center=(WIDTH//2, 150))
    surface.blit(titulo_surf, titulo_rect)
    
    # Sombra del título
    titulo_sombra = fuente_muy_grande.render(titulo_texto, True, (0, 0, 0))
    surface.blit(titulo_sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
    
    # Subtítulo
    subtitulo = fuente_titulo.render("EDICIÓN PREMIUM ORO", True, COLORES["ORO_SECUNDARIO"])
    surface.blit(subtitulo, (WIDTH//2 - subtitulo.get_width()//2, 230))
    
    # Botón jugar premium
    boton_jugar = pygame.Rect(WIDTH//2 - 150, 350, 300, 80)
    mouse_pos = pygame.mouse.get_pos()
    hover_jugar = boton_jugar.collidepoint(mouse_pos)
    
    dibujar_boton_premium(surface, boton_jugar, "JUGAR", hover_jugar)
    
    # Panel de bienvenida
    panel_wel = pygame.Rect(WIDTH//2 - 250, 450, 500, 200)
    panel_surf = pygame.Surface((500, 200), pygame.SRCALPHA)
    pygame.draw.rect(panel_surf, (20, 20, 20, 200), panel_surf.get_rect(), border_radius=15)
    pygame.draw.rect(panel_surf, COLORES["ORO_PRINCIPAL"], panel_surf.get_rect(), 3, border_radius=15)
    surface.blit(panel_surf, panel_wel)
    
    # Texto de bienvenida
    bienvenida = fuente_media.render("Bienvenido al Casino Premium", True, COLORES["ORO_CLARO"])
    surface.blit(bienvenida, (panel_wel.centerx - bienvenida.get_width()//2, panel_wel.y + 20))
    
    instrucciones = [
        "• Estrategia y suerte se unen en la mesa premium",
        "• Cartas doradas y plateadas exclusivas",
        "• Diseño de lujo en oro y negro",
        "• IA avanzada con personalidades únicas",
        "• Efectos visuales y animaciones premium"
    ]
    
    for i, linea in enumerate(instrucciones):
        texto = fuente_pequena.render(linea, True, COLORES["PLATA"])
        surface.blit(texto, (panel_wel.x + 30, panel_wel.y + 60 + i * 25))
    
    # Footer
    footer = fuente_pequena.render("© 2024 Casino Premium - Todos los derechos reservados", 
                                 True, COLORES["PLATA_OSCURO"])
    surface.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT - 40))
    
    return boton_jugar

# ---------- Loop Principal Premium ----------
def main():
    global particulas
    
    juego = PokerGame()
    running = True
    click_cooldown = 0
    estado_aplicacion = "menu"
    
    # Efectos de partículas iniciales
    for _ in range(100):
        crear_particulas(random.randint(0, WIDTH), random.randint(0, HEIGHT), 1, "oro")
    
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
                    boton_jugar = dibujar_menu_principal_premium(screen)
                    if boton_jugar.collidepoint(mouse):
                        estado_aplicacion = "jugando"
                        juego.iniciar_nueva_mano()
                        click_cooldown = 20
                        crear_particulas(mouse[0], mouse[1], 50, "oro")
                
                elif estado_aplicacion == "jugando":
                    if (juego.jugador_actual_index < len(juego.jugadores) and 
                        not juego.jugadores[juego.jugador_actual_index].es_ia and 
                        juego.estado not in (EstadoJuego.SHOWDOWN, EstadoJuego.FINAL)):
                        
                        fold_r, call_r, raise_r, allin_r = dibujar_controles_premium(screen, juego)
                        
                        if fold_r and fold_r.collidepoint(mouse):
                            juego.jugadores[juego.jugador_actual_index].en_juego = False
                            next_idx = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index)
                            juego.jugador_actual_index = next_idx if next_idx is not None else juego.jugador_actual_index
                            click_cooldown = 10
                            crear_particulas(mouse[0], mouse[1], 20, "brillo_oro")
                            
                        elif call_r and call_r.collidepoint(mouse):
                            j = juego.jugadores[juego.jugador_actual_index]
                            necesidad = max(0, juego.apuesta_minima - j.apuesta_actual)
                            apuesta = j.hacer_apuesta(necesidad)
                            juego.bote += apuesta
                            next_idx = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index)
                            juego.jugador_actual_index = next_idx if next_idx is not None else juego.jugador_actual_index
                            click_cooldown = 10
                            crear_particulas(mouse[0], mouse[1], 30, "oro")
                            
                        elif raise_r and raise_r.collidepoint(mouse):
                            j = juego.jugadores[juego.jugador_actual_index]
                            incremento = min(j.fichas, max(juego.apuesta_minima*2, int(juego.apuesta_minima*1.5)))
                            apuesta = j.hacer_apuesta(incremento)
                            juego.bote += apuesta
                            juego.apuesta_minima = j.apuesta_actual
                            next_idx = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index)
                            juego.jugador_actual_index = next_idx if next_idx is not None else juego.jugador_actual_index
                            click_cooldown = 10
                            crear_particulas(mouse[0], mouse[1], 40, "oro")
                            
                        elif allin_r and allin_r.collidepoint(mouse):
                            j = juego.jugadores[juego.jugador_actual_index]
                            apuesta = j.hacer_apuesta(j.fichas)
                            juego.bote += apuesta
                            next_idx = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index)
                            juego.jugador_actual_index = next_idx if next_idx is not None else juego.jugador_actual_index
                            click_cooldown = 10
                            crear_particulas(mouse[0], mouse[1], 60, "oro")
                
                if estado_aplicacion == "jugando" and juego.estado == EstadoJuego.FINAL:
                    btn_nueva = pygame.Rect(WIDTH//2-140, HEIGHT//2+80, 280, 60)
                    if btn_nueva.collidepoint(mouse):
                        juego.iniciar_nueva_mano()
                        click_cooldown = 12
                        crear_particulas(mouse[0], mouse[1], 40, "oro")
        
        # Lógica del juego
        if estado_aplicacion == "jugando":
            if (juego.jugador_actual_index < len(juego.jugadores) and
                juego.jugadores[juego.jugador_actual_index].es_ia and 
                juego.estado not in (EstadoJuego.SHOWDOWN, EstadoJuego.FINAL)):
                
                current = juego.jugadores[juego.jugador_actual_index]
                apuesta_req = max(0, juego.apuesta_minima - current.apuesta_actual)
                decision, cantidad = current.tomar_decision_ia(apuesta_req, juego.bote, juego.cartas_comunitarias, juego.estado, juego.apuesta_minima, len([x for x in juego.jugadores if x.en_juego]))
                
                if decision == "fold":
                    current.en_juego = False
                    crear_particulas(WIDTH//2, HEIGHT//2, 20, "brillo_oro")
                elif decision == "call":
                    apuesta = current.hacer_apuesta(cantidad)
                    juego.bote += apuesta
                    crear_particulas(WIDTH//2, HEIGHT//2, 25, "oro")
                elif decision == "raise":
                    apuesta = current.hacer_apuesta(cantidad)
                    juego.bote += apuesta
                    juego.apuesta_minima = current.apuesta_actual
                    crear_particulas(WIDTH//2, HEIGHT//2, 35, "oro")
                
                nxt = juego.encontrar_siguiente_jugador_index(juego.jugador_actual_index)
                juego.jugador_actual_index = nxt if nxt is not None else juego.jugador_actual_index
            
            juego.verificar_fin_ronda()
            if juego.ronda_terminada and juego.estado not in (EstadoJuego.SHOWDOWN, EstadoJuego.FINAL):
                juego.repartir_cartas_comunitarias()
                juego.siguiente_estado()
        
        # Renderizado
        screen.fill(COLORES["NEGRO_LUJO"])
        
        if estado_aplicacion == "menu":
            dibujar_menu_principal_premium(screen)
        elif estado_aplicacion == "jugando":
            dibujar_mesa_premium(screen, juego)
            dibujar_comunitarias_premium(screen, juego)
            dibujar_jugadores_premium(screen, juego)
            
            if (juego.jugador_actual_index < len(juego.jugadores) and
                not juego.jugadores[juego.jugador_actual_index].es_ia and 
                juego.estado not in (EstadoJuego.SHOWDOWN, EstadoJuego.FINAL)):
                
                dibujar_controles_premium(screen, juego)
            
            if juego.ganador:
                # Panel de ganador premium
                panel_ganador = pygame.Rect(WIDTH//2 - 300, HEIGHT//2 - 150, 600, 200)
                panel_surf = pygame.Surface((600, 200), pygame.SRCALPHA)
                pygame.draw.rect(panel_surf, (0, 0, 0, 220), panel_surf.get_rect(), border_radius=20)
                pygame.draw.rect(panel_surf, COLORES["ORO_PRINCIPAL"], panel_surf.get_rect(), 5, border_radius=20)
                pygame.draw.rect(panel_surf, COLORES["ORO_CLARO"], (2, 2, 596, 196), 3, border_radius=18)
                screen.blit(panel_surf, panel_ganador)
                
                ganador_texto = fuente_titulo.render(f"¡{juego.ganador.nombre} GANA!", True, COLORES["ORO_CLARO"])
                screen.blit(ganador_texto, (WIDTH//2 - ganador_texto.get_width()//2, HEIGHT//2 - 120))
                
                if juego.estado == EstadoJuego.SHOWDOWN and juego.ganador.mano_final:
                    mano_texto = fuente_media.render(f"Mano: {juego.ganador.ranking_mano.name.replace('_', ' ').title()}", 
                                                   True, COLORES["PLATA"])
                    screen.blit(mano_texto, (WIDTH//2 - mano_texto.get_width()//2, HEIGHT//2 - 60))
                
                premio_texto = fuente_media.render(f"Premio: ${juego.bote:,}", True, COLORES["ORO_SECUNDARIO"])
                screen.blit(premio_texto, (WIDTH//2 - premio_texto.get_width()//2, HEIGHT//2 - 20))
            
            if juego.estado == EstadoJuego.FINAL:
                btn_nueva = pygame.Rect(WIDTH//2-140, HEIGHT//2+80, 280, 60)
                mouse_pos = pygame.mouse.get_pos()
                dibujar_boton_premium(screen, btn_nueva, "NUEVA MANO", btn_nueva.collidepoint(mouse_pos))
        
        # Dibujar partículas
        for particula in particulas:
            particula.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()