# === COMBINADO EXACTO ===
# Ritmo = tu snippet (MAJOR_SCALE, EN, t += STEP)
# Melodía y Textura = del primer script (D dórico, arpegio/pad)
from music import *

# ---------- DATASET ----------
ritmo = [5,5,5,5,5,5,5,5,2,2,2,3,3,3,3,2,2,4,4,4,4,4,4,3,3,3,3,3,4,4,3,3,1,1,4,4,5,5,5,5,4,3,3,3,3,4,4,4,4,1,1,4,4,4,4,5,5,3,3,3,4,4,3,3,3,3,1,1,3,3,4,4,3,4,4,4,4,4,4,3,3,2,3,3,4,4,3,3,2,3,3,4,4,4,4,4,4,2,3,3]

# ---------- MAPEOS (melodía/textura del primer script) ----------
DUR = {1: SN, 2: EN, 3: QN, 4: DQN, 5: HN}
d_dorian = [D4, E4, F4, G4, A4, B4, C5, D5]

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

# ---------- SCORE Y EXPORT ----------
s = Score("Combinado_RitmoSnippet_MelTex", 92)
for p in (p_rhythm, p_bass, p_tex, p_lead):
    s.addPart(p)

Write.midi(s, "combinado_ritmo.mid")
print("Generado: combinado_ritmo.mid")
