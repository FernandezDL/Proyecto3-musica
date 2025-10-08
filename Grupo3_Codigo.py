# ================================================================
# Karen Jimena Hernández Ortega
# Diana Lucía Fernández Villatoro
# Daniel Esteban Morales Urizar
# ================================================================

from music import *

# ---------------------------- DATOS -----------------------------
ritmo = [
    5,5,5,5,5,5,5,5,2,2,2,3,3,3,3,2,2,4,4,4,4,4,4,3,3,3,3,3,4,4,3,3,1,1,4,4,5,5,5,5,
    4,3,3,3,3,4,4,4,4,1,1,4,4,4,4,5,5,3,3,3,4,4,3,3,3,3,1,1,3,3,4,4,3,4,4,4,4,4,4,3,
    3,2,3,3,4,4,3,3,2,3,3,4,4,4,4,4,4,2,3,3
]

# Rangos 
valor_min, valor_max = min(ritmo), max(ritmo)

# Paso
PASO = QN

# ---------------------- MAPEOS Y ESCALAS ------------------------
# Duraciones 
duracion_por_valor = {1: SN, 2: EN, 3: QN, 4: DQN, 5: HN}

# Modo D dórico (para melodía)
escala_d_dorica = [D4, E4, F4, G4, A4, B4, C5, D5]

def seleccionar_duracion(v):
    """Devuelve una duración musical basada en el valor."""
    return duracion_por_valor.get(int(v), EN)

def seleccionar_nota_melodia(v):
    """
    Elige nota de la escala dórica el valor.
    Para valores altos (>=4), sube una octava.
    """
    idx = (v - 1) % len(escala_d_dorica)
    base = escala_d_dorica[idx]
    if v >= 4:
        base += 12  # octava arriba
    return base

def acorde_desde_valor(v):
    """
    Mapea valores a acordes triada:
      1 → Dm  (D F A)
      2 → F   (F A C)
      3 → C   (C E G)
      4 → G   (G B D)
      5+→ Am  (A C E)
    """
    if v == 1: return [D4, F4, A4]
    if v == 2: return [F4, A4, C5]
    if v == 3: return [C4, E4, G4]
    if v == 4: return [G3, B3, D4]
    return [A3, C4, E4]

def energia_desde_valor(v):
    """
    Normaliza el valor a [0,1] para controlar dinámica/densidad.
    """
    if valor_max == valor_min:
        return 0.5
    return (v - valor_min) / float(valor_max - valor_min)

# ---------------------- PARTES / INSTRUMENTOS -------------------
# Melódicos
parte_ritmo   = Part("Ritmo_Snippet", XYLOPHONE, 0)  # ritmo (xilófono)
parte_melodia = Part("Melodia_DDoria", 0, 1)         # lead
parte_textura = Part("Textura_ArpPad", 1, 2)         # arpegio/pad
parte_bajo    = Part("Bajo_Raiz",      2, 3)         # raíz -12

# Percusión (GM canal 10 = 9 en 0-based)
parte_bateria = Part("Bateria_GM", 0, 9)
parte_shaker  = Part("Perc_Shaker", 0, 9)

# Notas estándar GM (percusión)
BOMBO           = 36  # Bass Drum 1
CAJA            = 38  # Acoustic Snare
CHARLES_CERRADO = 42  # Closed Hi-Hat
CHARLES_ABIERTO = 46  # Open Hi-Hat
SHAKER          = 82  # Shaker

# =========================== RITMO ===============================
# Mapea la secuencia a una escala mayor (C4..C6) con figuras de EN.
t = 0.0
for h in ritmo:
    pitch = mapScale(h, valor_min, valor_max, C4, C6, MAJOR_SCALE)
    frase = Phrase(t)
    frase.addNote(Note(pitch, EN, 80 if h < 12 else 95))
    parte_ritmo.addPhrase(frase)
    t += PASO

# ========================== MELODÍA ==============================
# Valores bajos cortos, altos más largos y fuertes.
t = 0.0
for v in ritmo:
    nota = seleccionar_nota_melodia(v)
    dur = EN if v in (1, 2) else QN
    vel = 85 + (5 if v >= 4 else 0)
    frase = Phrase(t)
    frase.addNote(Note(nota, dur, vel))
    parte_melodia.addPhrase(frase)
    t += PASO

