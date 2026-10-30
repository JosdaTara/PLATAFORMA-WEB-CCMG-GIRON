-- =====================================================================
-- Cambio de esquema: reportes de Casa de Vida y seguimiento de participantes
-- Fecha: 30/10/2026
--
-- Motivo:
--   RF13/RF14 piden asociar cada reporte a su Casa de Vida o Área, al periodo
--   que cubre y, en el reporte general del Supervisor, a los reportes de las
--   casas que lo componen. RF11 pide registrar el estado del seguimiento.
--
--   reporte.tipo_reporte:
--     CASA_VIDA    -> reporte semanal que el Líder o su equipo envían al Supervisor (RF14)
--     GENERAL_AREA -> reporte mensual que el Supervisor envía al Pastor (RF13)
-- =====================================================================

BEGIN;

ALTER TABLE public.reporte
    ADD COLUMN tipo_reporte character varying(20) DEFAULT 'CASA_VIDA' NOT NULL,
    ADD COLUMN id_casa_vida integer REFERENCES public.casa_vida(id_casa_vida),
    ADD COLUMN id_area integer REFERENCES public.area(id_area),
    ADD COLUMN fecha_inicio date,
    ADD COLUMN fecha_fin date,
    ADD COLUMN id_reporte_general integer REFERENCES public.reporte(id_reporte),
    ADD CONSTRAINT chk_reporte_tipo CHECK (
        (tipo_reporte = 'CASA_VIDA' AND id_casa_vida IS NOT NULL)
        OR (tipo_reporte = 'GENERAL_AREA' AND id_area IS NOT NULL AND id_reporte_general IS NULL)
    ),
    ADD CONSTRAINT chk_reporte_fechas CHECK (fecha_inicio IS NULL OR fecha_fin IS NULL OR fecha_inicio <= fecha_fin);

-- Un solo reporte por Casa de Vida y semana, y uno solo por Área y mes (RN06).
CREATE UNIQUE INDEX uq_reporte_casa_periodo ON public.reporte (id_casa_vida, periodo) WHERE tipo_reporte = 'CASA_VIDA';
CREATE UNIQUE INDEX uq_reporte_area_periodo ON public.reporte (id_area, periodo) WHERE tipo_reporte = 'GENERAL_AREA';
CREATE INDEX idx_reporte_general ON public.reporte (id_reporte_general);

ALTER TABLE public.seguimiento
    ADD COLUMN tipo character varying(20) DEFAULT 'VISITA' NOT NULL,
    ADD COLUMN estado character varying(15) DEFAULT 'ABIERTO' NOT NULL,
    ADD COLUMN actualizado_en timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    ADD CONSTRAINT chk_seguimiento_tipo CHECK (tipo IN ('VISITA', 'LLAMADA', 'CONSEJERIA', 'OTRO')),
    ADD CONSTRAINT chk_seguimiento_estado CHECK (estado IN ('ABIERTO', 'EN_PROCESO', 'CERRADO'));

COMMIT;
