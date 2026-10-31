# Informe de auditoría y corrección de diagramas ERS

**Proyecto:** Plataforma web para la gestión y seguimiento del Plan Vida Abundante, iglesia CCMG de Girón
**Documento auditado:** `DOCUMENTACION/02_requerimientos/IEEE_PLATAFORMA_WEB_CCMG_.docx` (ERS, IEEE 830, Revisión 2), sección 2.3
**Tipo:** SRS · **Fecha:** 31/10/2026
**Herramientas:** skills *Documentation Specialist* (flujo de auditoría) y *Diagrams* (selección y diseño de diagramas)

## Resumen ejecutivo

| Aspecto | Resultado |
|---|---|
| Calidad de los diagramas originales | Deficiente (Figura 1) y preliminar (Figura 2) |
| Recomendación | Revisión mayor: sustituir las Figuras 1 y 2 |
| Hallazgos | 7 críticos, 9 altos y 9 medios |
| Entregado | 6 diagramas de casos de uso y 5 vistas entidad-relación, en PNG, SVG y fuente editable |
| Validación | 28 de 28 RF cubiertos; 15 tablas y 32 FK idénticas a `esquema.sql`; renderizado sin errores |
| Pendiente | 9 observaciones que requieren decisión del equipo o del cliente (ver `OBSERVACIONES_PENDIENTES.md`) |

No se modificó código fuente, base de datos ni ningún documento original.

---

## Etapa 1. Auditoría: documentación examinada

| Documento | Contenido relevante | Estado |
|---|---|---|
| `IEEE_PLATAFORMA_WEB_CCMG_.docx` | Figura 1 (casos de uso) y Figura 2 (modelo conceptual de clases); RF01–RF28, RN01–RN25, HU-01–HU-44, CU01–CU06 | Auditado |
| `ERS_PVA.md` | Versión Markdown de la misma ERS. Solo contiene los pies de figura, sin imágenes ni fuente | Mismo contenido que el IEEE |
| `F-DC-125_Informe_final_..._Parte1.docx` | No contiene diagramas UML ni ER | Sin hallazgos |
| `DOCUMENTACION/03_diseno/base_datos/esquema.sql` y `cambios/*.sql` | Esquema real de PostgreSQL | Fuente de verdad del DER |
| `ccmg/apps/*/models.py`, `urls.py`, `views*.py`, `alcance.py`, `nucleo/mixins.py`, `nucleo/permissions.py` | Funcionalidades y permisos implementados | Fuente de verdad de actores y casos de uso |
| `DOCUMENTACION/03_diseno/uml/` | Primera corrección de esta sesión (v1) | Sustituida por esta entrega (v2) y eliminada |

---

## Etapa 2. Diagnóstico

Severidad según el flujo de auditoría de *Documentation Specialist*: **Crítico** = información incorrecta; **Alto** = cobertura incompleta; **Medio** = notación, consistencia o presentación.

### 2.1 Diagrama de casos de uso (Figura 1 original)

