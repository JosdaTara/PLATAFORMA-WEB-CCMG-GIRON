-- =====================================================================
-- Cambio de esquema: reporte de asistencia de las Casas de Vida por totales
-- Fecha: 17/11/2026
--
--   En las Casas de Vida las personas vienen y van, así que la asistencia
--   ya no se marca persona por persona: el Líder o su equipo llenan un
--   reporte con los totales de la reunión (asistentes, niños, nuevos,
--   conversiones, Escuelas de Formación, VEA, sábado, dominical y la
--   ofrenda). La tabla reporte_asistencia guarda esos totales y queda 1 a 1
--   con el reporte semanal que se envía al Supervisor (tabla reporte).
--
--   A una persona nueva solo se le toman nombre y teléfono, por eso el
--   documento de identidad del participante deja de ser obligatorio (sigue
--   siendo único cuando se registra, p. ej. en las Escuelas de Formación).
--
--   Antes de ejecutarlo, haga un respaldo:
--     pg_dump -U postgres -d CCMG_GIRON -f respaldo_antes_de_reporte_asistencia.sql
--   Uso:
--     psql -U postgres -d CCMG_GIRON -f cambios/2026-11-17_reporte_asistencia_totales.sql
-- =====================================================================

SET client_encoding = 'UTF8';

BEGIN;

ALTER TABLE public.participante ALTER COLUMN documento_identidad DROP NOT NULL;

CREATE TABLE IF NOT EXISTS public.reporte_asistencia (
    id_reporte integer PRIMARY KEY REFERENCES public.reporte(id_reporte),
    fecha date NOT NULL,
    id_lider integer REFERENCES public.usuario(id_usuario),
    lideres_servidores integer NOT NULL DEFAULT 0,
    asistentes integer NOT NULL DEFAULT 0,
    ninos integer NOT NULL DEFAULT 0,
    nuevos integer NOT NULL DEFAULT 0,
    conversiones integer NOT NULL DEFAULT 0,
    reconciliaciones integer NOT NULL DEFAULT 0,
    ausentes integer NOT NULL DEFAULT 0,
    pasos_vida integer NOT NULL DEFAULT 0,
    ciclo_conexion integer NOT NULL DEFAULT 0,
    modulo_liderazgo integer NOT NULL DEFAULT 0,
    seminario_biblico integer NOT NULL DEFAULT 0,
    vea integer NOT NULL DEFAULT 0,
    sabado integer,
    dominical integer NOT NULL DEFAULT 0,
    ofrenda numeric(12,2) NOT NULL DEFAULT 0,
    id_ofrenda integer REFERENCES public.ofrenda(id_ofrenda),
    CONSTRAINT reporte_asistencia_no_negativos CHECK (
        lideres_servidores >= 0 AND asistentes >= 0 AND ninos >= 0 AND nuevos >= 0
        AND conversiones >= 0 AND reconciliaciones >= 0 AND ausentes >= 0
        AND pasos_vida >= 0 AND ciclo_conexion >= 0 AND modulo_liderazgo >= 0
        AND seminario_biblico >= 0 AND vea >= 0 AND (sabado IS NULL OR sabado >= 0)
        AND dominical >= 0 AND ofrenda >= 0
    )
);

COMMENT ON TABLE public.reporte_asistencia IS
    'Totales de la reunión semanal de una Casa de Vida (RF09, RF14). 1 a 1 con reporte.';
COMMENT ON COLUMN public.reporte_asistencia.sabado IS
    'Solo para las Casas de Vida de las Áreas R21 y ZONAR21; NULL en las demás.';
COMMENT ON COLUMN public.reporte_asistencia.id_ofrenda IS
    'Registro que el reporte creó en el módulo de Ofrendas (NULL si la ofrenda fue 0).';

ALTER TABLE public.reporte_asistencia OWNER TO postgres;

COMMIT;
