#!/usr/bin/env bash
# Regenera los PNG y SVG de todos los diagramas en local (nada se envía a internet).
#
# Uso (desde cualquier carpeta):
#   GRAPHVIZ_BIN=/ruta/carpeta/bin/de/graphviz bash renderizar.sh
#
# Herramientas:
#   - Graphviz 12+ (dot y neato).
#   - Python 3: generar_cu.py y generar_der.py escriben los .dot.
set -euo pipefail
cd "$(dirname "$0")"

: "${GRAPHVIZ_BIN:?Indique la carpeta bin de Graphviz en GRAPHVIZ_BIN}"
PYTHON="${PYTHON:-python}"
DOT="$GRAPHVIZ_BIN/dot"
NEATO="$GRAPHVIZ_BIN/neato"

# CU-00 a CU-05: posiciones fijas definidas en generar_cu.py (neato -n2 respeta las coordenadas)
(
  cd 01_casos_de_uso
  "$PYTHON" generar_cu.py
  for f in cu-0[0-5]-*.dot; do
    "$NEATO" -n2 -Tpng -Gdpi=150 "$f" -o "${f%.dot}.png"
    "$NEATO" -n2 -Tsvg "$f" -o "${f%.dot}.svg"
    echo "OK  $f"
  done
  # Las figuras de actor se incrustan en el SVG para que se abra en cualquier equipo.
  "$PYTHON" -c "import glob, generar_cu; [generar_cu.incrustar_imagenes(f) for f in glob.glob('cu-0[0-5]-*.svg')]"
  rm -rf __pycache__
)

# Entidad-relación
"$PYTHON" 02_entidad_relacion/generar_der.py
for f in 02_entidad_relacion/*.dot; do
  "$DOT" -Tsvg "$f" -o "${f%.dot}.svg"
  "$DOT" -Tpng -Gdpi=150 "$f" -o "${f%.dot}.png"
  echo "OK  $f"
done
