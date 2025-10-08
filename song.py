# Traffic GT 
from music import *

# ========= DATOS =========
ritmo = [5,5,5,5,5,5,5,5,2,2,2,3,3,3,3,2,2,4,4,4,4,4,4,3,3,3,3,3,4,4,3,3,1,1,4,4,5,5,5,5,4,3,3,3,3,4,4,4,4,1,1,4,4,4,4,5,5,3,3,3,4,4,3,3,3,3,1,1,3,3,4,4,3,4,4,4,4,4,4,3,3,2,3,3,4,4,3,3,2,3,3,4,4,4,4,4,4,2,3,3]

# ========= TRÍO POR TERCILES (RITMO) =========
lo, hi = min(ritmo), max(ritmo)
t1 = lo + (hi - lo) / 3.0
t2 = lo + 2 * (hi - lo) / 3.0

p_lo = Part("Fluido",  FLUTE,    0)     # tercil bajo
p_md = Part("Medio",   CLARINET, 1)     # tercil medio
p_hi = Part("Alto",    HARP,     2)     # tercil alto

STEP = QN
t = 0.0
for x in ritmo:
    pitch = mapScale(x, lo, hi, C2, C6, PENTATONIC_SCALE)
    ph = Phrase(t); ph.addNote( Note(pitch, QN, 90) )
    if x <= t1:   p_lo.addPhrase(ph)
    elif x <= t2: p_md.addPhrase(ph)
    else:         p_hi.addPhrase(ph)
    t += STEP 

## ========= MELODÍA (HORA) =========
min_m, max_m = min(ritmo), max(ritmo)

# Melodía
p_mel = Part("MelodiaHora", XYLOPHONE, 3)
t = 0.0
for h in ritmo:
    pitch = mapScale(h, min_m, max_m, C4, C6, MAJOR_SCALE)
    ph = Phrase(t); ph.addNote( Note(pitch, EN, 80 if h < 12 else 95) )
    p_mel.addPhrase(ph)
    t += STEP  

## ========= TEXTURA =========


# Score final compacto
s = Score("Traffic GT", 100)
for p in (p_lo, p_md, p_hi, p_mel):
    s.addPart(p) 


Play.midi(s)
Write.midi(s, "traffic_gt_min_simple.mid")
