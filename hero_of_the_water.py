"""
HERO OF WATER v5.0
Jogo educativo sobre a ODS 6 - Água Limpa e Saneamento
5 fases com mecanicas unicas, sistema de estrelas e progressao
Side-scrolling camera, audio system com suporte a arquivos externos
Trilha sonora chiptune gerada proceduralmente

Equipe: Filipe Henry, André de Lira, Júlio Sérgio, João Victor

=== CUSTOM AUDIO FILES ===
Place any of these files in the game directory to override generated audio:
  custom_music_menu.wav      - Menu music
  custom_music_phase1.wav    - Phase 1 music
  custom_music_phase2.wav    - Phase 2 music
  custom_music_phase3.wav    - Phase 3 music
  custom_music_phase4.wav    - Phase 4 music
  custom_music_gameplay.wav  - Fallback gameplay music (if phase-specific missing)
  custom_sfx_jump.wav        - Jump sound effect
  custom_sfx_collect.wav     - Collect item sound
  custom_sfx_hurt.wav        - Damage/hurt sound
  custom_sfx_repair.wav      - Repair complete sound
  custom_sfx_deliver.wav     - Deliver water sound
  custom_sfx_menu_click.wav  - Menu click sound
  custom_sfx_menu_hover.wav  - Menu hover sound
  custom_sfx_phase_complete.wav - Phase complete jingle
  custom_sfx_star_earned.wav - Star earned sound
  custom_sfx_throw.wav       - Net throw sound
  custom_sfx_error.wav       - Error/wrong sound
  custom_sfx_station.wav     - Station correct sound
"""

# ============================================================
# IMPORTACAO DE BIBLIOTECAS
# ============================================================
import pygame          # Biblioteca principal para jogos (graficos, som, eventos)
import sys             # Para saida do sistema (sys.exit())
import random          # Para geracao de numeros aleatorios (posicoes, variacao)
import math            # Operacoes matematicas (seno, cosseno, radianos)
import time as time_module  # Medicao de tempo real (timer, delta time)
import wave            # Manipulacao de arquivos WAV para gerar musica
import struct          # Empacotamento de bytes para WAV
import os              # Manipulacao de caminhos de arquivos

# ============================================================
# INICIALIZACAO DO PYGAME
# ============================================================
pygame.init()  # Inicializa todos os modulos do Pygame
# Inicializa o mixer de audio com frequencia 22050Hz, 16 bits, 2 canais (stereo)
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)

# Dimensoes da tela (largura x altura)
SCREEN_W, SCREEN_H = 960, 640
# Cria a janela do jogo em modo tela cheia com escala
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Hero of Water - Samuel v5.0")  # Titulo da janela
clock = pygame.time.Clock()   # Relogio para controlar FPS
FPS = 60                      # Quadros por segundo

# Diretorio onde esta o arquivo do jogo
GAME_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# PALETA DE CORES
# ============================================================
# ---------- CORES BASICAS ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)     # Azul do ceu
SKY_TOP = (90, 170, 220)       # Topo do gradiente do ceu
DARK_BLUE = (13, 27, 42)       # Azul escuro (loading, fundos)

# ---------- CORES DA AGUA ----------
WATER_BLUE = (64, 164, 223)    # Azul principal da agua
WATER_LIGHT = (100, 195, 240)  # Agua clara (destaque)
WATER_DARK = (40, 120, 180)    # Agua escura (sombra)

# ---------- CORES DA GRAMA E TERRA ----------
GRASS_GREEN = (76, 153, 0)
GRASS_LIGHT = (100, 180, 30)
GRASS_DARK = (55, 115, 0)
DIRT_BROWN = (139, 90, 43)
DIRT_DARK = (100, 65, 30)
DIRT_LIGHT = (170, 120, 60)

# ---------- CORES DE INTERFACE ----------
RED = (220, 50, 50)            # Vermelho generico (erro, perigo)
HEART_RED = (230, 60, 70)      # Vermelho do coracao (vidas)
HEART_DARK = (180, 40, 50)     # Sombra do coracao
YELLOW = (255, 215, 0)         # Amarelo generico
STAR_YELLOW = (255, 200, 50)   # Amarelo da estrela
STAR_DARK = (200, 160, 30)     # Sombra da estrela
ORANGE = (230, 126, 34)        # Laranja
GREEN_OK = (80, 200, 80)       # Verde de sucesso

# ---------- CORES DOS BOTOES ----------
GREEN_BTN = (100, 180, 60)     # Botao verde (normal)
GREEN_BTN_H = (120, 200, 80)   # Botao verde (hover/destacado)
BROWN_BTN = (120, 80, 40)      # Botao marrom (normal)
BROWN_BTN_H = (150, 100, 55)   # Botao marrom (hover)
GRAY_BTN = (100, 100, 110)     # Botao cinza
GRAY_BTN_H = (130, 130, 140)   # Botao cinza (hover)

# ---------- CORES DO PERSONAGEM SAMUEL ----------
SAMUEL_SKIN = (160, 100, 60)        # Pele
SAMUEL_SKIN_LIGHT = (180, 120, 75)  # Pele clara (destaque)
SAMUEL_HAIR = (45, 25, 12)          # Cabelo afro
CAPE_RED = (200, 40, 40)            # Capa vermelha
CAPE_DARK = (160, 30, 30)           # Sombra da capa
SHIRT_WHITE = (240, 240, 240)       # Camisa branca
VEST_ORANGE = (220, 140, 40)        # Colete laranja
VEST_DARK = (190, 115, 30)          # Sombra do colete
PANTS_BROWN = (100, 70, 40)         # Calca marrom
PANTS_DARK = (80, 55, 30)           # Sombra da calca
SHOE_RED = (200, 50, 50)            # Tenis vermelho
BELT_BROWN = (80, 50, 25)           # Cinto

# ---------- CORES DOS CENARIOS ----------
TREE_GREEN = (50, 140, 50)     # Folhagem da arvore
TREE_DARK = (35, 100, 35)      # Folhagem escura
TREE_LIGHT = (70, 170, 70)     # Folhagem clara
TREE_TRUNK = (120, 70, 30)     # Tronco
CLOUD_WHITE = (245, 250, 255)  # Nuvem branca
CLOUD_SHADOW = (215, 225, 238) # Sombra da nuvem
PIPE_GRAY = (140, 140, 150)    # Cano cinza
PIPE_DARK = (100, 100, 110)    # Cano escuro
PIPE_LIGHT = (180, 180, 190)   # Cano claro
PIPE_RUST = (160, 100, 60)     # Cano enferrujado
HOUSE_WALL = (200, 180, 160)   # Parede da casa
HOUSE_WALL2 = (180, 160, 140)  # Parede variante
HOUSE_ROOF = (180, 80, 60)     # Telhado
HOUSE_ROOF2 = (160, 100, 70)   # Telhado variante
HOUSE_DOOR = (120, 70, 40)     # Porta
POLLUTION_GREEN = (80, 120, 40)  # Poluicao verde
POLLUTION_DARK = (50, 80, 30)    # Poluicao escura
MACHINE_BLUE = (60, 140, 160)    # Maquina azul
MACHINE_DARK = (40, 100, 120)    # Maquina escura
MACHINE_LIGHT = (80, 170, 190)   # Maquina clara
BUILDING_GRAY = (70, 75, 85)     # Predio cinza
BUILDING_DARK = (50, 55, 65)     # Predio escuro
BUILDING_LIGHT = (90, 95, 105)   # Predio claro
SAND_COLOR = (210, 190, 150)     # Cor da areia
BRICK_RED = (160, 80, 60)        # Tijolo vermelho
BRICK_DARK = (130, 60, 45)       # Tijolo escuro
CONCRETE_GRAY = (160, 155, 150)  # Concreto
WINDOW_DARK = (30, 35, 45)       # Janela escura (apagada)
WINDOW_LIT = (255, 220, 100)     # Janela acesa

# ---------- CORES DA INTERFACE DO USUARIO (UI) ----------
GOLD = (255, 200, 50)           # Dourado (estrelas, destaque)
SILVER = (180, 180, 190)        # Prata
POPUP_BG = (20, 40, 60)         # Fundo do popup tutorial
PHASE_CARD_LOCKED = (60, 65, 75)  # Cartao de fase bloqueada
PHASE_CARD_1 = (60, 140, 180)   # Cor da Fase 1
PHASE_CARD_2 = (140, 100, 60)   # Cor da Fase 2
PHASE_CARD_3 = (80, 160, 100)   # Cor da Fase 3
PHASE_CARD_4 = (100, 80, 150)   # Cor da Fase 4
TITLE_BLUE = (40, 120, 200)     # Azul do titulo

# ---------- CORES DO SERTAO (Fase 3) ----------
SERTAO_SKY_TOP = (200, 130, 60)      # Ceu dourado/ambar superior
SERTAO_SKY_MID = (220, 170, 90)      # Ceu dourado medio
SERTAO_SKY_BOT = (235, 200, 130)     # Horizonte quente
SERTAO_MOUNT_FAR = (80, 55, 45)      # Montanhas distantes
SERTAO_MOUNT_MID = (100, 70, 50)     # Montanhas medias
SERTAO_MOUNT_NEAR = (120, 85, 55)    # Colinas proximas
SERTAO_GROUND = (185, 155, 100)      # Solo arido principal
SERTAO_GROUND2 = (170, 140, 88)      # Solo arido sombra
SERTAO_GROUND3 = (200, 170, 110)     # Solo arido claro
SERTAO_CRACK = (150, 120, 75)        # Rachaduras no solo
CACTUS_GREEN = (60, 110, 50)         # Verde do cacto
CACTUS_DARK = (45, 85, 38)           # Sombra do cacto
CACTUS_SPINE = (230, 220, 180)       # Espinho do cacto
DRY_TRUNK = (110, 75, 45)            # Tronco de arvore seca
DRY_BRANCH = (130, 90, 55)           # Galho seco
DRY_LEAF = (100, 120, 50)            # Folha seca/esparsa
FENCE_WOOD = (140, 100, 60)          # Madeira da cerca
FENCE_DARK = (110, 75, 40)           # Sombra da cerca
ADOBE_WALL = (210, 185, 145)         # Parede de adobe/barro
ADOBE_DARK = (185, 160, 120)         # Sombra adobe
TERRACOTTA = (185, 90, 55)           # Telha terracota
TERRACOTTA_D = (155, 70, 40)         # Telha sombra
LIME_WHITE = (240, 235, 220)         # Cal branca (casa caiada)
CLAY_BRICK = (175, 105, 70)          # Tijolo de argila
CLAY_BRICK_D = (150, 85, 55)         # Tijolo sombra
METAL_ROOF = (140, 130, 120)         # Telhado de metal/zinco
METAL_ROOF_D = (110, 100, 90)        # Telhado zinco sombra
WATER_TANK = (80, 120, 160)          # Caixa d'agua azul
WATER_TANK_D = (60, 95, 130)         # Caixa d'agua sombra
WELL_STONE = (160, 145, 120)         # Pedra do poco
WELL_STONE_D = (130, 115, 92)        # Pedra poco sombra
LAUNDRY_1 = (220, 80, 80)            # Roupa no varal 1
LAUNDRY_2 = (80, 150, 200)           # Roupa no varal 2
LAUNDRY_3 = (240, 220, 160)          # Roupa no varal 3
SUN_GLOW = (255, 220, 80)            # Brilho do sol
SUN_CORE = (255, 245, 180)           # Nucleo do sol

# ---------- CORES DA ESTACAO DE TRATAMENTO ----------
STATION_FILTER = (100, 160, 200)    # Estacao de filtragem
STATION_TREAT = (180, 140, 60)      # Estacao de tratamento quimico
STATION_DISINF = (160, 60, 160)     # Estacao de desinfeccao
STATION_RELEASE = (60, 180, 100)    # Estacao de liberacao

# ============================================================
# FONTES (carregamento das fontes do sistema)
# ============================================================
# Fontes do sistema em varios tamanhos para UI
font_tiny = pygame.font.SysFont('arial', 16)   # Fonte bem pequena (dicas, legendas)
font_small = pygame.font.SysFont('arial', 20)  # Fonte pequena (textos curtos)
font_med = pygame.font.SysFont('arial', 26)    # Fonte media (botoes, status)
font_big = pygame.font.SysFont('arial', 36)    # Fonte grande (titulos secundarios)
font_title = pygame.font.SysFont('arial', 48)  # Fonte de titulo
font_huge = pygame.font.SysFont('arial', 60)   # Fonte enorme (destaque)

# ============================================================
# SISTEMA DE MUTE (silenciar/ativar audio)
# ============================================================
audio_muted = False  # Estado global: False = som ativo, True = muted
audio_volume = 0.7   # Volume geral (0.0 a 1.0)
global_sfx = None    # Referencia global ao dicionario de SFX para atualizar volume em tempo real

def set_volume(val):
    """Define o volume geral (0.0 a 1.0) e atualiza a musica e todos os SFX."""
    global audio_volume
    global global_sfx
    audio_volume = max(0.0, min(1.0, val))
    vol = 0 if audio_muted else audio_volume
    pygame.mixer.music.set_volume(vol)
    if global_sfx:
        for snd in global_sfx.values():
            snd.set_volume(vol)

def toggle_mute():
    """Alterna entre som ligado e desligado."""
    global audio_muted
    audio_muted = not audio_muted
    set_volume(audio_volume)

def play_sfx(sfx_dict, name):
    """Toca um efeito sonoro se o audio nao estiver mutado e o som existir."""
    if not audio_muted and sfx_dict and name in sfx_dict:
        sfx_dict[name].set_volume(audio_volume)
        sfx_dict[name].stop()
        sfx_dict[name].play()

def draw_mute_button(surface, x=SCREEN_W - 40, y=10):
    """Desenha o icone de alto-falante para mutar/desmutar no canto superior direito."""
    # Circulo de fundo semi-transparente
    pygame.draw.circle(surface, (30, 30, 40, 180), (x + 12, y + 12), 14)
    pygame.draw.circle(surface, (60, 60, 70), (x + 12, y + 12), 14, 2)
    # Corpo do alto-falante
    pygame.draw.rect(surface, WHITE, (x + 4, y + 8, 6, 8))
    pygame.draw.polygon(surface, WHITE, [(x + 10, y + 6), (x + 16, y + 2), (x + 16, y + 22), (x + 10, y + 18)])
    if audio_muted:
        # Se mutado, desenha um X vermelho sobre o alto-falante
        pygame.draw.line(surface, RED, (x + 2, y + 2), (x + 22, y + 22), 3)
        pygame.draw.line(surface, RED, (x + 22, y + 2), (x + 2, y + 22), 3)
    else:
        # Se ativo, desenha ondas sonoras ao lado
        pygame.draw.arc(surface, WHITE, (x + 16, y + 5, 8, 14), -0.8, 0.8, 2)
    return pygame.Rect(x, y, 28, 28)  # Retorna o retangulo para deteccao de clique


# ============================================================
# FONTE PIXEL ART PERSONALIZADA (para titulos estilizados)
# ============================================================

# Dicionario com mapas de pixels para cada letra (5x5)
# '1' = pixel aceso, '.' = pixel apagado
PIXEL_LETTERS = {
    'H': ["1..1","1..1","1111","1..1","1..1"],
    'E': ["1111","1...","111.","1...","1111"],
    'R': ["111.","1..1","111.","1.1.","1..1"],
    'O': [".11.","1..1","1..1","1..1",".11."],
    'F': ["1111","1...","111.","1...","1..."],
    'T': ["11111","..1..","..1..","..1..","..1.."],
    'W': ["1...1","1...1","1.1.1","11.11",".1.1."],
    'A': [".11.","1..1","1111","1..1","1..1"],
    'D': ["111.","1..1","1..1","1..1","111."],
    ' ': ["...","...","...","...","..."],  # Espaco em branco
}


def draw_pixel_text(surface, text, x, y, scale, color, shadow_color=None):
    """Desenha texto em estilo pixel art na tela. scale = tamanho de cada pixel."""
    cursor_x = x
    for ch in text.upper():
        letter = PIXEL_LETTERS.get(ch)  # Obtem o mapa de pixels da letra
        if letter is None:  # Se letra nao definida, pula
            cursor_x += 3 * scale + scale
            continue
        if shadow_color:  # Sombra opcional atras do texto
            for row_i, row in enumerate(letter):
                for col_i, c in enumerate(row):
                    if c == '1':
                        px = cursor_x + col_i * scale + 2
                        py = y + row_i * scale + 2
                        pygame.draw.rect(surface, shadow_color, (px, py, scale, scale))
        # Desenha os pixels da letra principal
        for row_i, row in enumerate(letter):
            for col_i, c in enumerate(row):
                if c == '1':
                    px = cursor_x + col_i * scale
                    py = y + row_i * scale
                    pygame.draw.rect(surface, color, (px, py, scale, scale))
        letter_width = max(len(row) for row in letter)
        cursor_x += letter_width * scale + scale  # Avanca cursor


def pixel_text_width(text, scale):
    """Calcula a largura total de um texto em pixel art sem desenha-lo."""
    total = 0
    for ch in text.upper():
        letter = PIXEL_LETTERS.get(ch)
        if letter is None:
            total += 3 * scale + scale
            continue
        letter_width = max(len(row) for row in letter)
        total += letter_width * scale + scale
    total -= scale  # Ajuste do ultimo espacamento
    return max(0, total)


# ============================================================
# GERACAO DE MUSICA (chiptune / WAV procedural)
# ============================================================

# ---------- GERADORES DE ONDAS DE AUDIO ----------

def generate_square_wave(freq, duration, sample_rate=22050, volume=0.3):
    """Gera uma onda quadrada (som chiptune classico) com a frequencia e duracao especificadas."""
    samples = []
    period = sample_rate / freq if freq > 0 else sample_rate
    for i in range(int(sample_rate * duration)):
        if freq <= 0:
            samples.append(0)  # Silencio se frequencia for 0
        else:
            # Onda quadrada: alterna entre +volume e -volume
            val = volume if (i % int(period)) < int(period / 2) else -volume
            samples.append(val)
    return samples


def generate_sine_wave(freq, duration, sample_rate=22050, volume=0.2):
    """Gera uma onda senoidal (som suave) com a frequencia e duracao especificadas."""
    samples = []
    for i in range(int(sample_rate * duration)):
        if freq <= 0:
            samples.append(0)
        else:
            t = i / sample_rate
            val = volume * math.sin(2 * math.pi * freq * t)
            samples.append(val)
    return samples


def generate_triangle_wave(freq, duration, sample_rate=22050, volume=0.25):
    """Gera uma onda triangular (som mais suave que quadrada) para melodias."""
    samples = []
    for i in range(int(sample_rate * duration)):
        if freq <= 0:
            samples.append(0)
        else:
            t = i / sample_rate
            period = 1.0 / freq
            phase = (t % period) / period  # Fase dentro do periodo (0 a 1)
            if phase < 0.5:
                val = volume * (4 * phase - 1)
            else:
                val = volume * (3 - 4 * phase)
            samples.append(val)
    return samples


def mix_tracks(track1, track2, target_peak=0.85):
    """Mistura duas faixas de audio somando as amostras e normaliza o pico para `target_peak`."""
    length = max(len(track1), len(track2))
    result = []
    for i in range(length):
        s1 = track1[i] if i < len(track1) else 0
        s2 = track2[i] if i < len(track2) else 0
        result.append(max(-1.0, min(1.0, s1 + s2)))  # Soma e limita
    # Normaliza o pico para target_peak, garantindo volume consistente entre fases
    peak = max(1e-8, max(abs(v) for v in result))
    if peak > 0:
        scale = target_peak / peak
        result = [v * scale for v in result]
    return result


def write_wav(filename, samples, sample_rate=22050):
    """Escreve uma lista de amostras em um arquivo WAV (estéreo, 16 bits)."""
    filepath = os.path.join(GAME_DIR, filename)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(2)          # 2 canais (estéreo)
        wf.setsampwidth(2)          # 16 bits por amostra
        wf.setframerate(sample_rate)  # Frequência de amostragem
        buf = bytearray(len(samples) * 4)  # Buffer: 4 bytes por amostra (2 canais * 2 bytes)
        for i, s in enumerate(samples):
            # Converte float (-1..1) para inteiro 16 bits (-32767..32767)
            val = int(max(-32767, min(32767, s * 32767)))
            struct.pack_into('<hh', buf, i * 4, val, val)  # Empacota 2 canais (esquerdo=direito)
        wf.writeframes(bytes(buf))
    return filepath


# Dicionario com frequencias das notas musicais em Hz (notacao: letra + oitava)
NOTE_FREQS = {
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 'G3': 196.00,
    'A3': 220.00, 'B3': 246.94, 'C4': 261.63, 'D4': 293.66, 'E4': 329.63,
    'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25,
    'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00,
    'Bb3': 233.08, 'Eb4': 311.13, 'Ab3': 207.65, 'Bb4': 466.16,
    'F#4': 369.99, 'G#4': 415.30, 'Db4': 277.18, 'Gb4': 369.99,
    'R': 0,  # 'R' = Rest (pausa/silencio)
}


def generate_melody(notes, note_duration, sample_rate=22050, volume=0.25):
    """Gera uma melodia a partir de uma lista de notas usando onda quadrada com fade in/out."""
    samples = []
    for note in notes:
        freq = NOTE_FREQS.get(note, 0)
        tone = generate_square_wave(freq, note_duration, sample_rate, volume)
        fade = int(sample_rate * 0.01)  # Fade de 10ms
        # Aplica fade in (inicio suave)
        for i in range(min(fade, len(tone))):
            tone[i] *= i / fade
        # Aplica fade out (final suave)
        for i in range(min(fade, len(tone))):
            tone[len(tone) - 1 - i] *= i / fade
        samples.extend(tone)
    return samples


def generate_melody_triangle(notes, note_duration, sample_rate=22050, volume=0.20):
    """Gera melodia usando ondas triangulares (som mais macio que quadrado)."""
    samples = []
    for note in notes:
        freq = NOTE_FREQS.get(note, 0)
        tone = generate_triangle_wave(freq, note_duration, sample_rate, volume)
        fade = int(sample_rate * 0.015)  # Fade de 15ms
        for i in range(min(fade, len(tone))):
            tone[i] *= i / fade
        for i in range(min(fade, len(tone))):
            tone[len(tone) - 1 - i] *= i / fade
        samples.extend(tone)
    return samples


def generate_bass(notes, note_duration, sample_rate=22050, volume=0.15):
    """Gera linha de baixo usando ondas senoidais (som grave e suave)."""
    samples = []
    for note in notes:
        freq = NOTE_FREQS.get(note, 0)
        tone = generate_sine_wave(freq, note_duration, sample_rate, volume)
        samples.extend(tone)
    return samples


def generate_all_music():
    """Gera todos os arquivos WAV de musica chiptune se nao existirem.
    Retorna um dicionario com os caminhos dos arquivos de musica."""
    music_files = {}

    # Primeiro verifica se existem arquivos de musica personalizados (.mp3 ou .wav)
    track_names = ['menu', 'phase1', 'phase2', 'phase3', 'phase4']
    for track in track_names:
        for ext in ('.mp3', '.wav'):
            custom_path = os.path.join(GAME_DIR, f'custom_music_{track}{ext}')
            if os.path.exists(custom_path):
                music_files[track] = custom_path
                break
        if track in music_files:
            continue
        # Se nao tem musica especifica da fase, tenta usar a musica gameplay generica
        if track != 'menu':
            for ext in ('.mp3', '.wav'):
                fallback = os.path.join(GAME_DIR, f'custom_music_gameplay{ext}')
                if os.path.exists(fallback):
                    music_files[track] = fallback
                    break
        if track in music_files:
            continue

    # Gera as musicas que estiverem faltando (cada fase tem melodia e baixo proprios)
    if 'menu' not in music_files:
        fname = 'music_menu.wav'
        fpath = os.path.join(GAME_DIR, fname)
        if not os.path.exists(fpath):
            melody_notes = [
                'C4', 'R', 'E4', 'G4', 'R', 'C5', 'R', 'R',
                'G4', 'R', 'E4', 'R', 'C4', 'R', 'R', 'R',
                'F4', 'R', 'A4', 'C5', 'R', 'A4', 'R', 'R',
                'G4', 'R', 'F4', 'E4', 'R', 'R', 'C4', 'R',
                'C4', 'R', 'G4', 'R', 'E4', 'R', 'C5', 'R',
                'E5', 'R', 'C5', 'R', 'G4', 'E4', 'C4', 'R',
            ]
            bass_notes = [
                'C3', 'C3', 'C3', 'C3', 'E3', 'E3', 'E3', 'E3',
                'G3', 'G3', 'G3', 'G3', 'C3', 'C3', 'C3', 'C3',
                'F3', 'F3', 'F3', 'F3', 'A3', 'A3', 'A3', 'A3',
                'G3', 'G3', 'G3', 'G3', 'E3', 'E3', 'C3', 'C3',
                'C3', 'C3', 'G3', 'G3', 'E3', 'E3', 'C3', 'C3',
                'F3', 'F3', 'A3', 'A3', 'G3', 'G3', 'C3', 'C3',
            ]
            mel = generate_melody_triangle(melody_notes, 0.35, volume=0.18)
            bas = generate_bass(bass_notes, 0.35, volume=0.10)
            samples = mix_tracks(mel, bas)
            write_wav(fname, samples)
        music_files['menu'] = fpath

    if 'phase1' not in music_files:
        fname = 'music_phase1.wav'
        fpath = os.path.join(GAME_DIR, fname)
        if not os.path.exists(fpath):
            melody_notes = [
                'C4', 'D4', 'E4', 'G4', 'A4', 'G4', 'E4', 'D4',
                'C4', 'E4', 'G4', 'A4', 'C5', 'A4', 'G4', 'E4',
                'G4', 'A4', 'C5', 'D5', 'C5', 'A4', 'G4', 'E4',
                'D4', 'E4', 'G4', 'A4', 'G4', 'E4', 'D4', 'C4',
                'E4', 'G4', 'A4', 'C5', 'R', 'A4', 'G4', 'E4',
                'D4', 'C4', 'D4', 'E4', 'G4', 'E4', 'D4', 'C4',
            ]
            bass_notes = [
                'C3', 'C3', 'C3', 'C3', 'G3', 'G3', 'G3', 'G3',
                'A3', 'A3', 'A3', 'A3', 'E3', 'E3', 'E3', 'E3',
                'G3', 'G3', 'G3', 'G3', 'D3', 'D3', 'D3', 'D3',
                'C3', 'C3', 'C3', 'C3', 'G3', 'G3', 'C3', 'C3',
                'A3', 'A3', 'E3', 'E3', 'G3', 'G3', 'C3', 'C3',
                'D3', 'D3', 'E3', 'E3', 'G3', 'G3', 'C3', 'C3',
            ]
            mel = generate_melody(melody_notes, 0.30, volume=0.18)
            bas = generate_bass(bass_notes, 0.30, volume=0.11)
            samples = mix_tracks(mel, bas)
            write_wav(fname, samples)
        music_files['phase1'] = fpath

    if 'phase2' not in music_files:
        fname = 'music_phase2.wav'
        fpath = os.path.join(GAME_DIR, fname)
        if not os.path.exists(fpath):
            melody_notes = [
                'D4', 'R', 'F4', 'R', 'A4', 'Bb4', 'A4', 'F4',
                'D4', 'E4', 'F4', 'A4', 'Bb4', 'A4', 'R', 'D4',
                'F4', 'G4', 'Bb4', 'A4', 'F4', 'D4', 'R', 'E4',
                'F4', 'A4', 'D5', 'Bb4', 'A4', 'F4', 'E4', 'D4',
                'D4', 'F4', 'A4', 'Bb4', 'R', 'A4', 'G4', 'F4',
                'E4', 'D4', 'F4', 'A4', 'Bb4', 'A4', 'D4', 'R',
            ]
            bass_notes = [
                'D3', 'D3', 'D3', 'D3', 'F3', 'F3', 'A3', 'A3',
                'Bb3', 'Bb3', 'A3', 'A3', 'D3', 'D3', 'D3', 'D3',
                'G3', 'G3', 'Bb3', 'Bb3', 'F3', 'F3', 'D3', 'D3',
                'A3', 'A3', 'D3', 'D3', 'Bb3', 'Bb3', 'A3', 'A3',
                'D3', 'D3', 'F3', 'F3', 'Bb3', 'Bb3', 'A3', 'A3',
                'G3', 'G3', 'Bb3', 'Bb3', 'D3', 'D3', 'D3', 'D3',
            ]
            mel = generate_melody(melody_notes, 0.20, volume=0.25)
            bas = generate_bass(bass_notes, 0.20, volume=0.16)
            samples = mix_tracks(mel, bas)
            write_wav(fname, samples)
        music_files['phase2'] = fpath

    if 'phase3' not in music_files:
        fname = 'music_phase3.wav'
        fpath = os.path.join(GAME_DIR, fname)
        if not os.path.exists(fpath):
            melody_notes = [
                'F4', 'R', 'A4', 'R', 'C5', 'R', 'F5', 'R',
                'R', 'C5', 'R', 'A4', 'R', 'F4', 'R', 'R',
                'G4', 'R', 'Bb4', 'R', 'D5', 'R', 'F5', 'R',
                'R', 'D5', 'R', 'Bb4', 'R', 'G4', 'R', 'R',
                'A4', 'R', 'C5', 'R', 'F5', 'R', 'R', 'C5',
                'Bb4', 'R', 'A4', 'R', 'F4', 'R', 'R', 'R',
            ]
            bass_notes = [
                'F3', 'F3', 'F3', 'F3', 'A3', 'A3', 'A3', 'A3',
                'C3', 'C3', 'C3', 'C3', 'F3', 'F3', 'F3', 'F3',
                'G3', 'G3', 'G3', 'G3', 'Bb3', 'Bb3', 'Bb3', 'Bb3',
                'D3', 'D3', 'D3', 'D3', 'G3', 'G3', 'G3', 'G3',
                'A3', 'A3', 'A3', 'A3', 'F3', 'F3', 'F3', 'F3',
                'Bb3', 'Bb3', 'A3', 'A3', 'F3', 'F3', 'F3', 'F3',
            ]
            mel = generate_melody_triangle(melody_notes, 0.38, volume=0.20)
            bas = generate_bass(bass_notes, 0.38, volume=0.12)
            samples = mix_tracks(mel, bas)
            write_wav(fname, samples)
        music_files['phase3'] = fpath

    if 'phase4' not in music_files:
        fname = 'music_phase4.wav'
        fpath = os.path.join(GAME_DIR, fname)
        if not os.path.exists(fpath):
            melody_notes = [
                'A4', 'C5', 'A4', 'C5', 'E5', 'C5', 'E5', 'C5',
                'A4', 'C5', 'A4', 'C5', 'B4', 'A4', 'B4', 'A4',
                'E4', 'A4', 'E4', 'A4', 'C5', 'A4', 'C5', 'A4',
                'D5', 'C5', 'D5', 'C5', 'B4', 'A4', 'B4', 'A4',
                'A4', 'E4', 'A4', 'E4', 'C5', 'B4', 'C5', 'B4',
                'A4', 'C5', 'A4', 'E4', 'A4', 'E4', 'A4', 'R',
            ]
            bass_notes = [
                'A3', 'A3', 'A3', 'A3', 'E3', 'E3', 'E3', 'E3',
                'A3', 'A3', 'A3', 'A3', 'E3', 'E3', 'E3', 'E3',
                'C3', 'C3', 'C3', 'C3', 'A3', 'A3', 'A3', 'A3',
                'D3', 'D3', 'D3', 'D3', 'E3', 'E3', 'E3', 'E3',
                'A3', 'A3', 'E3', 'E3', 'A3', 'A3', 'E3', 'E3',
                'A3', 'A3', 'A3', 'A3', 'E3', 'E3', 'A3', 'A3',
            ]
            mel = generate_melody(melody_notes, 0.22, volume=0.23)
            bas = generate_bass(bass_notes, 0.22, volume=0.15)
            samples = mix_tracks(mel, bas)
            write_wav(fname, samples)
        music_files['phase4'] = fpath

    return music_files


def play_music(music_files, track_name):
    """Carrega e toca uma musica em loop. Usa arquivo externo customizado se disponivel."""
    try:
        filepath = music_files.get(track_name)
        if filepath and os.path.exists(filepath):
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(0 if audio_muted else audio_volume)
            pygame.mixer.music.play(-1)  # -1 = loop infinito
    except Exception:
        pass  # Ignora erros de audio silenciosamente


def stop_music():
    """Para a musica atual."""
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


# ============================================================
# GERACAO DE EFEITOS SONOROS (SFX)
# ============================================================

def _make_sound(freq_start, freq_end, duration_ms, volume=0.3, wave_type='square'):
    """Gera proceduralmente um efeito sonoro com variacao de frequencia (sweep).
    freq_start = frequencia inicial, freq_end = frequencia final.
    wave_type pode ser 'square', 'triangle' ou 'sine'."""
    sr = 22050  # Taxa de amostragem
    n = int(sr * duration_ms / 1000)  # Numero de amostras
    if n <= 0:
        n = 1
    buf = bytearray(n * 4)  # Buffer: n amostras * 4 bytes (2 canais * 2 bytes)
    for i in range(n):
        t = i / n  # Progressao de 0 a 1
        freq = freq_start + (freq_end - freq_start) * t  # Frequencia varia linearmente
        if freq <= 0:
            val = 0
        elif wave_type == 'square':
            # Onda quadrada: sinal binario (+/- volume)
            period = sr / freq
            val = volume if (i % max(1, int(period))) < max(1, int(period / 2)) else -volume
        elif wave_type == 'triangle':
            # Onda triangular: transicao linear suave
            period = 1.0 / freq
            tt = i / sr
            phase = (tt % period) / period
            if phase < 0.5:
                val = volume * (4 * phase - 1)
            else:
                val = volume * (3 - 4 * phase)
        else:  # 'sine'
            val = volume * math.sin(2 * math.pi * freq * i / sr)
        # Envelope ADSR simplificado: fade in (5%) e fade out (20%)
        env = 1.0
        if i < n * 0.05:
            env = i / max(1, (n * 0.05))
        elif i > n * 0.8:
            env = (n - i) / max(1, (n * 0.2))
        ival = int(max(-32767, min(32767, val * env * 32767)))  # Converte para 16 bits
        struct.pack_into('<hh', buf, i * 4, ival, ival)  # 2 canais identicos (mono -> stereo)
    sound = pygame.mixer.Sound(buffer=bytes(buf))
    sound.set_volume(0.4)
    return sound


def _load_custom_sfx(name):
    """Tenta carregar um arquivo de efeito sonoro personalizado.
    Retorna o Sound do Pygame ou None se nao existir."""
    path = os.path.join(GAME_DIR, f'custom_sfx_{name}.wav')
    if os.path.exists(path):
        try:
            snd = pygame.mixer.Sound(path)
            snd.set_volume(0.4)
            return snd
        except Exception:
            pass
    return None


