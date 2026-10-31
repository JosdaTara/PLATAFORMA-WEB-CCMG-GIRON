# Observaciones que requieren validación

Puntos donde la ERS, las reglas de negocio y el código no coinciden, o donde la información es ambigua. Los diagramas siguen el **funcionamiento real del sistema** y no toman decisiones que cambien el modelo. Cada punto indica quién debe decidir y qué se propone.

| # | Tema | Prioridad | Decide |
|---|---|---|---|
| O1 | Quién consulta y exporta reportes | Alta | Cliente y equipo |
| O2 | Participantes sin Casa de Vida | Alta | Cliente |
| O3 | Super Administrador fuera de la ERS | Media | Equipo |
| O4 | Responsable de ofrendas como actor | Media | Equipo |
| O5 | Columna redundante `casa_vida.id_supervisor` | Media | Equipo |
| O6 | Columnas sin uso en REPORTE | Baja | Equipo |
| O7 | Significado de "área" en RN12 | Baja | Equipo |
| O8 | El Pastor registra asistencia en formación | Baja | Cliente |
| O9 | Reemplazar el IEEE original por la copia corregida | Media | Equipo |
| O10 | Quién puede crear Administradores (resuelta; queda la edición de Administradores) | Media | Cliente |

---

### O1. Quién consulta y exporta reportes

- **RF15** lista como actores al Pastor, Supervisor, Líder y Coordinador.
- **RF27** (exportar) lista a Pastor, Supervisor, Líder y Coordinador.
- **HU-43** (exportar) lista solo a Pastor, Supervisor y Coordinador.
- **El código** deja consultar y exportar los reportes de su Casa también al **usuario de apoyo**; CU02 y HU-23 necesitan que el apoyo vea si el reporte ya fue enviado.

**Diagrama actual:** sigue al código (el equipo completo consulta y exporta).
**Propuesta:** añadir "usuarios de apoyo" a RF15 y RF27, y "Líder y usuarios de apoyo" a HU-43.

### O2. Participantes sin Casa de Vida

- **RN09** exige que todo participante tenga Casa de Vida. **HU-04** (criterio 3) dice lo mismo.
- **CU06** dice "asociado a su Casa de Vida **o** proceso de formación", y el Coordinador registra participantes de formación que pueden no pertenecer a ninguna Casa.
- **La base de datos** permite un participante sin membresía (la pertenencia está en `CASA_VIDA_MIEMBRO`, opcional).

**Diagrama actual:** PARTICIPANTE 1 : 0..N CASA_VIDA_MIEMBRO, como en la base de datos.
**Pregunta al cliente:** ¿un participante de Escuelas de Formación debe pertenecer siempre a una Casa de Vida? Si la respuesta es no, hay que corregir RN09 y HU-04. Si es sí, hay que exigirlo en el registro de formación.

### O3. Super Administrador fuera de la ERS

El rol `SUPERADMIN` existe en la base de datos y en el código, pero la ERS no lo describe en la sección 2.4 ni en ningún RF.

**Diagrama actual:** se incluye, justificado por `2026-10-31_rol_superadmin.sql` y `SuperAdminRequiredMixin`.
**Propuesta:** describirlo en 2.4 y crear un requisito para la bitácora de auditoría (hoy solo la respalda RNF18).

### O4. Responsable de ofrendas como actor

No es un rol sino un permiso (`usuario.responsable_ofrendas`) que el Pastor concede a un usuario de cualquier rol (RN14).

**Diagrama actual:** se modela como actor, porque UML define un actor como un *papel* que desempeña un usuario, no como un rol de la base de datos. Una nota en CU-00 aclara que no es un nivel de la jerarquía sino un permiso.
**A confirmar:** que el director del proyecto acepte esta representación.

### O5. Columna redundante `casa_vida.id_supervisor`

Repite `area.id_supervisor` (dependencia transitiva, viola la 3FN). El código no la usa como fuente de verdad (`nucleo/mixins.py`, `pva/alcance.py`) y la sincroniza a mano (`pva/forms.py`, `pva/views.py`).

**Diagrama actual:** se dibuja con línea punteada y la etiqueta "copia redundante".
**Propuesta:** eliminarla con una migración y obtener el supervisor por `casa.id_area.id_supervisor`. No se aplicó porque la tarea prohíbe cambiar la base de datos.

### O6. Columnas sin uso en REPORTE

