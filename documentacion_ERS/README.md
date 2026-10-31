# Documentación ERS: diagramas corregidos

Diagramas de casos de uso UML y modelo entidad-relación de la plataforma web PVA – CCMG Girón, auditados contra la ERS (IEEE 830), el código Django y el esquema de PostgreSQL.

- Informe completo: [03_informe/INFORME_CORRECCIONES.md](03_informe/INFORME_CORRECCIONES.md)
- Dudas pendientes: [03_informe/OBSERVACIONES_PENDIENTES.md](03_informe/OBSERVACIONES_PENDIENTES.md)

## Casos de uso (`01_casos_de_uso/`)

| Figura | Archivo | Contenido |
|---|---|---|
| CU-00 | `cu-00-jerarquia-actores` | Jerarquía de actores |
| CU-01 | `cu-01-acceso-pagina-publica` | Acceso a la plataforma y página pública |
| CU-02 | `cu-02-administracion` | Usuarios, ofrendas y auditoría |
| CU-03 | `cu-03-casas-vida-pastor` | Módulo PVA: gestión del Pastor |
| CU-04 | `cu-04-casas-vida-supervisor-equipo` | Módulo PVA: Supervisor de Área y equipo de la Casa |
| CU-05 | `cu-05-escuelas-formacion` | Módulo Escuelas de Formación |

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

- **Casos de uso:** editar el `.puml`. También se puede pegar en draw.io (*Organizar → Insertar → Avanzado → PlantUML*).
- **Entidad-relación:** editar las tablas `ENTIDADES` y `RELACIONES` de `02_entidad_relacion/generar_der.py` y ejecutar `python validar_der.py` para comprobar que el modelo sigue igual a `esquema.sql`.
- **Regenerar todo** (en local, sin enviar nada a internet):

```bash
PLANTUML_JAR=/ruta/plantuml.jar GRAPHVIZ_DOT=/ruta/dot bash renderizar.sh
```

Requiere Java, PlantUML 1.2025 o superior, Graphviz 12 o superior y Python 3.
