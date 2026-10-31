-- =====================================================================
-- Cambio de esquema: ofrendas (RF17, RN14, HU-08)
-- Fecha: 30/10/2026
--
--   usuario.responsable_ofrendas: el Pastor autoriza expresamente a un
--   usuario como responsable de ofrendas (RN14).
--   ofrenda.valor > 0: no se guarda una ofrenda con valor menor o igual
--   a cero (criterio de aceptación 2 de HU-08).
--   ofrenda.actualizado_en y modificado_por: trazabilidad de correcciones (RNF18).
-- =====================================================================

BEGIN;

ALTER TABLE public.usuario
    ADD COLUMN responsable_ofrendas boolean DEFAULT false NOT NULL;

ALTER TABLE public.ofrenda
    ADD COLUMN actualizado_en timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN modificado_por integer REFERENCES public.usuario(id_usuario),
    ADD CONSTRAINT chk_ofrenda_valor CHECK (valor > 0);

CREATE INDEX idx_ofrenda_fecha ON public.ofrenda USING btree (fecha);

COMMIT;