- `reporte.tipo_modulo` siempre vale `CASA_VIDA`: los reportes de formación se calculan al momento y no se guardan.
- `reporte.ruta_archivo` no se escribe en ninguna parte del código: la exportación se genera bajo demanda.

**Diagrama actual:** se muestran tal como están en la base de datos (DER-03).
**Propuesta:** eliminarlas o documentar su uso futuro.

### O7. Significado de "área" en RN12

RN12 dice que cada proceso de formación "deberá estar asociado al **área** correspondiente, como Pasos de Vida, Escuelas Vida...". Aquí "área" significa *tipo de proceso*, no la entidad AREA del módulo PVA.

**Diagrama actual:** se modela como el atributo `tipo_proceso`, sin relación con AREA.
**Propuesta:** cambiar "área" por "tipo de proceso" en RN12 para evitar confusión con las Áreas de Casas de Vida.

### O8. El Pastor registra asistencia en formación

RF09 no incluye al Pastor entre los actores de *Registrar asistencia*, pero RF12, HU-06 y el código (`RegistrarActividadView`) le permiten registrar actividades y su asistencia en Escuelas de Formación.

**Diagrama actual:** el Pastor puede *Registrar asistencia de formación* en CU-05, porque ahí hereda del Coordinador, (no en el módulo PVA, donde el código no se lo permite).
**Propuesta:** añadir al Pastor a RF09 para Escuelas de Formación.

### O9. Qué figuras van en la ERS

Existen tres versiones de los diagramas:

1. Las originales, en `IEEE_PLATAFORMA_WEB_CCMG_.docx` (sin modificar).
2. La v1, que estaba en `DOCUMENTACION/03_diseno/uml/` (eliminada el 31/10/2026).
3. Esta entrega (v2), en `documentacion_ERS/`.

**Estado:** los diagramas vigentes ya están insertados en `IEEE_PLATAFORMA_WEB_CCMG_diagramas_corregidos.docx` (generada desde el original sin modificar): CU-01 (general) como Figura 1a, CU-00 (jerarquía) como Figura 1b y CU-02 a CU-05 (por módulo) como Figuras 1c a 1f; DER-00, DER-01, DER-02, DER-04 y DER-03 como Figuras 2a a 2e. Los diagramas por módulo y los entidad-relación van en páginas apaisadas para que el texto se lea. El diagrama general ocupa todo el ancho de una página vertical; en papel su letra queda pequeña (unos 4,5 puntos), así que conviene revisarlo en el PDF o en el SVG.
**Pendiente:** decidir si la copia corregida reemplaza al original.

### O10. Quién puede crear Administradores (resuelta el 31/10/2026)

- **Regla del cliente:** solo el Super Administrador crea Administradores y otros Super Administradores; el Administrador crea las cuentas de los niveles 3 a 5.
- **Antes:** el Administrador (Pastor) podía asignar el rol `PASTOR` a otro usuario, porque `UsuarioForm` solo le ocultaba el rol `SUPERADMIN`.
- **Corrección:** `UsuarioForm` (`cuentas/forms.py`) ya no ofrece el rol `PASTOR` a quien no es Super Administrador, ni al crear una cuenta ni al editarla. Como la lista de roles del formulario es la que valida el servidor, un envío manipulado con ese rol también se rechaza. Quien ya es Administrador conserva su rol al editar sus propios datos.
- **Pruebas:** `CreacionDeAdministradoresTests` (`cuentas/tests/test_superadmin.py`), con cinco casos: el Pastor no crea ni asciende Administradores, sigue creando los niveles inferiores y conserva su rol al editarse; el Super Administrador sí crea Administradores. Sin la corrección, los dos casos de la regla fallan. La suite completa (184 pruebas) pasa.

**Queda por decidir:** el Administrador todavía puede editar o desactivar a otro Administrador que ya exista, y cambiarle el rol a uno inferior. La regla del cliente habla de crear; si «gestiona todo» significa que solo el Super Administrador administra a los Administradores, hay que restringir también esas acciones.

---

## Restricciones respetadas

- No se agregaron funcionalidades: cada caso de uso tiene RF o RN y una vista en el código.
- No se agregaron entidades: las 15 son tablas reales; las tablas internas de Django (`auth_*`, `django_*`) se omiten por no ser del dominio.
- No se cambiaron reglas de negocio: las discrepancias quedan aquí para decisión.
- No se modificó código, base de datos ni documentos originales.