def generate_sfx():
    """Gera ou carrega todos os efeitos sonoros do jogo.
    Retorna um dicionario com os nomes dos efeitos como chaves e objetos Sound como valores."""
    sfx = {}

    # Tenta carregar arquivos customizados primeiro; se falhar, gera proceduralmente
    sfx['collect'] = _load_custom_sfx('collect') or _make_sound(400, 800, 120, 0.25, 'square')
    sfx['repair'] = _load_custom_sfx('repair') or _make_sound(300, 900, 250, 0.25, 'square')
    sfx['deliver'] = _load_custom_sfx('deliver') or _make_sound(350, 700, 200, 0.3, 'sine')
    sfx['hit'] = _load_custom_sfx('hurt') or _make_sound(300, 100, 150, 0.3, 'square')
    sfx['station'] = _load_custom_sfx('station') or _make_sound(600, 900, 100, 0.25, 'square')
    sfx['error'] = _load_custom_sfx('error') or _make_sound(200, 100, 200, 0.25, 'square')
    sfx['throw'] = _load_custom_sfx('throw') or _make_sound(250, 500, 150, 0.2, 'triangle')
    sfx['menu_click'] = _load_custom_sfx('menu_click') or _make_sound(500, 600, 60, 0.2, 'square')
    sfx['menu_hover'] = _load_custom_sfx('menu_hover') or _make_sound(400, 420, 40, 0.1, 'sine')

    # Som de pulo
    sfx['jump'] = _load_custom_sfx('jump') or _make_sound(200, 500, 100, 0.2, 'square')

    # Som de estrela ganha
    sfx['star'] = _load_custom_sfx('star_earned') or _make_sound(600, 1200, 200, 0.2, 'triangle')

    # Jingle de vitoria (3 notas: Dó, Mi, Sol)
    custom_victory = _load_custom_sfx('phase_complete')
    if custom_victory:
        sfx['victory'] = custom_victory
    else:
        sr = 22050
        n1, n2, n3 = int(sr * 0.15), int(sr * 0.15), int(sr * 0.3)
        total = n1 + n2 + n3
        buf = bytearray(total * 4)
        notes = [(523.25, n1), (659.25, n2), (783.99, n3)]
        idx = 0
        for freq, length in notes:
            for i in range(length):
                env = 1.0
                if i < length * 0.05:
                    env = i / max(1, (length * 0.05))
                elif i > length * 0.7:
                    env = (length - i) / max(1, (length * 0.3))
                period = sr / freq
                val = 0.3 if (i % max(1, int(period))) < max(1, int(period / 2)) else -0.3
                ival = int(max(-32767, min(32767, val * env * 32767)))
                struct.pack_into('<hh', buf, idx * 4, ival, ival)
                idx += 1
        sfx['victory'] = pygame.mixer.Sound(buffer=bytes(buf))
        sfx['victory'].set_volume(0.5)

    return sfx


# ============================================================
# SISTEMA DE CAMERA (rolagem lateral suave)
# ============================================================

class Camera:
    """Controla a camera side-scrolling para niveis maiores que a tela."""

    def __init__(self, level_width, level_height=SCREEN_H):
        self.x = 0.0                # Posicao X da camera no mundo
        self.y = 0                  # Posicao Y (fixa, sem scroll vertical)
        self.level_width = level_width    # Largura total do nivel
        self.level_height = level_height  # Altura total
        self.smooth = 0.08          # Fator de suavizacao (0 = fixo, 1 = instantaneo)

    def update(self, target_x, target_y=None):
        """Segue o personagem suavemente. target_x/y sao coordenadas do mundo."""
        # Centraliza a camera no personagem, sem ultrapassar os limites do nivel
        desired_x = target_x - SCREEN_W // 2
        desired_x = max(0, min(self.level_width - SCREEN_W, desired_x))
        # Interpolacao linear para movimento suave
        self.x += (desired_x - self.x) * self.smooth
        self.x = max(0, min(self.level_width - SCREEN_W, self.x))

    def apply(self, world_x, world_y):
        """Converte coordenadas do mundo para coordenadas da tela."""
        return int(world_x - self.x), int(world_y)

    def world_rect_visible(self, rect):
        """Verifica se um retangulo no mundo esta visivel na tela."""
        return rect.right > self.x and rect.left < self.x + SCREEN_W


# ============================================================
# ESTADO GLOBAL DO JOGO (progresso, estrelas, dificuldade)
# ============================================================
import json

SAVE_FILE = os.path.join(GAME_DIR, "savegame.json")

class GameState:
    """Armazena o estado persistente do jogo: dificuldade, fases desbloqueadas, estrelas."""

    def __init__(self):
        self.difficulty = "media"
        self.unlocked = [True, False, False, False]
        self.stars = [0, 0, 0, 0]
        self.load()

    def reset(self):
        """Reinicia o progresso conforme a dificuldade."""
        if self.difficulty == "facil":
            self.unlocked = [True, True, True, True]
        else:
            self.unlocked = [True, False, False, False]
        self.stars = [0, 0, 0, 0]
        self.save()

    def complete_phase(self, idx, num_stars):
        """Registra a conclusão de uma fase e desbloqueia a próxima."""
        self.stars[idx] = max(self.stars[idx], num_stars)
        if idx + 1 < 4:
            self.unlocked[idx + 1] = True
        self.save()

    def total_stars(self):
        return sum(self.stars)

    def progress(self):
        done = sum(1 for s in self.stars if s > 0)
        return int(done / 4 * 100)

    def save(self):
        """Salva o progresso em arquivo JSON."""
        try:
            data = {
                "difficulty": self.difficulty,
                "unlocked": self.unlocked,
                "stars": self.stars,
            }
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    def load(self):
        """Carrega o progresso do arquivo JSON, se existir."""
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.difficulty = data.get("difficulty", "media")
            self.stars = data.get("stars", [0, 0, 0, 0])[:4]
            self.unlocked = data.get("unlocked", [True, False, False, False])[:4]
        except Exception:
            self.difficulty = "media"
            self.stars = [0, 0, 0, 0]
            self.unlocked = [True, False, False, False]

game_state = GameState()

def get_initial_lives(phase_idx):
    """Retorna o número de vidas iniciais conforme dificuldade e índice de fase (0-3)."""
    if game_state.difficulty == "facil":
        return 5
    elif game_state.difficulty == "media":
        return 4
    else:  # dificil
        return 3

def difficulty_drain(base_rate):
    """Ajusta a taxa de dreno de água conforme a dificuldade."""
    if game_state.difficulty == "facil":
        return base_rate * 0.58
    elif game_state.difficulty == "dificil":
        return base_rate * 1.68
    return base_rate * 1.12

# ============================================================
# CLASSE BOTAO (interface interativa)
# ============================================================
class Button:
    """Botão generico com efeito hover, sombra, borda e texto centralizado."""

    def __init__(self, x, y, w, h, text, color, hover_color, text_color=WHITE, font=None):
        self.rect = pygame.Rect(x, y, w, h)      # Retangulo do botao
        self.text = text                           # Texto do botao
        self.color = color                         # Cor normal
        self.hover_color = hover_color             # Cor quando o mouse passa por cima
        self.text_color = text_color               # Cor do texto
        self.font = font or font_big               # Fonte (padrao: font_big)
        self.hovered = False                       # Mouse esta em cima?
        self.enabled = True                        # Botao esta habilitado?
        self._was_hovered = False                  # Estado anterior (para efeitos)

    def update(self, mouse_pos):
        """Atualiza estado hover baseado na posicao do mouse."""
        self.hovered = self.enabled and self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        """Desenha o botao na tela com sombra, destaque e borda."""
        color = self.hover_color if self.hovered else self.color
        if not self.enabled:
            color = (60, 60, 65)  # Botao desabilitado fica cinza
        shadow = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.w, self.rect.h)
        pygame.draw.rect(surface, (0, 0, 0, 80), shadow, border_radius=12)  # Sombra
        pygame.draw.rect(surface, color, self.rect, border_radius=12)        # Fundo
        highlight = pygame.Rect(self.rect.x + 4, self.rect.y + 4, self.rect.w - 8, self.rect.h // 3)
        h_color = tuple(min(255, c + 30) for c in color)  # Cor mais clara para destaque
        pygame.draw.rect(surface, h_color, highlight, border_radius=8)  # Destaque superior
        border_color = tuple(max(0, c - 40) for c in color)  # Cor escura para borda
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=12)  # Borda
        text_surf = self.font.render(self.text, True, self.text_color if self.enabled else (100, 100, 100))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def clicked(self, event):
        """Verifica se o botao foi clicado (botao esquerdo do mouse)."""
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


# ============================================================
# FUNCOES DE DESENHO
# ============================================================

