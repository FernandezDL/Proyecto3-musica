# ============================================================
# PROYECTO 3: Sonificación de Tráfico Guatemala
# Dataset: Datos de tráfico Roosevelt-Trébol (Septiembre)
# ============================================================

from music import *

# ============================================================
# DATOS DEL DATASET
# ritmo = ESTADO del tráfico (1=Fluido, 5=Congestionado)
# melodia = HORA del día (0-23 hrs, codificado 0-16)
# ============================================================
ritmo = [5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 3, 3, 3, 3, 2, 2, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 4, 4, 3, 3, 1, 1, 4, 4, 5, 5, 5, 5, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 5, 5, 3, 3, 3, 4, 4, 3, 3, 3, 3, 1, 1, 3, 3, 4, 4, 3, 4, 4, 4, 4, 4, 4, 3, 3, 2, 3, 3, 4, 4, 3, 3, 2, 3, 3, 4, 4, 4, 4, 4, 4, 2, 3, 3]
melodia = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3]

# Rangos de los datos
min_r, max_r = min(ritmo), max(ritmo)
min_m, max_m = min(melodia), max(melodia)

# ============================================================
# CLASIFICACIÓN POR TERCILES (Técnica de agrupamiento)
# Divide los datos en 3 grupos: bajo, medio, alto
# ============================================================
sorted_r = sorted(ritmo)
tercil_1 = sorted_r[len(sorted_r) // 3]      # Límite inferior (~2)
tercil_2 = sorted_r[2 * len(sorted_r) // 3]  # Límite superior (~4)


# ============================================================
# CONFIGURACIÓN DEL SCORE
# Tempo 120 BPM para loop de videojuego (estándar)
# ============================================================
score = Score("Traffic Loop - Guatemala", 120)

# ============================================================
# FRAGMENTO 1: RITMO - PERCUSIÓN POR TERCILES
# Mapea el estado del tráfico a 3 instrumentos percusivos
# ============================================================

# PERCUSIÓN 1: Tráfico FLUIDO (1-2) 
p_perc_low = Part("Perc_Fluido", GLOCKENSPIEL, 0)
phr_perc_low = Phrase(0.0)

# PERCUSIÓN 2: Tráfico MODERADO (3-4) 
p_perc_mid = Part("Perc_Moderado", STEEL_DRUMS, 1)
phr_perc_mid = Phrase(0.0)

for r in ritmo:
    # Duración: más tráfico = notas más largas
    dur = mapValue(r, min_r, max_r, SN, EN)
    
    # Pitch según intensidad
    pitch_low = mapScale(r, min_r, max_r, C5, C6, PENTATONIC_SCALE)
    pitch_mid = mapScale(r, min_r, max_r, C4, C5, MINOR_SCALE)
    
    # Dinámica moderada
    dyn_low = int(mapValue(r, min_r, max_r, 60, 90))
    dyn_mid = int(mapValue(r, min_r, max_r, 70, 100))
    
    # Asignar según tercil
    if r <= tercil_1:  # Tráfico bajo
        phr_perc_low.addNote(Note(pitch_low, dur, dyn_low))
    elif r <= tercil_2:  # Tráfico medio
        phr_perc_mid.addNote(Note(pitch_mid, dur, dyn_mid))
    # Si r > tercil_2 no añadimos nada aquí (se maneja en bajo)

p_perc_low.addPhrase(phr_perc_low)
p_perc_mid.addPhrase(phr_perc_mid)

# ============================================================
# FRAGMENTO 2: BAJO 
# Representa la intensidad del tráfico con énfasis en congestión
# ============================================================

p_bajo = Part("Bajo_Trafico", SYNTH_BASS1, 2)
phr_bajo = Phrase(0.0)

for r in ritmo:
    # Pitch: grave cuando hay congestión
    pitch = mapScale(r, min_r, max_r, C2, C3, CHROMATIC_SCALE)
    
    # Duración: congestión = notas largas (atasco)
    dur = mapValue(r, min_r, max_r, EN, HN)
    
    # Dinámica: ENFATIZAR congestión severa
    if r >= 4:  # Tráfico pesado/severo
        dyn = 110
    else:
        dyn = 75
    
    phr_bajo.addNote(Note(pitch, dur, dyn))

p_bajo.addPhrase(phr_bajo)

# ============================================================
# FRAGMENTO 3: MELODÍA 
# Representa las horas del día 
# ============================================================

p_melodia = Part("Melodia_Hora", SQUARE, 3)
phr_melodia = Phrase(0.0)

for i, m in enumerate(melodia):
    # Pitch: ascendente según hora
    pitch = mapScale(m, min_m, max_m, C4, C6, MAJOR_SCALE)
    
    # Duración sincronizada con ritmo
    r = ritmo[i % len(ritmo)]
    dur = mapValue(r, min_r, max_r, EN, QN)
    
    # Dinámica: horas pico más fuertes (12-16 hrs)
    if m >= 12:
        dyn = 95
    else:
        dyn = 75
    
    phr_melodia.addNote(Note(pitch, dur, dyn))

p_melodia.addPhrase(phr_melodia)

# ============================================================
# TEXTURA/ACOMPAÑAMIENTO: PAD ATMOSFÉRICO
# Crea ambiente con notas largas basadas en estado promedio
# ============================================================

p_pad = Part("Pad_Ambiente", WARM_PAD, 4)
phr_pad = Phrase(0.0)

# Agrupar ritmo en bloques de 8 para crear notas sostenidas
for i in range(0, len(ritmo), 8):
    bloque = ritmo[i:i+8]
    if len(bloque) == 0:
        break
    
    # Promedio del bloque
    promedio = sum(bloque) / len(bloque)
    
    # Pitch según intensidad promedio
    pitch = mapScale(promedio, min_r, max_r, C3, C5, DORIAN_SCALE)
    
    # Notas largas (whole note)
    phr_pad.addNote(Note(pitch, WN * 2, 60))

p_pad.addPhrase(phr_pad)

# ============================================================
# FX/AMBIENTE: ÉNFASIS EN CONGESTIÓN SEVERA
# Agrega impactos solo cuando tráfico = 5
# ============================================================

p_fx = Part("FX_Congestion", ORCHESTRA_HIT, 5)

time = 0.0
for r in ritmo:
    dur = mapValue(r, min_r, max_r, SN, HN)
    
    # Solo agregar FX cuando hay congestión máxima
    if r == 5:
        ph = Phrase(time)
        ph.addNote(Note(C2, QN, 120))  # Nota grave potente
        p_fx.addPhrase(ph)
    
    time += dur

# ============================================================
# CONSTRUCCIÓN FINAL Y EXPORTACIÓN
# Orden: Percusión → Bajo → Melodía → Texturas → FX
# ============================================================

score.addPart(p_perc_low)   # 1. Percusión ligera
score.addPart(p_perc_mid)   # 2. Percusión media
score.addPart(p_bajo)       # 3. Bajo
score.addPart(p_melodia)    # 4. Melodía
score.addPart(p_pad)        # 5. Pad/Ambiente
score.addPart(p_fx)         # 6. FX/Impactos

# ============================================================
# REPRODUCIR Y GUARDAR
# ============================================================
Play.midi(score)

# Para exportar a BandLab:
Write.midi(score, "traffic_loop.mid")