| # | Sev. | Hallazgo | Justificación |
|---|---|---|---|
| U1 | Crítico | Casos de uso compuestos: *Gestionar usuarios, roles y permisos*; *Consultar participantes, asistencia y reportes*; *Consultar asistencia y reportes de formación* | Un caso de uso es un objetivo. Agruparlos impide expresar que el usuario de apoyo no consulta el seguimiento, y rompe la trazabilidad 1:1 con RF06, RF10, RF11 y RF15 |
| U2 | Crítico | El usuario de apoyo aparece con las mismas consultas que el Líder, seguimiento incluido | RF11 y el código (`SeguimientoListView.dispatch`) excluyen al apoyo |
| U3 | Alto | Faltan funcionalidades reales: Gestionar Áreas (RN20), Importar datos (RF26), Exportar (RF27), Desactivar y reactivar (RF28), Seguimiento (RF11), Recuperar y cambiar contraseña (RF25), Panel por rol (RF23) | Cada una tiene vista y URL en el código |
| U4 | Alto | Iniciar y cerrar sesión solo figuran en una nota | Son RF01 y RF02 con su propio CU01. Una nota no es notación de caso de uso |
| U5 | Alto | Falta el Super Administrador | Rol real (fila 6 de `rol`), con función exclusiva: la bitácora de auditoría |
| U6 | Alto | Falta el responsable de ofrendas | RF17 y RN14 lo exigen; el código lo implementa con `usuario.responsable_ofrendas` |
| U7 | Alto | Líder y apoyo no consultan su Casa de Vida | RN04, RN05 y `CasaListView` (filtrada por `casas_visibles`) se lo permiten |
| U8 | Medio | *Llenar reporte* y *Enviar reporte* como pasos de un mismo formulario | En la plataforma son dos objetivos: registrar la asistencia de cada actividad (`asistencia_registrar`) y enviar el reporte semanal (`reporte_enviar_casa`) |
| U9 | Medio | *Generar reportes de formación* y *Consultar asistencia y reportes de formación* se solapan | Existe una sola vista: `formacion:reportes` |
| U10 | Medio | No se distingue que solo el Pastor desactiva procesos de formación | RF28, RN24 y `ProcesoEstadoView` |
| U11 | Medio | No hay ninguna relación «include» ni «extend» | Comportamientos obligatorios u opcionales quedan sin modelar |
| U12 | Medio | No hay generalización de actores; Aprendiz, Anfitrión y Maestro de Niños no aparecen | La ERS los lista como actores y el sistema los trata con un solo rol |

### 2.2 Modelo de datos (Figura 2 original)

| # | Sev. | Hallazgo | Corrección según `esquema.sql` |
|---|---|---|---|
| E1 | Crítico | Es un diagrama de clases conceptual: sin PK, FK ni tipos | DER lógico con PK, FK, UK, tipos, NOT NULL y CHECK |
| E2 | Crítico | Usuario 1 : N Área (supervisa) | 1 : 1 opcional. Índice único `uq_area_supervisor` |
| E3 | Crítico | Casa de Vida 1 : N Participante directa | N : M resuelta con `CASA_VIDA_MIEMBRO` (fecha de ingreso, estado; UK casa + participante) |
| E4 | Crítico | Escuela de Formación N : 1 Participante | N : M resuelta con `INSCRIPCION_FORMACION` |
| E5 | Crítico | Reporte 1 : N Asistencia | No existe esa FK. REPORTE se relaciona con USUARIO (envía, recibe), CASA_VIDA, AREA y consigo mismo (`id_reporte_general`) |
| E6 | Alto | Falta el equipo de apoyo de la Casa de Vida | `CASA_VIDA_EQUIPO`, con una sola Casa activa por usuario |
| E7 | Alto | "EscuelaFormación" sin coordinador | `PROCESO_FORMACION` con FK `id_coordinador` |
| E8 | Alto | Actividad solo ligada a formación | Arco exclusivo: casa XOR proceso (`chk_actividad_modulo`) |
| E9 | Alto | Falta AUDITORIA | Soporta RNF18 y la bitácora |
| E10 | Medio | Reporte con atributo `estado (enviado)` | No existe; el reporte existe solo cuando se envía |
| E11 | Medio | Asistencia con `fecha` | La fecha está en ACTIVIDAD; repetirla viola la 3FN |
| E12 | Medio | Seguimiento sin responsable ni proceso | FK a USUARIO (RN10) y a PROCESO_FORMACION |
| E13 | Medio | Atributos incompletos en Usuario, Ofrenda y estados de baja lógica | Se transcriben todos desde el esquema |

### 2.3 Primera corrección (v1, ya eliminada)

El contenido de la v1 era correcto, pero la presentación no cumplía los criterios visuales:

- Se renderizó con el motor interno de PlantUML (sin Graphviz): líneas cruzadas, generalizaciones enredadas y un recorte en la parte superior del DER.
- Un solo DER con 15 entidades y todos sus atributos: ilegible al tamaño de una página.
- La guía de diagramas de *Documentation Specialist* recomienda unos 16 nodos por figura como máximo y dividir las figuras saturadas.

---

## Etapa 3. Correcciones realizadas

### 3.1 Casos de uso (PlantUML, distribución con Graphviz)