# ========================== TEXTURA ==============================
# Para v<=2: arpegio rápido; si no, pad sostenido con el acorde completo.
t = 0.0
for v in ritmo:
    acorde = acorde_desde_valor(v)
    frase = Phrase(t)

    if v <= 2:
        # Arpegio breve para aire y movimiento en valores “suaves”.
        subdur = max(SN, seleccionar_duracion(v) / len(acorde))
        for nota in acorde:
            frase.addNote(Note(nota, subdur, 75))
    else:
        # Pad sostenido para “rellenar” y dar cuerpo cuando sube la energía.
        dur_pad = max(QN, seleccionar_duracion(v))
        for nota in acorde:
            frase.addNote(Note(nota, dur_pad, 68))

    parte_textura.addPhrase(frase)
    t += PASO

# ============================ BAJO ===============================
# Toca la raíz de cada acorde una octava abajo, en negras estables.
t = 0.0
for v in ritmo:
    raiz = acorde_desde_valor(v)[0] - 12
    frase = Phrase(t)
    frase.addNote(Note(raiz, QN, 80))
    parte_bajo.addPhrase(frase)
    t += PASO

# ========================== BATERÍA ==============================
# Patrón: charles a 8avos; caja en 2 y 4; bombo en 1 + “&” si hay acento.
t = 0.0
compas_idx = 0  # cuenta de negras; cada PASO = QN

for v in ritmo:
    # Charles: pulso y contratiempo; abre levemente en valores altos.
    frase_hh_1 = Phrase(t)
    frase_hh_1.addNote(Note(CHARLES_CERRADO, EN, 60))
    parte_bateria.addPhrase(frase_hh_1)

    frase_hh_2 = Phrase(t + EN)
    hh_pitch = CHARLES_ABIERTO if v >= 4 else CHARLES_CERRADO
    frase_hh_2.addNote(Note(hh_pitch, EN, 58))
    parte_bateria.addPhrase(frase_hh_2)

    # Caja en 2 y 4 (índices 1 y 3 en 0-based dentro del compás)
    if compas_idx % 4 in (1, 3):
        frase_caja = Phrase(t)
        frase_caja.addNote(Note(CAJA, QN, 90))
        parte_bateria.addPhrase(frase_caja)

    # Bombo en 1; refuerzo en el “&” si el valor es alto.
    if compas_idx % 4 == 0:
        frase_bombo_1 = Phrase(t)
        frase_bombo_1.addNote(Note(BOMBO, QN, 85))
        parte_bateria.addPhrase(frase_bombo_1)

    if v >= 5:
        frase_bombo_2 = Phrase(t + EN)
        frase_bombo_2.addNote(Note(BOMBO, EN, 78))
        parte_bateria.addPhrase(frase_bombo_2)

    t += PASO
    compas_idx += 1

# =========================== SHAKER ==============================
# 16avos constantes con microtiming y densidad/acentos por energía.
t = 0.0
for v in ritmo:
    e = energia_desde_valor(v)         
    base_vel = int(48 + 48 * e)        

    acentos = [
        base_vel + int(8 * e),         # fuerte
        base_vel - int(6 - 4 * e),     # flojo (un poco menos flojo con e)
        base_vel + int(10 * e),        # acentito que crece con e
        base_vel - int(10 - 8 * e)     # casi ghost salvo e alta
    ]

    micro = 0.03 * e * SN              # hasta ~3% de una semicorchea
    offsets = [0.0, micro, 0.0, micro]

    omitir_ultimo = (e < 0.25)

    for i in range(4):
        if omitir_ultimo and i == 3:
            continue
        vel = max(30, min(127, acentos[i])) 
        frase = Phrase(t + i * SN + offsets[i])
        frase.addNote(Note(SHAKER, SN, vel))
        parte_shaker.addPhrase(frase)

    t += PASO

# ====================== SCORE Y EXPORTACIÓN ======================
score = Score("traffic", 92)

for p in (parte_ritmo, parte_bajo, parte_textura, parte_melodia, parte_bateria, parte_shaker):
    score.addPart(p)

Write.midi(score, "trafficgt.mid")