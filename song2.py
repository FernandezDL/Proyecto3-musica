# === JythonMusic / jMusic ===
# Asegúrate que tu entorno tenga jMusic/jythonMusic (from music import *)
from music import *

# ---------- DATASET ----------
ritmo = [5,5,5,5,5,5,5,5,2,2,2,3,3,3,3,2,2,4,4,4,4,4,4,3,3,3,3,3,4,4,3,3,1,1,4,4,5,5,5,5,4,3,3,3,3,4,4,4,4,1,1,4,4,4,4,5,5,3,3,3,4,4,3,3,3,3,1,1,3,3,4,4,3,4,4,4,4,4,4,3,3,2,3,3,4,4,3,3,2,3,3,4,4,4,4,4,4,2,3,3]

# ---------- MAPEOS ----------
DUR = {1: SN, 2: EN, 3: QN, 4: DQN, 5: HN}
# Escala D Dórico (D4=62)
d_dorian = [D4, E4, F4, G4, A4, B4, C5, D5]

# Utilidades
def pick_duration(v):
    return DUR.get(int(v), EN)

def pick_drum_pitch(v, i):
    if v % 2 == 0:
        return 42  # hi-hat en valores pares
    else:
        return 36 if (i % 2 == 0) else 38  # alterna kick/snare en impares

def pick_melody_pitch(v):
    idx = (v - 1) % len(d_dorian)
    base = d_dorian[idx]
    if v >= 4:
        base += 12  # sube 1 octava para valores altos
    return base

def chord_from_value(v):
    # 1→ Dm (D F A), 2→ F (F A C), 3→ C (C E G), 4→ G (G B D), 5→ Am (A C E)
    if v == 1:
        return [D4, F4, A4]
    elif v == 2:
        return [F4, A4, C5]
    elif v == 3:
        return [C4, E4, G4]
    elif v == 4:
        return [G3, B3, D4]
    else:
        return [A3, C4, E4]

# ---------- FRAGMENTO 1: RITMO (Percusión) ----------
def build_percussion(ritmo_vals, velocity=90):
    p = Phrase()
    for i, v in enumerate(ritmo_vals):
        dur = pick_duration(v)
        pit = pick_drum_pitch(v, i)
        n = Note(pit, dur, velocity)
        p.addNote(n)
    # Opcional: cierre de compás
    return p

# ---------- FRAGMENTO 2: MELODÍA ----------
def build_melody(ritmo_vals, base_vel=85):
    p = Phrase()
    for v in ritmo_vals:
        pitch = pick_melody_pitch(v)
        dur = EN if v in (1,2) else QN
        n = Note(pitch, dur, base_vel + (5 if v >= 4 else 0))
        p.addNote(n)
    return p

# ---------- FRAGMENTO 3: TEXTURA (Pads / Arpegio) ----------
def build_texture(ritmo_vals, as_arpeggio=True, vel_pad=70, vel_arp=75):
    p = Phrase()
    for v in ritmo_vals:
        dur = pick_duration(v)
        chord = chord_from_value(v)
        if as_arpeggio and v <= 2:
            # Arpegio rápido
            subdur = max(SN, dur / len(chord))
            for pit in chord:
                p.addNote(Note(pit, subdur, vel_arp))
        else:
            for pit in chord:
                p.addNote(Note(pit, max(QN, dur), vel_pad))
    return p

# ---------- ARMADO DEL LOOP (≥ 2 minutos) ----------
def build_loop(ritmo_vals, tempo_bpm=92):
    score = Score("Sonificacion Dataset", tempo_bpm)

    # Partes
    drums = Part("Drums", 0, 9)   
    lead  = Part("Lead", 0, 0)
    pad   = Part("Texture", 0, 1)
    bass  = Part("Bass", 0, 2)

    # Frases base
    ph_drums = build_percussion(ritmo_vals)
    ph_lead  = build_melody(ritmo_vals)
    ph_tex   = build_texture(ritmo_vals, as_arpeggio=True)

    # Bajo: tomar la fundamental de cada acorde por valores, con negras
    ph_bass = Phrase()
    for v in ritmo_vals:
        fund = chord_from_value(v)[0] - 12  # una octava abajo
        ph_bass.addNote(Note(fund, QN, 80))

    # Repetir hasta ≥ 120s
    # Calculamos duración aproximada de un ciclo
    temp_score = Score("tmp", tempo_bpm)
    temp_part = Part()
    temp_part.addPhrase(ph_drums.copy())
    temp_score.addPart(temp_part)
    cycle_seconds = temp_score.getEndTime()  # jMusic retorna en segundos

    repeats = int(120.0 / max(1.0, cycle_seconds)) + 1

    # Añadir frases repetidas a cada parte
    for _ in range(repeats):
        drums.addPhrase(ph_drums.copy())
        lead.addPhrase(ph_lead.copy())
        pad.addPhrase(ph_tex.copy())
        bass.addPhrase(ph_bass.copy())


    score.addPart(drums)
    score.addPart(bass)
    score.addPart(pad)
    score.addPart(lead)

    return score

# Construir y exportar
score = build_loop(ritmo, tempo_bpm=92)
Write.midi(score, "sonificacion_loop.mid")
print("Exportado: sonificacion_loop.mid")