| Figura | Archivo | Contenido | Decisiones |
|---|---|---|---|
| CU-00 | `cu-00-jerarquia-actores` | Generalización de actores | Separar la jerarquía libera a los demás diagramas de flechas de herencia. Reconcilia la ERS (Aprendiz, Anfitrión, Maestro de Niños) con el sistema (un rol `APOYO_CASA_VIDA`) |
| CU-01 | `cu-01-acceso-pagina-publica` | Acceso y página pública | `Iniciar sesión` «include» `Visualizar panel` (CU01 paso 4); `Recuperar contraseña` «extend» `Iniciar sesión` |
| CU-02 | `cu-02-administracion` | Usuarios, ofrendas, auditoría | `Gestionar usuarios` «include» `Asignar rol` (`id_rol` NOT NULL) |
| CU-03 | `cu-03-casas-vida-pastor` | Gestión del Pastor en el módulo PVA | `Desactivar / reactivar` «extend» las tres gestiones (RF28) |
| CU-04 | `cu-04-casas-vida-supervisor-equipo` | Supervisor y equipo de la Casa | Supervisor a la derecha y equipo a la izquierda: los casos de uso compartidos quedan en el centro y no se cruzan líneas. `Enviar reporte general` «include» `Consultar reportes` (CU03 paso 1) |
| CU-05 | `cu-05-escuelas-formacion` | Escuelas de Formación | `Desactivar proceso` es un caso de uso solo del Pastor, no un «extend»: un «extend» lo heredaría el Coordinador, que no tiene ese permiso |

Criterios de notación aplicados:

- Asociaciones actor y caso de uso sin flecha (navegabilidad no relevante), «include» y «extend» punteadas con la flecha hacia el caso de uso correcto.
- Actores abstractos en cursiva (UML 2.5).
- Cada caso de uso muestra los RF o RN que lo respaldan, para la trazabilidad.
- *Iniciar sesión* no se incluye en cada caso de uso: es una precondición.
- *Enviar reporte semanal* no incluye *Registrar actividad y asistencia*: se registra durante la semana y se envía después (precondición, CU02).

### 3.2 Entidad-relación (Graphviz DOT, generado desde un único modelo)

| Vista | Archivo | Contenido |
|---|---|---|
| DER-00 | `der-00-general` | Las 15 entidades agrupadas por módulo, solo con PK, UK y las FK de negocio |
| DER-01 | `der-01-seguridad-auditoria` | ROL, USUARIO, AUDITORIA con todos sus atributos |
| DER-02 | `der-02-casas-vida-estructura` | AREA, CASA_VIDA, CASA_VIDA_EQUIPO, CASA_VIDA_MIEMBRO, PARTICIPANTE, OFRENDA |
| DER-03 | `der-03-casas-vida-operacion` | ACTIVIDAD, ASISTENCIA, SEGUIMIENTO, REPORTE |
| DER-04 | `der-04-escuelas-formacion` | PROCESO_FORMACION, INSCRIPCION_FORMACION |

Decisiones:

- **Un solo modelo, varias vistas.** `generar_der.py` contiene las entidades y relaciones una sola vez y escribe los cinco `.dot`. Si cambia el esquema, se edita en un lugar y las cinco vistas quedan coherentes.
- **La vista general (DER-00) omite los tipos de dato** y usa letra más grande y menos separación, para que se lea en una página apaisada. Los tipos están en las vistas detalladas.
- **Cada atributo se detalla en una sola vista.** En las demás, la entidad aparece como *referencia* (borde punteado, cabecera gris, solo PK y las FK que usa esa vista).
- **El color de cabecera codifica el módulo** (azul seguridad, verde estructura PVA, naranja operación PVA, lila formación).
- **Notación de pata de gallo** (Information Engineering): `||` uno, `|o` cero o uno, `o{` cero o muchos. Cada relación sale de la fila de la PK y llega a la fila de la FK.
- **Línea punteada gris:** FK de trazabilidad (`creado_por`, `modificado_por`, `registrado_por`, `id_responsable`, `id_usuario_destino`) y la copia redundante `casa_vida.id_supervisor`. La vista general las omite para no saturarse.
- **Atributo en negrita = NOT NULL.** Las restricciones (CHECK, UK compuestas, valores permitidos) aparecen al pie de cada tabla.
- **Se usó Graphviz en lugar de Mermaid** (la opción por defecto de *Documentation Specialist* para ER): Mermaid no permite agrupar por módulo ni anclar relaciones a filas, y su distribución produjo un diagrama de 2.900 px de ancho con muchos cruces. *Diagrams* recomienda Graphviz para grafos complejos.

