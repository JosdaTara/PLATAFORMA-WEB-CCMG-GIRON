# Documentación ERS: diagramas corregidos

Diagramas de casos de uso UML y modelo entidad-relación de la plataforma web PVA – CCMG Girón, auditados contra la ERS (IEEE 830), el código Django y el esquema de PostgreSQL.

- Informe completo: [03_informe/INFORME_CORRECCIONES.md](03_informe/INFORME_CORRECCIONES.md)
- Dudas pendientes: [03_informe/OBSERVACIONES_PENDIENTES.md](03_informe/OBSERVACIONES_PENDIENTES.md)

## Casos de uso (`01_casos_de_uso/`)

| Figura | Archivo | Contenido |
|---|---|---|
| CU-00 | `cu-00-jerarquia-actores` | Jerarquía de actores |
| **CU-01** | `cu-01-general` | **Diagrama general único** de la plataforma, con servidor, servicios de seguridad y sistemas externos |
| CU-02 | `cu-02-acceso-seguridad` | Acceso a la plataforma y servicios de seguridad |
| CU-03 | `cu-03-administracion` | Usuarios, ofrendas y auditoría |
| CU-04 | `cu-04-casas-vida` | Módulo PVA – Casas de Vida |
| CU-05 | `cu-05-escuelas-formacion` | Módulo Escuelas de Formación |

En todos los diagramas de casos de uso las personas están en una columna a la izquierda y los sistemas externos (servidor PostgreSQL, servidor de correo SMTP) a la derecha.

## Entidad-relación (`02_entidad_relacion/`)

| Vista | Archivo | Contenido |
|---|---|---|
| DER-00 | `der-00-general` | Modelo general por módulos (claves y relaciones de negocio) |
| DER-01 | `der-01-seguridad-auditoria` | ROL, USUARIO, AUDITORIA |
| DER-02 | `der-02-casas-vida-estructura` | Áreas, Casas de Vida, equipo, miembros, participantes, ofrendas |
| DER-03 | `der-03-casas-vida-operacion` | Actividades, asistencia, seguimiento, reportes |
| DER-04 | `der-04-escuelas-formacion` | Procesos e inscripciones de formación |

Cada diagrama tiene tres archivos: fuente editable (`.puml` o `.dot`), `.png` (150 ppp) y `.svg` (vectorial, recomendado para Word y PDF).

## Cómo editar y regenerar

- **Casos de uso:** CU-01 a CU-05 se editan en `01_casos_de_uso/generar_cu.py`. Cada actor y cada caso de uso tiene sus coordenadas; ahí se agregan casos, se cambian nombres o se mueven elementos. CU-00 se edita en su `.puml`.
- **Entidad-relación:** editar las tablas `ENTIDADES` y `RELACIONES` de `02_entidad_relacion/generar_der.py` y ejecutar `python validar_der.py` para comprobar que el modelo sigue igual a `esquema.sql`.
- **Regenerar todo** (en local, sin enviar nada a internet):

```bash
PLANTUML_JAR=/ruta/plantuml.jar GRAPHVIZ_BIN=/ruta/graphviz/bin bash renderizar.sh
```

Requiere Java, PlantUML 1.2025 o superior, Graphviz 12 o superior y Python 3.
