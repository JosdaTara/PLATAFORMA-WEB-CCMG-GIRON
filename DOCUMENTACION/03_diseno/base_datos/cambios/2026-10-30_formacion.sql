-- =====================================================================
-- Cambio de esquema: Escuelas de Formación (RF18–RF22)
-- Fecha: 30/10/2026
--
--   seguimiento.id_proceso_formacion: el seguimiento que registra el
--   Coordinador queda asociado al proceso, para que los reportes de cada
--   proceso muestren solo su información (HU-27, HU-30, HU-33, HU-36).
-- =====================================================================

BEGIN;

ALTER TABLE public.seguimiento
    ADD COLUMN id_proceso_formacion integer REFERENCES public.proceso_formacion(id_proceso_formacion),
    ADD CONSTRAINT chk_seguimiento_proceso CHECK (
        tipo_modulo <> 'ESCUELAS_FORMACION' OR id_proceso_formacion IS NOT NULL
    );

CREATE INDEX idx_seguimiento_proceso ON public.seguimiento USING btree (id_proceso_formacion);
CREATE INDEX idx_actividad_proceso ON public.actividad USING btree (id_proceso_formacion);
CREATE INDEX idx_inscripcion_proceso ON public.inscripcion_formacion USING btree (id_proceso_formacion);

COMMIT;