def draw_samuel(surface, x, y, facing_right=True, frame=0, carrying=False, repairing=False, has_grabber=False):
    """
    Desenha o personagem Samuel na tela com pixels.
    - facing_right: direcao que esta olhando
    - frame: quadro de animacao (0 = parado)
    - carrying: se esta carregando um galao de agua
    - repairing: se esta com chave inglesa (consertando)
    - has_grabber: se esta com ferramenta de coleta de lixo
    """
    SCALE = 1.0
    OX, OY = 8, 8
    TW, TH = 50, 76

    temp = pygame.Surface((TW, TH), pygame.SRCALPHA)
    s = 2
    leg_offset = int(math.sin(frame * 0.15) * 4) if frame != 0 else 0
    cx, cy = OX, OY

    cape_sway = int(math.sin(frame * 0.1) * 3)
    cape_pts = [(cx + 8, cy + 22), (cx - 4 + cape_sway, cy + 52), (cx + 14, cy + 48)]
    pygame.draw.polygon(temp, CAPE_RED, cape_pts)
    pygame.draw.polygon(temp, CAPE_DARK, cape_pts, 2)

    hair_cx, hair_cy = cx + 16, cy + 8
    for dx in range(-11, 12):
        for dy in range(-12, 3):
            if dx * dx + (dy * 1.1) ** 2 < 130:
                pygame.draw.rect(temp, SAMUEL_HAIR, (hair_cx + dx * s // 2, hair_cy + dy * s // 2, s, s))
    for dx in range(-5, 0):
        for dy in range(-9, -5):
            if dx * dx + dy * dy < 20:
                pygame.draw.rect(temp, (70, 40, 22), (hair_cx + dx * s // 2, hair_cy + dy * s // 2, s, s))

    pygame.draw.rect(temp, SAMUEL_SKIN, (cx + 8, cy + 10, 16, 16))
    pygame.draw.rect(temp, SAMUEL_SKIN_LIGHT, (cx + 10, cy + 12, 6, 4))

    pygame.draw.rect(temp, BLACK, (cx + 18, cy + 16, 3, 4))
    pygame.draw.rect(temp, WHITE, (cx + 19, cy + 16, 1, 2))
    pygame.draw.rect(temp, BLACK, (cx + 13, cy + 16, 2, 3))

    pygame.draw.rect(temp, (120, 60, 30), (cx + 13, cy + 22, 6, 2))
    pygame.draw.rect(temp, (140, 70, 35), (cx + 14, cy + 23, 4, 1))

    pygame.draw.rect(temp, SHIRT_WHITE, (cx + 7, cy + 26, 18, 16))

    pygame.draw.rect(temp, VEST_ORANGE, (cx + 5, cy + 26, 6, 16))
    pygame.draw.rect(temp, VEST_ORANGE, (cx + 21, cy + 26, 6, 16))
    pygame.draw.rect(temp, VEST_DARK, (cx + 5, cy + 26, 6, 16), 1)
    pygame.draw.rect(temp, VEST_DARK, (cx + 21, cy + 26, 6, 16), 1)
    pygame.draw.rect(temp, VEST_DARK, (cx + 7, cy + 26, 3, 4))
    pygame.draw.rect(temp, VEST_DARK, (cx + 22, cy + 26, 3, 4))

    pygame.draw.rect(temp, BELT_BROWN, (cx + 6, cy + 40, 20, 3))
    pygame.draw.rect(temp, YELLOW, (cx + 14, cy + 40, 4, 3))

    pygame.draw.rect(temp, PANTS_BROWN, (cx + 7, cy + 43, 8, 13 + leg_offset))
    pygame.draw.rect(temp, PANTS_BROWN, (cx + 17, cy + 43, 8, 13 - leg_offset))
    pygame.draw.rect(temp, PANTS_DARK, (cx + 7, cy + 43, 8, 13 + leg_offset), 1)
    pygame.draw.rect(temp, PANTS_DARK, (cx + 17, cy + 43, 8, 13 - leg_offset), 1)

    shoe_y1 = cy + 56 + leg_offset
    shoe_y2 = cy + 56 - leg_offset
    pygame.draw.rect(temp, SHOE_RED, (cx + 4, shoe_y1, 12, 6))
    pygame.draw.rect(temp, SHOE_RED, (cx + 16, shoe_y2, 12, 6))
    pygame.draw.rect(temp, WHITE, (cx + 4, shoe_y1, 12, 2))
    pygame.draw.rect(temp, WHITE, (cx + 16, shoe_y2, 12, 2))

    if has_grabber:
        gx, gy = cx + 28, cy + 26
        pygame.draw.rect(temp, (120, 120, 130), (gx, gy, 3, 22))
        pygame.draw.rect(temp, (150, 150, 160), (gx - 2, gy + 20, 7, 4))
        pygame.draw.line(temp, (150, 150, 160), (gx - 2, gy + 24), (gx - 4, gy + 28), 2)
        pygame.draw.line(temp, (150, 150, 160), (gx + 5, gy + 24), (gx + 7, gy + 28), 2)

    if repairing:
        wx, wy = cx + 28, cy + 28
        pygame.draw.rect(temp, (160, 160, 170), (wx, wy, 4, 16))
        pygame.draw.rect(temp, (180, 180, 190), (wx - 3, wy - 4, 10, 6))
        pygame.draw.rect(temp, (140, 140, 150), (wx, wy - 2, 4, 2))

    if carrying:
        gx, gy = cx + 28, cy + 32
        pygame.draw.rect(temp, WATER_BLUE, (gx, gy, 10, 14))
        pygame.draw.rect(temp, WATER_LIGHT, (gx, gy, 10, 4))
        pygame.draw.rect(temp, WATER_DARK, (gx, gy, 10, 14), 1)
        pygame.draw.rect(temp, (100, 100, 110), (gx + 3, gy - 3, 4, 4))

    sw, sh = int(TW * SCALE), int(TH * SCALE)
    scaled = pygame.transform.scale(temp, (sw, sh))
    bx = int(x + 16 - (OX + 16) * SCALE)
    by = int(y + 62 - (OY + 62) * SCALE)
    if facing_right:
        surface.blit(scaled, (bx, by))
    else:
        surface.blit(pygame.transform.flip(scaled, True, False), (bx, by))


def draw_heart(surface, x, y, filled=True):
    """Desenha um coracao (vida). filled=True = cheio, False = vazio."""
    color = HEART_RED if filled else (70, 70, 75)
    pygame.draw.circle(surface, color, (x + 6, y + 5), 6)
    pygame.draw.circle(surface, color, (x + 16, y + 5), 6)
    pygame.draw.polygon(surface, color, [(x, y + 7), (x + 11, y + 20), (x + 22, y + 7)])
    if filled:
        pygame.draw.circle(surface, (255, 120, 130), (x + 8, y + 3), 2)


def draw_star(surface, x, y, filled=True, size=1.0):
    """Desenha uma estrela pequena. filled=True = amarela, False = cinza vazada."""
    color = STAR_YELLOW if filled else (70, 70, 75)
    s = size
    points = []
    for i in range(5):
        angle = math.radians(i * 72 - 90)
        points.append((x + 10 + math.cos(angle) * 10 * s, y + 10 + math.sin(angle) * 10 * s))
        angle2 = math.radians(i * 72 - 90 + 36)
        points.append((x + 10 + math.cos(angle2) * 4 * s, y + 10 + math.sin(angle2) * 4 * s))
    pygame.draw.polygon(surface, color, points)
    if filled:
        pygame.draw.polygon(surface, (255, 230, 100), points[:4] + [points[-1]])


def draw_star_big(surface, x, y, filled=True, size=30):
    """Desenha uma estrela grande (para telas de resultado)."""
    color = STAR_YELLOW if filled else (70, 70, 75)
    points = []
    for i in range(5):
        angle = math.radians(i * 72 - 90)
        points.append((x + math.cos(angle) * size, y + math.sin(angle) * size))
        angle2 = math.radians(i * 72 - 90 + 36)
        points.append((x + math.cos(angle2) * size * 0.4, y + math.sin(angle2) * size * 0.4))
    pygame.draw.polygon(surface, color, points)
    if filled:
        inner = []
        for i in range(5):
            angle = math.radians(i * 72 - 90)
            inner.append((x + math.cos(angle) * size * 0.6, y + math.sin(angle) * size * 0.6))
        pygame.draw.polygon(surface, (255, 235, 120), inner)


def draw_cloud(surface, x, y, size=1.0):
    """Desenha uma nuvem composta de elipses."""
    s = int(10 * size)
    pygame.draw.ellipse(surface, CLOUD_SHADOW, (x + 2, y + 4, s * 5, int(s * 1.8)))
    pygame.draw.ellipse(surface, CLOUD_WHITE, (x, y, s * 5, int(s * 1.8)))
    pygame.draw.ellipse(surface, CLOUD_WHITE, (x + s, y - s, s * 3, int(s * 1.6)))
    pygame.draw.ellipse(surface, (250, 252, 255), (x + int(s * 1.5), y - int(s * 0.4), s * 2, int(s * 1.2)))


def draw_tree(surface, x, y, variant=0):
    """Desenha uma arvore com tronco e copa (2 variacoes de formato)."""
    trunk_h = 30 + variant * 5
    pygame.draw.rect(surface, TREE_TRUNK, (x + 14, y + 28, 12, trunk_h))
    pygame.draw.rect(surface, (100, 55, 20), (x + 16, y + 32, 4, trunk_h - 8))
    if variant % 2 == 0:
        pygame.draw.ellipse(surface, TREE_DARK, (x - 4, y - 4, 48, 38))
        pygame.draw.ellipse(surface, TREE_GREEN, (x, y, 40, 32))
        pygame.draw.ellipse(surface, TREE_LIGHT, (x + 8, y + 3, 18, 14))
    else:
        pygame.draw.ellipse(surface, TREE_DARK, (x - 2, y - 8, 44, 42))
        pygame.draw.ellipse(surface, TREE_GREEN, (x + 2, y - 4, 36, 36))
        pygame.draw.ellipse(surface, TREE_LIGHT, (x + 10, y, 16, 16))


def draw_water_bar(surface, x, y, current, maximum):
    """Desenha a barra de agua com icone de gota e preenchimento."""
    bar_w = 140
    bar_h = 16
    # Gota d'agua ao lado da barra
    pygame.draw.polygon(surface, WATER_BLUE, [(x - 10, y + 12), (x - 5, y + 2), (x, y + 12)])
    pygame.draw.circle(surface, WATER_BLUE, (x - 5, y + 13), 5)
    pygame.draw.circle(surface, WHITE, (x - 7, y + 11), 2)
    # Fundo da barra
    pygame.draw.rect(surface, (30, 30, 35), (x + 4, y + 2, bar_w, bar_h), border_radius=4)
    fill_w = max(0, int((current / maximum) * (bar_w - 4)))
    if fill_w > 0:
        pygame.draw.rect(surface, WATER_BLUE, (x + 6, y + 4, fill_w, bar_h - 4), border_radius=3)
        pygame.draw.rect(surface, WATER_LIGHT, (x + 6, y + 4, fill_w, 5), border_radius=3)


def draw_timer(surface, x, y, seconds_left):
    """Desenha um cronometro com icone de relogio. Muda de cor conforme o tempo acaba."""
    mins = int(seconds_left) // 60
    secs = int(seconds_left) % 60
    color = WHITE if seconds_left > 30 else (YELLOW if seconds_left > 10 else RED)
    text = font_med.render(f"{mins}:{secs:02d}", True, color)
    pygame.draw.circle(surface, WHITE, (x - 14, y + 10), 10, 2)
    pygame.draw.line(surface, WHITE, (x - 14, y + 10), (x - 14, y + 4), 2)
    pygame.draw.line(surface, WHITE, (x - 14, y + 10), (x - 8, y + 10), 2)
    surface.blit(text, (x, y))


def draw_lixo(surface, x, y, tipo, frame=0):
    """Desenha um item de lixo com leve flutuacao (bob).
    tipo: 0=Garrafa PET, 1=Lata, 2=Pneu, 3=Sacola, 4=Caixa."""
    bob = math.sin(frame * 0.04 + tipo) * 4
    yy = int(y + bob)
    if tipo == 0:  # Garrafa PET (verde)
        pygame.draw.rect(surface, (140, 200, 140), (x, yy, 14, 22))
        pygame.draw.rect(surface, (120, 180, 120), (x + 4, yy - 6, 6, 8))
        pygame.draw.rect(surface, (100, 160, 100), (x + 5, yy - 8, 4, 4))
        pygame.draw.rect(surface, (160, 220, 160), (x + 2, yy + 4, 4, 8))
    elif tipo == 1:  # Lata de aluminio
        pygame.draw.rect(surface, (170, 170, 180), (x, yy, 16, 18))
        pygame.draw.rect(surface, (200, 50, 50), (x, yy + 5, 16, 8))
        pygame.draw.rect(surface, (150, 150, 160), (x, yy, 16, 3))
    elif tipo == 2:  # Pneu
        pygame.draw.circle(surface, (40, 40, 45), (x + 12, y + 12), 14)
        pygame.draw.circle(surface, (55, 55, 60), (x + 12, y + 12), 10)
        pygame.draw.circle(surface, WATER_DARK, (x + 12, y + 12), 5)
    elif tipo == 3:  # Sacola plastica
        pygame.draw.ellipse(surface, (210, 210, 220), (x, yy, 18, 22))
        pygame.draw.ellipse(surface, (190, 190, 200), (x + 3, yy + 3, 12, 12))
        pygame.draw.arc(surface, (190, 190, 200), (x + 4, yy - 4, 10, 10), 0, 3.14, 2)
    elif tipo == 4:  # Caixa de papelao
        pygame.draw.rect(surface, (160, 130, 80), (x, yy, 18, 14))
        pygame.draw.rect(surface, (140, 110, 65), (x, yy, 18, 14), 2)
        pygame.draw.line(surface, (140, 110, 65), (x + 9, yy), (x + 9, yy + 14), 1)


def draw_trash_bin(surface, x, y):
    """Desenha uma lixeira com simbolo de reciclagem."""
    # Corpo
    pygame.draw.rect(surface, (80, 90, 80), (x, y + 8, 36, 44))
    pygame.draw.rect(surface, (60, 70, 60), (x, y + 8, 36, 44), 2)
    # Tampa
    pygame.draw.rect(surface, (90, 100, 90), (x - 3, y, 42, 10), border_radius=3)
    pygame.draw.rect(surface, (70, 80, 70), (x - 3, y, 42, 10), 2, border_radius=3)
    # Alca
    pygame.draw.rect(surface, (100, 110, 100), (x + 14, y - 4, 8, 6))
    # Simbolo de reciclagem (circulo com 3 setas)
    pygame.draw.circle(surface, GREEN_OK, (x + 18, y + 30), 8, 2)
    for angle_offset in [0, 120, 240]:
        a = math.radians(angle_offset)
        ax = x + 18 + int(math.cos(a) * 6)
        ay = y + 30 + int(math.sin(a) * 6)
        pygame.draw.circle(surface, GREEN_OK, (ax, ay), 2)


def draw_pipe_segment(surface, x, y, broken=True, progress=0.0, double_fill=False):
    """Desenha um segmento de cano. double_fill=True deixa o cano visivelmente mais destruído."""
    body_color = (155, 100, 60) if double_fill else PIPE_GRAY
    pygame.draw.rect(surface, body_color, (x, y, 80, 22))
    pygame.draw.rect(surface, PIPE_LIGHT if not double_fill else (200, 140, 90), (x, y, 80, 6))
    pygame.draw.rect(surface, PIPE_DARK, (x, y + 16, 80, 6))
    pygame.draw.rect(surface, PIPE_DARK, (x, y - 2, 8, 26))
    pygame.draw.rect(surface, PIPE_DARK, (x + 72, y - 2, 8, 26))

    if broken and progress < 1.0:
        if double_fill:
            # Cano muito mais destruído: múltiplas rachaduras e ferrugem extensa
            pygame.draw.rect(surface, PIPE_RUST, (x + 15, y + 1, 50, 20))
            # 3 rachaduras zigzag
            for cr, cx_off in [(0, 28), (2, 42), (1, 55)]:
                pts = [(x + cx_off, y - 3), (x + cx_off + 4, y + 7),
                       (x + cx_off - 2, y + 15), (x + cx_off + 3, y + 25)]
                pygame.draw.lines(surface, BLACK, False, pts, 2)
            # Pedaço dobrado no topo
            pygame.draw.rect(surface, (130, 75, 35), (x + 20, y - 7, 40, 8))
            pygame.draw.rect(surface, BLACK, (x + 20, y - 7, 40, 8), 1)
            # Mais gotículas
            for i in range(10):
                jx = x + 20 + random.randint(-5, 55)
                jy = y + 22 + random.randint(0, 30 - int(progress * 25))
                jr = random.randint(2, 6)
                pygame.draw.circle(surface, WATER_BLUE, (jx, jy), jr)
                pygame.draw.circle(surface, WATER_LIGHT, (jx - 1, jy - 1), max(1, jr - 2))
            # Ícone "2x" piscando
            lbl = pygame.font.SysFont('arial', 11, bold=True).render("2x", True, (255, 60, 60))
            surface.blit(lbl, (x + 62, y - 14))
        else:
            # Cano normal quebrado
            pygame.draw.rect(surface, PIPE_RUST, (x + 30, y + 2, 20, 18))
            points = [(x + 38, y - 2), (x + 42, y + 8), (x + 36, y + 16), (x + 40, y + 24)]
            pygame.draw.lines(surface, BLACK, False, points, 3)
            for i in range(6):
                jx = x + 38 + random.randint(-8, 12)
                jy = y + 22 + random.randint(0, 25 - int(progress * 20))
                jr = random.randint(2, 5)
                pygame.draw.circle(surface, WATER_BLUE, (jx, jy), jr)
                pygame.draw.circle(surface, WATER_LIGHT, (jx - 1, jy - 1), max(1, jr - 2))

    if 0 < progress < 1.0:
        bw = 60
        pygame.draw.rect(surface, (30, 30, 35), (x + 10, y - 18, bw, 10), border_radius=3)
        bar_color = (255, 140, 30) if double_fill else GREEN_OK
        pygame.draw.rect(surface, bar_color, (x + 10, y - 18, int(bw * progress), 10), border_radius=3)

    if progress >= 1.0:
        pygame.draw.rect(surface, (200, 200, 80), (x + 28, y - 3, 24, 28), border_radius=4)
        pygame.draw.rect(surface, (180, 180, 60), (x + 28, y - 3, 24, 28), 2, border_radius=4)


def draw_house(surface, x, y, has_water=False, variant=0, frame=0):
    """Desenha uma casa sertaneja. Cada variante tem arquitetura completamente diferente."""
    win_color = WATER_LIGHT if has_water else WINDOW_DARK
    v = variant % 6

    # Helper: caixa d'agua padrao + cano + gotas animadas
    def _water_tank(tx, ty, tw=22, th=18, pipe_ox=8, pipe_h=24):
        # Suporte
        pipe_x = tx + pipe_ox
        pygame.draw.rect(surface, (100, 100, 110), (pipe_x, ty + th, 4, pipe_h))
        # Tanque
        pygame.draw.rect(surface, WATER_TANK_D, (tx - 1, ty - 1, tw + 2, th + 2), border_radius=3)
        pygame.draw.rect(surface, WATER_TANK, (tx, ty, tw, th), border_radius=3)
        pygame.draw.rect(surface, (100, 175, 220), (tx + 2, ty + 2, tw - 4, 4), border_radius=2)
        pygame.draw.rect(surface, WATER_TANK_D, (tx, ty + th, tw, 4))
        # Gotas animadas quando tem agua
        if has_water and frame > 0:
            drop_off = (frame * 2) % 22
            for di in range(3):
                dy_d = ty + th + 4 + (drop_off + di * 7) % 22
                if dy_d < ty + th + 26:
                    pygame.draw.circle(surface, WATER_BLUE, (pipe_x + 2, dy_d), 2)
                    pygame.draw.circle(surface, WATER_LIGHT, (pipe_x + 1, dy_d - 1), 1)

    if v == 0:
        # Casa de adobe caiada — torre lateral com caixa
        pygame.draw.rect(surface, LIME_WHITE, (x, y, 68, 58))
        pygame.draw.rect(surface, ADOBE_DARK, (x, y, 68, 58), 2)
        for ti in range(0, 68, 14):
            pygame.draw.rect(surface, ADOBE_DARK, (x + ti, y + 20, 12, 1))
            pygame.draw.rect(surface, ADOBE_DARK, (x + ti + 6, y + 40, 10, 1))
        roof_pts = [(x - 8, y + 2), (x + 34, y - 24), (x + 76, y + 2)]
        pygame.draw.polygon(surface, TERRACOTTA, roof_pts)
        pygame.draw.polygon(surface, TERRACOTTA_D, roof_pts, 2)
        for ti in range(0, 80, 10):
            tx1 = x - 8 + ti
            pygame.draw.line(surface, TERRACOTTA_D, (tx1, y + 2), (min(x + 76, tx1 + 5), y + 2), 1)
        pygame.draw.rect(surface, (90, 55, 30), (x + 26, y + 28, 16, 30))
        pygame.draw.ellipse(surface, (90, 55, 30), (x + 26, y + 22, 16, 14))
        pygame.draw.circle(surface, (200, 170, 80), (x + 36, y + 44), 2)
        pygame.draw.rect(surface, ADOBE_DARK, (x + 4, y + 10, 18, 16))
        pygame.draw.rect(surface, win_color, (x + 5, y + 11, 16, 14))
        pygame.draw.line(surface, ADOBE_DARK, (x + 13, y + 11), (x + 13, y + 25), 1)
        pygame.draw.line(surface, ADOBE_DARK, (x + 5, y + 18), (x + 21, y + 18), 1)
        # Torre lateral
        pygame.draw.rect(surface, LIME_WHITE, (x + 50, y - 30, 18, 32))
        pygame.draw.rect(surface, ADOBE_DARK, (x + 50, y - 30, 18, 32), 1)
        _water_tank(x + 48, y - 48, 22, 18, 8, 22)

    elif v == 1:
        # Casa de tijolo aparente com telhado de zinco
        pygame.draw.rect(surface, CLAY_BRICK, (x, y, 72, 60))
        # Padrao de tijolo — clipado para nao sair da parede
        for row in range(0, 60, 8):
            offset = 14 if (row // 8) % 2 == 1 else 0
            for col in range(0, 72, 28):
                bx_start = col - offset
                bx_end = bx_start + 26
                bx_start = max(0, bx_start)
                bx_end = min(72, bx_end)
                if bx_end > bx_start:
                    pygame.draw.rect(surface, CLAY_BRICK_D, (x + bx_start, y + row, bx_end - bx_start, 7), 1)
            # Segundo offset para preencher o início da linha impar
            if offset > 0:
                pygame.draw.rect(surface, CLAY_BRICK_D, (x, y + row, min(28 - offset, 72), 7), 1)
        roof_pts2 = [(x - 4, y + 2), (x + 38, y - 16), (x + 80, y + 2), (x + 80, y + 10), (x - 4, y + 10)]
        pygame.draw.polygon(surface, METAL_ROOF, roof_pts2)
        for zi in range(0, 84, 8):
            pygame.draw.line(surface, METAL_ROOF_D, (x - 4 + zi, y + 2), (x - 4 + zi, y + 10), 1)
        pygame.draw.rect(surface, (80, 50, 25), (x + 20, y + 30, 14, 30))
        pygame.draw.rect(surface, (80, 50, 25), (x + 36, y + 30, 14, 30))
        pygame.draw.line(surface, (60, 35, 15), (x + 34, y + 30), (x + 34, y + 60), 2)
        pygame.draw.circle(surface, (200, 160, 60), (x + 30, y + 46), 2)
        pygame.draw.circle(surface, (200, 160, 60), (x + 44, y + 46), 2)
        for wx_off in [4, 52]:
            pygame.draw.rect(surface, (60, 40, 20), (x + wx_off, y + 10, 16, 16))
            pygame.draw.rect(surface, win_color, (x + wx_off + 1, y + 11, 14, 14))
            pygame.draw.line(surface, (60, 40, 20), (x + wx_off + 8, y + 11), (x + wx_off + 8, y + 25), 1)
        pygame.draw.rect(surface, CLAY_BRICK_D, (x - 2, y + 60, 76, 4))
        pygame.draw.rect(surface, DRY_TRUNK, (x + 4, y + 36, 4, 28))
        pygame.draw.rect(surface, DRY_TRUNK, (x + 64, y + 36, 4, 28))
        # Caixa d'agua sobre o telhado de zinco
        _water_tank(x + 26, y - 34, 20, 16, 6, 18)

    elif v == 2:
        # Casa de 2 andares com sacada — telhado laranja distinto
        pygame.draw.rect(surface, (215, 195, 160), (x, y, 62, 84))
        pygame.draw.rect(surface, (175, 150, 115), (x, y, 62, 84), 2)
        pygame.draw.rect(surface, (175, 150, 115), (x, y + 42, 62, 3))
        roof3 = [(x - 6, y + 2), (x + 31, y - 32), (x + 68, y + 2)]
        pygame.draw.polygon(surface, (185, 90, 40), roof3)
        pygame.draw.polygon(surface, (155, 65, 25), roof3, 2)
        for wx3 in [x + 4, x + 42]:
            pygame.draw.rect(surface, (90, 70, 45), (wx3, y + 48, 14, 18))
            pygame.draw.rect(surface, win_color, (wx3 + 1, y + 49, 12, 16))
            pygame.draw.line(surface, (90, 70, 45), (wx3 + 7, y + 49), (wx3 + 7, y + 65), 1)
        pygame.draw.rect(surface, (155, 130, 95), (x - 4, y + 42, 70, 6), border_radius=2)
        pygame.draw.rect(surface, (130, 105, 75), (x - 4, y + 48, 70, 3))
        for wx3 in [x + 4, x + 42]:
            pygame.draw.rect(surface, (90, 70, 45), (wx3, y + 8, 14, 14))
            pygame.draw.rect(surface, win_color, (wx3 + 1, y + 9, 12, 12))
        pygame.draw.rect(surface, (80, 50, 25), (x + 23, y + 54, 16, 30))
        pygame.draw.circle(surface, YELLOW, (x + 33, y + 70), 2)
        # Caixa d'agua no topo centralizada
        _water_tank(x + 20, y - 38, 22, 16, 9, 20)

    elif v == 3:
        # Casa azulada com frisos e janelas arqueadas
        pygame.draw.rect(surface, (185, 210, 215), (x, y, 66, 58))
        pygame.draw.rect(surface, (145, 170, 175), (x, y, 66, 58), 2)
        pygame.draw.rect(surface, (145, 170, 175), (x, y, 66, 5))
        pygame.draw.rect(surface, (145, 170, 175), (x, y + 53, 66, 5))
        roof4 = [(x - 5, y + 2), (x + 33, y - 24), (x + 71, y + 2)]
        pygame.draw.polygon(surface, (80, 110, 150), roof4)
        pygame.draw.polygon(surface, (60, 90, 130), roof4, 2)
        pygame.draw.rect(surface, (70, 45, 20), (x + 25, y + 28, 16, 30))
        pygame.draw.ellipse(surface, (70, 45, 20), (x + 25, y + 22, 16, 14))
        pygame.draw.circle(surface, (200, 170, 80), (x + 35, y + 44), 2)
        for wx4 in [x + 5, x + 47]:
            pygame.draw.rect(surface, (110, 140, 155), (wx4 - 2, y + 10, 18, 16))
            pygame.draw.rect(surface, win_color, (wx4, y + 12, 14, 12))
            pygame.draw.line(surface, (110, 140, 155), (wx4 + 7, y + 12), (wx4 + 7, y + 24), 1)
        # Caixa d'agua lateral esquerda
        pygame.draw.rect(surface, (155, 155, 165), (x - 10, y - 22, 6, 26))
        _water_tank(x - 12, y - 40, 20, 16, 7, 20)

    elif v == 4:
        # Casinha de pobre com telhado de palha — cor diferente (rosada)
        pygame.draw.rect(surface, (215, 175, 160), (x + 5, y + 10, 56, 50))
        pygame.draw.rect(surface, (185, 145, 130), (x + 5, y + 10, 56, 50), 2)
        roof5_pts = [(x + 2, y + 12), (x + 33, y - 22), (x + 64, y + 12)]
        pygame.draw.polygon(surface, (130, 100, 50), roof5_pts)
        for pi in range(0, 65, 5):
            pygame.draw.line(surface, (110, 82, 36),
                             (x + 2 + pi, y + 12),
                             (x + 20 + pi // 2, y - 22 + pi // 3), 1)
        pygame.draw.rect(surface, (90, 60, 30), (x + 22, y + 34, 14, 26))
        pygame.draw.circle(surface, (200, 160, 60), (x + 32, y + 47), 2)
        pygame.draw.rect(surface, (80, 65, 40), (x + 7, y + 14, 16, 14))
        pygame.draw.rect(surface, win_color, (x + 8, y + 15, 14, 12))
        pygame.draw.rect(surface, (80, 65, 40), (x + 40, y + 14, 16, 14))
        pygame.draw.rect(surface, win_color, (x + 41, y + 15, 14, 12))
        for pi in range(0, 56, 9):
            pygame.draw.rect(surface, (160, 140, 110), (x + 5 + pi, y + 56, 8, 6), 1)
        # Galinha
        hx2, hy2 = x - 6, y + 48
        pygame.draw.ellipse(surface, (230, 220, 200), (hx2, hy2, 10, 8))
        pygame.draw.circle(surface, (230, 220, 200), (hx2 + 9, hy2 - 2), 5)
        pygame.draw.polygon(surface, (220, 100, 60), [(hx2 + 13, hy2 - 2), (hx2 + 16, hy2 + 1), (hx2 + 13, hy2 + 1)])
        pygame.draw.rect(surface, (220, 100, 60), (hx2 + 12, hy2 + 3, 1, 4))
        pygame.draw.circle(surface, (200, 60, 60), (hx2 + 13, hy2 - 4), 2)
        # Caixa d'agua pequena no topo da parede
        _water_tank(x + 46, y - 18, 18, 14, 5, 16)

    else:  # v == 5
        # Casa amarelada 2 andares — fachada diferente das outras
        pygame.draw.rect(surface, (230, 210, 155), (x, y, 70, 88))
        pygame.draw.rect(surface, (195, 175, 120), (x, y, 70, 88), 2)
        pygame.draw.rect(surface, (195, 175, 120), (x, y + 44, 70, 4))
        roof6 = [(x - 6, y + 2), (x + 35, y - 30), (x + 76, y + 2)]
        pygame.draw.polygon(surface, (160, 60, 60), roof6)
        pygame.draw.polygon(surface, (130, 40, 40), roof6, 2)
        for wx6 in [x + 5, x + 48]:
            pygame.draw.rect(surface, (155, 130, 80), (wx6, y + 6, 16, 16))
            pygame.draw.rect(surface, win_color, (wx6 + 1, y + 7, 14, 14))
            pygame.draw.line(surface, (155, 130, 80), (wx6 + 8, y + 7), (wx6 + 8, y + 21), 1)
        pygame.draw.rect(surface, (175, 155, 100), (x - 4, y + 44, 78, 5))
        pygame.draw.rect(surface, DRY_TRUNK, (x + 4, y + 44, 4, 44))
        pygame.draw.rect(surface, DRY_TRUNK, (x + 62, y + 44, 4, 44))
        for wx6 in [x + 5, x + 48]:
            pygame.draw.rect(surface, (155, 130, 80), (wx6, y + 52, 16, 16))
            pygame.draw.rect(surface, win_color, (wx6 + 1, y + 53, 14, 14))
        pygame.draw.rect(surface, (80, 50, 25), (x + 26, y + 56, 18, 32))
        pygame.draw.circle(surface, YELLOW, (x + 38, y + 74), 2)
        # Caixa d'agua centralizada no teto
        _water_tank(x + 24, y - 44, 22, 16, 8, 20)

    # Indicador flutuante de agua entregue
    if has_water:
        center_x = x + 34
        fy = y - 38
        pygame.draw.polygon(surface, WATER_BLUE, [(center_x, fy), (center_x - 8, fy + 14), (center_x + 8, fy + 14)])
        pygame.draw.circle(surface, WATER_BLUE, (center_x, fy + 15), 8)
        pygame.draw.circle(surface, WHITE, (center_x - 2, fy + 13), 2)


def draw_npc(surface, x, y, thirsty=True, variant=0, frame=0):
    """Desenha um morador do sertao. 7 personagens completamente distintos."""
    bob = int(math.sin(frame * 0.08 + variant * 1.2) * 3) if thirsty else 0
    droop = 4 if thirsty else 0
    dy = bob

    def _eyes_sad(ex, ey):
        pygame.draw.line(surface, BLACK, (ex + 7, ey + 10), (ex + 9, ey + 12), 2)
        pygame.draw.line(surface, BLACK, (ex + 13, ey + 10), (ex + 15, ey + 12), 2)
        pygame.draw.arc(surface, BLACK, (ex + 7, ey + 17, 8, 5), 0, 3.14, 2)

    def _eyes_happy(ex, ey):
        pygame.draw.circle(surface, BLACK, (ex + 8, ey + 11), 2)
        pygame.draw.circle(surface, BLACK, (ex + 14, ey + 11), 2)
        pygame.draw.arc(surface, BLACK, (ex + 7, ey + 13, 8, 7), 3.14, 6.28, 2)

    def _thirst_drop(dx, dy_d):
        pygame.draw.circle(surface, WATER_BLUE, (dx + 24, dy_d + 6), 3)
        pygame.draw.polygon(surface, WATER_BLUE, [(dx + 24, dy_d + 2), (dx + 22, dy_d + 6), (dx + 26, dy_d + 6)])

    def _bucket_empty(bx, by):
        pygame.draw.rect(surface, (120, 100, 80), (bx, by, 10, 8))
        pygame.draw.rect(surface, (100, 80, 60), (bx, by, 10, 8), 1)
        pygame.draw.arc(surface, (140, 120, 90), (bx + 1, by - 4, 8, 5), 0, 3.14, 1)

    def _bucket_full(bx, by):
        pygame.draw.rect(surface, (120, 100, 80), (bx, by, 10, 8))
        pygame.draw.rect(surface, WATER_BLUE, (bx + 1, by + 1, 8, 4))
        pygame.draw.arc(surface, (140, 120, 90), (bx + 1, by - 4, 8, 5), 0, 3.14, 1)

    v = variant % 7

    if v == 0:
        # Homem do campo com chapeu de couro e bota
        skin = (145, 95, 55)
        # Corpo
        pygame.draw.rect(surface, (160, 100, 50), (x + 3, y + 22 + droop + dy, 18, 18))
        pygame.draw.rect(surface, (130, 75, 35), (x + 3, y + 22 + droop + dy, 18, 18), 1)
        # Cabeca
        pygame.draw.circle(surface, skin, (x + 12, y + 12 + droop + dy), 10)
        pygame.draw.rect(surface, (40, 25, 12), (x + 4, y + 2 + droop + dy, 16, 8))
        # Chapeu de couro
        pygame.draw.rect(surface, (130, 85, 40), (x - 2, y + 2 + droop + dy, 28, 5))
        pygame.draw.rect(surface, (110, 70, 30), (x + 3, y - 4 + droop + dy, 18, 8))
        pygame.draw.rect(surface, (150, 100, 50), (x - 2, y + 2 + droop + dy, 28, 2))
        if thirsty:
            _eyes_sad(x, y + droop + dy)
            _thirst_drop(x, y + droop + dy)
        else:
            _eyes_happy(x, y + droop + dy)
        # Calcas
        pygame.draw.rect(surface, (60, 80, 120), (x + 4, y + 40 + droop + dy, 6, 16))
        pygame.draw.rect(surface, (60, 80, 120), (x + 13, y + 40 + droop + dy, 6, 16))
        # Botas
        pygame.draw.rect(surface, (50, 35, 20), (x + 2, y + 54 + droop + dy, 10, 5))
        pygame.draw.rect(surface, (50, 35, 20), (x + 12, y + 54 + droop + dy, 10, 5))
        bkt_y = y + 34 + droop + dy
        if thirsty: _bucket_empty(x + 19, bkt_y)
        else: _bucket_full(x + 19, bkt_y)

    elif v == 1:
        # Mulher idosa com lenco na cabeca
        skin = (160, 110, 70)
        # Saia longa
        pygame.draw.polygon(surface, (180, 80, 100), [(x + 3, y + 22 + droop + dy), (x + 21, y + 22 + droop + dy),
                             (x + 25, y + 58 + droop + dy), (x - 1, y + 58 + droop + dy)])
        # Blusa
        pygame.draw.rect(surface, (200, 160, 120), (x + 4, y + 22 + droop + dy, 16, 14))
        # Cabeca
        pygame.draw.circle(surface, skin, (x + 12, y + 12 + droop + dy), 9)
        # Lenco na cabeca
        pygame.draw.ellipse(surface, (230, 210, 180), (x + 2, y + 2 + droop + dy, 20, 12))
        pygame.draw.line(surface, (210, 185, 155), (x + 2, y + 10 + droop + dy), (x + 22, y + 8 + droop + dy), 2)
        if thirsty:
            _eyes_sad(x, y + droop + dy)
            _thirst_drop(x, y + droop + dy)
        else:
            _eyes_happy(x, y + droop + dy)
        # Bengala
        pygame.draw.line(surface, DRY_TRUNK, (x + 22, y + 26 + droop + dy), (x + 28, y + 58 + droop + dy), 2)
        pygame.draw.arc(surface, DRY_TRUNK, (x + 19, y + 22 + droop + dy, 8, 6), 0, 3.14, 2)
        # Pes
        pygame.draw.rect(surface, (70, 50, 30), (x + 2, y + 56 + droop + dy, 8, 4))
        pygame.draw.rect(surface, (70, 50, 30), (x + 13, y + 56 + droop + dy, 8, 4))
        bkt_y = y + 36 + droop + dy
        if thirsty: _bucket_empty(x - 4, bkt_y)
        else: _bucket_full(x - 4, bkt_y)

    elif v == 2:
        # Crianca pequena (altura reduzida)
        skin = (175, 125, 75)
        scale_y = 0
        # Corpo
        pygame.draw.rect(surface, (100, 180, 100), (x + 5, y + 18 + droop + dy + 8, 14, 14))
        # Cabeca grande (proporcao de crianca)
        pygame.draw.circle(surface, skin, (x + 12, y + 9 + droop + dy + 8), 11)
        pygame.draw.rect(surface, (40, 25, 12), (x + 4, y - 1 + droop + dy + 8, 16, 8))
        if thirsty:
            _eyes_sad(x, y + droop + dy + 8)
            _thirst_drop(x, y + droop + dy + 8)
        else:
            _eyes_happy(x, y + droop + dy + 8)
        # Calcao curto
        pygame.draw.rect(surface, (100, 130, 180), (x + 5, y + 32 + droop + dy + 8, 6, 8))
        pygame.draw.rect(surface, (100, 130, 180), (x + 13, y + 32 + droop + dy + 8, 6, 8))
        # Pes descalcos
        pygame.draw.ellipse(surface, skin, (x + 3, y + 39 + droop + dy + 8, 8, 4))
        pygame.draw.ellipse(surface, skin, (x + 13, y + 39 + droop + dy + 8, 8, 4))
        bkt_y = y + 26 + droop + dy + 8
        if thirsty: _bucket_empty(x + 18, bkt_y)
        else: _bucket_full(x + 18, bkt_y)

    elif v == 3:
        # Homem jovem com camiseta e tenis
        skin = (130, 85, 48)
        pygame.draw.rect(surface, (70, 120, 190), (x + 3, y + 22 + droop + dy, 18, 18))
        pygame.draw.rect(surface, (50, 100, 170), (x + 3, y + 22 + droop + dy, 18, 18), 1)
        pygame.draw.circle(surface, skin, (x + 12, y + 12 + droop + dy), 10)
        pygame.draw.rect(surface, (30, 18, 8), (x + 4, y + 2 + droop + dy, 16, 8))
        # Bone
        pygame.draw.rect(surface, (200, 60, 60), (x + 3, y + 4 + droop + dy, 18, 5))
        pygame.draw.rect(surface, (200, 60, 60), (x + 3, y + 2 + droop + dy, 18, 4))
        pygame.draw.rect(surface, (200, 60, 60), (x + 20, y + 6 + droop + dy, 6, 3))
        if thirsty:
            _eyes_sad(x, y + droop + dy)
            _thirst_drop(x, y + droop + dy)
        else:
            _eyes_happy(x, y + droop + dy)
        pygame.draw.rect(surface, (40, 55, 80), (x + 4, y + 40 + droop + dy, 6, 14))
        pygame.draw.rect(surface, (40, 55, 80), (x + 13, y + 40 + droop + dy, 6, 14))
        # Tenis
        pygame.draw.rect(surface, (240, 240, 245), (x + 2, y + 52 + droop + dy, 10, 5))
        pygame.draw.rect(surface, (240, 240, 245), (x + 12, y + 52 + droop + dy, 10, 5))
        bkt_y = y + 34 + droop + dy
        if thirsty: _bucket_empty(x + 19, bkt_y)
        else: _bucket_full(x + 19, bkt_y)

    elif v == 4:
        # Mulher jovem com vestido e tranca
        skin = (155, 105, 62)
        # Vestido
        pygame.draw.polygon(surface, (220, 120, 80), [(x + 3, y + 22 + droop + dy), (x + 21, y + 22 + droop + dy),
                             (x + 23, y + 56 + droop + dy), (x + 1, y + 56 + droop + dy)])
        # Torso
        pygame.draw.rect(surface, (200, 100, 60), (x + 5, y + 22 + droop + dy, 14, 12))
        # Cabeca
        pygame.draw.circle(surface, skin, (x + 12, y + 12 + droop + dy), 10)
        # Tranca longa
        pygame.draw.rect(surface, (30, 18, 8), (x + 3, y + 2 + droop + dy, 18, 8))
        pygame.draw.rect(surface, (35, 22, 10), (x + 16, y + 8 + droop + dy, 5, 22))
        if thirsty:
            _eyes_sad(x, y + droop + dy)
            _thirst_drop(x, y + droop + dy)
        else:
            _eyes_happy(x, y + droop + dy)
        # Sandalia
        pygame.draw.rect(surface, (120, 85, 50), (x + 3, y + 54 + droop + dy, 8, 4))
        pygame.draw.rect(surface, (120, 85, 50), (x + 13, y + 54 + droop + dy, 8, 4))
        bkt_y = y + 36 + droop + dy
        if thirsty: _bucket_empty(x - 4, bkt_y)
        else: _bucket_full(x - 4, bkt_y)

    elif v == 5:
        # Homem velho curvado com chapeu de palha
        skin = (140, 90, 52)
        # Postura curvada (offset)
        oy = 4 if thirsty else 2
        pygame.draw.rect(surface, (120, 140, 80), (x + 2, y + 20 + droop + dy + oy, 17, 16))
        pygame.draw.circle(surface, skin, (x + 11, y + 11 + droop + dy + oy), 9)
        # Chapeu de palha
        pygame.draw.ellipse(surface, (200, 175, 100), (x - 3, y + 3 + droop + dy + oy, 28, 8))
        pygame.draw.rect(surface, (190, 165, 90), (x + 2, y - 4 + droop + dy + oy, 18, 9))
        pygame.draw.rect(surface, (170, 145, 75), (x - 3, y + 3 + droop + dy + oy, 28, 2))
        if thirsty:
            _eyes_sad(x - 1, y + droop + dy + oy)
            _thirst_drop(x, y + droop + dy + oy)
        else:
            _eyes_happy(x - 1, y + droop + dy + oy)
        # Calcas dobradas
        pygame.draw.rect(surface, (80, 95, 60), (x + 3, y + 36 + droop + dy + oy, 5, 14))
        pygame.draw.rect(surface, (80, 95, 60), (x + 12, y + 36 + droop + dy + oy, 5, 14))
        # Bengala
        pygame.draw.line(surface, DRY_TRUNK, (x + 20, y + 24 + droop + dy + oy), (x + 26, y + 52 + droop + dy + oy), 2)
        # Pes
        pygame.draw.rect(surface, (55, 38, 22), (x + 1, y + 49 + droop + dy + oy, 8, 4))
        pygame.draw.rect(surface, (55, 38, 22), (x + 11, y + 49 + droop + dy + oy, 8, 4))
        bkt_y = y + 30 + droop + dy + oy
        if thirsty: _bucket_empty(x - 6, bkt_y)
        else: _bucket_full(x - 6, bkt_y)

    else:  # v == 6
        # Mae carregando panela na cabeca
        skin = (165, 112, 65)
        # Corpo/blusa
        pygame.draw.rect(surface, (160, 80, 160), (x + 3, y + 22 + droop + dy, 18, 18))
        # Saia
        pygame.draw.polygon(surface, (130, 60, 130), [(x + 1, y + 36 + droop + dy), (x + 23, y + 36 + droop + dy),
                             (x + 25, y + 56 + droop + dy), (x - 1, y + 56 + droop + dy)])
        # Cabeca
        pygame.draw.circle(surface, skin, (x + 12, y + 12 + droop + dy), 10)
        pygame.draw.rect(surface, (30, 18, 8), (x + 3, y + 2 + droop + dy, 18, 8))
        # Lenco colorido
        pygame.draw.ellipse(surface, (220, 80, 80), (x + 2, y + 1 + droop + dy, 20, 10))
        if thirsty:
            _eyes_sad(x, y + droop + dy)
            _thirst_drop(x, y + droop + dy)
        else:
            _eyes_happy(x, y + droop + dy)
        # Panela/moringa na cabeca (elemento cultural nordestino)
        pygame.draw.ellipse(surface, (140, 90, 60), (x + 4, y - 5 + droop + dy, 16, 10))
        pygame.draw.rect(surface, (120, 75, 45), (x + 6, y - 8 + droop + dy, 12, 6))
        pygame.draw.ellipse(surface, (140, 90, 60), (x + 4, y - 10 + droop + dy, 16, 6))
        # Pes
        pygame.draw.rect(surface, (80, 55, 30), (x + 3, y + 54 + droop + dy, 8, 4))
        pygame.draw.rect(surface, (80, 55, 30), (x + 13, y + 54 + droop + dy, 8, 4))
        bkt_y = y + 36 + droop + dy
        if thirsty: _bucket_empty(x + 20, bkt_y)
        else: _bucket_full(x + 20, bkt_y)


def draw_purification_machine(surface, x, y, filling=False, fill_progress=0):
    """Desenha a maquina de purificacao de agua.
    Mostra o nivel de agua interno e, se enchendo, o galhao e a barra de progresso."""
    pygame.draw.rect(surface, MACHINE_DARK, (x, y, 50, 70))
    pygame.draw.rect(surface, MACHINE_BLUE, (x + 3, y + 3, 44, 64))
    txt = font_tiny.render("ÁGUA", True, WHITE)
    surface.blit(txt, (x + 14, y + 5))
    txt2 = font_tiny.render("PURA", True, WHITE)
    surface.blit(txt2, (x + 14, y + 17))
    # Tanque interno com nivel d'agua animado
    pygame.draw.rect(surface, (20, 50, 80), (x + 8, y + 30, 34, 20))
    water_h = 16 + int(math.sin(time_module.time() * 3) * 2)
    pygame.draw.rect(surface, WATER_BLUE, (x + 9, y + 31 + (19 - water_h), 32, water_h))
    pygame.draw.rect(surface, WATER_LIGHT, (x + 9, y + 31 + (19 - water_h), 32, 4))
    pygame.draw.rect(surface, WHITE, (x + 8, y + 30, 34, 20), 2)
    # Torneira
    pygame.draw.rect(surface, (160, 160, 170), (x + 18, y + 52, 14, 6))
    pygame.draw.rect(surface, (160, 160, 170), (x + 22, y + 56, 6, 10))
    if filling:
        # Goticulas caindo
        for i in range(3):
            wy = y + 66 + i * 4
            pygame.draw.rect(surface, WATER_BLUE, (x + 23, wy, 4, 3))
        # Galhao sendo enchido com barra de progresso
        pygame.draw.rect(surface, (180, 180, 190), (x + 16, y + 72, 18, 22))
        fill_h = int(18 * fill_progress)
        if fill_h > 0:
            pygame.draw.rect(surface, WATER_BLUE, (x + 18, y + 74 + (18 - fill_h), 14, fill_h))
        pygame.draw.rect(surface, (160, 160, 170), (x + 16, y + 72, 18, 22), 2)
    pygame.draw.rect(surface, (30, 80, 100), (x, y, 50, 70), 3)


def draw_treatment_station(surface, x, y, station_type, active=False, completed=False):
    """Desenha uma estação de tratamento (Fase 4) com cores e estado específicos."""
    colors = {"filtrar": STATION_FILTER, "tratar": STATION_TREAT,
              "desinfetar": STATION_DISINF, "liberar": STATION_RELEASE}
    labels = {"filtrar": "FILTRAR", "tratar": "TRATAR",
              "desinfetar": "DESINF.", "liberar": "LIBERAR"}

    base_color = colors.get(station_type, PIPE_GRAY)
    if completed:
        base_color = (80, 80, 85)
    elif active:
        base_color = tuple(min(255, c + 40) for c in base_color)

    # Base platform
    pygame.draw.rect(surface, (60, 60, 65), (x, y + 50, 70, 20))

    if station_type == "filtrar":
        # Filter machine — rectangular with mesh pattern
        pygame.draw.rect(surface, base_color, (x + 5, y, 60, 55), border_radius=4)
        pygame.draw.rect(surface, tuple(max(0, c - 30) for c in base_color), (x + 5, y, 60, 55), 3, border_radius=4)
        # Filter mesh
        for fy in range(y + 10, y + 48, 6):
            pygame.draw.line(surface, tuple(max(0, c - 60) for c in base_color), (x + 12, fy), (x + 58, fy), 1)
        for fx in range(x + 12, x + 60, 8):
            pygame.draw.line(surface, tuple(max(0, c - 60) for c in base_color), (fx, y + 10), (fx, y + 48), 1)
        # Inlet/outlet pipes
        pygame.draw.rect(surface, PIPE_GRAY, (x + 2, y + 20, 8, 8))
        pygame.draw.rect(surface, PIPE_GRAY, (x + 60, y + 20, 8, 8))

    elif station_type == "tratar":
        # Chemical tank — cylindrical with bubbles
        pygame.draw.ellipse(surface, base_color, (x + 8, y, 54, 20))
        pygame.draw.rect(surface, base_color, (x + 8, y + 8, 54, 40))
        pygame.draw.ellipse(surface, base_color, (x + 8, y + 38, 54, 14))
        pygame.draw.ellipse(surface, tuple(max(0, c - 30) for c in base_color), (x + 8, y, 54, 20), 2)
        pygame.draw.rect(surface, tuple(max(0, c - 30) for c in base_color), (x + 8, y + 8, 54, 40), 2)
        # Bubbles rising in tank
        t = time_module.time()
        for bi in range(3):
            bx_off = x + 18 + bi * 12
            by_off = y + 45 - int((t * 20 + bi * 15) % 35)
            pygame.draw.circle(surface, tuple(min(255, c + 80) for c in base_color), (bx_off, by_off), 3)
        # Chemical label
        chem = font_tiny.render("H2O", True, WHITE)
        surface.blit(chem, (x + 27, y + 18))

    elif station_type == "desinfetar":
        # Chlorine station — with Cl symbol and green glow
        pygame.draw.rect(surface, base_color, (x + 5, y, 60, 55), border_radius=6)
        pygame.draw.rect(surface, tuple(max(0, c - 30) for c in base_color), (x + 5, y, 60, 55), 3, border_radius=6)
        # Glow effect
        glow_v = int(80 + 40 * math.sin(time_module.time() * 3))
        pygame.draw.rect(surface, (30, glow_v, 30), (x + 8, y + 3, 54, 49), border_radius=4)
        # Cl symbol
        cl = font_med.render("Cl", True, (200, 255, 200))
        surface.blit(cl, (x + 24, y + 14))
        # Two gas nozzles
        pygame.draw.rect(surface, (130, 130, 140), (x + 12, y + 44, 8, 10))
        pygame.draw.rect(surface, (130, 130, 140), (x + 50, y + 44, 8, 10))

    elif station_type == "liberar":
        # Release valve — pipe with handle
        pygame.draw.rect(surface, base_color, (x + 5, y + 10, 60, 35), border_radius=4)
        pygame.draw.rect(surface, tuple(max(0, c - 30) for c in base_color), (x + 5, y + 10, 60, 35), 3, border_radius=4)
        # Valve wheel
        pygame.draw.circle(surface, (140, 140, 150), (x + 35, y + 28), 14, 3)
        for vi in range(4):
            va = vi * math.pi / 2
            pygame.draw.line(surface, (140, 140, 150), (x + 35, y + 28),
                             (x + 35 + int(math.cos(va) * 12), y + 28 + int(math.sin(va) * 12)), 2)
        pygame.draw.circle(surface, (160, 160, 170), (x + 35, y + 28), 4)
        # Water droplet flowing out
        t = time_module.time()
        for di in range(2):
            drop_y = y + 48 + int((t * 30 + di * 15) % 20)
            pygame.draw.circle(surface, WATER_BLUE, (x + 35, drop_y), 3)

    else:
        pygame.draw.rect(surface, base_color, (x + 5, y, 60, 55), border_radius=6)
        pygame.draw.rect(surface, tuple(max(0, c - 30) for c in base_color), (x + 5, y, 60, 55), 3, border_radius=6)

    label = font_tiny.render(labels[station_type], True, WHITE)
    surface.blit(label, (x + 35 - label.get_width() // 2, y + 56))
    if active and not completed:
        glow = int(128 + 127 * math.sin(time_module.time() * 5))
        pygame.draw.rect(surface, (glow, glow, min(255, glow + 50)), (x + 5, y, 60, 55), 2, border_radius=6)
    if completed:
        pygame.draw.line(surface, GREEN_OK, (x + 22, y + 28), (x + 30, y + 36), 4)
        pygame.draw.line(surface, GREEN_OK, (x + 30, y + 36), (x + 48, y + 18), 4)


# ============================================================
# TITLE SCREEN DRAWING
# ============================================================

def draw_samuel_hero(surface, x, y, frame=0):
    """Desenha o Samuel em tamanho herói (grande) para a tela de título."""
    s = 3
    cx = int(x)
    cy = int(y)
    cape_sway = int(math.sin(frame * 0.08) * 6)
    cape_sway2 = int(math.sin(frame * 0.08 + 1) * 4)
    cape_pts = [
        (cx + 12, cy + 42), (cx - 8 + cape_sway, cy + 130),
        (cx - 2 + cape_sway2, cy + 135), (cx + 10, cy + 120),
        (cx + 70, cy + 120), (cx + 82 + cape_sway2, cy + 135),
        (cx + 88 + cape_sway, cy + 130), (cx + 68, cy + 42),
    ]
    pygame.draw.polygon(surface, CAPE_RED, cape_pts)
    pygame.draw.polygon(surface, CAPE_DARK, cape_pts, 2)
    cape_inner = [(cx + 18, cy + 50), (cx + 2 + cape_sway // 2, cy + 120), (cx + 40, cy + 115)]
    pygame.draw.polygon(surface, (220, 60, 60), cape_inner)

    hair_cx = cx + 40
    hair_cy = cy + 14
    pygame.draw.ellipse(surface, SAMUEL_HAIR, (hair_cx - 28, hair_cy - 26, 56, 48))
    pygame.draw.ellipse(surface, SAMUEL_HAIR, (hair_cx - 32, hair_cy - 22, 64, 42))
    pygame.draw.ellipse(surface, SAMUEL_HAIR, (hair_cx - 26, hair_cy - 30, 52, 40))
    pygame.draw.ellipse(surface, (60, 35, 18), (hair_cx - 20, hair_cy - 24, 24, 18))
    pygame.draw.ellipse(surface, (55, 30, 15), (hair_cx + 4, hair_cy - 20, 18, 14))

    pygame.draw.rect(surface, SAMUEL_SKIN, (cx + 20, cy + 18, 40, 36))
    pygame.draw.rect(surface, SAMUEL_SKIN_LIGHT, (cx + 24, cy + 22, 14, 10))
    pygame.draw.ellipse(surface, WHITE, (cx + 24, cy + 30, 14, 12))
    pygame.draw.ellipse(surface, BLACK, (cx + 28, cy + 32, 8, 9))
    pygame.draw.ellipse(surface, WHITE, (cx + 30, cy + 32, 4, 4))
    pygame.draw.ellipse(surface, WHITE, (cx + 42, cy + 30, 14, 12))
    pygame.draw.ellipse(surface, BLACK, (cx + 44, cy + 32, 8, 9))
    pygame.draw.ellipse(surface, WHITE, (cx + 46, cy + 32, 4, 4))
    pygame.draw.ellipse(surface, (120, 60, 30), (cx + 30, cy + 44, 20, 10))
    pygame.draw.rect(surface, WHITE, (cx + 33, cy + 44, 14, 5))
    pygame.draw.rect(surface, SHIRT_WHITE, (cx + 16, cy + 54, 48, 32))
    pygame.draw.rect(surface, VEST_ORANGE, (cx + 10, cy + 54, 14, 32))
    pygame.draw.rect(surface, VEST_ORANGE, (cx + 56, cy + 54, 14, 32))
    pygame.draw.rect(surface, VEST_DARK, (cx + 10, cy + 54, 14, 32), 2)
    pygame.draw.rect(surface, VEST_DARK, (cx + 56, cy + 54, 14, 32), 2)
    pygame.draw.rect(surface, BELT_BROWN, (cx + 12, cy + 84, 56, 6))
    pygame.draw.rect(surface, YELLOW, (cx + 34, cy + 84, 12, 6))
    pygame.draw.rect(surface, SAMUEL_SKIN, (cx + 2, cy + 58, 10, 28))
    pygame.draw.rect(surface, SAMUEL_SKIN, (cx, cy + 84, 14, 10))
    pygame.draw.rect(surface, SAMUEL_SKIN, (cx + 68, cy + 58, 10, 28))
    pygame.draw.rect(surface, SAMUEL_SKIN, (cx + 66, cy + 84, 14, 10))
    pygame.draw.rect(surface, PANTS_BROWN, (cx + 16, cy + 90, 22, 28))
    pygame.draw.rect(surface, PANTS_BROWN, (cx + 42, cy + 90, 22, 28))
    pygame.draw.rect(surface, SHOE_RED, (cx + 10, cy + 118, 26, 12))
    pygame.draw.rect(surface, SHOE_RED, (cx + 44, cy + 118, 26, 12))
    pygame.draw.rect(surface, WHITE, (cx + 10, cy + 118, 26, 4))
    pygame.draw.rect(surface, WHITE, (cx + 44, cy + 118, 26, 4))


def draw_ods6_symbol(surface, x, y, size=50):
    """Desenha o símbolo do ODS 6 (Água Potável e Saneamento) com o número 6."""
    rect = pygame.Rect(x, y, size, size)
    ods_cyan = (38, 189, 226)
    pygame.draw.rect(surface, ods_cyan, rect, border_radius=max(2, size // 12))
    drop_cx = x + size // 2
    drop_top = y + int(size * 0.12)
    drop_mid = y + int(size * 0.38)
    drop_r = int(size * 0.16)
    pygame.draw.polygon(surface, WHITE, [
        (drop_cx, drop_top),
        (drop_cx - drop_r, drop_mid + drop_r // 2),
        (drop_cx + drop_r, drop_mid + drop_r // 2),
    ])
    pygame.draw.circle(surface, WHITE, (drop_cx, drop_mid + drop_r // 2), drop_r)
    num_font = pygame.font.SysFont('arial', max(10, int(size * 0.38)), bold=True)
    num_surf = num_font.render("6", True, WHITE)
    num_x = x + size // 2 - num_surf.get_width() // 2
    num_y = y + int(size * 0.58)
    surface.blit(num_surf, (num_x, num_y))


def draw_water_drop_title(surface, x, y, size=30, frame=0):
    """Desenha uma gota d'água decorativa com efeito de flutuação para a tela de título."""
    bob = int(math.sin(frame * 0.06) * 4)
    dy = y + bob
    drop_color = (64, 164, 223)
    drop_light = (100, 195, 240)
    r = size // 2
    pygame.draw.polygon(surface, drop_color, [(x + r, dy), (x, dy + int(r * 1.4)), (x + size, dy + int(r * 1.4))])
    pygame.draw.circle(surface, drop_color, (x + r, dy + int(r * 1.4)), r)
    pygame.draw.circle(surface, drop_light, (x + r - r // 3, dy + int(r * 1.0)), r // 3)
    pygame.draw.circle(surface, WHITE, (x + r - r // 3, dy + int(r * 0.8)), max(1, r // 5))


def draw_water_drop_collectible(surface, x, y, frame=0):
    """Draw a small collectible water drop."""
    bob = math.sin(frame * 0.08 + x * 0.01) * 4
    dy = int(y + bob)
    pygame.draw.polygon(surface, WATER_BLUE, [(x + 8, dy), (x, dy + 14), (x + 16, dy + 14)])
    pygame.draw.circle(surface, WATER_BLUE, (x + 8, dy + 15), 8)
    pygame.draw.circle(surface, WHITE, (x + 5, dy + 11), 3)


# ============================================================
# BACKGROUNDS (now accept cam_x for side-scrolling)
# ============================================================

def draw_sky_gradient(surface, top_color, bottom_color, height=350):
    """Desenha um gradiente vertical do céu interpolando duas cores."""
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_W, y))


def draw_bg_river(surface, frame, cam_x=0, level_w=SCREEN_W, pollution_ratio=0.0):
    """Desenha o fundo da Fase 1: margem de rio com prédios, árvores e água poluída."""
    draw_sky_gradient(surface, (90, 170, 220), (160, 210, 230))
    # Clouds (parallax)
    for i, (cx, cy, sz) in enumerate([(100, 30, 1.2), (350, 60, 0.9), (650, 25, 1.1), (850, 55, 0.7), (1200, 35, 1.0)]):
        ox = int((cx - frame * 0.2 * (i * 0.3 + 0.5) - cam_x * 0.1) % (level_w + 300) - 150)
        draw_cloud(surface, ox, cy, sz)
    # Buildings (parallax background) — varied colors, widths, windows
    _building_colors = [(150, 160, 170), (140, 130, 120), (160, 150, 140), (130, 140, 155), (170, 165, 155)]
    rng_b = random.Random(12345)
    for bx in range(0, level_w, 100):
        sx = int(bx - cam_x * 0.3)
        if sx < -100 or sx > SCREEN_W + 100:
            continue
        bh = 70 + rng_b.randint(0, 70)
        bw = rng_b.randint(40, 80)
        by = 280 - bh
        bc = _building_colors[rng_b.randint(0, len(_building_colors) - 1)]
        pygame.draw.rect(surface, bc, (sx + 5, by, bw, bh))
        pygame.draw.rect(surface, tuple(max(0, c - 20) for c in bc), (sx + 5, by, bw, bh), 1)
        win_spacing = rng_b.randint(14, 20)
        for wy in range(by + 8, by + bh - 10, win_spacing):
            for wx in range(sx + 10, sx + 5 + bw - 10, 14):
                if rng_b.random() > 0.25:
                    pygame.draw.rect(surface, (180, 210, 230), (wx, wy, 7, 9))
    # Trees between buildings
    rng_t = random.Random(54321)
    for tx in range(50, level_w, 130):
        sx = int(tx - cam_x * 0.28)
        if sx < -60 or sx > SCREEN_W + 60:
            continue
        tree_variant = rng_t.randint(0, 5)
        draw_tree(surface, sx, 262, tree_variant)

    # Upper bank
    pygame.draw.rect(surface, GRASS_GREEN, (0, 300, SCREEN_W, 40))
    pygame.draw.rect(surface, GRASS_DARK, (0, 300, SCREEN_W, 6))
    for gx in range(0, SCREEN_W, 12):
        gh = 4 + ((gx + int(cam_x)) * 3) % 8
        pygame.draw.rect(surface, GRASS_LIGHT, (gx, 296 - gh, 4, gh + 6))

    # River
    pr = pollution_ratio
    water_dark_c = (int(WATER_DARK[0] + (80 - WATER_DARK[0]) * pr),
                    int(WATER_DARK[1] + (70 - WATER_DARK[1]) * pr),
                    int(WATER_DARK[2] + (40 - WATER_DARK[2]) * pr))
    water_blue_c = (int(WATER_BLUE[0] + (100 - WATER_BLUE[0]) * pr),
                    int(WATER_BLUE[1] + (110 - WATER_BLUE[1]) * pr),
                    int(WATER_BLUE[2] + (50 - WATER_BLUE[2]) * pr))
    water_light_c = (int(WATER_LIGHT[0] + (120 - WATER_LIGHT[0]) * pr),
                     int(WATER_LIGHT[1] + (130 - WATER_LIGHT[1]) * pr),
                     int(WATER_LIGHT[2] + (60 - WATER_LIGHT[2]) * pr))
    pygame.draw.rect(surface, water_dark_c, (0, 340, SCREEN_W, 120))
    for wx in range(0, SCREEN_W, 25):
        world_wx = wx + cam_x
        wy = 340 + math.sin((world_wx + frame * 1.5) * 0.025) * 6
        pygame.draw.ellipse(surface, water_blue_c, (wx, int(wy), 35, 14))
    for wx in range(10, SCREEN_W, 40):
        world_wx = wx + cam_x
        wy = 420 + math.sin((world_wx + frame * 1.2) * 0.03) * 4
        pygame.draw.ellipse(surface, water_light_c, (wx, int(wy), 20, 8))

    # Lower bank
    pygame.draw.rect(surface, GRASS_GREEN, (0, 460, SCREEN_W, 20))
    pygame.draw.rect(surface, GRASS_DARK, (0, 460, SCREEN_W, 6))
    # Ground path
    pygame.draw.rect(surface, DIRT_BROWN, (0, 480, SCREEN_W, 160))
    pygame.draw.rect(surface, DIRT_DARK, (0, 480, SCREEN_W, 6))
    for dx in range(0, SCREEN_W, 50):
        pygame.draw.rect(surface, DIRT_LIGHT, (dx + 15, 510, 12, 6))


def draw_bg_neighborhood(surface, frame, cam_x=0, level_w=SCREEN_W):
    """Desenha o fundo da Fase 2: cidade noturna com estrelas e prédios iluminados."""
    # Céu noturno azul escuro
    draw_sky_gradient(surface, (8, 12, 38), (18, 28, 62), SCREEN_H)

    # Estrelas fixas (não rolam com câmera)
    rng_st = random.Random(99)
    for _ in range(70):
        _stx = rng_st.randint(0, SCREEN_W - 1)
        _sty = rng_st.randint(2, 170)
        _sbr = rng_st.randint(150, 255)
        _ssz = rng_st.randint(0, 3)
        if _ssz < 2:
            surface.set_at((_stx, _sty), (_sbr, _sbr, min(255, _sbr + 30)))
        else:
            pygame.draw.circle(surface, (_sbr, _sbr, min(255, _sbr + 30)), (_stx, _sty), 1)

    # Silhueta distante — prédios escuros ao fundo (parallax 0.1)
    rng_sf = random.Random(77)
    _sf_count = max(14, level_w // 90)
    _sf_data = []
    for _i in range(_sf_count):
        _sfx = _i * 95 + rng_sf.randint(-5, 5)
        _sfw = 40 + rng_sf.randint(0, 38)
        _sfh = 55 + rng_sf.randint(0, 110)
        _sf_data.append((_sfx, _sfw, _sfh))

    for _sfx, _sfw, _sfh in _sf_data:
        _ssx = int(_sfx - cam_x * 0.1)
        if _ssx < -80 or _ssx > SCREEN_W + 80:
            continue
        _sby = 378 - _sfh
        pygame.draw.rect(surface, (16, 20, 40), (_ssx, _sby, _sfw, _sfh))
        # Janelas apagadas na silhueta
        for _wy in range(_sby + 8, _sby + _sfh - 8, 20):
            for _wx in range(_ssx + 5, _ssx + _sfw - 8, 15):
                pygame.draw.rect(surface, (28, 38, 62), (_wx, _wy, 7, 9))

    # Prédios principais (parallax 0.3) — pré-computados para evitar RNG instável
    rng_b = random.Random(42)
    _b_count = max(10, level_w // 100)
    _b_data = []
    for _i in range(_b_count):
        _bx   = _i * 105 + rng_b.randint(-10, 10)
        _bw   = 60 + rng_b.randint(0, 40)
        _bh   = 100 + rng_b.randint(0, 120)
        _bc   = rng_b.randint(38, 62)
        _tower = rng_b.random() > 0.6
        # Pré-computa layout de janelas
        _wins = []
        _rows = (_bh - 25) // 22
        _cols = (_bw - 18) // 18
        for _r in range(max(1, _rows)):
            for _c in range(max(1, _cols)):
                _wins.append(rng_b.random() > 0.38)
        _b_data.append((_bx, _bw, _bh, _bc, _tower, _wins, _rows, _cols))

    for _bx, _bw, _bh, _bc, _tower, _wins, _rows, _cols in _b_data:
        _sx = int(_bx - cam_x * 0.3)
        if _sx < -110 or _sx > SCREEN_W + 110:
            continue
        _by = 380 - _bh
        # Corpo do prédio — tons escuros de cinza azulado
        pygame.draw.rect(surface, (_bc, _bc + 4, _bc + 10), (_sx, _by, _bw, _bh))
        pygame.draw.rect(surface, (_bc - 12, _bc - 8, _bc - 4), (_sx, _by, _bw, _bh), 2)
        # Linha horizontal entre andares
        for _fl in range(1, max(1, _bh // 22)):
            _fy = _by + _fl * 22
            if _fy < _by + _bh - 4:
                pygame.draw.line(surface, (_bc - 8, _bc - 4, _bc), (_sx + 1, _fy), (_sx + _bw - 2, _fy), 1)
        # Janelas
        for _idx, _lit in enumerate(_wins):
            _r = _idx // max(1, _cols)
            _c = _idx % max(1, _cols)
            _wy = _by + 10 + _r * 22
            _wx = _sx + 6 + _c * 18
            if _wy + 13 >= _by + _bh - 6 or _wx + 10 >= _sx + _bw - 4:
                continue
            pygame.draw.rect(surface, WINDOW_LIT if _lit else WINDOW_DARK, (_wx, _wy, 10, 13))
            if _lit:
                # Reflexo suave ao redor da janela acesa
                pygame.draw.rect(surface, (80, 65, 20), (_wx - 1, _wy - 1, 12, 15), 1)
        # Caixa d'água no topo
        if _tower:
            _tw = 13
            _th = 16
            _tx = _sx + _bw // 2 - _tw // 2
            _ty = _by - _th - 2
            pygame.draw.rect(surface, (_bc + 5, _bc + 8, _bc + 12), (_tx, _ty, _tw, _th))
            pygame.draw.rect(surface, (_bc - 10, _bc - 6, _bc - 2), (_tx, _ty, _tw, _th), 1)
            # Pernas
            pygame.draw.line(surface, (_bc - 8, _bc - 4, _bc), (_tx + 2, _ty + _th), (_tx + 2, _ty + _th + 5), 1)
            pygame.draw.line(surface, (_bc - 8, _bc - 4, _bc), (_tx + _tw - 3, _ty + _th), (_tx + _tw - 3, _ty + _th + 5), 1)


def draw_cactus(surface, x, y, variant=0, scale=1.0):
    """Desenha um cacto do sertao nordestino em variacoes de formato."""
    sc = scale
    bw = int(14 * sc)
    bh = int(50 * sc)
    # Tronco principal
    pygame.draw.rect(surface, CACTUS_GREEN, (x, y - bh, bw, bh), border_radius=int(6 * sc))
    pygame.draw.rect(surface, CACTUS_DARK, (x, y - bh, int(5 * sc), bh), border_radius=int(4 * sc))
    pygame.draw.rect(surface, (80, 140, 65), (x + int(9 * sc), y - bh, int(4 * sc), bh))
    if variant == 0:
        # Dois bracos em V
        arm_w = int(10 * sc)
        arm_h = int(28 * sc)
        # Braco esquerdo
        pygame.draw.rect(surface, CACTUS_GREEN, (x - int(12 * sc), y - int(38 * sc), arm_w, arm_h), border_radius=int(5 * sc))
        pygame.draw.rect(surface, CACTUS_DARK, (x - int(12 * sc), y - int(38 * sc), int(4 * sc), arm_h), border_radius=int(3 * sc))
        pygame.draw.rect(surface, CACTUS_GREEN, (x - int(12 * sc), y - int(38 * sc), arm_w, int(10 * sc)), border_radius=int(5 * sc))
        # Braco direito
        pygame.draw.rect(surface, CACTUS_GREEN, (x + bw, y - int(30 * sc), arm_w, int(24 * sc)), border_radius=int(5 * sc))
        pygame.draw.rect(surface, CACTUS_DARK, (x + bw, y - int(30 * sc), int(4 * sc), int(24 * sc)), border_radius=int(3 * sc))
        pygame.draw.rect(surface, CACTUS_GREEN, (x + bw, y - int(30 * sc), arm_w, int(10 * sc)), border_radius=int(5 * sc))
    elif variant == 1:
        # Alto e reto, sem bracos, com espinhos visiveis
        pygame.draw.rect(surface, CACTUS_GREEN, (x + int(2 * sc), y - int(bh * 1.4), int(10 * sc), int(bh * 0.5)), border_radius=int(5 * sc))
    elif variant == 2:
        # Cacto gordo baixo com um braco
        pygame.draw.rect(surface, CACTUS_GREEN, (x - int(8 * sc), y - int(20 * sc), int(8 * sc), int(16 * sc)), border_radius=int(4 * sc))
        pygame.draw.rect(surface, CACTUS_GREEN, (x - int(8 * sc), y - int(20 * sc), int(8 * sc), int(8 * sc)), border_radius=int(4 * sc))
    # Espinhos
    for si in range(0, bh, int(8 * sc)):
        pygame.draw.line(surface, CACTUS_SPINE, (x - 2, y - si - int(4 * sc)), (x - int(6 * sc), y - si - int(2 * sc)), 1)
        pygame.draw.line(surface, CACTUS_SPINE, (x + bw + 1, y - si - int(4 * sc)), (x + bw + int(5 * sc), y - si - int(2 * sc)), 1)


def draw_dry_tree(surface, x, y, variant=0):
    """Desenha uma arvore seca/esparsa tipica do sertao."""
    trunk_h = 40 + variant * 6
    trunk_w = 8 + variant % 3
    # Tronco
    pygame.draw.rect(surface, DRY_TRUNK, (x + 16, y + 10, trunk_w, trunk_h))
    pygame.draw.rect(surface, DRY_BRANCH, (x + 17, y + 14, 3, trunk_h - 10))
    # Galhos principais
    branches = [
        (x + 20, y + 14, x - 8 + variant * 4, y - 10, 3),
        (x + 20, y + 18, x + 44 - variant * 3, y - 4, 3),
        (x + 20, y + 26, x + 2 - variant * 2, y + 8, 2),
        (x + 20, y + 26, x + 40, y + 12, 2),
    ]
    for bx1, by1, bx2, by2, bw in branches:
        pygame.draw.line(surface, DRY_TRUNK, (bx1, by1), (bx2, by2), bw)
    if variant % 2 == 0:
        # Folhagem esparsa (poucos tufos)
        for fx, fy in [(x - 4, y - 18), (x + 36, y - 12), (x + 6, y - 6)]:
            pygame.draw.ellipse(surface, DRY_LEAF, (fx, fy, 18, 12))
            pygame.draw.ellipse(surface, (80, 100, 40), (fx + 3, fy + 3, 10, 6))
    else:
        # Folhagem reduzida num lado
        pygame.draw.ellipse(surface, DRY_LEAF, (x - 6, y - 14, 24, 16))
        pygame.draw.ellipse(surface, (80, 100, 40), (x - 2, y - 10, 14, 10))


def draw_fence_segment(surface, x, y, length=60):
    """Desenha um segmento de cerca de madeira do sertao."""
    post_h = 28
    # Postes
    for px in range(x, x + length + 1, 20):
        pygame.draw.rect(surface, FENCE_DARK, (px, y - post_h, 5, post_h))
        pygame.draw.rect(surface, FENCE_WOOD, (px + 1, y - post_h + 1, 3, post_h - 2))
        # Topo apontado
        pygame.draw.polygon(surface, FENCE_DARK, [(px, y - post_h), (px + 2, y - post_h - 5), (px + 4, y - post_h)])
    # Travessas horizontais
    pygame.draw.rect(surface, FENCE_WOOD, (x, y - post_h + 6, length, 4))
    pygame.draw.rect(surface, FENCE_DARK, (x, y - post_h + 6, length, 1))
    pygame.draw.rect(surface, FENCE_WOOD, (x, y - post_h + 16, length, 4))
    pygame.draw.rect(surface, FENCE_DARK, (x, y - post_h + 16, length, 1))


def draw_well(surface, x, y):
    """Desenha um poco de agua de pedra."""
    # Base circular de pedra
    pygame.draw.ellipse(surface, WELL_STONE_D, (x - 2, y + 2, 40, 16))
    pygame.draw.ellipse(surface, WELL_STONE, (x, y, 40, 16))
    # Parede cilindrica
    pygame.draw.rect(surface, WELL_STONE_D, (x, y - 20, 40, 22))
    pygame.draw.rect(surface, WELL_STONE, (x + 2, y - 20, 36, 20))
    # Pedras na parede
    for si in range(0, 36, 9):
        pygame.draw.rect(surface, WELL_STONE_D, (x + 2 + si, y - 18, 8, 6))
        pygame.draw.rect(surface, WELL_STONE_D, (x + 6 + si, y - 10, 8, 6))
    # Topo
    pygame.draw.ellipse(surface, WELL_STONE_D, (x - 2, y - 22, 44, 12))
    pygame.draw.ellipse(surface, WELL_STONE, (x, y - 22, 40, 10))
    # Estrutura do telhado
    pygame.draw.line(surface, DRY_TRUNK, (x + 4, y - 22), (x + 4, y - 46), 4)
    pygame.draw.line(surface, DRY_TRUNK, (x + 36, y - 22), (x + 36, y - 46), 4)
    pygame.draw.line(surface, DRY_TRUNK, (x + 4, y - 46), (x + 36, y - 46), 3)
    # Roldana
    pygame.draw.circle(surface, (100, 80, 55), (x + 20, y - 46), 6, 2)
    pygame.draw.circle(surface, (120, 95, 65), (x + 20, y - 46), 3)
    # Corda
    pygame.draw.line(surface, (140, 115, 80), (x + 20, y - 40), (x + 20, y - 22), 1)


def draw_clothesline(surface, x, y, length=80):
    """Desenha um varal com roupas secando."""
    # Postes
    pygame.draw.rect(surface, DRY_TRUNK, (x, y - 40, 4, 40))
    pygame.draw.rect(surface, DRY_TRUNK, (x + length, y - 40, 4, 40))
    # Fio do varal
    pygame.draw.line(surface, (160, 140, 100), (x + 2, y - 38), (x + length + 2, y - 38), 1)
    # Roupas
    clothes = [
        (x + 8,  LAUNDRY_1, 14, 18),
        (x + 28, LAUNDRY_2, 16, 14),
        (x + 50, LAUNDRY_3, 14, 18),
        (x + 68, LAUNDRY_1, 12, 16),
    ]
    for cx, cc, cw, ch in clothes:
        if cx + cw > x + length:
            break
        pygame.draw.rect(surface, cc, (cx, y - 36, cw, ch), border_radius=2)
        pygame.draw.rect(surface, tuple(max(0, c - 30) for c in cc), (cx, y - 36, cw, ch), 1, border_radius=2)
        # Pregadores
        pygame.draw.rect(surface, (100, 80, 60), (cx + 1, y - 38, 3, 4))
        pygame.draw.rect(surface, (100, 80, 60), (cx + cw - 4, y - 38, 3, 4))


def draw_bg_community(surface, frame, cam_x=0, level_w=SCREEN_W):
    """Desenha o fundo da Fase 3: comunidade sertaneja com sol quente, montes, vegetacao variada."""
    # --- CEU SERTANEJO ---
    draw_sky_gradient(surface, SERTAO_SKY_TOP, SERTAO_SKY_BOT, 360)

    # --- SOL QUENTE ---
    sun_x = SCREEN_W - 100
    sun_y = 55
    sun_pulse = int(6 * math.sin(frame * 0.02))
    for r in range(60 + sun_pulse, 30, -4):
        col = (255, min(255, 200 + (60 - r) * 2), max(0, 60 - (60 - r) * 3))
        pygame.draw.circle(surface, col, (sun_x, sun_y), r)
    pygame.draw.circle(surface, SUN_GLOW, (sun_x, sun_y), 32)
    pygame.draw.circle(surface, SUN_CORE, (sun_x, sun_y), 24)
    pygame.draw.circle(surface, (255, 255, 220), (sun_x - 4, sun_y - 4), 10)

    # --- NUVENS DISCRETAS (claras e esparsas para ceu quente) ---
    cloud_data = [
        (120, 30, 0.6), (380, 50, 0.5), (650, 22, 0.7),
        (950, 40, 0.55), (1250, 28, 0.6), (1550, 48, 0.5),
    ]
    for ci, (cx, cy, sz) in enumerate(cloud_data):
        ox = int((cx - frame * 0.12 * (ci * 0.15 + 0.3) - cam_x * 0.04) % (level_w + 400) - 200)
        if -80 < ox < SCREEN_W + 80:
            # Nuvem mais translucida — mistura com o ceu quente
            cs = int(10 * sz)
            pygame.draw.ellipse(surface, (240, 210, 170), (ox + 2, cy + 3, cs * 5, int(cs * 1.5)))
            pygame.draw.ellipse(surface, (248, 225, 190), (ox, cy, cs * 5, int(cs * 1.5)))
            pygame.draw.ellipse(surface, (252, 235, 200), (ox + cs, cy - cs, cs * 3, int(cs * 1.4)))

    # --- MONTES PEQUENOS (3 camadas, arredondados, mesma tonalidade marrom) ---
    # Camada distante — montes baixos e largos
    rng_m = random.Random(99)
    mound_far = []
    for mi in range(22):
        mw = 90 + rng_m.randint(0, 50)
        mh = 28 + rng_m.randint(0, 18)
        mx_pos = mi * (level_w // 20) + rng_m.randint(-20, 20)
        msx = int(mx_pos - cam_x * 0.07)
        mound_far.append((msx, mw, mh))
    ground_far_y = 280
    for msx, mw, mh in mound_far:
        if -mw < msx < SCREEN_W + mw:
            pygame.draw.rect(surface, SERTAO_MOUNT_FAR, (msx - mw // 2, ground_far_y - mh // 2, mw, mh // 2 + 100))
            pygame.draw.ellipse(surface, SERTAO_MOUNT_FAR, (msx - mw // 2, ground_far_y - mh, mw, mh))

    # Camada media
    rng_m2 = random.Random(77)
    mound_mid = []
    for mi in range(18):
        mw = 70 + rng_m2.randint(0, 40)
        mh = 22 + rng_m2.randint(0, 14)
        mx_pos = mi * (level_w // 17) + rng_m2.randint(-15, 15)
        msx = int(mx_pos - cam_x * 0.13)
        mound_mid.append((msx, mw, mh))
    ground_mid_y = 306
    for msx, mw, mh in mound_mid:
        if -mw < msx < SCREEN_W + mw:
            pygame.draw.rect(surface, SERTAO_MOUNT_MID, (msx - mw // 2, ground_mid_y - mh // 2, mw, mh // 2 + 80))
            pygame.draw.ellipse(surface, SERTAO_MOUNT_MID, (msx - mw // 2, ground_mid_y - mh, mw, mh))

    # Camada proxima — menores e mais definidos
    rng_m3 = random.Random(55)
    mound_near = []
    for mi in range(16):
        mw = 55 + rng_m3.randint(0, 30)
        mh = 16 + rng_m3.randint(0, 10)
        mx_pos = mi * (level_w // 15) + rng_m3.randint(-10, 10)
        msx = int(mx_pos - cam_x * 0.19)
        mound_near.append((msx, mw, mh, mi))
    ground_near_y = 326
    for msx, mw, mh, mi in mound_near:
        if -mw < msx < SCREEN_W + mw:
            pygame.draw.rect(surface, SERTAO_MOUNT_NEAR, (msx - mw // 2, ground_near_y - mh // 2, mw, mh // 2 + 60))
            pygame.draw.ellipse(surface, SERTAO_MOUNT_NEAR, (msx - mw // 2, ground_near_y - mh, mw, mh))

    # --- ARVORES VARIADAS ao redor dos montes (parallax 0.19 = mesma camada do monte próximo) ---
    # Posições cobrem 0 a 1110 para que nenhuma árvore desapareça no scroll máximo (~182px de offset)
    rng_tv = random.Random(42)
    tree_positions = [
        0, 58, 116, 174, 232, 290, 348, 406,
        464, 522, 580, 638, 696, 754, 812, 870,
        928, 986, 1044, 1102,
    ]
    # Pré-computa tipo e offset de TODAS as árvores antes de qualquer range check
    _tree_data = [(rng_tv.randint(0, 4), rng_tv.randint(-8, 8)) for _ in tree_positions]
    for i, tx in enumerate(tree_positions):
        sx = int(tx - cam_x * 0.19)
        tv, ty_off = _tree_data[i]
        if -70 < sx < SCREEN_W + 70:
            if tv == 0:
                # Arvoreta com sombra e copa densa — tom sertanejo
                _tc1 = (38, 92, 35)
                _tc2 = (55, 120, 48)
                _tc3 = (72, 145, 60)
                pygame.draw.rect(surface, (105, 68, 30), (sx + 12, 318 + ty_off, 5, 24))
                pygame.draw.ellipse(surface, _tc1, (sx - 4, 290 + ty_off, 38, 30))
                pygame.draw.ellipse(surface, _tc2, (sx, 293 + ty_off, 28, 22))
                pygame.draw.ellipse(surface, _tc3, (sx + 4, 296 + ty_off, 18, 14))
                pygame.draw.ellipse(surface, (25, 60, 22, 80), (sx + 2, 316 + ty_off, 26, 6))
            elif tv == 1:
                # Árvore seca sertaneja — galhos retorcidos com textura
                draw_dry_tree(surface, sx, 336 + ty_off, i % 3)
                pygame.draw.ellipse(surface, (80, 50, 20, 60), (sx + 4, 340 + ty_off, 22, 5))
            elif tv == 2:
                # Carnaúba estilizada — palmeira sertaneja com frondas curvas
                _cx2 = sx + 13
                _cy2 = 310 + ty_off
                pygame.draw.rect(surface, (100, 70, 35), (_cx2 - 2, _cy2, 5, 32))
                pygame.draw.rect(surface, (80, 55, 25), (_cx2 - 1, _cy2 + 8, 3, 22))
                for fi in range(7):
                    fa2 = math.radians(fi * 52 + i * 15 - 20)
                    flen = 20 + (fi % 3) * 4
                    fx2 = _cx2 + int(math.cos(fa2) * flen)
                    fy2 = _cy2 - 4 + int(math.sin(fa2) * 7)
                    pygame.draw.line(surface, (60, 120, 50), (_cx2, _cy2), (fx2, fy2), 2)
                    pygame.draw.ellipse(surface, (48, 105, 42), (fx2 - 5, fy2 - 3, 9, 6))
                pygame.draw.ellipse(surface, (65, 40, 15, 70), (_cx2 - 10, _cy2 + 28, 24, 6))
            elif tv == 3:
                # Arbusto sertanejo volumoso — 3 camadas de tom
                _bx = sx + 2
                _by = 316 + ty_off
                _bw = 32 + (i % 3) * 4
                _bh = 20 + (i % 2) * 4
                pygame.draw.ellipse(surface, (44, 85, 36), (_bx - 4, _by + 4, _bw + 8, _bh - 4))
                pygame.draw.ellipse(surface, (55, 105, 44), (_bx, _by, _bw, _bh))
                pygame.draw.ellipse(surface, (70, 128, 56), (_bx + 4, _by + 2, _bw - 8, _bh - 6))
                pygame.draw.ellipse(surface, (88, 148, 68), (_bx + 8, _by + 4, _bw - 16, _bh - 10))
                pygame.draw.ellipse(surface, (38, 60, 28, 90), (_bx - 2, _by + _bh, _bw + 4, 6))
            else:
                # Cacto de fundo maior e mais detalhado
                draw_cactus(surface, sx + 4, 348, i % 3, 0.72)

    # --- SOLO ARIDO ---
    pygame.draw.rect(surface, SERTAO_GROUND, (0, 348, SCREEN_W, SCREEN_H - 348))
    pygame.draw.rect(surface, SERTAO_GROUND2, (0, 348, SCREEN_W, 8))
    pygame.draw.rect(surface, SERTAO_GROUND3, (0, 362, SCREEN_W, 12))
    pygame.draw.rect(surface, SERTAO_GROUND, (0, 374, SCREEN_W, SCREEN_H - 374))

    # --- DETALHES DO CHAO: pré-computa TODOS os valores fora do range check ---
    # Isso garante que nenhum elemento mude de aparência conforme a câmera move.
    rng_gd = random.Random(17)
    _gd_elems = []
    for i in range(50):
        _gx_w = rng_gd.randint(0, level_w)
        _gy   = 382 + rng_gd.randint(0, 220)
        _gt   = rng_gd.randint(0, 4)
        _r1   = rng_gd.randint(0, 14)   # tamanho / variação
        _r2   = rng_gd.randint(0, 8)    # ângulo / detalhe
        _r3   = rng_gd.randint(0, 1)    # cor alternativa
        _gd_elems.append((_gx_w, _gy, _gt, _r1, _r2, _r3))

    for _gx_w, _gy, _gt, _r1, _r2, _r3 in _gd_elems:
        _gx_s = int(_gx_w - cam_x)
        if -30 < _gx_s < SCREEN_W + 30:
            if _gt == 0:  # grama seca — 3 hastes
                for _gi in range(3):
                    _gh = 4 + (_r1 + _gi) % 5
                    _ga = math.radians((_r2 * 5 + _gi * 30) - 40)
                    pygame.draw.line(surface, (115, 130, 45),
                                     (_gx_s + _gi * 4, _gy),
                                     (_gx_s + _gi * 4 + int(math.sin(_ga) * _gh), _gy - _gh), 1)
            elif _gt == 1:  # arbusto simples
                _bsz = 7 + _r1 % 6
                _bleaf = (85, 98, 40) if _r3 == 0 else (94, 70, 32)
                pygame.draw.rect(surface, (68, 44, 18), (_gx_s + 1, _gy - _bsz, 2, _bsz))
                pygame.draw.ellipse(surface, _bleaf,
                                    (_gx_s - _bsz // 2, _gy - _bsz - 1, _bsz + 3, int(_bsz * 0.55)))
                pygame.draw.ellipse(surface,
                                    (min(255, _bleaf[0]+12), min(255, _bleaf[1]+12), min(255, _bleaf[2]+6)),
                                    (_gx_s, _gy - _bsz - 2, _bsz - 2, int(_bsz * 0.38)))
            elif _gt == 2:  # pedra
                _pw = 6 + _r1 % 9
                _ph = 3 + _r2 % 4
                pygame.draw.ellipse(surface, (144, 128, 104), (_gx_s, _gy - _ph, _pw, _ph))
                pygame.draw.ellipse(surface, (162, 146, 122), (_gx_s + 1, _gy - _ph + 1, _pw - 2, _ph - 1))
            elif _gt == 3:  # mancha de terra
                pygame.draw.ellipse(surface, (150, 116, 70),
                                    (_gx_s - 8, _gy - 2, 16 + _r1 % 8, 4))
            else:  # pedrinha pequena
                pygame.draw.ellipse(surface, (136, 120, 96), (_gx_s, _gy, 4, 2))

    # Rachaduras — todos os valores pré-computados fora do range check
    rng_c = random.Random(33)
    _crack_elems = []
    for i in range(14):
        _cx_w = rng_c.randint(0, level_w - 100)
        _cy_c = 396 + rng_c.randint(0, 48)
        _cl   = rng_c.randint(10, 28)
        _cr1  = rng_c.randint(-4, 4)
        _cr2  = rng_c.randint(-6, 6)
        _crack_elems.append((_cx_w, _cy_c, _cl, _cr1, _cr2))

    for _cx_w, _cy_c, _cl, _cr1, _cr2 in _crack_elems:
        _cx_s = int(_cx_w - cam_x)
        if -30 < _cx_s < SCREEN_W + 30:
            pygame.draw.line(surface, SERTAO_CRACK,
                             (_cx_s, _cy_c), (_cx_s + _cl, _cy_c + _cr1), 1)
            pygame.draw.line(surface, SERTAO_CRACK,
                             (_cx_s + _cl // 2, _cy_c),
                             (_cx_s + _cl // 2 + _cr2, _cy_c + 6), 1)

    # Textura inferior — pedrinhas/manchas, todos os valores pré-computados
    rng_lo = random.Random(88)
    _lo_elems = []
    for i in range(70):
        _lx_w = rng_lo.randint(0, level_w)
        _ly   = 480 + rng_lo.randint(0, 140)
        _ltp  = rng_lo.randint(0, 3)
        _lr1  = rng_lo.randint(0, 12)
        _lr2  = rng_lo.randint(0, 2)
        _lo_elems.append((_lx_w, _ly, _ltp, _lr1, _lr2))

    for _lx_w, _ly, _ltp, _lr1, _lr2 in _lo_elems:
        _lx_s = int(_lx_w - cam_x)
        if -15 < _lx_s < SCREEN_W + 15:
            if _ltp == 0:
                _pw = 3 + _lr1 % 5
                pygame.draw.ellipse(surface, (155, 135, 105), (_lx_s, _ly, _pw, max(2, _pw - 1)))
            elif _ltp == 1:
                pygame.draw.ellipse(surface, (158, 128, 82),
                                    (_lx_s - 8, _ly, 14 + _lr1 % 10, 4))
            elif _ltp == 2:
                _cl2 = 7 + _lr1 % 12
                pygame.draw.line(surface, (144, 114, 68), (_lx_s, _ly),
                                 (_lx_s + _cl2, _ly + _lr2 - 1), 1)
            else:
                pygame.draw.circle(surface, (150, 120, 76), (_lx_s, _ly), 1 + _lr2)

    # --- CERCA (parallax 1.0 — sincronizada com as casas) ---
    for fw in range(0, level_w + 160, 160):
        fs = int(fw - cam_x)
        if -80 < fs < SCREEN_W + 80:
            draw_fence_segment(surface, fs, 466, 60)

    # --- POCOS e VARAIS (parallax 1.0) ---
    for wx_w in [100, 540, 920, 1380]:
        wx_s = int(wx_w - cam_x)
        if -60 < wx_s < SCREEN_W + 60:
            draw_well(surface, wx_s, 462)
    for clx_w in [300, 740, 1160, 1560]:
        clx_s = int(clx_w - cam_x)
        if -100 < clx_s < SCREEN_W + 100:
            draw_clothesline(surface, clx_s, 435, 80)

    # --- PARTICULAS DE POEIRA discretas ---
    rng_dust = random.Random(frame // 18 + 7)
    for di in range(12):
        dx_w = rng_dust.randint(0, SCREEN_W)
        dx_s = dx_w
        if -10 < dx_s < SCREEN_W + 10:
            dust_y = 440 - (frame * 1 + di * 22) % 80
            if dust_y > 360:
                pygame.draw.ellipse(surface, (200, 172, 120),
                                    (dx_s, dust_y, rng_dust.randint(3, 7), rng_dust.randint(2, 4)))

    # --- EFEITO DE CALOR (ondulacao discreta no horizonte) ---
    heat_y = 360
    for hx in range(0, SCREEN_W, 3):
        wave = int(math.sin((hx + frame * 1.8) * 0.06) * 1.5)
        col_h = (210, 175, 115)
        pygame.draw.line(surface, col_h, (hx, heat_y + wave), (hx, heat_y + wave + 2), 1)

    # --- NEBLINA/HAZE no horizonte (mais forte para empurrar montes ao fundo) ---
    haze_surf = pygame.Surface((SCREEN_W, 28), pygame.SRCALPHA)
    for hy in range(28):
        alpha = int(82 * (1.0 - hy / 28.0))
        haze_surf.fill((218, 182, 118, alpha), (0, hy, SCREEN_W, 1))
    surface.blit(haze_surf, (0, 336))


def draw_bg_treatment(surface, frame, cam_x=0, level_w=SCREEN_W):
    """Desenha o fundo da Fase 4: estação de tratamento industrial."""
    surface.fill((50, 55, 65))

    # ── TETO (y = 0-90) — não alterar ─────────────────────────────
    pygame.draw.rect(surface, (70, 75, 85), (0, 0, SCREEN_W, 90))
    pygame.draw.rect(surface, (60, 65, 75), (0, 90, SCREEN_W, 4))
    for ti in range(4):
        tx = int((ti * 260 + 30 - cam_x * 0.2) % (level_w + 400) - 150)
        if -120 < tx < SCREEN_W + 120:
            t_h = 120 + (ti * 37) % 60
            pygame.draw.rect(surface, (60, 90, 120), (tx, 90 - t_h, 90, t_h))
            wl = int(t_h * 0.6 + math.sin(frame * 0.02 + ti) * 5)
            pygame.draw.rect(surface, WATER_DARK, (tx + 3, 90 - wl, 84, wl))
            pygame.draw.rect(surface, WATER_BLUE, (tx + 3, 90 - wl, 84, 12))
            pygame.draw.rect(surface, (40, 60, 90), (tx, 90 - t_h, 90, t_h), 3)
            pygame.draw.rect(surface, (80, 80, 90), (tx + 75, 90 - t_h + 10, 10, 30))
            gauge_fill = int(28 * wl / t_h)
            pygame.draw.rect(surface, (80, 200, 80) if wl > t_h * 0.3 else (200, 80, 80),
                              (tx + 77, 90 - t_h + 38 - gauge_fill, 6, gauge_fill))
    for ph in [30, 55, 72]:
        pygame.draw.rect(surface, PIPE_GRAY, (0, ph, SCREEN_W, 8))
        pygame.draw.rect(surface, PIPE_LIGHT, (0, ph, SCREEN_W, 3))
        pygame.draw.rect(surface, (70, 70, 80), (0, ph, SCREEN_W, 8), 1)
        for px in range(0 - int(cam_x * 0.4) % 120, SCREEN_W + 120, 120):
            pygame.draw.rect(surface, (100, 100, 110), (px, ph - 2, 12, 12), border_radius=2)

    # ── PAREDE INDUSTRIAL (y = 96-495) ────────────────────────────

    # 1. Textura de parede: grade de painéis/tijolos (mais sutil possível)
    _tw, _th = 48, 36
    for _ty in range(96, 496, _th):
        pygame.draw.line(surface, (44, 49, 59), (0, _ty), (SCREEN_W, _ty), 1)
    for _tx in range(-int(cam_x * 0.08) % _tw, SCREEN_W + _tw, _tw):
        pygame.draw.line(surface, (44, 49, 59), (_tx, 96), (_tx, 496), 1)

    # 2. Manchas/sujeira estáticas na parede (posições fixas, não usam random global)
    _stains = [
        (130, 145, 28, 16), (285, 310, 18, 12), (480, 205, 24, 15),
        (660, 375, 16, 10), (810, 145, 20, 13), (940, 290, 26, 17),
        (1095, 425, 14, 9),  (1255, 180, 22, 14), (1375, 350, 18, 11),
        (1510, 245, 24, 16), (1645, 405, 17, 11), (1790, 165, 21, 14),
        (195, 455, 15, 10),  (745, 115, 19, 13),  (1045, 465, 23, 15),
        (1445, 120, 16, 11), (545, 440, 20, 12),  (1315, 480, 18, 11),
    ]
    for _sx, _sy, _sw, _sh in _stains:
        _ssp = int((_sx - cam_x * 0.10) % (level_w + 120) - 60)
        if -40 < _ssp < SCREEN_W + 40:
            pygame.draw.ellipse(surface, (46, 51, 61), (_ssp, _sy, _sw, _sh))

    # 3. Placas de setor no fundo profundo (parallax 0.12)
    _setor_data = [(200, "SETOR 04"), (560, "SETOR 07"), (920, "H₂O"),
                   (1280, "SETOR 02"), (1640, "SETOR 09")]
    for _bx, _blbl in _setor_data:
        _bsp = int((_bx - cam_x * 0.12) % (level_w + 200) - 100)
        if -80 < _bsp < SCREEN_W + 80:
            pygame.draw.rect(surface, (42, 58, 74), (_bsp, 116, 70, 30), border_radius=3)
            pygame.draw.rect(surface, (54, 74, 94), (_bsp, 116, 70, 30), 2, border_radius=3)
            _bt = font_tiny.render(_blbl, True, (110, 150, 185))
            surface.blit(_bt, (_bsp + 35 - _bt.get_width() // 2, 125))

    # 4. Stencil "ÁGUA É VIDA" no fundo (parallax 0.12)
    for _sx2, _soff in [(880, 0), (1600, 0)]:
        _ssp2 = int((_sx2 - cam_x * 0.12) % (level_w + 200) - 100)
        if -100 < _ssp2 < SCREEN_W + 100:
            # ícone gota
            pygame.draw.polygon(surface, (58, 72, 88),
                [(_ssp2 + 14, 192), (_ssp2, 212), (_ssp2 + 28, 212)])
            pygame.draw.circle(surface, (58, 72, 88), (_ssp2 + 14, 216), 11)
            _sv = font_tiny.render("ÁGUA É VIDA", True, (60, 74, 90))
            surface.blit(_sv, (_ssp2, 230))

    # 5. Tubulação principal grossa (parallax 0.22) — y = 158
    _P1Y = 158
    _p1o = int(cam_x * 0.22)
    pygame.draw.rect(surface, (67, 72, 84), (0, _P1Y, SCREEN_W, 16))
    pygame.draw.rect(surface, (82, 88, 100), (0, _P1Y, SCREEN_W, 4))
    pygame.draw.rect(surface, (54, 59, 71), (0, _P1Y + 14, SCREEN_W, 2))
    for _jx in range(-_p1o % 110, SCREEN_W + 110, 110):
        pygame.draw.rect(surface, (84, 90, 102), (_jx - 4, _P1Y - 3, 10, 22), border_radius=2)
        pygame.draw.rect(surface, (64, 69, 81), (_jx - 4, _P1Y - 3, 10, 22), 1, border_radius=2)

    # 6. Tubulação média (parallax 0.25) — y = 248
    _P2Y = 248
    _p2o = int(cam_x * 0.25)
    pygame.draw.rect(surface, (64, 69, 81), (0, _P2Y, SCREEN_W, 10))
    pygame.draw.rect(surface, (78, 84, 96), (0, _P2Y, SCREEN_W, 3))
    pygame.draw.rect(surface, (52, 57, 69), (0, _P2Y + 9, SCREEN_W, 1))
    for _jx in range(-_p2o % 140, SCREEN_W + 140, 140):
        pygame.draw.rect(surface, (80, 86, 98), (_jx - 3, _P2Y - 2, 8, 14), border_radius=2)

    # 7. Tubulação média (parallax 0.28) — y = 340
    _P3Y = 340
    _p3o = int(cam_x * 0.28)
    pygame.draw.rect(surface, (66, 71, 83), (0, _P3Y, SCREEN_W, 12))
    pygame.draw.rect(surface, (80, 86, 98), (0, _P3Y, SCREEN_W, 3))
    pygame.draw.rect(surface, (53, 58, 70), (0, _P3Y + 11, SCREEN_W, 1))
    for _jx in range(-_p3o % 125, SCREEN_W + 125, 125):
        pygame.draw.rect(surface, (82, 88, 100), (_jx - 3, _P3Y - 2, 8, 16), border_radius=2)

    # 8. Tubulação fina (parallax 0.32) — y = 420
    _P4Y = 420
    _p4o = int(cam_x * 0.32)
    pygame.draw.rect(surface, (62, 67, 79), (0, _P4Y, SCREEN_W, 7))
    pygame.draw.rect(surface, (75, 81, 93), (0, _P4Y, SCREEN_W, 2))
    for _jx in range(-_p4o % 175, SCREEN_W + 175, 175):
        pygame.draw.rect(surface, (78, 84, 96), (_jx - 2, _P4Y - 2, 6, 11), border_radius=1)

    # 9. Tubos verticais conectores (parallax 0.22)
    _VERTS = [175, 415, 640, 870, 1105, 1370, 1640]
    for _vx in _VERTS:
        _vs1 = int((_vx - cam_x * 0.22) % (level_w + 80) - 40)
        if -14 < _vs1 < SCREEN_W + 14:
            pygame.draw.rect(surface, (65, 70, 82), (_vs1 - 4, _P1Y + 16, 9, _P2Y - _P1Y - 16))
            pygame.draw.rect(surface, (77, 83, 95), (_vs1 - 4, _P1Y + 16, 3, _P2Y - _P1Y - 16))
        _vs2 = int((_vx + 60 - cam_x * 0.22) % (level_w + 80) - 40)
        if -14 < _vs2 < SCREEN_W + 14:
            pygame.draw.rect(surface, (63, 68, 80), (_vs2 - 3, _P2Y + 10, 7, _P3Y - _P2Y - 10))
            pygame.draw.rect(surface, (75, 81, 93), (_vs2 - 3, _P2Y + 10, 2, _P3Y - _P2Y - 10))
        _vs3 = int((_vx + 30 - cam_x * 0.28) % (level_w + 80) - 40)
        if -14 < _vs3 < SCREEN_W + 14:
            pygame.draw.rect(surface, (61, 66, 78), (_vs3 - 3, _P3Y + 12, 6, _P4Y - _P3Y - 12))
            pygame.draw.rect(surface, (73, 79, 91), (_vs3 - 3, _P3Y + 12, 2, _P4Y - _P3Y - 12))

    # 10. Válvulas nas tubulações (parallax 0.26)
    _VALVE_XS = [270, 510, 755, 1040, 1285, 1525, 1770]
    for _vi, _vvx in enumerate(_VALVE_XS):
        _vsp = int((_vvx - cam_x * 0.26) % (level_w + 100) - 50)
        if -24 < _vsp < SCREEN_W + 24:
            _vvy = [_P1Y, _P2Y, _P3Y][_vi % 3]
            pygame.draw.circle(surface, (76, 81, 95), (_vsp, _vvy + 8), 9)
            pygame.draw.circle(surface, (90, 96, 110), (_vsp, _vvy + 8), 9, 2)
            pygame.draw.circle(surface, (66, 71, 85), (_vsp, _vvy + 8), 5)
            _vc = (88, 58, 52) if _vi % 3 == 0 else (54, 78, 100)
            pygame.draw.circle(surface, _vc, (_vsp, _vvy + 8), 4, 2)
            pygame.draw.line(surface, (63, 68, 80), (_vsp - 9, _vvy + 1), (_vsp + 9, _vvy + 1), 2)
            pygame.draw.line(surface, (63, 68, 80), (_vsp, _vvy - 6), (_vsp, _vvy + 16), 2)

    # 11. Ventoinhas / dutos de ar (parallax 0.28)
    _FAN_XS = [345, 795, 1195, 1695]
    _FAN_Y = 295
    for _fi, _ffx in enumerate(_FAN_XS):
        _fsp = int((_ffx - cam_x * 0.28) % (level_w + 100) - 50)
        if -50 < _fsp < SCREEN_W + 50:
            pygame.draw.circle(surface, (57, 62, 74), (_fsp, _FAN_Y), 22)
            pygame.draw.circle(surface, (71, 77, 89), (_fsp, _FAN_Y), 22, 3)
            pygame.draw.circle(surface, (47, 52, 62), (_fsp, _FAN_Y), 22, 1)
            _fa = frame * 0.06 + _fi * 1.1
            for _bl in range(4):
                _ba = _fa + _bl * math.pi / 2
                _bx1 = int(_fsp + 4 * math.cos(_ba))
                _by1 = int(_FAN_Y + 4 * math.sin(_ba))
                _bx2 = int(_fsp + 18 * math.cos(_ba + 0.45))
                _by2 = int(_FAN_Y + 18 * math.sin(_ba + 0.45))
                pygame.draw.line(surface, (74, 79, 93), (_bx1, _by1), (_bx2, _by2), 4)
            pygame.draw.circle(surface, (80, 86, 100), (_fsp, _FAN_Y), 5)
            pygame.draw.circle(surface, (93, 99, 113), (_fsp, _FAN_Y), 5, 2)
            # Duto
            pygame.draw.rect(surface, (60, 65, 77), (_fsp - 6, _FAN_Y + 22, 12, 16))
            pygame.draw.rect(surface, (70, 75, 87), (_fsp - 6, _FAN_Y + 22, 12, 16), 1)

    # 12. Painéis de controle na parede (parallax 0.30)
    _PANEL_XS = [440, 950, 1435]
    _PANEL_Y = 176
    for _pi2, _ppx in enumerate(_PANEL_XS):
        _psp = int((_ppx - cam_x * 0.30) % (level_w + 100) - 50)
        if -60 < _psp < SCREEN_W + 60:
            pygame.draw.rect(surface, (47, 53, 65), (_psp, _PANEL_Y, 56, 66), border_radius=3)
            pygame.draw.rect(surface, (67, 73, 85), (_psp, _PANEL_Y, 56, 66), 2, border_radius=3)
            _LEDS = [(78, 195, 78), (195, 175, 38), (195, 58, 58)]
            for _li2, _lc in enumerate(_LEDS):
                _on = (frame // 35 + _li2 + _pi2) % 2 == 0
                _dc = _lc if _on else (_lc[0]//4, _lc[1]//4, _lc[2]//4)
                pygame.draw.circle(surface, _dc, (_psp + 11 + _li2 * 14, _PANEL_Y + 12), 4)
                pygame.draw.circle(surface, (78, 83, 95), (_psp + 11 + _li2 * 14, _PANEL_Y + 12), 4, 1)
            pygame.draw.rect(surface, (37, 43, 55), (_psp + 6, _PANEL_Y + 24, 10, 30))
            _bh2 = int(14 + 13 * math.sin(frame * 0.03 + _pi2 * 1.2))
            pygame.draw.rect(surface, (58, 155, 195), (_psp + 7, _PANEL_Y + 24 + 30 - _bh2, 8, _bh2))
            for _dl in range(3):
                pygame.draw.rect(surface, (53, 98, 128),
                                 (_psp + 22, _PANEL_Y + 26 + _dl * 9, 26, 5), border_radius=1)
            for _cx2, _cy2 in [(_psp + 3, _PANEL_Y + 3), (_psp + 51, _PANEL_Y + 3),
                                (_psp + 3, _PANEL_Y + 61), (_psp + 51, _PANEL_Y + 61)]:
                pygame.draw.circle(surface, (60, 66, 78), (_cx2, _cy2), 3)
                pygame.draw.circle(surface, (70, 76, 88), (_cx2, _cy2), 3, 1)

    # 14. Grades/ralos na parede (parallax 0.32)
    _GRATE_DATA = [(310, 205), (720, 370), (1160, 215), (1590, 368)]
    for _grx, _gry in _GRATE_DATA:
        _grsp = int((_grx - cam_x * 0.32) % (level_w + 100) - 50)
        if -45 < _grsp < SCREEN_W + 45:
            pygame.draw.rect(surface, (44, 49, 59), (_grsp, _gry, 34, 26), border_radius=2)
            pygame.draw.rect(surface, (60, 65, 77), (_grsp, _gry, 34, 26), 2, border_radius=2)
            for _gi in range(5):
                pygame.draw.line(surface, (38, 43, 53),
                                 (_grsp + 3 + _gi * 6, _gry + 3),
                                 (_grsp + 3 + _gi * 6, _gry + 23), 2)
            for _gi in range(3):
                pygame.draw.line(surface, (38, 43, 53),
                                 (_grsp + 3, _gry + 5 + _gi * 8),
                                 (_grsp + 31, _gry + 5 + _gi * 8), 1)

    # 15. Luzes de teto (cone sutil + luminária) (parallax 0.36)
    _LIGHT_XS = [220, 555, 820, 1140, 1455, 1745]
    for _li3, _llx in enumerate(_LIGHT_XS):
        _lsp = int((_llx - cam_x * 0.36) % (level_w + 100) - 50)
        if -65 < _lsp < SCREEN_W + 65:
            # Luminária
            pygame.draw.rect(surface, (70, 76, 88), (_lsp - 10, 94, 20, 8), border_radius=2)
            pygame.draw.rect(surface, (98, 106, 120), (_lsp - 8, 96, 16, 4))

    # 16. Luzes de alerta piscantes (parallax 0.36)
    _ALERT_DATA = [(475, 382), (895, 458), (1315, 385), (1695, 460)]
    for _ai, (_aax, _aay) in enumerate(_ALERT_DATA):
        _asp = int((_aax - cam_x * 0.36) % (level_w + 100) - 50)
        if -25 < _asp < SCREEN_W + 25:
            pygame.draw.rect(surface, (60, 65, 77), (_asp - 2, _aay - 20, 4, 20))
            _aon = (frame // 28 + _ai) % 3 != 0
            _ac = (198, 58, 48) if _aon else (78, 23, 18)
            pygame.draw.circle(surface, _ac, (_asp, _aay - 22), 7)
            pygame.draw.circle(surface, (218, 78, 68) if _aon else (88, 33, 28),
                               (_asp, _aay - 22), 7, 2)
            if _aon:
                pygame.draw.circle(surface, (178, 48, 38), (_asp, _aay - 22), 11, 1)

    # ── CHÃO (y = 500-640) — não alterar ──────────────────────────
    pygame.draw.rect(surface, (85, 88, 92), (0, 500, SCREEN_W, 140))
    pygame.draw.rect(surface, (75, 78, 82), (0, 500, SCREEN_W, 4))
    for gx in range(0, SCREEN_W, 40):
        pygame.draw.line(surface, (70, 73, 77), (gx, 500), (gx, 640), 1)
    for gy in range(500, 640, 40):
        pygame.draw.line(surface, (70, 73, 77), (0, gy), (SCREEN_W, gy), 1)
    for ax in range(20 - int(cam_x * 0.5) % 160, SCREEN_W + 160, 160):
        pygame.draw.polygon(surface, YELLOW, [(ax, 520), (ax + 20, 527), (ax, 534)])
    for gx in range(40 - int(cam_x * 0.5) % 200, SCREEN_W + 200, 200):
        pygame.draw.rect(surface, (60, 63, 67), (gx, 502, 30, 14), border_radius=2)
        for gi in range(4):
            pygame.draw.line(surface, (45, 48, 52), (gx + 4 + gi * 6, 504), (gx + 4 + gi * 6, 514), 2)
    for mx in range(0, SCREEN_W, 120):
        pygame.draw.rect(surface, YELLOW, (mx + 20, 505, 60, 3))

    # Água fluindo (borda entre teto e parede)
    flow_offset = (frame * 2) % 30
    for fx in range(-flow_offset, SCREEN_W, 30):
        pygame.draw.ellipse(surface, WATER_BLUE, (fx, 95, 12, 6))
        pygame.draw.ellipse(surface, WATER_LIGHT, (fx + 2, 96, 6, 4))


def draw_phase_select_bg(surface, frame):
    """Desenha o fundo da tela de seleção de fases com gradiente, colinas e água."""
    for y in range(SCREEN_H):
        ratio = y / SCREEN_H
        r = int(50 + 80 * ratio)
        g = int(120 + 80 * ratio)
        b = int(200 - 30 * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_W, y))
    sun_glow = int(5 * math.sin(frame * 0.02))
    pygame.draw.circle(surface, (255, 240, 160), (780, 100), 50 + sun_glow)
    pygame.draw.circle(surface, (255, 250, 200), (780, 100), 38)
    for i, (cx, cy, sz) in enumerate([(60, 40, 1.4), (280, 60, 1.0), (520, 30, 1.2), (770, 55, 0.8), (900, 25, 0.9)]):
        draw_cloud(surface, int((cx - frame * 0.3 * (i * 0.15 + 0.3)) % (SCREEN_W + 300) - 150), cy, sz)

    pts1 = [(0, 350)]
    for mx in range(0, SCREEN_W + 40, 40):
        my = 290 + int(50 * math.sin(mx * 0.005 + 1.5)) + int(30 * math.sin(mx * 0.012))
        pts1.append((mx, my))
    pts1.append((SCREEN_W, 350))
    pygame.draw.polygon(surface, (70, 110, 140), pts1)

    pts2 = [(0, 380)]
    for mx in range(0, SCREEN_W + 40, 30):
        my = 320 + int(40 * math.sin(mx * 0.007 + 0.5)) + int(25 * math.sin(mx * 0.015 + 2))
        pts2.append((mx, my))
    pts2.append((SCREEN_W, 380))
    pygame.draw.polygon(surface, (80, 125, 155), pts2)

    hill_color = (55, 130, 60)
    pts_hill = [(0, 430)]
    for hx in range(0, SCREEN_W + 20, 20):
        hy = 400 + int(20 * math.sin(hx * 0.01 + 1)) + int(10 * math.sin(hx * 0.025 + 2))
        pts_hill.append((hx, hy))
    pts_hill.append((SCREEN_W, 430))
    pygame.draw.polygon(surface, hill_color, pts_hill)

    random.seed(555)
    for _ in range(12):
        tx = random.randint(0, SCREEN_W - 40)
        ty = 390 + int(20 * math.sin(tx * 0.01 + 1)) + int(10 * math.sin(tx * 0.025 + 2)) - 30
        draw_tree(surface, tx, ty, random.randint(0, 3))
    random.seed()

    water_y = 430
    pygame.draw.rect(surface, WATER_DARK, (0, water_y, SCREEN_W, 80))
    for wx in range(0, SCREEN_W, 25):
        wy = water_y + math.sin((wx + frame * 1.5) * 0.025) * 5
        pygame.draw.ellipse(surface, WATER_BLUE, (wx, int(wy), 35, 14))

    pygame.draw.rect(surface, GRASS_GREEN, (0, water_y + 80, SCREEN_W, 15))
    pygame.draw.rect(surface, GRASS_DARK, (0, water_y + 80, SCREEN_W, 4))
    pygame.draw.rect(surface, DIRT_BROWN, (0, water_y + 95, SCREEN_W, SCREEN_H - water_y - 95))


# ============================================================
# HUD
# ============================================================

def draw_hud(surface, lives, max_lives, water, max_water, stars, phase_name, phase_num,
             objective, progress, total, timer_val=None, carrying_count=0, carry_max=0):
    """Desenha a interface HUD no topo da tela com vidas, água, estrelas e objetivos."""
    hud = pygame.Surface((SCREEN_W, 65), pygame.SRCALPHA)
    hud.fill((0, 0, 0, 160))
    surface.blit(hud, (0, 0))
    for i in range(max_lives):
        draw_heart(surface, 12 + i * 26, 6, i < lives)
    draw_water_bar(surface, 160, 6, water, max_water)
    for i in range(3):
        draw_star(surface, 330 + i * 26, 4, i < stars)
    phase_text = font_small.render(f"FASE {phase_num}: {phase_name}", True, WHITE)
    surface.blit(phase_text, (12, 38))
    if timer_val is not None:
        draw_timer(surface, 430, 6, timer_val)
    obj_text = font_small.render(objective, True, YELLOW)
    surface.blit(obj_text, (SCREEN_W - obj_text.get_width() - 12, 8))
    prog_text = font_med.render(f"{progress}/{total}", True, WHITE)
    surface.blit(prog_text, (SCREEN_W - prog_text.get_width() - 12, 32))
    if carry_max > 0:
        carry_txt = font_small.render(f"Carga: {carrying_count}/{carry_max}", True, WATER_BLUE)
        surface.blit(carry_txt, (430, 38))
    # Mute button + pause button
    draw_mute_button(surface)
    draw_pause_button(surface)


# ============================================================
# PLAYER CLASS
# ============================================================

class Player:
    """Classe do jogador — controla posição, física, vidas e estado."""

    def __init__(self, x, y):
        """Inicializa o jogador na posição (x, y) com atributos padrão."""
        self.x = x
        self.y = y
        self.vy = 0
        self.on_ground = True
        self.facing_right = True
        self.frame = 0
        self.moving = False
        self.speed = 3.7
        self.lives = 5
        self.max_lives = 5
        self.initial_lives = 5
        self.water = 100
        self.max_water = 100
        self.carrying = False
        self.invincible = 0
        self.flash = 0
        self.w = 32
        self.h = 62
        self.on_ladder = False
        self.repairing = False
        self.has_grabber = False
        self.carry_count = 0
        self.carry_max = 7

    def update(self, keys, ground_y=520, platforms=None, ladders=None, level_width=SCREEN_W):
        """Atualiza o jogador a cada frame: movimento, física, colisão com plataformas e escadas."""
        self.frame += 1
        self.moving = False
        self.repairing = False

        if self.invincible > 0:
            self.invincible -= 1
            self.flash += 1

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.facing_right = False
            self.moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.facing_right = True
            self.moving = True

        self.on_ladder = False
        if ladders:
            player_rect = pygame.Rect(self.x + 8, self.y + 10, self.w - 16, self.h - 10)
            for ladder in ladders:
                if player_rect.colliderect(ladder.rect):
                    if keys[pygame.K_UP] or keys[pygame.K_w]:
                        self.on_ladder = True
                        self.vy = 0
                        self.y -= 3
                        self.moving = True
                    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        self.on_ladder = True
                        self.vy = 0
                        self.y += 3
                        self.moving = True
                    elif not self.on_ground:
                        self.on_ladder = True
                        self.vy = 0
                    break

        if not self.on_ladder:
            if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
                self.vy = -12
                self.on_ground = False

            self.vy += 0.6
            self.y += self.vy

        self.on_ground = False
        going_down_ladder = self.on_ladder and (keys[pygame.K_DOWN] or keys[pygame.K_s])
        if platforms and not going_down_ladder:
            player_rect = pygame.Rect(self.x + 4, self.y + self.h - 8, self.w - 8, 8)
            for plat in platforms:
                if (player_rect.colliderect(plat.rect) and
                    self.vy >= 0 and
                    self.y + self.h - 8 <= plat.rect.top + 10):
                    self.y = plat.rect.top - self.h
                    self.vy = 0
                    self.on_ground = True
                    break

        if self.y >= ground_y - self.h:
            self.y = ground_y - self.h
            self.vy = 0
            self.on_ground = True

        self.x = max(0, min(level_width - self.w, self.x))

    def draw(self, surface, cam_x=0):
        """Desenha o jogador na tela, considerando a câmera e o efeito de invencibilidade."""
        if self.invincible > 0 and self.flash % 6 < 3:
            return
        sx = self.x - cam_x
        f = self.frame if self.moving else 0
        draw_samuel(surface, sx, self.y, self.facing_right, f, self.carrying, self.repairing, self.has_grabber)

    def rect(self):
        """Retorna o retângulo de colisão do jogador."""
        return pygame.Rect(self.x + 4, self.y + 4, self.w - 8, self.h - 8)

    def hit(self):
        """Aplica dano ao jogador se não estiver invencível. Retorna True se atingido."""
        if self.invincible <= 0:
            self.lives -= 1
            self.invincible = 90
            self.flash = 0
            return True
        return False

    def hearts_lost(self):
        """Retorna quantos corações foram perdidos desde o início da fase."""
        return self.initial_lives - self.lives


# ============================================================
# PLATFORM AND LADDER CLASSES
# ============================================================

class Platform:
    """Plataforma estacionária para o jogador pisar."""

    def __init__(self, x, y, w, h=12):
        """Cria uma plataforma na posição (x, y) com largura w e altura h."""
        self.rect = pygame.Rect(x, y, w, h)
        self.color = CONCRETE_GRAY
        self.dark = (130, 125, 120)

    def draw(self, surface, cam_x=0):
        """Desenha a plataforma com bordas destacadas."""
        r = pygame.Rect(self.rect.x - cam_x, self.rect.y, self.rect.w, self.rect.h)
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, self.dark, r, 2)
        pygame.draw.rect(surface, (180, 175, 170), (r.x, r.y, r.w, 3))


class Ladder:
    """Escada que o jogador pode subir/descer."""

    def __init__(self, x, y, h):
        """Cria uma escada na posição (x, y) com altura h."""
        # Rect estendido 20px acima para detectar jogador em cima da plataforma
        self.rect = pygame.Rect(x - 4, y - 20, 32, h + 20)
        self.x = x
        self.y = y
        self.h = h

    def draw(self, surface, cam_x=0):
        """Desenha a escada com corrimãos e degraus."""
        sx = self.x - cam_x
        pygame.draw.rect(surface, (140, 100, 50), (sx, self.y, 4, self.h))
        pygame.draw.rect(surface, (140, 100, 50), (sx + 20, self.y, 4, self.h))
        for ry in range(self.y + 10, self.y + self.h, 16):
            pygame.draw.rect(surface, (160, 120, 60), (sx + 2, ry, 20, 4))


# ============================================================
# PARTICLE
# ============================================================

class Particle:
    """Partícula simples com física, cor e tempo de vida para efeitos visuais."""

    def __init__(self, x, y, color, vx=0, vy=-2, life=25):
        """Cria uma partícula na posição (x, y) com cor, velocidade e vida útil."""
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx + random.uniform(-2, 2)
        self.vy = vy + random.uniform(-2, 1)
        self.life = life
        self.max_life = life

    def update(self):
        """Atualiza posição e reduz o tempo de vida da partícula."""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08
        self.life -= 1

    def draw(self, surface, cam_x=0):
        """Desenha a partícula com tamanho proporcional à vida restante."""
        if self.life > 0:
            sz = max(1, int(4 * self.life / self.max_life))
            pygame.draw.circle(surface, self.color, (int(self.x - cam_x), int(self.y)), sz)


# ============================================================
# NET PROJECTILE (Phase 1)
# ============================================================

class NetProjectile:
    """Projétil de rede lançado pelo jogador na Fase 1 para capturar lixo."""

    def __init__(self, x, y, target_x, target_y):
        """Cria um projétil que se move de (x, y) em direção a (target_x, target_y)."""
        self.x = float(x)
        self.y = float(y)
        self.target_x = target_x
        self.target_y = target_y
        dx = target_x - x
        dy = target_y - y
        dist = max(1, math.sqrt(dx * dx + dy * dy))
        speed = 8
        self.vx = dx / dist * speed
        self.vy = dy / dist * speed
        self.alive = True
        self.timer = 60

    def update(self):
        """Move o projétil e marca como morto após o tempo limite."""
        self.x += self.vx
        self.y += self.vy
        self.timer -= 1
        if self.timer <= 0:
            self.alive = False

    def draw(self, surface, cam_x=0):
        """Desenha o projétil como um círculo com padrão de rede."""
        sx = int(self.x - cam_x)
        sy = int(self.y)
        # Net shape
        pygame.draw.circle(surface, (200, 200, 210), (sx, sy), 8, 2)
        pygame.draw.line(surface, (180, 180, 190), (sx - 6, sy), (sx + 6, sy), 1)
        pygame.draw.line(surface, (180, 180, 190), (sx, sy - 6), (sx, sy + 6), 1)
        pygame.draw.line(surface, (180, 180, 190), (sx - 4, sy - 4), (sx + 4, sy + 4), 1)
        pygame.draw.line(surface, (180, 180, 190), (sx + 4, sy - 4), (sx - 4, sy + 4), 1)

    def rect(self):
        """Retorna o retângulo de colisão do projétil."""
        return pygame.Rect(self.x - 8, self.y - 8, 16, 16)


# ============================================================
# STAR CALCULATION (lives-based)
# ============================================================

def calc_stars(hearts_lost):
    """Calcula estrelas (1-3) conforme dificuldade e danos recebidos."""
    d = game_state.difficulty
    if d == "dificil":
        # 3★ = 0 dano | 2★ = 1 dano | 1★ = 2+ danos
        if hearts_lost == 0:
            return 3
        elif hearts_lost == 1:
            return 2
        else:
            return 1
    elif d == "media":
        # 3★ = 0-1 dano | 2★ = 2 danos | 1★ = 3+ danos
        if hearts_lost <= 1:
            return 3
        elif hearts_lost <= 2:
            return 2
        else:
            return 1
    else:  # facil
        # 3★ = 0-1 dano | 2★ = 2-3 danos | 1★ = 4+ danos
        if hearts_lost <= 1:
            return 3
        elif hearts_lost <= 3:
            return 2
        else:
            return 1


# ============================================================
# STORY INTRO SCREEN
# ============================================================

def story_intro_screen():
    """Exibe a introdução da história com texto animado (efeito de digitação)."""
    story_text = (
        "A água, que deveria ser um direito básico, tornou-se um recurso escasso.\n"
        "\n"
        "Rios estão poluídos, comunidades inteiras sofrem sem acesso à água potável "
        "e o problema cresce a cada dia.\n"
        "\n"
        "Em meio a esse cenário surge um jovem determinado chamado Samuel, "
        "que se recusa a aceitar essa realidade.\n"
        "\n"
        "Equipado com tecnologia e conhecimento, ele decide agir.\n"
        "\n"
        "Sua missão é enfrentar a poluição, recuperar rios, consertar sistemas de "
        "saneamento e levar água limpa de volta à população.\n"
        "\n"
        "Mas ele não pode fazer isso sozinho.\n"
        "\n"
        "Cada decisão importa. Cada ação pode transformar a cidade.\n"
        "\n"
        "Mais do que salvar a cidade, o objetivo é gerar consciência."
    )

    char_index = 0
    total_chars = len(story_text)
    char_timer = 0
    char_delay = 12
    finished = False
    blink_timer = 0
    last_time = pygame.time.get_ticks()
    intro_frame = 0
    story_font = pygame.font.SysFont('arial', 22)
    prompt_font = pygame.font.SysFont('arial', 20)

    while True:
        current_time = pygame.time.get_ticks()
        dt = current_time - last_time
        last_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_m:
                    toggle_mute()
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
                else:
                    return

        if not finished:
            char_timer += dt
            chars_to_add = int(char_timer / char_delay)
            if chars_to_add > 0:
                char_timer -= chars_to_add * char_delay
                char_index = min(total_chars, char_index + chars_to_add)
                if char_index >= total_chars:
                    finished = True

        blink_timer += dt
        intro_frame += 1

        for gy in range(SCREEN_H):
            ratio = gy / SCREEN_H
            gr = int(10 + 15 * ratio)
            gg = int(15 + 25 * ratio)
            gb = int(30 + 40 * ratio)
            pygame.draw.line(screen, (gr, gg, gb), (0, gy), (SCREEN_W, gy))

        title_txt = "HERO OF WATER"
        ttw = pixel_text_width(title_txt, 3)
        draw_pixel_text(screen, title_txt, SCREEN_W // 2 - ttw // 2, 12, 3, (60, 120, 180), (0, 0, 0))
        draw_water_drop_title(screen, 20, 8, 18, intro_frame)

        for ri in range(5):
            rx = int((ri * 210 + intro_frame * 0.8) % (SCREEN_W + 100)) - 50
            ry = SCREEN_H - 30 + int(math.sin(intro_frame * 0.05 + ri * 1.5) * 4)
            rw = 60 + ri * 10
            rh = 8 + int(math.sin(intro_frame * 0.04 + ri) * 2)
            alpha_color = (40 + ri * 8, 100 + ri * 15, 180 + ri * 10)
            pygame.draw.ellipse(screen, alpha_color, (rx, ry, rw, rh))

        visible_text = story_text[:char_index]
        lines = visible_text.split('\n')
        y_offset = 60
        max_line_width = SCREEN_W - 120
        for line in lines:
            if line.strip() == '':
                y_offset += 14
                continue
            words = line.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + (' ' if current_line else '') + word
                test_surf = story_font.render(test_line, True, WHITE)
                if test_surf.get_width() > max_line_width and current_line:
                    rendered = story_font.render(current_line, True, (220, 230, 245))
                    screen.blit(rendered, (60, y_offset))
                    y_offset += 28
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                rendered = story_font.render(current_line, True, (220, 230, 245))
                screen.blit(rendered, (60, y_offset))
                y_offset += 28

        show_prompt = True
        if finished:
            show_prompt = (blink_timer // 500) % 2 == 0
        if show_prompt:
            label = "Pressione ENTER para continuar" if finished else "ENTER para pular"
            prompt = prompt_font.render(label, True, (150, 180, 220))
            screen.blit(prompt, (SCREEN_W // 2 - prompt.get_width() // 2, SCREEN_H - 60))

        draw_mute_button(screen)
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# DIFFICULTY SCREEN
# ============================================================

def difficulty_screen(music_files):
    """Tela de seleção de dificuldade: Fácil, Médio ou Difícil."""
    play_music(music_files, 'menu')
    btn_back = Button(30, 560, 140, 40, "VOLTAR", BROWN_BTN, BROWN_BTN_H, font=font_med)

    # Cards com layout mais limpo: faixa lateral colorida + texto
    card_w, card_h = 500, 85
    start_y = 210
    spacing = 14
    cards = []
    font_title = font_med
    font_desc = font_tiny

    card_data = [
        ("FÁCIL", "Todas as fases desbloqueadas desde o início", (60, 180, 60), (90, 210, 90), (50, 160, 50), "facil"),
        ("MÉDIA", "Desbloqueia fases em sequência, progresso salvo", (210, 160, 40), (235, 185, 55), (180, 140, 30), "media"),
        ("DIFÍCIL", "Falhar qualquer missão reseta TODO o progresso!", (210, 60, 60), (235, 75, 75), (180, 50, 50), "dificil"),
    ]
    for i, (label, desc, color, hover, border, value) in enumerate(card_data):
        cy = start_y + i * (card_h + spacing)
        cards.append({
            "rect": pygame.Rect(SCREEN_W // 2 - card_w // 2, cy, card_w, card_h),
            "label": label, "desc": desc,
            "color": color, "hover_color": hover, "border": border,
            "icon_color": tuple(min(255, c + 30) for c in color),
            "value": value,
        })

    frame = 0

    while True:
        mouse = pygame.mouse.get_pos()
        btn_back.update(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                if event.key == pygame.K_m:
                    toggle_mute()
            if btn_back.clicked(event):
                return "back"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
                for c in cards:
                    if c["rect"].collidepoint(event.pos):
                        return c["value"]

        frame += 1

        # Fundo gradiente + água + terra
        draw_sky_gradient(screen, (25, 70, 130), (70, 140, 170), SCREEN_H)
        pygame.draw.rect(screen, WATER_DARK, (0, SCREEN_H - 140, SCREEN_W, 140))
        for wx in range(0, SCREEN_W, 30):
            wy = SCREEN_H - 140 + math.sin((wx + frame * 1.5) * 0.03) * 6
            pygame.draw.ellipse(screen, WATER_BLUE, (wx, int(wy), 35, 12))
        pygame.draw.rect(screen, DIRT_BROWN, (0, SCREEN_H - 30, SCREEN_W, 30))
        pygame.draw.rect(screen, GRASS_GREEN, (0, SCREEN_H - 34, SCREEN_W, 6))

        # Nuvens
        for i, (cx, cy, sz) in enumerate([(80, 35, 1.0), (400, 65, 0.7), (750, 25, 0.9)]):
            ox = int((cx - frame * 0.2 * (i * 0.2 + 0.3)) % (SCREEN_W + 200) - 100)
            draw_cloud(screen, ox, cy, sz)

        # Título com sublinhado
        title = font_title.render("SELECIONE A DIFICULDADE", True, WHITE)
        title_shadow = font_title.render("SELECIONE A DIFICULDADE", True, (0, 0, 0))
        screen.blit(title_shadow, (SCREEN_W // 2 - title.get_width() // 2 + 2, 22))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 20))
        pygame.draw.line(screen, WATER_BLUE, (SCREEN_W // 2 - 120, 55), (SCREEN_W // 2 + 120, 55), 2)

        sub = font_small.render("O nível de dificuldade define como o progresso é gerenciado:", True, WATER_LIGHT)
        screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 75))

        # Desenha os cards
        for c in cards:
            rect = c["rect"]
            hovered = rect.collidepoint(mouse)
            main_color = c["hover_color"] if hovered else c["color"]

            # Sombra
            pygame.draw.rect(screen, (0, 0, 0, 60), (rect.x + 3, rect.y + 3, rect.w, rect.h), border_radius=8)

            # Faixa lateral esquerda (60px) — cor sólida
            bar_rect = pygame.Rect(rect.x, rect.y, 60, rect.h)
            pygame.draw.rect(screen, c["border"], bar_rect, border_radius=8)
            pygame.draw.rect(screen, c["border"], bar_rect, border_radius=8)
            # Preenche a faixa sem cantos arredondados extras
            fill_rect = pygame.Rect(rect.x + 2, rect.y, 56, rect.h)

            # Fundo branco principal
            white_bg = pygame.Rect(rect.x + 60, rect.y, rect.w - 60, rect.h)
            pygame.draw.rect(screen, (245, 245, 250), white_bg, border_radius=8)
            bg_color = (235, 245, 235) if hovered else (245, 245, 250)
            if hovered:
                bg_color = tuple(min(255, c + 10) for c in bg_color)
            pygame.draw.rect(screen, bg_color, white_bg, border_radius=8)

            # Borda geral
            border_c = GOLD if hovered else (200, 200, 210)
            bw = 3 if hovered else 2
            pygame.draw.rect(screen, border_c, rect, bw, border_radius=8)

            # Círculo/indicador na faixa lateral
            cx = rect.x + 30
            cy = rect.y + rect.h // 2
            pygame.draw.circle(screen, WHITE, (cx, cy), 14)
            pygame.draw.circle(screen, c["icon_color"], (cx, cy), 11)
            # Letra inicial dentro do círculo
            letter = c["label"][0]
            l_surf = font_med.render(letter, True, WHITE)
            screen.blit(l_surf, (cx - l_surf.get_width() // 2, cy - l_surf.get_height() // 2))

            # Nome da dificuldade
            label_surf = font_title.render(c["label"], True, c["border"])
            screen.blit(label_surf, (rect.x + 72, rect.y + 10))

            # Descrição
            desc_surf = font_desc.render(c["desc"], True, (80, 80, 90))
            screen.blit(desc_surf, (rect.x + 72, rect.y + 42))

            # Indicador de clique no hover
            if hovered:
                arrow = font_tiny.render("▶ SELECIONAR", True, c["border"])
                screen.blit(arrow, (rect.right - arrow.get_width() - 12, rect.y + rect.h // 2 - 8))

        btn_back.draw(screen)
        draw_mute_button(screen)
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# TITLE SCREEN
# ============================================================

def title_screen(music_files):
    """Tela inicial do jogo com título animado e botões Jogar / Instruções."""
    play_music(music_files, 'menu')
    has_progress = game_state.progress() > 0

    if has_progress:
        btn_play = Button(SCREEN_W // 2 - 110, 370, 220, 48, "NOVO JOGO", GREEN_BTN, GREEN_BTN_H, font=font_med)
        btn_cont = Button(SCREEN_W // 2 - 110, 425, 220, 48, "CONTINUAR", (40, 120, 190), (60, 145, 220), font=font_med)
        btn_inst = Button(SCREEN_W // 2 - 110, 480, 220, 40, "INSTRUÇÕES", BROWN_BTN, BROWN_BTN_H, font=font_med)
        btn_story = Button(SCREEN_W // 2 - 110, 527, 220, 40, "HISTÓRIA", (70, 100, 160), (90, 120, 190), font=font_med)
        btn_credits = Button(SCREEN_W // 2 - 110, 574, 220, 36, "CRÉDITOS", (80, 80, 100), (100, 100, 120), font=font_small)
    else:
        btn_play = Button(SCREEN_W // 2 - 110, 410, 220, 55, "JOGAR", GREEN_BTN, GREEN_BTN_H)
        btn_cont = None
        btn_inst = Button(SCREEN_W // 2 - 110, 475, 220, 45, "INSTRUÇÕES", BROWN_BTN, BROWN_BTN_H, font=font_med)
        btn_story = Button(SCREEN_W // 2 - 110, 530, 220, 45, "HISTÓRIA", (70, 100, 160), (90, 120, 190), font=font_med)
        btn_credits = Button(SCREEN_W // 2 - 110, 585, 220, 40, "CRÉDITOS", (80, 80, 100), (100, 100, 120), font=font_small)

    ODS_BTN_X = SCREEN_W - 88   # posição fixa do botão ODS6
    ODS_BTN_Y = SCREEN_H - 100
    ODS_BTN_SZ = 52
    ods_rect = pygame.Rect(ODS_BTN_X - 4, ODS_BTN_Y - 4, ODS_BTN_SZ + 8, ODS_BTN_SZ + 28)
    settings_rect = pygame.Rect(SCREEN_W - 80, 10, 28, 28)  # Botão de configurações
    frame = 0

    while True:
        mouse = pygame.mouse.get_pos()
        btn_play.update(mouse)
        if btn_cont:
            btn_cont.update(mouse)
        btn_inst.update(mouse)
        btn_story.update(mouse)
        btn_credits.update(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "play"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_m:
                    toggle_mute()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
                elif settings_rect.collidepoint(event.pos):
                    settings_screen()
                elif ods_rect.collidepoint(event.pos):
                    ods6_info_screen()
            if btn_play.clicked(event):
                return "play"
            if btn_cont and btn_cont.clicked(event):
                return "continue"
            if btn_inst.clicked(event):
                return "instructions"
            if btn_story.clicked(event):
                return "story"
            if btn_credits.clicked(event):
                credits_screen()

        frame += 1
        draw_sky_gradient(screen, (60, 130, 200), (120, 180, 210), 400)

        for i, (cx, cy, sz) in enumerate([(80, 30, 1.3), (350, 55, 0.9), (650, 20, 1.1), (850, 50, 0.7)]):
            draw_cloud(screen, int((cx - frame * 0.3) % (SCREEN_W + 300) - 150), cy, sz)

        random.seed(77)
        for i in range(8):
            bx = i * 130 + random.randint(-10, 10)
            bw = 60 + random.randint(0, 40)
            bh = 80 + random.randint(0, 80)
            by = 370 - bh
            pygame.draw.rect(screen, (140, 150, 165), (bx, by, bw, bh))
            for wy in range(by + 8, by + bh - 10, 18):
                for wx in range(bx + 6, bx + bw - 12, 16):
                    pygame.draw.rect(screen, (180, 210, 230), (wx, wy, 8, 10))
        random.seed()

        pygame.draw.rect(screen, WATER_DARK, (0, 370, SCREEN_W, 100))
        for wx in range(0, SCREEN_W, 22):
            wy = 370 + math.sin((wx + frame * 2) * 0.02) * 6
            pygame.draw.ellipse(screen, WATER_BLUE, (wx, int(wy), 30, 12))

        pygame.draw.rect(screen, DIRT_BROWN, (0, 470, SCREEN_W, 170))

        title_y = int(40 + math.sin(frame * 0.03) * 5)
        small_scale = 4
        text1 = "HERO OF"
        tw1 = pixel_text_width(text1, small_scale)
        text1_x = SCREEN_W // 2 - tw1 // 2
        draw_pixel_text(screen, text1, text1_x, title_y, small_scale, (220, 235, 255), (0, 0, 0))
        draw_water_drop_title(screen, text1_x - 40, title_y - 2, 24, frame)

        big_scale = 10
        glow = int(200 + 55 * math.sin(frame * 0.05))
        text2 = "WATER"
        tw2 = pixel_text_width(text2, big_scale)
        water_text_x = SCREEN_W // 2 - tw2 // 2
        water_text_y = title_y + small_scale * 5 + 12
        draw_pixel_text(screen, text2, water_text_x, water_text_y, big_scale, (80, 170, glow), (0, 0, 0))
        draw_water_drop_title(screen, water_text_x + tw2 + 10, water_text_y + 10, 28, frame)

        samuel_y = 160 + int(math.sin(frame * 0.04) * 5)
        draw_samuel_hero(screen, SCREEN_W // 2 - 40, samuel_y, frame)

        # Botão ODS6 — posição fixa coincidindo com ods_rect para o clique funcionar
        draw_ods6_symbol(screen, ODS_BTN_X, ODS_BTN_Y, ODS_BTN_SZ)
        hint_font = pygame.font.SysFont('arial', 14, bold=True)
        ods_lbl = hint_font.render("ODS 6 — clique", True, WHITE)
        ods_lbl_sh = hint_font.render("ODS 6 — clique", True, (20, 40, 80))
        lbl_x = ODS_BTN_X + ODS_BTN_SZ // 2 - ods_lbl.get_width() // 2
        lbl_y = ODS_BTN_Y + ODS_BTN_SZ + 4
        screen.blit(ods_lbl_sh, (lbl_x + 1, lbl_y + 1))
        screen.blit(ods_lbl, (lbl_x, lbl_y))

        btn_play.draw(screen)
        if btn_cont:
            btn_cont.draw(screen)
        btn_inst.draw(screen)
        btn_story.draw(screen)
        btn_credits.draw(screen)
        draw_mute_button(screen)
        # Ícone de engrenagem (configurações)
        gx, gy = SCREEN_W - 80, 10
        pygame.draw.circle(screen, (150, 170, 190), (gx + 14, gy + 14), 10, 2)
        pygame.draw.circle(screen, (150, 170, 190), (gx + 14, gy + 14), 4)
        for ang in range(0, 360, 45):
            rx = int(gx + 14 + 10 * math.cos(math.radians(ang)))
            ry = int(gy + 14 + 10 * math.sin(math.radians(ang)))
            pygame.draw.circle(screen, (150, 170, 190), (rx, ry), 2)

        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# INSTRUCTIONS SCREEN (animated, polished)
# ============================================================

def instructions_screen():
    """Tela de instruções com controles, objetivos e sistema de estrelas."""
    btn_back = Button(SCREEN_W // 2 - 100, 565, 200, 45, "VOLTAR", BROWN_BTN, BROWN_BTN_H, font=font_med)
    frame = 0

    while True:
        mouse = pygame.mouse.get_pos()
        btn_back.update(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_m:
                    toggle_mute()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
            if btn_back.clicked(event):
                return

        frame += 1

        # Animated background gradient
        shift = int(math.sin(frame * 0.01) * 10)
        for y in range(SCREEN_H):
            ratio = y / SCREEN_H
            r = int(15 + 20 * ratio + shift)
            g = int(25 + 35 * ratio)
            b = int(50 + 40 * ratio - shift)
            r = max(0, min(255, r))
            b = max(0, min(255, b))
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_W, y))

        # Animated water ripples at bottom
        for ri in range(8):
            rx = int((ri * 140 + frame * 0.6) % (SCREEN_W + 100)) - 50
            ry = SCREEN_H - 20 + int(math.sin(frame * 0.04 + ri * 1.2) * 3)
            pygame.draw.ellipse(screen, (30, 80, 140), (rx, ry, 80, 10))

        # Title with decoration
        title = font_title.render("INSTRUÇÕES", True, WATER_BLUE)
        title_shadow = font_title.render("INSTRUÇÕES", True, (0, 0, 0))
        screen.blit(title_shadow, (SCREEN_W // 2 - title.get_width() // 2 + 2, 22))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 20))

        # Decorative water drops around title
        draw_water_drop_title(screen, 60, 15, 16, frame)
        draw_water_drop_title(screen, SCREEN_W - 80, 15, 16, frame + 30)

        # Samuel demonstrating - animated walking
        sam_x = 60 + int(math.sin(frame * 0.03) * 20)
        sam_face = frame % 120 < 60
        draw_samuel(screen, sam_x, 75, sam_face, frame)

        # Control section with icons
        section_y = 90
        sections = [
            ("CONTROLES", YELLOW, [
                ("Setas / WASD", "Mover Samuel", (100, 180, 255)),
                ("Espaço / W / Seta cima", "Pular", (100, 180, 255)),
                ("E", "Interagir (coletar, consertar, entregar)", (100, 180, 255)),
                ("Clique direito / F (Fase 1)", "Lançar rede para lixo distante", (100, 180, 255)),
                ("M", "Mutar/desmutar som", (100, 180, 255)),
                ("ESC", "Menu / Sair", (100, 180, 255)),
            ]),
            ("OBJETIVO", GOLD, [
                ("", "Samuel precisa salvar a cidade da crise hídrica!", WHITE),
                ("", "Complete as 5 fases para restaurar a água limpa.", WHITE),
            ]),
            ("SISTEMA DE ESTRELAS", STAR_YELLOW, [
                ("3 Estrelas", "Perdeu no máximo 1 coração", GREEN_OK),
                ("2 Estrelas", "Perdeu no máximo 2 corações", YELLOW),
                ("1 Estrela", "Completou a fase (3+ corações perdidos)", ORANGE),
            ]),
            ("ATENÇÃO", RED, [
                ("", "Dificuldade Difícil: falhar uma missão reseta tudo!", (255, 120, 120)),
            ]),
        ]

        y_pos = section_y
        for sec_title, sec_color, items in sections:
            # Section header with line
            header = font_med.render(sec_title, True, sec_color)
            screen.blit(header, (160, y_pos))
            pygame.draw.line(screen, sec_color, (160, y_pos + 28), (SCREEN_W - 60, y_pos + 28), 1)
            y_pos += 34
            for key, desc, color in items:
                if key:
                    # Key box
                    key_surf = font_tiny.render(key, True, WHITE)
                    kw = key_surf.get_width() + 12
                    pygame.draw.rect(screen, (40, 50, 70), (170, y_pos, kw, 22), border_radius=4)
                    pygame.draw.rect(screen, (80, 90, 110), (170, y_pos, kw, 22), 1, border_radius=4)
                    screen.blit(key_surf, (176, y_pos + 3))
                    # Description
                    desc_surf = font_tiny.render(desc, True, color)
                    screen.blit(desc_surf, (180 + kw + 8, y_pos + 3))
                else:
                    desc_surf = font_small.render(desc, True, color)
                    screen.blit(desc_surf, (170, y_pos))
                y_pos += 24
            y_pos += 6

        # ODS 6 badge
        draw_ods6_symbol(screen, SCREEN_W - 70, 90, 40)

        btn_back.draw(screen)
        draw_mute_button(screen)
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# ODS 6 INFO SCREEN
# ============================================================

def ods6_info_screen():
    """Tela informativa sobre o ODS 6 (Água Potável e Saneamento)."""
    btn_back = Button(SCREEN_W // 2 - 100, 565, 200, 45, "VOLTAR", BROWN_BTN, BROWN_BTN_H, font=font_med)
    frame = 0

    info_lines = [
        ("O que é a ODS 6?", WATER_BLUE, [
            "A ODS 6 (Objetivo de Desenvolvimento Sustentável 6) faz parte da",
            "Agenda 2030 da ONU e tem como foco garantir a disponibilidade",
            "e gestão sustentável da água potável e saneamento para todos.",
        ]),
        ("Metas principais até 2030:", YELLOW, [
            "• Alcançar o acesso universal e equitativo à água potável",
            "• Alcançar o acesso a saneamento e higiene adequados",
            "• Melhorar a qualidade da água reduzindo a poluição",
            "• Aumentar a eficiência do uso da água em todos os setores",
            "• Proteger e restaurar ecossistemas relacionados à água",
        ]),
        ("Situação atual no mundo:", GOLD, [
            "• 2,2 bilhões de pessoas não têm acesso à água potável",
            "• 3,5 bilhões de pessoas vivem sem saneamento seguro",
            "• A cada minuto, uma criança morre de doenças relacionadas",
            "  à água contaminada e falta de saneamento básico",
        ]),
        ("Como você pode ajudar:", GREEN_OK, [
            "• Economize água no dia a dia (banho, escovação, etc.)",
            "• Não descarte lixo em rios, lagos ou praias",
            "• Cobrar do poder público investimentos em saneamento",
            "• Compartilhar informações sobre a importância da água",
        ]),
    ]

    while True:
        mouse = pygame.mouse.get_pos()
        btn_back.update(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_m:
                    toggle_mute()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
            if btn_back.clicked(event):
                return

        frame += 1

        # Background gradient
        for y in range(SCREEN_H):
            ratio = y / SCREEN_H
            gr = int(10 + 20 * ratio)
            gg = int(20 + 35 * ratio)
            gb = int(40 + 50 * ratio)
            pygame.draw.line(screen, (gr, gg, gb), (0, y), (SCREEN_W, y))

        # Water drop decorations
        draw_water_drop_title(screen, 30, 15, 20, frame)
        draw_water_drop_title(screen, SCREEN_W - 60, 15, 20, frame + 25)

        # Title
        title = font_title.render("ODS 6: ÁGUA POTÁVEL", True, WATER_BLUE)
        title_shadow = font_title.render("ODS 6: ÁGUA POTÁVEL", True, (0, 0, 0))
        screen.blit(title_shadow, (SCREEN_W // 2 - title.get_width() // 2 + 2, 22))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 20))
        sub = font_med.render("E SANEAMENTO", True, WATER_LIGHT)
        screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 70))

        draw_ods6_symbol(screen, SCREEN_W - 60, SCREEN_H - 80, 35)

        # Sections
        y_pos = 110
        for sec_title, sec_color, lines_list in info_lines:
            header = font_med.render(sec_title, True, sec_color)
            screen.blit(header, (50, y_pos))
            y_pos += 28
            for line in lines_list:
                line_surf = font_tiny.render(line, True, (200, 210, 220))
                screen.blit(line_surf, (60, y_pos))
                y_pos += 20
            y_pos += 8

        btn_back.draw(screen)
        draw_mute_button(screen)
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# CREDITS SCREEN
# ============================================================

def credits_screen():
    """Tela de créditos com a equipe de desenvolvimento."""
    btn_back = Button(SCREEN_W // 2 - 100, 565, 200, 45, "VOLTAR", BROWN_BTN, BROWN_BTN_H, font=font_med)
    frame = 0

    credits_data = [
        ("HERO OF WATER v5.0", TITLE_BLUE, True),
        ("", WHITE, False),
        ("Um jogo educativo sobre a ODS 6", WATER_LIGHT, False),
        ("Água Limpa e Saneamento", WATER_BLUE, False),
        ("", WHITE, False),
        ("DESENVOLVEDORES", YELLOW, True),
        ("Filipe Henry", WHITE, False),
        ("André de Lira", WHITE, False),
        ("Júlio Sérgio", WHITE, False),
        ("João Victor", WHITE, False),
        ("", WHITE, False),
        ("TURMA", YELLOW, True),
        ("Análise e Desenvolvimento de Sistemas - ADS 2026", WATER_LIGHT, False),
        ("", WHITE, False),
        ("AGRADECIMENTOS ESPECIAIS", YELLOW, True),
        ("A todos que acreditam que a água é um direito", WATER_LIGHT, False),
        ("de todos e que podemos fazer a diferença!", WATER_LIGHT, False),
        ("", WHITE, False),
        ("ODS 6 - Água Potável e Saneamento para Todos", GREEN_OK, False),
    ]

    while True:
        mouse = pygame.mouse.get_pos()
        btn_back.update(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_m:
                    toggle_mute()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
            if btn_back.clicked(event):
                return

        frame += 1

        # Background com gradiente escuro e estrelas decorativas
        for y in range(SCREEN_H):
            ratio = y / SCREEN_H
            gr = int(5 + 10 * ratio)
            gg = int(8 + 15 * ratio)
            gb = int(20 + 30 * ratio)
            pygame.draw.line(screen, (gr, gg, gb), (0, y), (SCREEN_W, y))

        # Estrelas cintilantes
        random.seed(42)
        for _ in range(40):
            sx = (random.randint(0, SCREEN_W) + frame) % SCREEN_W
            sy = (random.randint(0, SCREEN_H) + frame) % SCREEN_H
            brightness = int(150 + 105 * math.sin(frame * 0.02 + sx * 0.1 + sy * 0.1))
            pygame.draw.circle(screen, (brightness, brightness, brightness), (sx, sy), 1)
        random.seed()

        # Título
        title = font_big.render("CRÉDITOS", True, GOLD)
        title_shadow = font_big.render("CRÉDITOS", True, (0, 0, 0))
        screen.blit(title_shadow, (SCREEN_W // 2 - title.get_width() // 2 + 2, 22))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 20))

        # Gota decorativa
        draw_water_drop_title(screen, 50, 15, 16, frame)
        draw_water_drop_title(screen, SCREEN_W - 80, 15, 16, frame + 30)

        # Lista de créditos
        y_pos = 90
        for text, color, is_header in credits_data:
            if text == "":
                y_pos += 14
                continue
            if is_header:
                surf = font_med.render(text, True, color)
            else:
                surf = font_small.render(text, True, color)
            screen.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2, y_pos))
            y_pos += 28 if is_header else 22

        btn_back.draw(screen)
        draw_mute_button(screen)
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# SETTINGS SCREEN (volume control)
# ============================================================

def settings_screen():
    """Tela de configurações com controle deslizante de volume."""
    btn_back = Button(SCREEN_W // 2 - 100, 530, 200, 45, "VOLTAR", BROWN_BTN, BROWN_BTN_H, font=font_med)

    slider_x = SCREEN_W // 2 - 150
    slider_y = 280
    slider_w = 300
    slider_h = 12
    knob_r = 16

    frame = 0
    dragging = False

    while True:
        mouse = pygame.mouse.get_pos()
        btn_back.update(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_m:
                    toggle_mute()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
                else:
                    knob_x = slider_x + int(audio_volume * slider_w)
                    knob_rect = pygame.Rect(knob_x - knob_r, slider_y - knob_r, knob_r * 2, knob_r * 2)
                    if knob_rect.collidepoint(event.pos) or pygame.Rect(slider_x, slider_y - 8, slider_w, slider_h + 16).collidepoint(event.pos):
                        dragging = True
                        new_vol = (event.pos[0] - slider_x) / slider_w
                        set_volume(new_vol)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            if event.type == pygame.MOUSEMOTION and dragging:
                new_vol = (event.pos[0] - slider_x) / slider_w
                set_volume(new_vol)
            if btn_back.clicked(event):
                return

        frame += 1

        # Background gradiente escuro
        for y in range(SCREEN_H):
            ratio = y / SCREEN_H
            gr = int(10 + 15 * ratio)
            gg = int(15 + 20 * ratio)
            gb = int(30 + 35 * ratio)
            pygame.draw.line(screen, (gr, gg, gb), (0, y), (SCREEN_W, y))

        # Partículas decorativas
        random.seed(99)
        for _ in range(30):
            sx = (random.randint(0, SCREEN_W) + frame * 0.2) % SCREEN_W
            sy = (random.randint(0, SCREEN_H) + frame * 0.1) % SCREEN_H
            alpha = max(0, min(255, int(100 + 155 * math.sin(frame * 0.015 + sx * 0.05 + sy * 0.07))))
            pygame.draw.circle(screen, (alpha // 2, alpha // 2, alpha), (int(sx), int(sy)), 1)
        random.seed()

        # Título
        title = font_title.render("CONFIGURAÇÕES", True, WATER_BLUE)
        title_shadow = font_title.render("CONFIGURAÇÕES", True, (0, 0, 0))
        screen.blit(title_shadow, (SCREEN_W // 2 - title.get_width() // 2 + 2, 32))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 30))

        # Linha decorativa
        pygame.draw.line(screen, WATER_BLUE, (SCREEN_W // 2 - 120, 82), (SCREEN_W // 2 + 120, 82), 2)

        # Rótulo do volume
        vol_label = font_big.render("VOLUME", True, (200, 220, 240))
        screen.blit(vol_label, (SCREEN_W // 2 - vol_label.get_width() // 2, 200))

        # Slider track (fundo escuro)
        track_rect = pygame.Rect(slider_x, slider_y, slider_w, slider_h)
        pygame.draw.rect(screen, (40, 45, 60), track_rect, border_radius=slider_h // 2)

        # Slider fill (parte preenchida até o knob)
        fill_w = int(audio_volume * slider_w)
        if fill_w > 0:
            fill_rect = pygame.Rect(slider_x, slider_y, fill_w, slider_h)
            pygame.draw.rect(screen, WATER_BLUE, fill_rect, border_radius=slider_h // 2)

        # Knob
        knob_x = slider_x + int(audio_volume * slider_w)
        knob_center = (knob_x, slider_y + slider_h // 2)
        pygame.draw.circle(screen, (60, 70, 85), knob_center, knob_r + 3)  # sombra
        knob_color = (140, 210, 255) if pygame.Rect(knob_x - knob_r, slider_y - knob_r, knob_r * 2, knob_r * 2).collidepoint(mouse) else WHITE
        pygame.draw.circle(screen, knob_color, knob_center, knob_r)
        pygame.draw.circle(screen, (100, 160, 200), knob_center, knob_r, 2)

        # Texto de porcentagem
        pct = int(audio_volume * 100)
        pct_text = font_med.render(f"{pct}%", True, WATER_LIGHT)
        screen.blit(pct_text, (SCREEN_W // 2 - pct_text.get_width() // 2, slider_y + 40))

        # Indicador de mute
        mute_label = font_small.render(f"{'MUTADO' if audio_muted else 'MUTAR'}: clique no alto-falante", True, (150, 170, 190))
        screen.blit(mute_label, (SCREEN_W // 2 - mute_label.get_width() // 2, 430))

        btn_back.draw(screen)
        draw_mute_button(screen)

        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# PHASE SELECT SCREEN
# ============================================================

def phase_select_screen():
    """Tela de seleção de fases com cards, estrelas e progresso."""
    btn_back = Button(30, 560, 140, 40, "VOLTAR", BROWN_BTN, BROWN_BTN_H, font=font_med)
    phase_names = ["Canal do Recife", "Bairro Precario", "Agua p/ Todos",
                   "Est. Tratamento"]
    phase_colors = [PHASE_CARD_1, PHASE_CARD_2, PHASE_CARD_3, PHASE_CARD_4]

    phase_buttons = []
    card_w, card_h = 190, 180
    total_w = 4 * card_w + 3 * 20
    start_x = (SCREEN_W - total_w) // 2
    for i in range(4):
        bx = start_x + i * (card_w + 20)
        by = 220
        phase_buttons.append(pygame.Rect(bx, by, card_w, card_h))

    frame = 0

    while True:
        mouse = pygame.mouse.get_pos()
        btn_back.update(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                if event.key == pygame.K_m:
                    toggle_mute()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
            if btn_back.clicked(event):
                return "back"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(phase_buttons):
                    if rect.collidepoint(event.pos) and game_state.unlocked[i]:
                        return i

        frame += 1
        draw_phase_select_bg(screen, frame)

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 60))
        screen.blit(overlay, (0, 0))

        title = font_title.render("ESCOLHA A FASE", True, WHITE)
        title_shadow = font_title.render("ESCOLHA A FASE", True, (0, 0, 0))
        screen.blit(title_shadow, (SCREEN_W // 2 - title.get_width() // 2 + 2, 32))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 30))

        total_stars = game_state.total_stars()
        progress = game_state.progress()

        draw_star(screen, 240, 95, True)
        stars_txt = font_med.render(f"Estrelas: {total_stars}/12", True, GOLD)
        screen.blit(stars_txt, (268, 92))
        prog_txt = font_med.render(f"Progresso: {progress}%", True, WHITE)
        screen.blit(prog_txt, (520, 92))

        bar_x, bar_y, bar_w = 240, 130, 480
        pygame.draw.rect(screen, (40, 45, 55), (bar_x, bar_y, bar_w, 14), border_radius=7)
        fill = int(bar_w * progress / 100)
        if fill > 0:
            pygame.draw.rect(screen, GREEN_OK, (bar_x, bar_y, fill, 14), border_radius=7)

        for i, rect in enumerate(phase_buttons):
            unlocked = game_state.unlocked[i]
            hovered = unlocked and rect.collidepoint(mouse)
            color = phase_colors[i] if unlocked else PHASE_CARD_LOCKED
            if hovered:
                color = tuple(min(255, c + 25) for c in color)

            pygame.draw.rect(screen, (0, 0, 0), (rect.x + 4, rect.y + 4, rect.w, rect.h), border_radius=10)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            border_c = GOLD if hovered else tuple(max(0, c - 30) for c in color)
            pygame.draw.rect(screen, border_c, rect, 3, border_radius=10)

            num = font_big.render(str(i + 1), True, WHITE if unlocked else (80, 80, 85))
            screen.blit(num, (rect.centerx - num.get_width() // 2, rect.y + 15))

            if unlocked:
                name = font_tiny.render(phase_names[i], True, WHITE)
                screen.blit(name, (rect.centerx - name.get_width() // 2, rect.y + 60))
                for s in range(3):
                    sx = rect.centerx - 36 + s * 26
                    draw_star(screen, sx, rect.y + 90, s < game_state.stars[i])
                descs = ["Limpeza de rios", "Consertar canos", "Distribuir agua",
                         "Puzzles tratamento"]
                desc = font_tiny.render(descs[i], True, (200, 210, 220))
                screen.blit(desc, (rect.centerx - desc.get_width() // 2, rect.y + 130))
            else:
                lx, ly = rect.centerx, rect.y + 90
                pygame.draw.rect(screen, (90, 90, 95), (lx - 15, ly, 30, 25), border_radius=4)
                pygame.draw.arc(screen, (90, 90, 95), (lx - 10, ly - 15, 20, 20), 0, 3.14, 3)
                pygame.draw.circle(screen, (70, 70, 75), (lx, ly + 10), 4)
                locked_txt = font_tiny.render("BLOQUEADA", True, (100, 100, 105))
                screen.blit(locked_txt, (rect.centerx - locked_txt.get_width() // 2, rect.y + 130))

        if game_state.difficulty == "dificil":
            warn_txt = "DIFÍCIL: Falhar qualquer missão reseta TODO o progresso!"
            warn_col = (220, 80, 80)
        elif game_state.difficulty == "media":
            warn_txt = "MÉDIA: Fases desbloqueiam em sequência — progresso salvo"
            warn_col = (230, 180, 60)
        else:
            warn_txt = "FÁCIL: Todas as fases disponíveis — sem penalidade"
            warn_col = (100, 220, 100)
        warn = font_small.render(warn_txt, True, warn_col)
        screen.blit(warn, (SCREEN_W // 2 - warn.get_width() // 2, 440))

        ods = font_small.render("ODS 6 - Água Limpa e Saneamento", True, WATER_BLUE)
        screen.blit(ods, (SCREEN_W // 2 - ods.get_width() // 2, 490))

        note_alt = font_tiny.render("Dica: você pode alterar a dificuldade voltando ao menu principal.", True, (160, 180, 200))
        screen.blit(note_alt, (SCREEN_W // 2 - note_alt.get_width() // 2, 520))

        btn_back.draw(screen)
        draw_mute_button(screen)
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# COMPLETION / GAME OVER / VICTORY SCREENS
# ============================================================

def phase_complete_screen(phase_num, phase_name, message, score, stars_earned, time_taken, ods_fact=None):
    """Tela de conclusão de fase com animação de estrelas e pontuação."""
    btn_next = Button(SCREEN_W // 2 - 120, 500, 240, 55, "PRÓXIMA FASE", GREEN_BTN, GREEN_BTN_H, font=font_med)
    if phase_num >= 4:
        btn_next.text = "VITÓRIA!"
    frame = 0
    star_anim = [0, 0, 0]

    while True:
        mouse = pygame.mouse.get_pos()
        btn_next.update(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "next"
                if event.key == pygame.K_m:
                    toggle_mute()
            if btn_next.clicked(event):
                return "next"

        frame += 1
        for i in range(3):
            if frame > 30 + i * 20 and star_anim[i] < 1.0:
                star_anim[i] = min(1.0, star_anim[i] + 0.05)

        draw_sky_gradient(screen, (80, 160, 200), (150, 200, 160), SCREEN_H)
        draw_cloud(screen, 100, 30, 1.2)
        draw_cloud(screen, 500, 60, 0.9)
        draw_cloud(screen, 750, 20, 1.0)

        random.seed(frame // 3)
        for _ in range(20):
            cx = random.randint(0, SCREEN_W)
            cy = (random.randint(0, SCREEN_H) + frame * 2) % SCREEN_H
            cc = random.choice([GOLD, RED, GREEN_OK, WATER_BLUE, WHITE])
            pygame.draw.rect(screen, cc, (cx, cy, 6, 6))
        random.seed()

        title = font_title.render("MISSÃO CONCLUÍDA!", True, GOLD)
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 40))
        parabens = font_big.render("PARABÉNS!", True, WHITE)
        screen.blit(parabens, (SCREEN_W // 2 - parabens.get_width() // 2, 110))
        msg = font_med.render(message, True, WHITE)
        screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, 165))

        for i in range(3):
            sx = SCREEN_W // 2 - 100 + i * 100
            sy = 230
            if i < stars_earned and star_anim[i] > 0:
                size = int(30 * star_anim[i])
                draw_star_big(screen, sx, sy, True, size)
            else:
                draw_star_big(screen, sx, sy, False, 30)

        stats_y = 290
        score_txt = font_med.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_txt, (SCREEN_W // 2 - score_txt.get_width() // 2, stats_y))
        time_txt = font_med.render(f"Tempo: {int(time_taken)}s", True, WHITE)
        screen.blit(time_txt, (SCREEN_W // 2 - time_txt.get_width() // 2, stats_y + 35))
        stars_txt = font_med.render(f"Estrelas: {stars_earned}/3", True, GOLD)
        screen.blit(stars_txt, (SCREEN_W // 2 - stars_txt.get_width() // 2, stats_y + 70))

        if ods_fact:
            fact_box = pygame.Surface((600, 70), pygame.SRCALPHA)
            fact_box.fill((0, 0, 0, 140))
            screen.blit(fact_box, (SCREEN_W // 2 - 300, 400))
            pygame.draw.rect(screen, WATER_BLUE, (SCREEN_W // 2 - 300, 400, 600, 70), 2, border_radius=6)
            ods_label = font_tiny.render("ODS 6", True, WATER_BLUE)
            screen.blit(ods_label, (SCREEN_W // 2 - ods_label.get_width() // 2, 405))
            draw_ods6_symbol(screen, SCREEN_W // 2 - 75, 398, 22)
            wrap_y = 425
            words = ods_fact.split(' ')
            line = ''
            for w in words:
                test = line + ' ' + w if line else w
                if font_tiny.size(test)[0] > 560:
                    r = font_tiny.render(line, True, (220, 230, 245))
                    screen.blit(r, (SCREEN_W // 2 - r.get_width() // 2, wrap_y))
                    wrap_y += 18
                    line = w
                else:
                    line = test
            if line:
                r = font_tiny.render(line, True, (220, 230, 245))
                screen.blit(r, (SCREEN_W // 2 - r.get_width() // 2, wrap_y))

        btn_next.draw(screen)
        draw_mute_button(screen)
        pygame.display.flip()
        clock.tick(FPS)


def gameover_screen():
    """Tela de game over quando o jogador perde todas as vidas."""
    btn_retry = Button(SCREEN_W // 2 - 120, 420, 240, 55, "RECOMECAR", RED, (240, 70, 70), font=font_med)
    frame = 0
    while True:
        mouse = pygame.mouse.get_pos()
        btn_retry.update(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_m:
                    toggle_mute()
            if btn_retry.clicked(event):
                return

        frame += 1
        screen.fill((15, 10, 20))
        title = font_huge.render("MISSÃO FALHA", True, RED)
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 100))
        msg1 = font_big.render("A cidade ainda precisa de você!", True, WATER_BLUE)
        screen.blit(msg1, (SCREEN_W // 2 - msg1.get_width() // 2, 220))
        if game_state.difficulty == "dificil":
            msg2 = font_med.render("Todo o progresso foi perdido.", True, (200, 100, 100))
            screen.blit(msg2, (SCREEN_W // 2 - msg2.get_width() // 2, 290))
            msg3 = font_med.render("Você precisa recomeçar da Fase 1.", True, WHITE)
            screen.blit(msg3, (SCREEN_W // 2 - msg3.get_width() // 2, 330))
        else:
            msg2 = font_med.render("Não desista! Tente novamente.", True, (220, 180, 80))
            screen.blit(msg2, (SCREEN_W // 2 - msg2.get_width() // 2, 300))
        btn_retry.draw(screen)
        hint = font_small.render("Dica: colete gotas de água e evite obstáculos!", True, YELLOW)
        screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 520))
        draw_mute_button(screen)
        pygame.display.flip()
        clock.tick(FPS)


def victory_screen():
    """Tela de vitória exibida após completar todas as 5 fases."""
    frame = 0
    btn_menu = Button(SCREEN_W // 2 - 100, 530, 200, 50, "MENU", GREEN_BTN, GREEN_BTN_H, font=font_med)
    while True:
        mouse = pygame.mouse.get_pos()
        btn_menu.update(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_m:
                    toggle_mute()
            if btn_menu.clicked(event):
                return

        frame += 1
        draw_sky_gradient(screen, (20, 50, 100), (60, 120, 160), SCREEN_H)

        random.seed(789)
        for _ in range(60):
            sx = random.randint(0, SCREEN_W)
            sy = random.randint(0, SCREEN_H)
            b = int(120 + 135 * math.sin(frame * 0.02 + sx * 0.05))
            pygame.draw.circle(screen, (b, b, b), (sx, sy), 1)
        random.seed()

        random.seed(frame // 2)
        for _ in range(30):
            cx = random.randint(0, SCREEN_W)
            cy = (random.randint(0, SCREEN_H) + frame * 3) % SCREEN_H
            cc = random.choice([GOLD, RED, GREEN_OK, WATER_BLUE, STAR_YELLOW])
            pygame.draw.rect(screen, cc, (cx, cy, 5, 5))
        random.seed()

        title = font_huge.render("PARABÉNS!", True, GOLD)
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 40))
        sub = font_title.render("A CIDADE FOI SALVA!", True, WATER_BLUE)
        screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 115))

        draw_samuel(screen, SCREEN_W // 2 - 16, 185 + int(math.sin(frame * 0.04) * 6), True, frame)

        total = game_state.total_stars()
        for i in range(total):
            draw_star_big(screen, 200 + i * 40, 295, True, 16)

        stats = font_med.render(f"Estrelas totais: {total}/15", True, GOLD)
        screen.blit(stats, (SCREEN_W // 2 - stats.get_width() // 2, 335))

        msgs = [
            "Você ajudou a levar água limpa para todos!",
            "A ODS 6 busca garantir água potável e saneamento",
            "para todas as pessoas até 2030.",
            "Cada ação conta. Você fez a diferença!"
        ]
        for i, m in enumerate(msgs):
            color = WATER_BLUE if i == 0 else (180, 200, 220)
            t = font_small.render(m, True, color)
            screen.blit(t, (SCREEN_W // 2 - t.get_width() // 2, 380 + i * 24))

        creditos = font_tiny.render("Hero of Water — Desenvolvido por: Filipe Henry, André de Lira, Júlio Sérgio, João Victor | ADS 2026", True, (140, 160, 180))
        screen.blit(creditos, (SCREEN_W // 2 - creditos.get_width() // 2, 495))

        btn_menu.draw(screen)
        draw_mute_button(screen)
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# TUTORIAL POPUP
# ============================================================

def show_tutorial(surface, title_text, lines):
    """Exibe um popup de tutorial com título, linhas de texto e botão INICIAR."""
    btn_ok = Button(SCREEN_W // 2 - 80, 460, 160, 45, "INICIAR", GREEN_BTN, GREEN_BTN_H, font=font_med)
    while True:
        mouse = pygame.mouse.get_pos()
        btn_ok.update(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_e):
                    return
                if event.key == pygame.K_m:
                    toggle_mute()
            if btn_ok.clicked(event):
                return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        bw, bh = 600, 340
        bx = (SCREEN_W - bw) // 2
        by = (SCREEN_H - bh) // 2
        pygame.draw.rect(surface, POPUP_BG, (bx, by, bw, bh), border_radius=12)
        pygame.draw.rect(surface, WATER_BLUE, (bx, by, bw, bh), 3, border_radius=12)

        t = font_big.render(title_text, True, WATER_BLUE)
        surface.blit(t, (SCREEN_W // 2 - t.get_width() // 2, by + 20))

        for i, line in enumerate(lines):
            l_surf = font_small.render(line, True, WHITE)
            surface.blit(l_surf, (SCREEN_W // 2 - l_surf.get_width() // 2, by + 75 + i * 28))

        btn_ok.draw(surface)
        draw_mute_button(surface)
        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# MENU DE PAUSA
# ============================================================

def draw_pause_button(surface, x=SCREEN_W - 75, y=10):
    """Desenha o botão de pausa (dois traços verticais) ao lado do mute."""
    pygame.draw.circle(surface, (30, 30, 40, 180), (x + 12, y + 12), 14)
    pygame.draw.circle(surface, (60, 60, 70), (x + 12, y + 12), 14, 2)
    pygame.draw.rect(surface, WHITE, (x + 7, y + 5, 4, 14))
    pygame.draw.rect(surface, WHITE, (x + 14, y + 5, 4, 14))
    return pygame.Rect(x, y, 28, 28)

def pause_menu():
    """Exibe o menu de pausa sobre o jogo. Retorna 'resume' ou 'quit'."""
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))

    btn_resume = Button(SCREEN_W // 2 - 100, SCREEN_H // 2 - 30, 200, 50, "CONTINUAR", GREEN_BTN, GREEN_BTN_H)
    btn_settings = Button(SCREEN_W // 2 - 100, SCREEN_H // 2 + 35, 200, 45, "CONFIGURAÇÕES", (70, 100, 140), (90, 120, 170), font=font_med)
    btn_quit = Button(SCREEN_W // 2 - 100, SCREEN_H // 2 + 95, 200, 45, "SAIR DA FASE", RED, (240, 70, 70), font=font_med)

    while True:
        mouse = pygame.mouse.get_pos()
        btn_resume.update(mouse)
        btn_settings.update(mouse)
        btn_quit.update(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                if event.key == pygame.K_m:
                    toggle_mute()
                if event.key == pygame.K_RETURN:
                    return "resume"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
            if btn_resume.clicked(event):
                return "resume"
            if btn_settings.clicked(event):
                settings_screen()
            if btn_quit.clicked(event):
                return "quit"

        screen.blit(overlay, (0, 0))

        title = font_title.render("PAUSADO", True, WHITE)
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, SCREEN_H // 2 - 140))
        pygame.draw.line(screen, WATER_BLUE, (SCREEN_W // 2 - 80, SCREEN_H // 2 - 105), (SCREEN_W // 2 + 80, SCREEN_H // 2 - 105), 2)

        dica = font_tiny.render("ESC ou ENTER para continuar", True, (150, 170, 190))
        screen.blit(dica, (SCREEN_W // 2 - dica.get_width() // 2, SCREEN_H // 2 + 160))

        btn_resume.draw(screen)
        btn_settings.draw(screen)
        btn_quit.draw(screen)
        draw_mute_button(screen)

        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# PHASE 1: LIMPAR O CANAL (side-scrolling, trash bin, net throw)
# ============================================================

def run_phase_1(music_files, sfx=None):
    """Fase 1 — Limpar o Canal: side-scrolling, coletar lixo com rede, depositar em lixeiras."""
    play_music(music_files, 'phase1')

    LEVEL_W = SCREEN_W * 3  # 3x wider
    camera = Camera(LEVEL_W)

    player = Player(40, 458)  # Start at LEFT edge
    player.has_grabber = True
    player.carry_count = 0
    player.carry_max = 7
    _lives = get_initial_lives(0)
    player.lives = _lives
    player.max_lives = _lives
    player.initial_lives = _lives
    frame = 0
    start_time = None

    # Trash bins: left, center, and right
    bins = [
        {"x": 80, "y": 475},
        {"x": LEVEL_W // 2, "y": 475},
        {"x": LEVEL_W - 120, "y": 475},
    ]
    for b in bins:
        b["rect"] = pygame.Rect(b["x"], b["y"], 36, 52)

    # Obstacles — posições completamente aleatórias a cada run
    obstacles = []
    _obs_zone = LEVEL_W - 400
    _used_xs = []
    for i in range(14):
        for _ in range(30):
            ox = random.randint(300, LEVEL_W - 150)
            if all(abs(ox - ux) > 80 for ux in _used_xs):
                break
        _used_xs.append(ox)
        obstacles.append({"x": ox, "y": 510, "rect": pygame.Rect(ox + 5, 510, 40, 16)})

    # Ground lixos — posições aleatórias, garantidamente fora dos obstáculos
    # Zona de exclusão de cada obstáculo: centro em (obs["x"]+22), visual 45px wide → excluir ±52px do centro
    _obs_exclusions = [(obs["x"] + 22 - 52, obs["x"] + 22 + 52) for obs in obstacles]
    lixos = []
    _lixo_xs = []
    _global_attempts = 0
    while len(lixos) < 27 and _global_attempts < 1000:
        _global_attempts += 1
        lx = random.randint(180, LEVEL_W - 100)
        ly = 482 + random.randint(-4, 4)
        # Obstáculo: nunca colocar em cima (regra dura)
        if any(x0 <= lx <= x1 for (x0, x1) in _obs_exclusions):
            continue
        # Lixo-lixo: gap de 40px (reduzido se necessário para garantir 25 lixos)
        needed_gap = 40 if len(lixos) < 22 else 25
        if any(abs(lx - lx2) < needed_gap for lx2 in _lixo_xs):
            continue
        _lixo_xs.append(lx)
        lixos.append({"x": lx, "y": ly, "tipo": len(lixos) % 5, "collected": False, "in_river": False,
                       "rect": pygame.Rect(lx - 5, ly - 5, 26, 30)})

    # River lixos (in the water, need net to catch)
    river_lixos = []
    for i in range(15):
        lx = 150 + i * (LEVEL_W - 300) // 15 + random.randint(-30, 30)
        ly = 350 + random.randint(0, 80)
        river_lixos.append({"x": lx, "y": ly, "tipo": i % 5, "collected": False, "in_river": True,
                            "rect": pygame.Rect(lx - 5, ly - 5, 26, 30)})

    all_lixos = lixos + river_lixos

    # Water drops — sem sobreposição com obstáculos do chão
    _n_drops_1 = {"facil": 12, "media": 10, "dificil": 8}.get(game_state.difficulty, 12)
    drops = []
    _drop_xs_1 = []
    for i in range(_n_drops_1):
        for _ in range(80):
            dx = 100 + i * (LEVEL_W - 200) // _n_drops_1 + random.randint(-40, 40)
            dy = 430 + random.randint(-15, 15)
            if (all(not (x0 <= dx <= x1) for (x0, x1) in _obs_exclusions) and
                    all(abs(dx - dx2) > 40 for dx2 in _drop_xs_1)):
                break
        _drop_xs_1.append(dx)
        drops.append({"x": dx, "y": dy, "collected": False,
                       "rect": pygame.Rect(dx - 5, dy - 5, 26, 30)})

    particles = []
    nets = []  # Net projectiles
    collected_total = 0
    deposited = 0
    total = len(all_lixos)
    _deposit_water_milestone = 0  # rastreia restaurações de água a cada 7 depósitos

    # Targeting reticle
    reticle_x, reticle_y = 0, 0
    show_reticle = False

    draw_bg_river(screen, 0, 0, LEVEL_W, pollution_ratio=1.0)
    show_tutorial(screen, "FASE 1: CANAL DO RECIFE", [
        "O canal está cheio de lixo!",
        "Use E para coletar lixo próximo (máx. 7 por vez)",
        "Leve o lixo até uma lixeira (esquerda, centro ou direita)",
        "",
        "Para lixo no rio: botão DIREITO do mouse ou tecla F para lançar a rede",
        "Gotas de água recuperam sua barra de água",
    ])
    start_time = time_module.time()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        # Convert mouse to world coords for reticle
        world_mouse_x = mouse_pos[0] + camera.x
        world_mouse_y = mouse_pos[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_menu()
                    if result == "quit":
                        return "quit", 0, 0, 0
                if event.key == pygame.K_m:
                    toggle_mute()
                if event.key == pygame.K_e:
                    pr = player.rect()
                    # Check if near any bin to deposit
                    deposited_at_bin = False
                    for b in bins:
                        if player.carry_count > 0 and pr.colliderect(b["rect"]):
                            deposited += player.carry_count
                            player.carry_count = 0
                            play_sfx(sfx, 'deliver')
                            for _ in range(10):
                                particles.append(Particle(b["x"] + 18, b["y"], GREEN_OK, 0, -3))
                            deposited_at_bin = True
                            # Recupera UM POUCO de água a cada 7 depósitos (como 1 gota)
                            new_milestone = deposited // 7
                            if new_milestone > _deposit_water_milestone:
                                _deposit_water_milestone = new_milestone
                                player.water = min(player.max_water, player.water + 15)
                                for _ in range(6):
                                    particles.append(Particle(player.x + 16, player.y + 10, WATER_BLUE, 0, -3))
                            break
                    if not deposited_at_bin:
                        # Collect nearby ground lixo
                        for l in all_lixos:
                            if not l["collected"] and not l["in_river"] and player.carry_count < player.carry_max:
                                if pr.colliderect(l["rect"]):
                                    l["collected"] = True
                                    player.carry_count += 1
                                    collected_total += 1
                                    player.water = min(player.max_water, player.water + 3)
                                    play_sfx(sfx, 'collect')
                                    for _ in range(6):
                                        particles.append(Particle(l["x"] + 8, l["y"] + 8, GREEN_OK))
                                    break

            # Tecla F — lançar rede (mesmo efeito do botão direito do mouse)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                if player.carry_count < player.carry_max:
                    net = NetProjectile(player.x + 16, player.y + 20, world_mouse_x, world_mouse_y)
                    nets.append(net)
                    play_sfx(sfx, 'throw')

            # Right click to throw net
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if player.carry_count < player.carry_max:
                    net = NetProjectile(player.x + 16, player.y + 20, world_mouse_x, world_mouse_y)
                    nets.append(net)
                    play_sfx(sfx, 'throw')

            # Mute / pause button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                pause_rect = pygame.Rect(SCREEN_W - 75, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
                elif pause_rect.collidepoint(event.pos):
                    p = pause_menu()
                    if p == "quit":
                        return "quit", 0, 0, 0

        frame += 1
        keys = pygame.key.get_pressed()
        player.update(keys, ground_y=540, level_width=LEVEL_W)
        camera.update(player.x)

        # Update nets
        for net in nets[:]:
            net.update()
            if not net.alive:
                nets.remove(net)
                continue
            nr = net.rect()
            for l in all_lixos:
                if not l["collected"] and l["in_river"] and nr.colliderect(l["rect"]):
                    l["collected"] = True
                    collected_total += 1
                    player.carry_count = min(player.carry_max, player.carry_count + 1)
                    play_sfx(sfx, 'collect')
                    for _ in range(6):
                        particles.append(Particle(l["x"] + 8, l["y"] + 8, WATER_BLUE))
                    net.alive = False
                    break

        # Collect drops
        pr = player.rect()
        for d in drops:
            if not d["collected"] and pr.colliderect(d["rect"]):
                d["collected"] = True
                player.water = min(player.max_water, player.water + 15)
                play_sfx(sfx, 'collect')
                for _ in range(6):
                    particles.append(Particle(d["x"] + 8, d["y"] + 8, WATER_BLUE))

        # Obstacle damage
        for obs in obstacles:
            if pr.colliderect(obs["rect"]):
                if player.hit():
                    play_sfx(sfx, 'hit')
                    player.water = max(0, player.water - 8)

        # Water drain
        player.water = max(0, player.water - difficulty_drain(0.06))

        if player.lives <= 0 or player.water <= 0:
            return "dead", 0, 0, 0



        if player.lives <= 0 or player.water <= 0:
            return "dead", 0, 0, 0

        # Victory: all lixo deposited
        if deposited >= total:
            play_sfx(sfx, 'victory')
            elapsed = time_module.time() - start_time
            score = max(100, 500 - int(elapsed * 3)) + player.lives * 50
            stars = calc_stars(player.hearts_lost())
            return "win", score, stars, elapsed

        # Draw
        cam_x = camera.x
        pollution_ratio = 1.0 - (deposited / total) if total > 0 else 0.0
        draw_bg_river(screen, frame, cam_x, LEVEL_W, pollution_ratio)

        # Obstacles
        for obs in obstacles:
            sx, sy = camera.apply(obs["x"], obs["y"])
            if -50 < sx < SCREEN_W + 50:
                pygame.draw.ellipse(screen, POLLUTION_DARK, (sx, sy, 45, 18))
                pygame.draw.ellipse(screen, POLLUTION_GREEN, (sx + 2, sy + 2, 41, 14))
                bx_off = int(math.sin(frame * 0.1) * 6)
                by_off = -int(abs(math.sin(frame * 0.08)) * 8)
                pygame.draw.circle(screen, (100, 140, 50), (sx + 22 + bx_off, sy + by_off), 3)

        # Trash bins (3)
        for b in bins:
            bsx, bsy = camera.apply(b["x"], b["y"])
            if -50 < bsx < SCREEN_W + 50:
                draw_trash_bin(screen, bsx, bsy)
                if player.carry_count > 0:
                    pr_bin = player.rect()
                    if abs(player.x - b["x"]) < 80:
                        txt = font_tiny.render(f"Depositar [{player.carry_count}]", True, YELLOW)
                        screen.blit(txt, (bsx - 10, bsy - 20))

        # Ground lixos
        for l in all_lixos:
            if not l["collected"]:
                sx, sy = camera.apply(l["x"], l["y"])
                if -30 < sx < SCREEN_W + 30:
                    draw_lixo(screen, sx, sy, l["tipo"], frame)
                    if not l["in_river"]:
                        txt = font_tiny.render("E", True, YELLOW)
                        screen.blit(txt, (sx + 4, sy - 18))

        # Water drops
        for d in drops:
            if not d["collected"]:
                sx, sy = camera.apply(d["x"], d["y"])
                if -30 < sx < SCREEN_W + 30:
                    draw_water_drop_collectible(screen, sx, sy, frame)

        # Nets
        for net in nets:
            net.draw(screen, cam_x)

        # Reticle (show when mouse is in river area)
        if 340 < world_mouse_y < 460:
            pygame.draw.circle(screen, (255, 255, 100), mouse_pos, 12, 2)
            pygame.draw.line(screen, (255, 255, 100), (mouse_pos[0] - 16, mouse_pos[1]), (mouse_pos[0] + 16, mouse_pos[1]), 1)
            pygame.draw.line(screen, (255, 255, 100), (mouse_pos[0], mouse_pos[1] - 16), (mouse_pos[0], mouse_pos[1] + 16), 1)

        player.draw(screen, cam_x)

        for p in particles[:]:
            p.update()
            p.draw(screen, cam_x)
            if p.life <= 0:
                particles.remove(p)

        remaining = total - deposited
        elapsed = time_module.time() - start_time
        draw_hud(screen, player.lives, player.max_lives, player.water, player.max_water,
                 0, "CANAL DO RECIFE", 1, f"Deposite lixo na lixeira", deposited, total,
                 elapsed, player.carry_count, player.carry_max)

        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# PHASE 2: CONSERTAR VAZAMENTOS (side-scrolling)
# ============================================================

def run_phase_2(music_files, sfx=None):
    """Fase 2 — Bairro Precário: consertar canos quebrados e levar água para as casas."""
    play_music(music_files, 'phase2')

    LEVEL_W = SCREEN_W * 2
    camera = Camera(LEVEL_W)

    player = Player(80, 340)
    _lives = get_initial_lives(1)
    player.lives = _lives
    player.max_lives = _lives
    player.initial_lives = _lives
    frame = 0
    start_time = None

    ground_y = 560
    # Randomiza offsets das plataformas e escadas a cada run (±60px por grupo)
    _r = [random.randint(-55, 55) for _ in range(15)]
    platforms = [
        Platform(max(0, 0 + _r[0]), 480, 280, 14),
        Platform(max(0, 370 + _r[1]), 480, 280, 14),
        Platform(max(0, 750 + _r[2]), 480, 210, 14),
        Platform(max(0, 1000 + _r[3]), 480, 240, 14),
        Platform(max(0, 1340 + _r[4]), 480, 200, 14),
        Platform(max(0, 80 + _r[5]), 380, 240, 14),
        Platform(max(0, 410 + _r[6]), 380, 240, 14),
        Platform(max(0, 745 + _r[7]), 380, 185, 14),
        Platform(max(0, 1040 + _r[8]), 380, 205, 14),
        Platform(max(0, 1390 + _r[9]), 380, 180, 14),
        Platform(max(0, 145 + _r[10]), 280, 200, 14),
        Platform(max(0, 445 + _r[11]), 280, 205, 14),
        Platform(max(0, 715 + _r[12]), 280, 200, 14),
        Platform(max(0, 1090 + _r[13]), 280, 200, 14),
        Platform(max(0, 1440 + _r[14]), 280, 160, 14),
    ]
    # Escadas conectam plataformas — posição acompanha a plataforma base
    _lr = [random.randint(-30, 30) for _ in range(12)]
    ladders = [
        Ladder(255 + _r[0] + _lr[0], 480, 80),
        Ladder(630 + _r[1] + _lr[1], 480, 80),
        Ladder(1195 + _r[3] + _lr[2], 480, 80),
        Ladder(135 + _r[5] + _lr[3], 380, 100),
        Ladder(515 + _r[6] + _lr[4], 380, 100),
        Ladder(795 + _r[7] + _lr[5], 380, 100),
        Ladder(1095 + _r[8] + _lr[6], 380, 100),
        Ladder(1495 + _r[9] + _lr[7], 380, 100),
        Ladder(245 + _r[10] + _lr[8], 280, 100),
        Ladder(545 + _r[11] + _lr[9], 280, 100),
        Ladder(815 + _r[12] + _lr[10], 280, 100),
        Ladder(1195 + _r[13] + _lr[11], 280, 100),
    ]

    # 12 canos aleatórios: 5 no nível baixo, 4 no médio, 3 no alto
    _pipe_xs_458 = sorted([60, 450, random.randint(700, 900), random.randint(1050, 1200), random.randint(1350, 1500)])
    _pipe_xs_358 = sorted([120, 480, random.randint(750, 900), 1500])
    _pipe_xs_258 = sorted([200, random.randint(500, 650), 1150])
    pipes = []
    for x in _pipe_xs_458:
        pipes.append({"x": x, "y": 458, "broken": True, "progress": 0.0, "fixed": False, "double_fill": False})
    for x in _pipe_xs_358:
        pipes.append({"x": x, "y": 358, "broken": True, "progress": 0.0, "fixed": False, "double_fill": False})
    for x in _pipe_xs_258:
        pipes.append({"x": x, "y": 258, "broken": True, "progress": 0.0, "fixed": False, "double_fill": False})
    # 5 canos precisam de dois consertos (double fill)
    for idx in random.sample(range(len(pipes)), 5):
        pipes[idx]["double_fill"] = True
    for p in pipes:
        p["rect"] = pygame.Rect(p["x"] - 10, p["y"] - 10, 100, 42)

    # Drip zones definidas ANTES das drops para poder filtrar sobreposição
    _drip_xs = [random.randint(280, 400), random.randint(600, 780), random.randint(1150, 1350)]
    drip_zones = [
        {"x": _drip_xs[0], "y": 300, "w": 30, "rect": pygame.Rect(_drip_xs[0], 300, 30, 180)},
        {"x": _drip_xs[1], "y": 200, "w": 25, "rect": pygame.Rect(_drip_xs[1], 200, 25, 280)},
        {"x": _drip_xs[2], "y": 250, "w": 28, "rect": pygame.Rect(_drip_xs[2], 250, 28, 250)},
    ]

    # Drops filtradas: só posições que não sobrepõem canos nem drip zones
    _all_drop_positions = [(180, 460), (560, 460), (240, 360), (600, 360), (350, 260),
                           (680, 260), (860, 260), (1000, 460), (1300, 360), (1450, 260)]
    _n_drops_2 = {"facil": 10, "media": 9, "dificil": 7}.get(game_state.difficulty, 10)
    _valid_drop_pos = []
    for _ddx, _ddy in _all_drop_positions:
        _dr = pygame.Rect(_ddx - 16, _ddy - 16, 32, 32)
        if (not any(_dr.colliderect(p["rect"]) for p in pipes) and
                not any(_dr.colliderect(z["rect"]) for z in drip_zones)):
            _valid_drop_pos.append((_ddx, _ddy))
    _n_to_sample = min(_n_drops_2, len(_valid_drop_pos))
    drops = []
    for dx, dy in random.sample(_valid_drop_pos, _n_to_sample):
        drops.append({"x": dx, "y": dy, "collected": False, "rect": pygame.Rect(dx - 5, dy - 5, 26, 30)})

    # Detritos caindo — quantidade e velocidade por dificuldade
    _debris_cfg = {"facil": (14, 1.5, 3.0), "media": (18, 2.0, 4.0), "dificil": (22, 2.5, 5.0)}
    _n_deb, _spd_min, _spd_range = _debris_cfg.get(game_state.difficulty, (14, 1.5, 3.0))
    debris_list = []
    for i in range(_n_deb):
        debris_list.append({
            "x": 100 + i * (LEVEL_W - 200) // _n_deb + random.randint(0, 40),
            "y": random.randint(-300, -50),
            "speed": _spd_min + random.random() * _spd_range,
            "w": 12, "h": 12,
        })

    particles = []
    fixed = 0
    total = len(pipes)
    _fix_water_milestone = 0  # rastreia restaurações de água a cada 4 consertos

    draw_bg_neighborhood(screen, 0, 0, LEVEL_W)
    show_tutorial(screen, "FASE 2: BAIRRO PRECÁRIO", [
        "Os canos estão desgastados e vazando!",
        "Use escadas para subir e descer entre plataformas.",
        "",
        "Segure E próximo ao cano para consertar",
        "Setas cima/baixo = subir/descer escadas",
        "Cuidado com detritos e zonas de goteira!",
    ])
    start_time = time_module.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    p = pause_menu()
                    if p == "quit":
                        return "quit", 0, 0, 0
                if event.key == pygame.K_m:
                    toggle_mute()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                pause_rect = pygame.Rect(SCREEN_W - 75, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
                elif pause_rect.collidepoint(event.pos):
                    p = pause_menu()
                    if p == "quit":
                        return "quit", 0, 0, 0

        frame += 1
        keys = pygame.key.get_pressed()
        player.update(keys, ground_y=ground_y, platforms=platforms, ladders=ladders, level_width=LEVEL_W)
        camera.update(player.x)

        pr = player.rect()
        if keys[pygame.K_e]:
            for pipe in pipes:
                if not pipe["fixed"] and pr.colliderect(pipe["rect"]):
                    player.repairing = True
                    pipe["progress"] += 0.008
                    threshold = 2.0 if pipe["double_fill"] else 1.0
                    if pipe["progress"] >= threshold:
                        pipe["fixed"] = True
                        pipe["broken"] = False
                        fixed += 1
                        # Cano 2x = 75% da barra; cano padrão = 35% da barra
                        _water_reward = int(player.max_water * 0.75) if pipe["double_fill"] else int(player.max_water * 0.35)
                        player.water = min(player.max_water, player.water + _water_reward)
                        play_sfx(sfx, 'repair')
                        _n_particles = 14 if pipe["double_fill"] else 10
                        for _ in range(_n_particles):
                            particles.append(Particle(pipe["x"] + 40, pipe["y"], WATER_BLUE, 0, -3, 30))
                    break

        for pipe in pipes:
            if pipe["broken"] and not pipe["fixed"]:
                jet = pygame.Rect(pipe["x"] + 30, pipe["y"] + 20, 20, 30)
                if pr.colliderect(jet):
                    if player.hit():
                        play_sfx(sfx, 'hit')
                        player.water = max(0, player.water - 5)

        for zone in drip_zones:
            if pr.colliderect(zone["rect"]):
                if player.hit():
                    play_sfx(sfx, 'hit')
                    player.water = max(0, player.water - 3)

        for deb in debris_list:
            deb["y"] += deb["speed"]
            if deb["y"] > ground_y + 50:
                deb["y"] = random.randint(-300, -50)
                deb["x"] = random.randint(50, LEVEL_W - 50)
                deb["speed"] = 1.5 + random.random() * 1.5
            deb_rect = pygame.Rect(deb["x"], deb["y"], deb["w"], deb["h"])
            if pr.colliderect(deb_rect):
                if player.hit():
                    play_sfx(sfx, 'hit')
                    player.water = max(0, player.water - 4)
                deb["y"] = random.randint(-300, -50)

        for d in drops:
            if not d["collected"] and pr.colliderect(d["rect"]):
                d["collected"] = True
                player.water = min(player.max_water, player.water + 15)
                play_sfx(sfx, 'collect')
                for _ in range(6):
                    particles.append(Particle(d["x"] + 8, d["y"] + 8, WATER_BLUE))

        player.water = max(0, player.water - difficulty_drain(0.07))

        if player.lives <= 0 or player.water <= 0:
            return "dead", 0, 0, 0

        if fixed >= total:
            play_sfx(sfx, 'victory')
            elapsed = time_module.time() - start_time
            score = max(100, 500 - int(elapsed * 2)) + player.lives * 50
            stars = calc_stars(player.hearts_lost())
            return "win", score, stars, elapsed

        cam_x = camera.x
        draw_bg_neighborhood(screen, frame, cam_x, LEVEL_W)
        pygame.draw.rect(screen, CONCRETE_GRAY, (0, ground_y - 5, SCREEN_W, 5))
        pygame.draw.rect(screen, (70, 70, 75), (0, ground_y, SCREEN_W, SCREEN_H - ground_y))

        for plat in platforms:
            plat.draw(screen, cam_x)
        for ladder in ladders:
            ladder.draw(screen, cam_x)

        for zone in drip_zones:
            zsx = int(zone["x"] - cam_x)
            if -50 < zsx < SCREEN_W + 50:
                for dy in range(zone["y"], ground_y, 8):
                    if random.random() > 0.3:
                        dx = zsx + random.randint(0, zone["w"])
                        pygame.draw.circle(screen, WATER_BLUE, (dx, dy + (frame * 3) % 8), 2)

        for deb in debris_list:
            if deb["y"] > -20:
                dsx = int(deb["x"] - cam_x)
                if -20 < dsx < SCREEN_W + 20:
                    pygame.draw.rect(screen, (120, 100, 80), (dsx, int(deb["y"]), deb["w"], deb["h"]))
                    pygame.draw.rect(screen, (90, 70, 50), (dsx, int(deb["y"]), deb["w"], deb["h"]), 2)

        for pipe in pipes:
            psx = int(pipe["x"] - cam_x)
            if -100 < psx < SCREEN_W + 100:
                threshold = 2.0 if pipe["double_fill"] else 1.0
                draw_pipe_segment(screen, psx, pipe["y"], pipe["broken"],
                                  pipe["progress"] / threshold, pipe["double_fill"])
                if pipe["broken"] and not pipe["fixed"] and not pipe["double_fill"]:
                    txt = font_tiny.render("Segure E", True, YELLOW)
                    screen.blit(txt, (psx + 15, pipe["y"] - 25))

        for d in drops:
            if not d["collected"]:
                sx, sy = camera.apply(d["x"], d["y"])
                if -30 < sx < SCREEN_W + 30:
                    draw_water_drop_collectible(screen, sx, sy, frame)

        player.draw(screen, cam_x)
        for p in particles[:]:
            p.update()
            p.draw(screen, cam_x)
            if p.life <= 0:
                particles.remove(p)

        elapsed = time_module.time() - start_time
        draw_hud(screen, player.lives, player.max_lives, player.water, player.max_water,
                 0, "VAZAMENTOS", 2, "Conserte os canos [segure E]", fixed, total, elapsed)

        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# PHASE 3: DISTRIBUIR AGUA (side-scrolling)
# ============================================================

def run_phase_3(music_files, sfx=None):
    """Fase 3 — Água para Todos: distribuir água para NPCs sedentos pela comunidade."""
    play_music(music_files, 'phase3')

    LEVEL_W = SCREEN_W * 2
    camera = Camera(LEVEL_W)

    player = Player(450, 358)
    player.water = player.max_water
    _lives = get_initial_lives(2)
    player.lives = _lives
    player.max_lives = _lives
    player.initial_lives = _lives
    frame = 0
    start_time = None

    machines = [
        {"x": 460, "y": 390, "rect": pygame.Rect(455, 385, 60, 80), "filling": False, "fill_progress": 0.0},
        {"x": 1100, "y": 390, "rect": pygame.Rect(1095, 385, 60, 80), "filling": False, "fill_progress": 0.0},
    ]

    npcs = []
    # 7 NPCs evenly spaced, each needs 2 deliveries
    npc_positions = [
        (80, 400), (250, 400), (450, 400), (650, 400),
        (900, 400), (1150, 400), (1450, 400),
    ]
    for i, (nx, ny) in enumerate(npc_positions):
        npcs.append({"x": nx, "y": ny, "thirsty": True, "variant": i % 7,
                      "water_needed": 2, "water_received": 0,
                      "rect": pygame.Rect(nx - 5, ny - 5, 30, 60)})

    # Obstáculos cacto — posições longe de NPCs, máquinas, varais e poços
    puddles = [
        {"x": 168, "y": 450, "w": 44, "h": 14, "rect": pygame.Rect(168, 432, 44, 44), "variant": 0},
        {"x": 590, "y": 450, "w": 44, "h": 14, "rect": pygame.Rect(590, 432, 44, 44), "variant": 1},
        {"x": 1005, "y": 450, "w": 44, "h": 14, "rect": pygame.Rect(1005, 432, 44, 44), "variant": 2},
        {"x": 1310, "y": 450, "w": 44, "h": 14, "rect": pygame.Rect(1310, 432, 44, 44), "variant": 0},
    ]

    rocks = []
    for i in range(7):
        rocks.append({
            "x": random.randint(50, LEVEL_W - 50),
            "y": float(random.randint(-400, -100)),
            "speed": 1.2 + random.random(),
            "size": 10 + random.randint(0, 6),
        })

    platforms = [Platform(140, 370, 100, 12), Platform(700, 370, 80, 12), Platform(1200, 370, 90, 12)]

    _n_drops_3 = {"facil": 8, "media": 7, "dificil": 6}.get(game_state.difficulty, 8)
    drops = []
    _drop_xs_3 = []
    for i in range(_n_drops_3):
        for _ in range(80):
            dx = 50 + i * (LEVEL_W - 100) // _n_drops_3 + random.randint(-40, 40)
            dy = 420 + random.randint(-10, 10)
            # Clearance lateral das poças (não sobrepor em x)
            clear_puddle = all(dx < p["x"] - 35 or dx > p["x"] + p["w"] + 35 for p in puddles)
            clear_drop = all(abs(dx - dx2) > 40 for dx2 in _drop_xs_3)
            if clear_puddle and clear_drop:
                break
        _drop_xs_3.append(dx)
        drops.append({"x": dx, "y": dy, "collected": False, "rect": pygame.Rect(dx - 5, dy - 5, 26, 30)})

    particles = []
    delivered = 0
    total = sum(npc["water_needed"] for npc in npcs)
    houses_fully_served = 0
    _house_water_milestone = 0  # rastreia restaurações de água a cada 2 casas servidas

    # Nuvens tóxicas — obstáculos flutuantes que patrulham o cenário
    clouds_hazard = []
    for _ci in range(5):
        _cx = float(200 + _ci * (LEVEL_W - 400) // 5 + random.randint(-60, 60))
        _cvx = random.choice([-1.0, 1.0]) * (0.85 + random.random() * 0.45)
        clouds_hazard.append({
            "x": _cx, "y": float(348 + random.randint(0, 28)),
            "vx": _cvx, "w": 50, "h": 24,
        })

    draw_bg_community(screen, 0, 0, LEVEL_W)
    show_tutorial(screen, "FASE 3: ÁGUA PARA TODOS", [
        f"A comunidade está com sede! São {len(npcs)} moradores!",
        "Use uma das 2 máquinas de purificação para encher o galão",
        "e leve água para cada morador.",
        "",
        "Cuidado com cactos, pedras e nuvens tóxicas!",
        "E na máquina = encher  |  E no morador = entregar",
    ])
    start_time = time_module.time()
    player.invincible = 120  # 2 segundos de invencibilidade no início da fase 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    p = pause_menu()
                    if p == "quit":
                        return "quit", 0, 0, 0
                if event.key == pygame.K_m:
                    toggle_mute()
                if event.key == pygame.K_e and player.carrying:
                    pr = player.rect()
                    for npc in npcs:
                        if npc["thirsty"] and pr.colliderect(npc["rect"]):
                            npc["water_received"] += 1
                            player.carrying = False
                            delivered += 1
                            play_sfx(sfx, 'deliver')
                            for _ in range(10):
                                particles.append(Particle(npc["x"] + 12, npc["y"], WATER_BLUE, 0, -3))
                                particles.append(Particle(npc["x"] + 12, npc["y"] - 10, STAR_YELLOW, 0, -2))
                            if npc["water_received"] >= npc["water_needed"]:
                                npc["thirsty"] = False
                                houses_fully_served += 1
                                # Casa completa: +1,5 gotas (22) sempre
                                player.water = min(player.max_water, player.water + 22)
                                for _ in range(8):
                                    particles.append(Particle(npc["x"] + 12, npc["y"] - 10, WATER_BLUE, 0, -3))
                                # A cada 2 casas completas: bônus de +2,5 gotas (37)
                                new_milestone = houses_fully_served // 2
                                if new_milestone > _house_water_milestone:
                                    _house_water_milestone = new_milestone
                                    player.water = min(player.max_water, player.water + 37)
                                    for _ in range(12):
                                        particles.append(Particle(npc["x"] + 12, npc["y"] - 20, STAR_YELLOW, 0, -4))
                            break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                pause_rect = pygame.Rect(SCREEN_W - 75, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
                elif pause_rect.collidepoint(event.pos):
                    p = pause_menu()
                    if p == "quit":
                        return "quit", 0, 0, 0

        frame += 1
        keys = pygame.key.get_pressed()
        player.update(keys, ground_y=470, platforms=platforms, level_width=LEVEL_W)
        camera.update(player.x)

        pr = player.rect()
        active_machine = None
        for mach in machines:
            if keys[pygame.K_e] and not player.carrying and pr.colliderect(mach["rect"]):
                active_machine = mach
                break
        if active_machine:
            active_machine["filling"] = True
            active_machine["fill_progress"] += 0.012
            if active_machine["fill_progress"] >= 1.0:
                player.carrying = True
                active_machine["filling"] = False
                active_machine["fill_progress"] = 0.0
                play_sfx(sfx, 'collect')
        else:
            for mach in machines:
                if mach["filling"]:
                    mach["fill_progress"] = max(0, mach["fill_progress"] - 0.005)
                    if mach["fill_progress"] <= 0:
                        mach["filling"] = False

        for puddle in puddles:
            if pr.colliderect(puddle["rect"]):
                if player.hit():
                    play_sfx(sfx, 'hit')
                    player.water = max(0, player.water - 5)

        for rock in rocks:
            rock["y"] += rock["speed"]
            if rock["y"] > 480:
                rock["y"] = float(random.randint(-400, -100))
                rock["x"] = random.randint(50, LEVEL_W - 50)
            rock_rect = pygame.Rect(rock["x"] - rock["size"] // 2, int(rock["y"]) - rock["size"] // 2,
                                     rock["size"], rock["size"])
            if pr.colliderect(rock_rect):
                if player.hit():
                    play_sfx(sfx, 'hit')
                    player.water = max(0, player.water - 5)
                rock["y"] = float(random.randint(-400, -100))

        for d in drops:
            if not d["collected"] and pr.colliderect(d["rect"]):
                d["collected"] = True
                player.water = min(player.max_water, player.water + 15)
                play_sfx(sfx, 'collect')

        for cloud in clouds_hazard:
            cloud["x"] += cloud["vx"]
            if cloud["x"] < 0 or cloud["x"] > LEVEL_W - cloud["w"]:
                cloud["vx"] *= -1
                cloud["x"] = max(0.0, min(float(LEVEL_W - cloud["w"]), cloud["x"]))
            cloud_rect = pygame.Rect(int(cloud["x"]) + 8, int(cloud["y"]) + 4,
                                     cloud["w"] - 16, cloud["h"] - 8)
            if pr.colliderect(cloud_rect):
                if player.hit():
                    play_sfx(sfx, 'hit')
                    player.water = max(0, player.water - 4)

        player.water = max(0, player.water - difficulty_drain(0.05))

        if player.lives <= 0 or player.water <= 0:
            return "dead", 0, 0, 0

        if delivered >= total:
            play_sfx(sfx, 'victory')
            elapsed = time_module.time() - start_time
            score = max(100, 600 - int(elapsed * 2)) + player.lives * 50
            stars = calc_stars(player.hearts_lost())
            return "win", score, stars, elapsed

        cam_x = camera.x
        draw_bg_community(screen, frame, cam_x, LEVEL_W)

        for plat in platforms:
            plat.draw(screen, cam_x)

        # Cactos-obstáculo — destacados como perigo claro para o jogador
        for puddle in puddles:
            sx, sy = camera.apply(puddle["x"], puddle["y"])
            if -60 < sx < SCREEN_W + 60:
                _cv = puddle.get("variant", 0)
                _pw = puddle["w"]
                # Aura de perigo no chão (laranja translúcido)
                _hsurf = pygame.Surface((_pw + 32, 22), pygame.SRCALPHA)
                pygame.draw.ellipse(_hsurf, (220, 80, 20, 100), (0, 0, _pw + 32, 22))
                pygame.draw.ellipse(_hsurf, (255, 160, 40, 60), (6, 4, _pw + 20, 14))
                screen.blit(_hsurf, (sx - 8, 448))
                # Contorno escuro (outline) antes dos cactos — simula borda
                draw_cactus(screen, sx + 2, 464, _cv, 1.05)
                # Cactos em escala maior com cores mais vivas
                draw_cactus(screen, sx + 4, 462, _cv, 1.0)
                draw_cactus(screen, sx + _pw - 12, 462, (_cv + 1) % 3, 0.92)
                # Marcador de perigo: losango laranja acima do cluster
                _mx = sx + _pw // 2
                _my = 404
                _dmnd = [(_mx, _my - 8), (_mx + 7, _my), (_mx, _my + 8), (_mx - 7, _my)]
                pygame.draw.polygon(screen, (220, 70, 15), _dmnd)
                pygame.draw.polygon(screen, (255, 190, 40), _dmnd, 2)
                pygame.draw.rect(screen, (255, 220, 60), (_mx - 1, _my - 5, 3, 7))
                pygame.draw.circle(screen, (255, 220, 60), (_mx, _my + 5), 2)

        _house_variants = [0, 1, 2, 3, 4, 5, 3]
        for i, npc in enumerate(npcs):
            sx, sy = camera.apply(npc["x"] - 20, npc["y"] - 60)
            if -100 < sx < SCREEN_W + 100 and sy > 300:
                draw_house(screen, sx, sy, not npc["thirsty"], _house_variants[i % 7], frame)
                # --- Decoracoes perto de cada casa ---
                ground_y = sy + 150
                # Pequenas plantacoes (2 fileiras de cultivo)
                for pi in range(4):
                    px_d = sx + 70 + pi * 8
                    pygame.draw.rect(screen, (90, 70, 35), (px_d, ground_y - 10, 3, 10))
                    pygame.draw.ellipse(screen, (70, 140, 55), (px_d - 4, ground_y - 18, 10, 10))
                    pygame.draw.ellipse(screen, (50, 120, 40), (px_d - 2, ground_y - 22, 6, 7))
                # Flores coloridas perto da porta
                flower_colors = [(220, 80, 80), (240, 190, 60), (100, 160, 220), (200, 100, 200)]
                for fi in range(3):
                    fxd = sx - 10 + fi * 8
                    fc = flower_colors[(i + fi) % len(flower_colors)]
                    pygame.draw.rect(screen, (80, 120, 40), (fxd + 2, ground_y - 12, 2, 12))
                    pygame.draw.circle(screen, fc, (fxd + 3, ground_y - 14), 4)
                    pygame.draw.circle(screen, (255, 240, 180), (fxd + 3, ground_y - 14), 2)
                # Bicicleta perto do varal da casa i==4
                if i == 4:
                    bx_d = sx - 110
                    by_d = ground_y - 18
                    # Rodas
                    pygame.draw.circle(screen, (55, 55, 60), (bx_d, by_d), 13, 3)
                    pygame.draw.circle(screen, (55, 55, 60), (bx_d + 32, by_d), 13, 3)
                    # Raios
                    for _ra in range(4):
                        _ang = math.radians(_ra * 45)
                        _rx, _ry = int(math.cos(_ang) * 11), int(math.sin(_ang) * 11)
                        pygame.draw.line(screen, (110, 110, 120), (bx_d, by_d),
                                         (bx_d + _rx, by_d + _ry), 1)
                        pygame.draw.line(screen, (110, 110, 120), (bx_d + 32, by_d),
                                         (bx_d + 32 + _rx, by_d + _ry), 1)
                    # Aros
                    pygame.draw.circle(screen, (140, 140, 150), (bx_d, by_d), 5)
                    pygame.draw.circle(screen, (140, 140, 150), (bx_d + 32, by_d), 5)
                    # Quadro (frame triangular)
                    pygame.draw.line(screen, (185, 75, 55), (bx_d + 4, by_d - 4),
                                     (bx_d + 18, by_d - 18), 3)
                    pygame.draw.line(screen, (185, 75, 55), (bx_d + 28, by_d - 4),
                                     (bx_d + 18, by_d - 18), 3)
                    pygame.draw.line(screen, (185, 75, 55), (bx_d + 18, by_d - 18),
                                     (bx_d + 18, by_d - 28), 3)
                    pygame.draw.line(screen, (210, 110, 90), (bx_d + 4, by_d),
                                     (bx_d + 28, by_d - 10), 2)
                    # Guidão
                    pygame.draw.line(screen, (100, 100, 115), (bx_d + 12, by_d - 28),
                                     (bx_d + 26, by_d - 28), 3)
                    pygame.draw.line(screen, (100, 100, 115), (bx_d + 12, by_d - 28),
                                     (bx_d + 12, by_d - 22), 2)
                    # Selim
                    pygame.draw.rect(screen, (45, 30, 15), (bx_d + 15, by_d - 32, 12, 5))

        for rock in rocks:
            if rock["y"] > -20:
                sx, sy = camera.apply(rock["x"], int(rock["y"]))
                if -20 < sx < SCREEN_W + 20:
                    pygame.draw.circle(screen, (120, 100, 80), (sx, sy), rock["size"] // 2)

        for mach in machines:
            msx, msy = camera.apply(mach["x"], mach["y"])
            if -80 < msx < SCREEN_W + 80:
                # Aura azulada sutil ao redor da máquina (destaque visual)
                _gcx, _gcy = msx + 25, msy + 35
                _gsurf = pygame.Surface((160, 160), pygame.SRCALPHA)
                for _gr, _ga in [(72, 10), (52, 20), (34, 34), (18, 50)]:
                    pygame.draw.ellipse(_gsurf, (70, 150, 255, _ga),
                                        (80 - _gr, 80 - _gr, _gr * 2, _gr * 2))
                screen.blit(_gsurf, (_gcx - 80, _gcy - 80))
                draw_purification_machine(screen, msx, msy, mach["filling"], mach["fill_progress"])
                if not player.carrying:
                    txt = font_tiny.render("E = Encher", True, YELLOW)
                    screen.blit(txt, (msx + 2, msy - 15))

        for npc in npcs:
            sx, sy = camera.apply(npc["x"], npc["y"])
            if -30 < sx < SCREEN_W + 30:
                draw_npc(screen, sx, sy, npc["thirsty"], npc["variant"], frame)
                if npc["thirsty"] and player.carrying:
                    txt = font_tiny.render("E", True, YELLOW)
                    screen.blit(txt, (sx + 6, sy - 20))
                if npc["thirsty"] and npc["water_received"] > 0:
                    # Show partial progress
                    prog_txt = font_tiny.render(f"{npc['water_received']}/{npc['water_needed']}", True, WATER_BLUE)
                    screen.blit(prog_txt, (sx + 2, sy - 32))

        for d in drops:
            if not d["collected"]:
                sx, sy = camera.apply(d["x"], d["y"])
                if -30 < sx < SCREEN_W + 30:
                    draw_water_drop_collectible(screen, sx, sy, frame)

        # Nuvens tóxicas
        for cloud in clouds_hazard:
            csx = int(cloud["x"] - cam_x)
            if -70 < csx < SCREEN_W + 70:
                _cw, _ch = cloud["w"], cloud["h"]
                _csurf = pygame.Surface((_cw + 24, _ch + 16), pygame.SRCALPHA)
                pygame.draw.ellipse(_csurf, (140, 195, 55, 120), (12, 8, _cw, _ch))
                pygame.draw.ellipse(_csurf, (180, 225, 80, 75), (15, 10, _cw - 6, _ch - 4))
                pygame.draw.ellipse(_csurf, (90, 150, 35, 100), (12, 8, _cw, _ch), 2)
                pygame.draw.ellipse(_csurf, (210, 240, 110, 55),
                                    (16, 10, _cw // 2, _ch // 2))
                for _di in range(4):
                    _dx = 16 + _di * (_cw // 4)
                    _dy = 10 + (_di % 2) * (_ch // 3)
                    pygame.draw.circle(_csurf, (230, 255, 130, 50), (_dx, _dy), 3)
                screen.blit(_csurf, (csx - 12, int(cloud["y"]) - 8))

        player.draw(screen, cam_x)

        if player.carrying:
            txt = font_tiny.render("Carregando agua!", True, WATER_BLUE)
            screen.blit(txt, (int(player.x - cam_x) - 14, int(player.y) - 18))

        for p in particles[:]:
            p.update()
            p.draw(screen, cam_x)
            if p.life <= 0:
                particles.remove(p)

        elapsed = time_module.time() - start_time
        draw_hud(screen, player.lives, player.max_lives, player.water, player.max_water,
                 0, "AGUA P/ TODOS", 3, "Entregue agua [E]", delivered, total, elapsed)

        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# PHASE 4: ESTACAO DE TRATAMENTO (harder, more obstacles, tighter timer)
# ============================================================

def run_phase_4(music_files, sfx=None):
    """Fase 4 — Estação de Tratamento: ativar máquinas de purificação na ordem correta."""
    play_music(music_files, 'phase4')

    LEVEL_W = SCREEN_W * 2
    camera = Camera(LEVEL_W)

    player = Player(80, 438)
    _lives = get_initial_lives(3)
    player.lives = _lives
    player.max_lives = _lives
    player.initial_lives = _lives
    frame = 0
    start_time = None

    station_types = ["filtrar", "tratar", "desinfetar", "liberar"]

    def create_stations():
        x_positions = list(range(100, LEVEL_W - 100, (LEVEL_W - 200) // 4))
        random.shuffle(x_positions)
        stns = []
        for i, st in enumerate(station_types):
            sx = x_positions[i] if i < len(x_positions) else 100 + i * 300
            stns.append({"x": sx, "y": 400, "type": st, "active": False, "completed": False,
                          "rect": pygame.Rect(sx - 5, 395, 80, 80)})
        return stns

    stations = create_stations()
    current_step = 0
    rounds_done = 0
    total_rounds = 5
    errors = 0
    particles = []
    round_msg = ""
    msg_timer = 0

    # Timer por rodada — fácil: sempre 30s; média/difícil: diminui com rounds
    def _calc_round_timer(rd):
        if game_state.difficulty == "facil":
            return 30.0
        return max(15.0, 30.0 - rd * 3)

    round_timer = _calc_round_timer(0)
    round_timer_start = None

    # More obstacles
    toxic_puddles = []
    steam_vents = []
    moving_machines = []

    def generate_hazards(round_num):
        nonlocal toxic_puddles, steam_vents, moving_machines

        # Poças tóxicas — gap mínimo de 70px entre elas para o jogador (32px) sempre conseguir passar
        toxic_puddles = []
        _puddle_ranges = []  # (x_inicio, x_fim) de cada poça já colocada
        n_puddles = 3 + round_num
        for i in range(n_puddles):
            w = 35 + random.randint(0, 20)
            placed = False
            for _ in range(80):
                ox = random.randint(80, LEVEL_W - 80 - w)
                # Verifica gap mínimo de 70px de qualquer poça existente
                gap_ok = all(ox > xe + 70 or ox + w < xs - 70 for (xs, xe) in _puddle_ranges)
                if gap_ok:
                    placed = True
                    break
            if not placed:
                continue  # descarta se não há espaço — melhor poucos que bloqueantes
            _puddle_ranges.append((ox, ox + w))
            toxic_puddles.append({
                "x": ox, "y": 490,
                "w": w, "h": 12,
                "rect": pygame.Rect(ox, 490, w, 12),
            })

        # Vapores — espaçamento mínimo de 100px entre vents
        steam_vents = []
        _vent_xs = []
        for i in range(1 + round_num // 2):
            placed = False
            for _ in range(60):
                vx = random.randint(100, LEVEL_W - 100)
                if all(abs(vx - vx2) > 100 for vx2 in _vent_xs):
                    placed = True
                    break
            if not placed:
                continue
            _vent_xs.append(vx)
            steam_vents.append({
                "x": vx, "y": 470, "w": 20, "h": 30,
                "active_timer": 0,
                "rect": pygame.Rect(vx, 440, 20, 60),
            })

        # Máquinas móveis — se movem, sempre deixam passagem
        moving_machines = []
        for i in range(round_num):
            mx = float(random.randint(200, LEVEL_W - 200))
            moving_machines.append({
                "x": mx, "y": 480,
                "speed": 1.5 + random.random(),
                "dir": 1 if i % 2 == 0 else -1,
                "w": 30, "h": 20,
            })

    generate_hazards(0)

    # Water drops — sem sobreposição com vents nem poças
    _n_drops_4 = {"facil": 8, "media": 7, "dificil": 6}.get(game_state.difficulty, 8)

    def _make_drops_4():
        d, _xs = [], []
        for i in range(_n_drops_4):
            for _ in range(80):
                dx = 100 + i * (LEVEL_W - 200) // _n_drops_4 + random.randint(-30, 30)
                dy = 460 + random.randint(-10, 10)
                _dr = pygame.Rect(dx - 13, dy - 13, 26, 26)
                clear_vent = all(not _dr.colliderect(v["rect"]) for v in steam_vents)
                clear_puddle = all(abs(dx - p["x"]) > 55 for p in toxic_puddles)
                clear_d = all(abs(dx - x2) > 40 for x2 in _xs)
                if clear_vent and clear_puddle and clear_d:
                    break
            _xs.append(dx)
            d.append({"x": dx, "y": dy, "collected": False, "rect": pygame.Rect(dx - 5, dy - 5, 26, 30)})
        return d

    drops = _make_drops_4()

    draw_bg_treatment(screen, 0, 0, LEVEL_W)
    show_tutorial(screen, "FASE 4: TRATAMENTO DE ÁGUA", [
        "Você está na estação de tratamento!",
        "Processe 5 lotes na sequência correta:",
        "",
        "1.FILTRAR  >  2.TRATAR  >  3.DESINFETAR  >  4.LIBERAR",
        "CUIDADO: poças tóxicas, vapor e máquinas!",
        "Timer apertado! Errar = perder uma vida!",
    ])
    start_time = time_module.time()
    round_timer_start = time_module.time()
    player.invincible = 120  # 2 segundos de invencibilidade no início da fase 4

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    p = pause_menu()
                    if p == "quit":
                        return "quit", 0, 0, 0
                if event.key == pygame.K_m:
                    toggle_mute()
                if event.key == pygame.K_e:
                    pr = player.rect()
                    for i, s in enumerate(stations):
                        if not s["completed"] and pr.colliderect(s["rect"]):
                            if i == current_step:
                                s["completed"] = True
                                current_step += 1
                                play_sfx(sfx, 'station')
                                for _ in range(8):
                                    particles.append(Particle(s["x"] + 35, s["y"] + 25, GREEN_OK, 0, -3))
                                round_msg = "Correto!"
                                msg_timer = 40

                                if current_step >= 4:
                                    rounds_done += 1
                                    current_step = 0
                                    stations = create_stations()
                                    round_timer = _calc_round_timer(rounds_done)
                                    round_timer_start = time_module.time()
                                    generate_hazards(rounds_done)
                                    # Regenerate drops sem sobreposição com novos hazards
                                    drops = _make_drops_4()
                                    # Recompensa: +50% barra de água e 3s de invencibilidade
                                    player.water = min(player.max_water, player.water + player.max_water // 2)
                                    player.invincible = 180  # 3 segundos a 60 FPS
                                    for _ in range(12):
                                        particles.append(Particle(player.x + 16, player.y + 10, WATER_BLUE, 0, -4))
                                    round_msg = f"Lote {rounds_done}/5 tratado!"
                                    msg_timer = 60
                            else:
                                errors += 1
                                player.hit()
                                player.water = max(0, player.water - 8)
                                play_sfx(sfx, 'error')
                                current_step = 0
                                for st in stations:
                                    st["completed"] = False
                                round_msg = "Sequencia errada!"
                                msg_timer = 50
                            break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mute_rect = pygame.Rect(SCREEN_W - 40, 10, 28, 28)
                pause_rect = pygame.Rect(SCREEN_W - 75, 10, 28, 28)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()
                elif pause_rect.collidepoint(event.pos):
                    p = pause_menu()
                    if p == "quit":
                        return "quit", 0, 0, 0

        frame += 1
        keys = pygame.key.get_pressed()
        player.update(keys, ground_y=500, level_width=LEVEL_W)
        camera.update(player.x)

        if msg_timer > 0:
            msg_timer -= 1

        if round_timer_start is not None:
            time_left = round_timer - (time_module.time() - round_timer_start)
            if time_left <= 0 and rounds_done < total_rounds:
                if game_state.difficulty == "dificil":
                    return "dead", 0, 0, 0
                elif game_state.difficulty == "media":
                    player.lives = max(0, player.lives - 2)
                    if player.lives <= 0:
                        return "dead", 0, 0, 0
                else:  # facil
                    player.hit()
                    player.water = max(0, player.water - 5)
                current_step = 0
                for st in stations:
                    st["completed"] = False
                stations = create_stations()
                round_timer = _calc_round_timer(rounds_done)
                round_timer_start = time_module.time()
                round_msg = "Tempo esgotado!"
                msg_timer = 50
                generate_hazards(rounds_done)
        else:
            time_left = round_timer

        pr = player.rect()

        # Toxic puddle damage
        for obs in toxic_puddles:
            if pr.colliderect(obs["rect"]):
                if player.hit():
                    play_sfx(sfx, 'hit')
                    player.water = max(0, player.water - 5)

        # Steam vent damage
        for vent in steam_vents:
            vent["active_timer"] += 1
            if (vent["active_timer"] // 60) % 2 == 0:  # Active every other second
                if pr.colliderect(vent["rect"]):
                    if player.hit():
                        play_sfx(sfx, 'hit')
                        player.water = max(0, player.water - 4)

        # Moving machinery
        for mach in moving_machines:
            mach["x"] += mach["speed"] * mach["dir"]
            if mach["x"] < 50 or mach["x"] > LEVEL_W - 80:
                mach["dir"] *= -1
            mach_rect = pygame.Rect(int(mach["x"]), mach["y"], mach["w"], mach["h"])
            if pr.colliderect(mach_rect):
                if player.hit():
                    play_sfx(sfx, 'hit')
                    player.water = max(0, player.water - 4)

        # Water drops
        for d in drops:
            if not d["collected"] and pr.colliderect(d["rect"]):
                d["collected"] = True
                player.water = min(player.max_water, player.water + 12)
                play_sfx(sfx, 'collect')

        player.water = max(0, player.water - difficulty_drain(0.05))

        if player.lives <= 0 or player.water <= 0:
            return "dead", 0, 0, 0

        if rounds_done >= total_rounds:
            play_sfx(sfx, 'victory')
            elapsed = time_module.time() - start_time
            score = max(100, 600 - int(elapsed * 3) - errors * 50) + player.lives * 50
            stars = calc_stars(player.hearts_lost())
            return "win", score, stars, elapsed

        cam_x = camera.x
        draw_bg_treatment(screen, frame, cam_x, LEVEL_W)

        # Draw toxic puddles
        for obs in toxic_puddles:
            sx, sy = camera.apply(obs["x"], obs["y"])
            if -60 < sx < SCREEN_W + 60:
                pygame.draw.ellipse(screen, (100, 180, 40), (sx, sy, obs["w"], obs["h"]))
                pygame.draw.ellipse(screen, (120, 200, 60), (sx + 2, sy + 2, obs["w"] - 4, obs["h"] - 4))
                # Toxic bubbles
                bx_off = int(math.sin(frame * 0.12 + obs["x"]) * 5)
                pygame.draw.circle(screen, (140, 220, 80), (sx + obs["w"] // 2 + bx_off, sy - 3), 3)

        # Draw steam vents
        for vent in steam_vents:
            sx, sy = camera.apply(vent["x"], vent["y"])
            if -30 < sx < SCREEN_W + 30:
                # Vent base
                pygame.draw.rect(screen, (100, 100, 110), (sx, sy, vent["w"], 10))
                pygame.draw.rect(screen, (80, 80, 90), (sx, sy, vent["w"], 10), 2)
                # Steam when active
                if (vent["active_timer"] // 60) % 2 == 0:
                    for si in range(5):
                        steam_y = sy - 5 - si * 8 - (frame % 8)
                        steam_alpha = max(0, 200 - si * 40)
                        steam_w = vent["w"] + si * 4
                        pygame.draw.ellipse(screen, (200, 200, 210), (sx - si * 2, steam_y, steam_w, 8))

        # Draw moving machinery
        for mach in moving_machines:
            sx, sy = camera.apply(int(mach["x"]), mach["y"])
            if -40 < sx < SCREEN_W + 40:
                pygame.draw.rect(screen, (150, 60, 60), (sx, sy, mach["w"], mach["h"]))
                pygame.draw.rect(screen, (120, 40, 40), (sx, sy, mach["w"], mach["h"]), 2)
                # Gears
                gear_angle = frame * 0.1
                gx = sx + mach["w"] // 2
                gy = sy + mach["h"] // 2
                for gi in range(4):
                    a = gear_angle + gi * math.pi / 2
                    pygame.draw.line(screen, YELLOW, (gx, gy),
                                     (gx + int(math.cos(a) * 6), gy + int(math.sin(a) * 6)), 2)
                # Warning sign
                pygame.draw.polygon(screen, YELLOW, [(sx + mach["w"] // 2, sy - 8),
                                                      (sx + mach["w"] // 2 - 5, sy - 2),
                                                      (sx + mach["w"] // 2 + 5, sy - 2)])

        # Stations
        for i, s in enumerate(stations):
            sx, sy = camera.apply(s["x"], s["y"])
            if -80 < sx < SCREEN_W + 80:
                is_next = (i == current_step and not s["completed"])
                draw_treatment_station(screen, sx, sy, s["type"], is_next, s["completed"])
                if is_next:
                    txt = font_tiny.render("E", True, YELLOW)
                    screen.blit(txt, (sx + 30, sy - 18))

        # Animated water particles flowing between completed stations
        completed_stations = [s for s in stations if s["completed"]]
        for cs in completed_stations:
            csx, csy = camera.apply(cs["x"], cs["y"])
            if -80 < csx < SCREEN_W + 80:
                flow_off = (frame * 3) % 60
                for fi in range(3):
                    fx = csx + 70 + flow_off + fi * 20
                    fy = csy + 25 + int(math.sin(frame * 0.15 + fi) * 4)
                    if fx < SCREEN_W + 20:
                        pygame.draw.circle(screen, WATER_BLUE, (fx, fy), 3)
                        pygame.draw.circle(screen, WATER_LIGHT, (fx - 1, fy - 1), 1)

        # Sequence visual
        seq_y = 110
        seq_txt = font_med.render("Sequencia:", True, WHITE)
        screen.blit(seq_txt, (30, seq_y))
        for i, st in enumerate(station_types):
            color = GREEN_OK if i < current_step else (YELLOW if i == current_step else (120, 120, 130))
            arrow = " > " if i < 3 else ""
            t = font_small.render(st.upper() + arrow, True, color)
            screen.blit(t, (180 + i * 160, seq_y + 4))

        round_txt = font_med.render(f"Lote: {rounds_done}/{total_rounds}", True, WHITE)
        screen.blit(round_txt, (30, 150))

        timer_color = WHITE
        if time_left < 10:
            timer_color = YELLOW
        if time_left < 5:
            timer_color = RED
        timer_txt = font_big.render(f"{max(0, int(time_left))}s", True, timer_color)
        screen.blit(timer_txt, (SCREEN_W - 100, 110))

        timer_bar_w = 150
        timer_ratio = max(0, time_left / round_timer) if round_timer > 0 else 0
        pygame.draw.rect(screen, (40, 40, 45), (SCREEN_W - 170, 155, timer_bar_w, 10), border_radius=5)
        fill_w = int(timer_bar_w * timer_ratio)
        if fill_w > 0:
            bar_color = GREEN_OK if timer_ratio > 0.5 else (YELLOW if timer_ratio > 0.25 else RED)
            pygame.draw.rect(screen, bar_color, (SCREEN_W - 170, 155, fill_w, 10), border_radius=5)

        # Water drops
        for d in drops:
            if not d["collected"]:
                dsx, dsy = camera.apply(d["x"], d["y"])
                if -30 < dsx < SCREEN_W + 30:
                    draw_water_drop_collectible(screen, dsx, dsy, frame)

        player.draw(screen, cam_x)

        if msg_timer > 0 and round_msg:
            color = GREEN_OK if "Correto" in round_msg or "tratado" in round_msg else RED
            mt = font_big.render(round_msg, True, color)
            screen.blit(mt, (SCREEN_W // 2 - mt.get_width() // 2, 200))

        for p in particles[:]:
            p.update()
            p.draw(screen, cam_x)
            if p.life <= 0:
                particles.remove(p)

        elapsed = time_module.time() - start_time
        draw_hud(screen, player.lives, player.max_lives, player.water, player.max_water,
                 0, "TRATAMENTO", 4, "Processe os lotes", rounds_done, total_rounds, elapsed)

        pygame.display.flip()
        clock.tick(FPS)



# ============================================================
# LOOP PRINCIPAL DO JOGO
# ============================================================

# Nomes e mensagens de conclusão para cada uma das 4 fases
PHASE_NAMES = ["Canal do Recife", "Bairro Precário", "Água para Todos",
               "Estação de Tratamento"]

PHASE_MESSAGES = [
    "Você limpou o Canal do Recife!",
    "Os vazamentos foram consertados!",
    "A comunidade tem água limpa!",
    "A água foi tratada com sucesso!",
]

ODS6_FACTS = [
    "Sabia que 80% do esgoto no mundo é despejado sem tratamento nos rios e mares?",
    "Sabia que 3,5 bilhões de pessoas vivem sem saneamento básico seguro no mundo?",
    "Sabia que a cada 2 minutos uma criança morre de doenças por falta de água potável?",
    "Sabia que o tratamento de água remove impurezas e micro-organismos que causam doenças?",
]


def main():
    """Função principal — gerencia a geração de áudio, seleção de dificuldade e o loop do jogo."""
    # Gera música se os arquivos não existirem
    needs_generation = False
    for fname in ['music_menu.wav', 'music_phase1.wav', 'music_phase2.wav',
                   'music_phase3.wav', 'music_phase4.wav']:
        fpath = os.path.join(GAME_DIR, fname)
        custom = os.path.join(GAME_DIR, f'custom_{fname}')
        if not os.path.exists(fpath) and not os.path.exists(custom):
            needs_generation = True
            break

    if needs_generation:
        screen.fill(DARK_BLUE)
        loading_text = font_big.render("Gerando trilha sonora...", True, WATER_BLUE)
        screen.blit(loading_text, (SCREEN_W // 2 - loading_text.get_width() // 2, SCREEN_H // 2 - 20))
        pygame.display.flip()

    music_files = generate_all_music()
    sfx = generate_sfx()
    global global_sfx
    global_sfx = sfx
    set_volume(audio_volume)

    # Lista de funções de cada fase, indexadas de 0 a 3
    PHASE_FUNCTIONS = [run_phase_1, run_phase_2, run_phase_3, run_phase_4]

    state = "title"

    while True:
        if state == "title":
            # Tela inicial — jogar, história ou instruções
            result = title_screen(music_files)
            if result == "play":
                chosen_difficulty = difficulty_screen(music_files)
                if chosen_difficulty == "back":
                    state = "title"
                    continue
                game_state.difficulty = chosen_difficulty
                game_state.reset()
                story_intro_screen()
                state = "select"
            elif result == "continue":
                # Continua partida existente sem resetar progresso
                state = "select"
            elif result == "instructions":
                instructions_screen()
                state = "title"
            elif result == "story":
                story_intro_screen()
                state = "title"

        elif state == "select":
            # Tela de seleção de fases
            result = phase_select_screen()
            if result == "back":
                state = "title"
            elif isinstance(result, int):
                phase_idx = result
                # Executa a fase escolhida
                result, score, stars, time_taken = PHASE_FUNCTIONS[phase_idx](music_files, sfx)

                if result == "win":
                    # Fase concluída com sucesso
                    game_state.complete_phase(phase_idx, stars)
                    action = phase_complete_screen(
                        phase_idx + 1, PHASE_NAMES[phase_idx],
                        PHASE_MESSAGES[phase_idx], score, stars, time_taken,
                        ODS6_FACTS[phase_idx]
                    )
                    state = "select"

                elif result == "dead":
                    # Jogador morreu — comportamento varia conforme dificuldade
                    if game_state.difficulty == "dificil":
                        game_state.reset()
                        gameover_screen()
                        state = "title"
                    elif game_state.difficulty == "media":
                        gameover_screen()
                        state = "select"
                    else:
                        gameover_screen()
                        state = "select"

                elif result == "quit":
                    # Dificuldade difícil: sair da fase reseta o progresso
                    if game_state.difficulty == "dificil":
                        game_state.reset()
                        state = "title"
                    else:
                        state = "select"


# Inicia o jogo quando executado diretamente
if __name__ == "__main__":
    main()