---

## Etapa 4. Validación

### 4.1 Sintaxis

Los 6 `.puml` y los 5 `.dot` se renderizan sin errores ni advertencias con PlantUML 1.2025.4 y Graphviz 12.2.1. Se revisó visualmente cada PNG: sin texto recortado, sin símbolos faltantes y sin líneas que atraviesen entidades.

### 4.2 Modelo de datos contra la base de datos

`02_entidad_relacion/validar_der.py` compara el modelo con `esquema.sql`:

```
Tablas comparadas: 15 · FK en BD (dominio): 32 · relaciones dibujadas: 32
  ✓ Sin diferencias entre el modelo y esquema.sql
```

Comprueba columnas, obligatoriedad (NOT NULL) y que cada FK tenga su relación con el destino correcto. En la primera ejecución detectó que `usuario.modificado_por` no tenía relación propia; se corrigió.

### 4.3 Cardinalidades

| Relación | Cardinalidad | Respaldo en el esquema |
|---|---|---|
| ROL – USUARIO | 1 : 0..N | `usuario.id_rol` NOT NULL |
| USUARIO – AREA (supervisa) | 0..1 : 0..1 | FK + índice único parcial `uq_area_supervisor` |
| AREA – CASA_VIDA | 0..1 : 0..N | `casa_vida.id_area` admite nulo |
| USUARIO – CASA_VIDA (lidera) | 0..1 : 0..N | `casa_vida.id_lider` admite nulo |
| CASA_VIDA ↔ USUARIO (equipo) | N : M vía CASA_VIDA_EQUIPO | UK (casa, usuario); UK (usuario) si activo |
| CASA_VIDA ↔ PARTICIPANTE | N : M vía CASA_VIDA_MIEMBRO | UK (casa, participante) |
| PROCESO_FORMACION ↔ PARTICIPANTE | N : M vía INSCRIPCION_FORMACION | UK (participante, proceso) |
| ACTIVIDAD ↔ PARTICIPANTE | N : M vía ASISTENCIA | UK (actividad, participante) |
| CASA_VIDA / PROCESO – ACTIVIDAD | 0..1 : 0..N (arco exclusivo) | `chk_actividad_modulo` |
| USUARIO – PROCESO_FORMACION | 1 : 0..N | `id_coordinador` NOT NULL |
| PARTICIPANTE – SEGUIMIENTO; USUARIO – SEGUIMIENTO | 1 : 0..N | FK NOT NULL (RN10) |
| USUARIO – REPORTE (envía) | 1 : 0..N | `id_usuario_envia` NOT NULL |
| CASA_VIDA – REPORTE; AREA – REPORTE | 0..1 : 0..N | `chk_reporte_tipo`; UK por periodo |
| REPORTE – REPORTE (agrupa) | 0..1 : 0..N | `id_reporte_general` |
| CASA_VIDA – OFRENDA; USUARIO – OFRENDA | 0..1 : 0..N | FK admiten nulo |
| USUARIO – AUDITORIA | 0..1 : 0..N | `auditoria.id_usuario` admite nulo |

### 4.4 Normalización

- **1FN:** atributos atómicos; los valores múltiples están en entidades asociativas.
- **2FN:** todas las tablas usan PK simple; las claves naturales compuestas son UK.
- **3FN:** se cumple salvo `casa_vida.id_supervisor` (dependencia transitiva casa → área → supervisor). Se representa marcada como redundante y se deja la decisión al equipo (observación O5).

### 4.5 Trazabilidad requisitos → casos de uso

Los 28 RF están cubiertos. Comprobación automática sobre las etiquetas de los `.puml`:

| RF | Diagramas | RF | Diagramas |
|---|---|---|---|
| RF01, RF02, RF23, RF24, RF25 | CU-01 | RF13, RF14 | CU-04 |
| RF03, RF04, RF17 | CU-02 | RF15 | CU-03, CU-04, CU-05 |
| RF05 | CU-03, CU-05 | RF16 | CU-03, CU-05 |
| RF06, RF08 | CU-04 | RF18 a RF22 | CU-05 |
| RF07, RF26 | CU-03 | RF27 | CU-02 a CU-05 |
| RF09, RF12 | CU-04, CU-05 | RF28 | CU-02, CU-03, CU-05 |
| RF10 | CU-03, CU-04 | RF11 | CU-03, CU-04, CU-05 |

