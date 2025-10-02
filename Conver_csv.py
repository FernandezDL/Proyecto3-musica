import pandas as pd
import hashlib
from pathlib import Path

# --- Config ---
INPUT = "pmt_septiembre.csv"
OUTPUT = "pmt_simplificado.csv"

# --- Helpers ---
def to_int_hash(text: str) -> int:
    h = hashlib.md5(text.encode("utf-8")).digest()
    return int.from_bytes(h[:8], byteorder="big", signed=False)

df = pd.read_csv(INPUT, dtype=str, encoding="utf-8", engine="python")

df.columns = df.columns.str.strip().str.upper()

requeridas = {"FECHA", "HORA", "ESTADO", "NOMBRE"}
faltantes = requeridas - set(df.columns)
if faltantes:
    raise ValueError(f"Faltan columnas en el CSV: {sorted(faltantes)}")

for c in ["FECHA", "HORA", "ESTADO", "NOMBRE"]:
    df[c] = df[c].astype(str).str.strip()

combo = df["FECHA"] + "|" + df["HORA"] + "|" + df["ESTADO"]
df["clave_id"] = combo.apply(to_int_hash)
df["clave_id_norm"] = df["clave_id"] % 10000

codigos, uniques = pd.factorize(df["NOMBRE"], sort=False)
df["nombre_id"] = codigos + 1  # que inicie en 1

out = df[["clave_id_norm", "nombre_id"]].copy()

# Guardar
out.to_csv(OUTPUT, index=False)
