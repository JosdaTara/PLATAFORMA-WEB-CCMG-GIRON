#!/usr/bin/env bash
# Regenera los PNG y SVG de todos los diagramas en local (nada se envía a internet).
#
# Uso (desde cualquier carpeta):
#   PLANTUML_JAR=/ruta/plantuml.jar GRAPHVIZ_DOT=/ruta/dot bash renderizar.sh
#
# Herramientas:
#   - PlantUML 1.2025+ (casos de uso, .puml), con Graphviz como motor de distribución.
#   - Graphviz 12+ (diagramas entidad-relación, .dot).
#   - Python 3 (generar_der.py escribe los .dot a partir del modelo transcrito de esquema.sql).
set -euo pipefail
cd "$(dirname "$0")"

: "${PLANTUML_JAR:?Indique la ruta de plantuml.jar en PLANTUML_JAR}"
: "${GRAPHVIZ_DOT:?Indique la ruta de dot (Graphviz) en GRAPHVIZ_DOT}"
PYTHON="${PYTHON:-python}"

for f in 01_casos_de_uso/*.puml; do
  java -jar "$PLANTUML_JAR" -charset UTF-8 -graphvizdot "$GRAPHVIZ_DOT" -Sdpi=150 -tpng "$f"
  java -jar "$PLANTUML_JAR" -charset UTF-8 -graphvizdot "$GRAPHVIZ_DOT" -tsvg "$f"
  echo "OK  $f"
done

"$PYTHON" 02_entidad_relacion/generar_der.py
for f in 02_entidad_relacion/*.dot; do
  "$GRAPHVIZ_DOT" -Tsvg "$f" -o "${f%.dot}.svg"
  "$GRAPHVIZ_DOT" -Tpng -Gdpi=150 "$f" -o "${f%.dot}.png"
  echo "OK  $f"
done