### 4.6 Actores y permisos contra el código

| Caso de uso | Pastor | Super Adm. | Supervisor | Líder | Apoyo | Coordinador | Resp. ofrendas | Miembro Asist. | Control en el código |
|---|---|---|---|---|---|---|---|---|---|
| Consultar información pública | | | | | | | | ✔ | `publico:index`, sin sesión |
| Acceso (sesión, contraseña, panel) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | | `cuentas/urls.py` |
| Gestionar usuarios y asignar rol | ✔ | ✔ | | | | | | | `PastorRequiredMixin` |
| Consultar bitácora | | ✔ | | | | | | | `SuperAdminRequiredMixin` |
| Gestionar ofrendas | ✔ | ✔ | | | | | ✔ | | `puede_gestionar_ofrendas` |
| Gestionar Áreas, Casas, participantes PVA; importar; seguimiento PVA | ✔ | ✔ | | | | | | | `PastorCasasMixin` |
| Consultar Casas, participantes, asistencia, reportes | ✔ | ✔ | su Área | su Casa | su Casa | | | | `casas_visibles`, `CasaVidaScopeMixin` |
| Consultar seguimiento PVA | ✔ | ✔ | su Área | su Casa | | | | | `SeguimientoListView.dispatch` |
| Registrar actividad y asistencia (Casa) | | | | ✔ | ✔ | | | | `RegistrarAsistenciaView` |
| Enviar reporte semanal | | | | ✔ | ✔ | | | | `solo_roles(LIDER, APOYO)` |
| Enviar reporte general | | | ✔ | | | | | | `solo_roles(SUPERVISOR)` |
| Generar reporte consolidado | ✔ | ✔ | | | | | | | `solo_roles(PASTOR)` |
| Casos de uso de formación | ✔ | ✔ | | | | sus procesos | | | `PanelFormacionMixin`, `procesos_visibles` |
| Desactivar proceso | ✔ | ✔ | | | | | | | `ProcesoEstadoView` |

### 4.7 Coherencia entre modelos

| Comprobación | Resultado |
|---|---|
| Cada actor con cuenta tiene un valor en ROL o un atributo que lo soporte | ✔ Seis roles; responsable de ofrendas = `usuario.responsable_ofrendas`; Miembro Asistente no se almacena |
| Cada caso de uso que guarda datos tiene entidad | ✔ Usuarios → USUARIO, ROL; Áreas → AREA; Casas → CASA_VIDA, CASA_VIDA_EQUIPO; participantes → PARTICIPANTE, CASA_VIDA_MIEMBRO, INSCRIPCION_FORMACION; asistencia → ACTIVIDAD, ASISTENCIA; seguimiento → SEGUIMIENTO; reportes enviados → REPORTE; ofrendas → OFRENDA; baja lógica → `estado` o `activo`; bitácora → AUDITORIA |
| Casos de uso sin entidad propia | Consultas, generar reportes, exportar, panel, página pública. Calculan sobre datos existentes; es correcto |
| Entidades sin caso de uso | Ninguna |
| Módulos respetados | ✔ Cada diagrama corresponde a una app de Django; PARTICIPANTE, ACTIVIDAD y SEGUIMIENTO son compartidos, igual que en el código |

---

## Etapa 5. Entregables

```
documentacion_ERS/
├── README.md                          índice y cómo regenerar
├── renderizar.sh                      regenera PNG y SVG en local
├── 01_casos_de_uso/                   cu-00 … cu-05  (.puml, .png, .svg)
├── 02_entidad_relacion/               der-00 … der-04 (.dot, .png, .svg)
│   ├── generar_der.py                 modelo único → .dot
│   └── validar_der.py                 contraste con esquema.sql
└── 03_informe/
    ├── INFORME_CORRECCIONES.md        este informe
    └── OBSERVACIONES_PENDIENTES.md    dudas para el equipo y el cliente
```
