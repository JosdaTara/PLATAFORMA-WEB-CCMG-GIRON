"""Contrasta el modelo de generar_der.py con el esquema real de PostgreSQL.

Comprueba, para cada tabla del dominio: que existan las mismas columnas, que coincida la
obligatoriedad (NOT NULL) y que cada FK del esquema esté dibujada como relación con el mismo
destino. Uso:  python validar_der.py   (sale con código 1 si encuentra diferencias)
"""
import re
import sys
from pathlib import Path

from generar_der import ENTIDADES, RELACIONES

AQUI = Path(__file__).parent
BD = AQUI.parent.parent / "DOCUMENTACION" / "03_diseno" / "base_datos"
sql = (BD / "esquema.sql").read_text(encoding="utf-8")

columnas = {}  # tabla -> {columna: not_null}
for tabla, cuerpo in re.findall(r"CREATE TABLE public\.(\w+) \((.*?)\n\);", sql, re.S):
    cols = {}
    for linea in cuerpo.splitlines():
        m = re.match(r"\s+(\w+) .*", linea)
        if m and not linea.strip().startswith("CONSTRAINT"):
            cols[m.group(1)] = "NOT NULL" in linea or m.group(1).startswith("id_") and "DEFAULT nextval" in linea
    columnas[tabla] = cols

fks = set()  # (tabla, columna, tabla_destino)
for tabla, col, destino in re.findall(
    r"ALTER TABLE ONLY public\.(\w+)\s+ADD CONSTRAINT \w+ FOREIGN KEY \((\w+)\) REFERENCES public\.(\w+)\(", sql
):
    fks.add((tabla, col, destino))

errores = []
for entidad, (_, atributos, _) in ENTIDADES.items():
    tabla = entidad.lower()
    if tabla not in columnas:
        errores.append(f"{entidad}: no existe en esquema.sql")
        continue
    modelo = {a[1]: a[3] for a in atributos}
    real = columnas[tabla]
    for c in real.keys() - modelo.keys():
        errores.append(f"{entidad}.{c}: está en la BD y falta en el diagrama")
    for c in modelo.keys() - real.keys():
        errores.append(f"{entidad}.{c}: está en el diagrama y no en la BD")
    for c in modelo.keys() & real.keys():
        es_pk = any(a[1] == c and a[0] == "PK" for a in atributos)
        if not es_pk and modelo[c] != real[c]:
            errores.append(f"{entidad}.{c}: NOT NULL diagrama={modelo[c]} BD={real[c]}")

dibujadas = {(r[2].lower(), r[3], r[0].lower()) for r in RELACIONES}
for fk in sorted(fks):
    if fk[0].upper() in ENTIDADES and fk not in dibujadas:
        errores.append(f"FK sin relación en el diagrama: {fk[0]}.{fk[1]} -> {fk[2]}")
for d in sorted(dibujadas - fks):
    errores.append(f"Relación dibujada sin FK en la BD: {d[0]}.{d[1]} -> {d[2]}")

print(f"Tablas comparadas: {len(ENTIDADES)} · FK en BD (dominio): "
      f"{sum(1 for f in fks if f[0].upper() in ENTIDADES)} · relaciones dibujadas: {len(RELACIONES)}")
if errores:
    print("\n".join("  ✗ " + e for e in errores))
    sys.exit(1)
print("  ✓ Sin diferencias entre el modelo y esquema.sql")
