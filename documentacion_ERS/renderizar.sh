#!/usr/bin/env bash
# Regenera los PNG y SVG de todos los diagramas en local (nada se envía a internet).
#
# Uso (desde cualquier carpeta):
#   PLANTUML_JAR=/ruta/plantuml.jar GRAPHVIZ_BIN=/ruta/carpeta/bin/de/graphviz bash renderizar.sh
#
# Herramientas:
#   - Graphviz 12+ (dot y neato): casos de uso CU-01 a CU-05 y diagramas entidad-relación.
#   - PlantUML 1.2025+ con Graphviz: jerarquía de actores CU-00 (.puml).
#   - Python 3: generar_cu.py y generar_der.py escriben los .dot.
set -euo pipefail
cd "$(dirname "$0")"

: "${PLANTUML_JAR:?Indique la ruta de plantuml.jar en PLANTUML_JAR}"
: "${GRAPHVIZ_BIN:?Indique la carpeta bin de Graphviz en GRAPHVIZ_BIN}"
PYTHON="${PYTHON:-python}"
DOT="$GRAPHVIZ_BIN/dot"
NEATO="$GRAPHVIZ_BIN/neato"
# En Windows, PlantUML (Java) necesita el nombre completo del ejecutable.
[ -f "$DOT.exe" ] && DOT="$DOT.exe" && NEATO="$NEATO.exe"

# CU-00: jerarquía de actores (PlantUML)
java -jar "$PLANTUML_JAR" -charset UTF-8 -graphvizdot "$DOT" -Sdpi=150 -tpng 01_casos_de_uso/cu-00-jerarquia-actores.puml
java -jar "$PLANTUML_JAR" -charset UTF-8 -graphvizdot "$DOT" -tsvg 01_casos_de_uso/cu-00-jerarquia-actores.puml
echo "OK  cu-00-jerarquia-actores"

# CU-01 a CU-05: posiciones fijas definidas en generar_cu.py (neato -n2 respeta las coordenadas)
(
  cd 01_casos_de_uso
  "$PYTHON" generar_cu.py
  for f in cu-0[1-5]-*.dot; do
    "$NEATO" -n2 -Tpng -Gdpi=150 "$f" -o "${f%.dot}.png"
    "$NEATO" -n2 -Tsvg "$f" -o "${f%.dot}.svg"
    echo "OK  $f"
  done
  # Las figuras de actor se incrustan en el SVG para que se abra en cualquier equipo.
  "$PYTHON" -c "import glob, generar_cu; [generar_cu.incrustar_imagenes(f) for f in glob.glob('cu-0[1-5]-*.svg')]"
  rm -rf __pycache__
)

# Entidad-relación
"$PYTHON" 02_entidad_relacion/generar_der.py
for f in 02_entidad_relacion/*.dot; do
  "$DOT" -Tsvg "$f" -o "${f%.dot}.svg"
  "$DOT" -Tpng -Gdpi=150 "$f" -o "${f%.dot}.png"
  echo "OK  $f"
done
