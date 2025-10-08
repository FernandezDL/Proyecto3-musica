# === COMBINADO EXACTO ===
# Ritmo = tu snippet (MAJOR_SCALE, EN, t += STEP)
# Melodía y Textura = del primer script (D dórico, arpegio/pad)
from music import *

# ---------- DATASET ----------
ritmo = [5,5,5,5,5,5,5,5,2,2,2,3,3,3,3,2,2,4,4,4,4,4,4,3,3,3,3,3,4,4,3,3,1,1,4,4,5,5,5,5,4,3,3,3,3,4,4,4,4,1,1,4,4,4,4,5,5,3,3,3,4,4,3,3,3,3,1,1,3,3,4,4,3,4,4,4,4,4,4,3,3,2,3,3,4,4,3,3,2,3,3,4,4,4,4,4,4,2,3,3]

# ---------- MAPEOS (melodía/textura del primer script) ----------
DUR = {1: SN, 2: EN, 3: QN, 4: DQN, 5: HN}
d_dorian = [D4, E4, F4, G4, A4, B4, C5, D5]

# --- NUEVAS PARTES DE PERCUSIÓN ---
p_drums  = Part("Drums_Kit", 0, 9)     # canal 10 GM = 9 (0-based)
p_shkr   = Part("Perc_Shaker", 0, 9)

# GM Percussion (canal 10)
KICK = 36           # Bass Drum 1
SNARE = 38          # Acoustic Snare
HH_CLOSED = 42      # Closed Hi-Hat
HH_OPEN = 46        # Open Hi-Hat
SHAKER = 82         # Shaker

def pick_duration(v):
    return DUR.get(int(v), EN)

def pick_melody_pitch(v):
    idx = (v - 1) % len(d_dorian)
    base = d_dorian[idx]
    if v >= 4:
        base += 12  # octava arriba para valores altos
    return base

def chord_from_value(v):
    # 1→ Dm (D F A), 2→ F (F A C), 3→ C (C E G), 4→ G (G B D), 5→ Am (A C E)
    if v == 1: return [D4, F4, A4]
    if v == 2: return [F4, A4, C5]
    if v == 3: return [C4, E4, G4]
    if v == 4: return [G3, B3, D4]
    return [A3, C4, E4]

# ---------- PARTES ----------
p_rhythm = Part("RitmoSnippet", XYLOPHONE, 0)  # tu ritmo
p_lead   = Part("Lead_DDorian",  0, 1)        # melodía (script 1)
p_tex    = Part("Texture_ArpPad",1, 2)        # textura (script 1)
p_bass   = Part("Bass_Root",     2, 3)        # bajo raíz -12

# ---------- RITMO (TU SNIPPET, SIN CAMBIOS) ----------
min_m, max_m = min(ritmo), max(ritmo)
STEP = QN
t = 0.0
for h in ritmo:
    pitch = mapScale(h, min_m, max_m, C4, C6, MAJOR_SCALE)
    ph = Phrase(t); ph.addNote( Note(pitch, EN, 80 if h < 12 else 95) )
    p_rhythm.addPhrase(ph)
    t += STEP

# ---------- MELODÍA (del primer script; misma grilla de tiempo) ----------
t2 = 0.0
for v in ritmo:
    pit = pick_melody_pitch(v)
    dur = EN if v in (1,2) else QN
    ph = Phrase(t2); ph.addNote(Note(pit, dur, 85 + (5 if v >= 4 else 0)))
    p_lead.addPhrase(ph)
    t2 += STEP

# ---------- TEXTURA (del primer script; misma grilla) ----------
t3 = 0.0
for v in ritmo:
    chord = chord_from_value(v)
    if v <= 2:
        # arpegio rápido
        subdur = max(SN, pick_duration(v) / len(chord))
        ph = Phrase(t3)
        for pit in chord:
            ph.addNote(Note(pit, subdur, 75))
        p_tex.addPhrase(ph)
    else:
        # pad sostenido
        ph = Phrase(t3)
        dur_pad = max(QN, pick_duration(v))
        for pit in chord:
            ph.addNote(Note(pit, dur_pad, 68))
        p_tex.addPhrase(ph)
    t3 += STEP

# ---------- BAJO: raíz del acorde -12, negras ----------
t4 = 0.0
for v in ritmo:
    root = chord_from_value(v)[0] - 12
    phb = Phrase(t4); phb.addNote(Note(root, QN, 80))
    p_bass.addPhrase(phb)
    t4 += STEP

# --- NUEVAS PARTES DE PERCUSIÓN ---
p_drums  = Part("Drums_Kit", 0, 9)     # canal 10 GM = 9 (0-based)
p_shkr   = Part("Perc_Shaker", 0, 9)

# GM Percussion (canal 10)
KICK = 36           # Bass Drum 1
SNARE = 38          # Acoustic Snare
HH_CLOSED = 42      # Closed Hi-Hat
HH_OPEN = 46        # Open Hi-Hat
SHAKER = 82         # Shaker

# --- PATRÓN 1: Batería (hi-hat 8avos, caja en 2 y 4, bombo básico) ---
t_d = 0.0
beat_idx = 0  # cuenta de negras (cada STEP = QN)
for v in ritmo:
    # Hi-hat en 8avos: en el pulso y el "and"
    ph_hh_1 = Phrase(t_d);     ph_hh_1.addNote(Note(HH_CLOSED, EN, 60))
    ph_hh_2 = Phrase(t_d + EN); 
    # abre un poco el hi-hat cuando el valor es alto para dar variación
    hh_pitch = HH_OPEN if v >= 4 else HH_CLOSED
    ph_hh_2.addNote(Note(hh_pitch, EN, 58))
    p_drums.addPhrase(ph_hh_1); p_drums.addPhrase(ph_hh_2)

    # Caja en 2 y 4 (contando beats 1..4 → índices 1 y 3 en 0-based)
    if beat_idx % 4 in (1, 3):
        ph_sn = Phrase(t_d); ph_sn.addNote(Note(SNARE, QN, 90))
        p_drums.addPhrase(ph_sn)

    # Bombo: en el 1 y opcional en el "and" si el valor es grande
    if beat_idx % 4 == 0:
        ph_k1 = Phrase(t_d); ph_k1.addNote(Note(KICK, QN, 85))
        p_drums.addPhrase(ph_k1)
    if v >= 5:  # acento extra cuando el número es alto
        ph_k2 = Phrase(t_d + EN); ph_k2.addNote(Note(KICK, EN, 78))
        p_drums.addPhrase(ph_k2)

    t_d += STEP
    beat_idx += 1

# --- PATRÓN 2: Shaker (16avos constantes con leve acentuación) ---
t_s = 0.0
for v in ritmo:
    # cuatro 16avos dentro de cada negra (STEP = QN)
    accents = [62, 55, 58, 55]  # acento suave en el primero y tercero
    for i in range(4):
        ph = Phrase(t_s + i * SN)
        # un pelín más fuerte cuando v es grande
        vel = accents[i] + (4 if v >= 4 else 0)
        ph.addNote(Note(SHAKER, SN, vel))
        p_shkr.addPhrase(ph)
    t_s += STEP
    
# ---------- SCORE Y EXPORT ----------
s = Score("Combinado_RitmoSnippet_MelTex", 92)
for p in (p_rhythm, p_bass, p_tex, p_lead):
    s.addPart(p)

s.addPart(p_drums)
s.addPart(p_shkr)

Write.midi(s, "combinado_ritmo2.mid")
print("Generado: combinado_ritmo.mid")
