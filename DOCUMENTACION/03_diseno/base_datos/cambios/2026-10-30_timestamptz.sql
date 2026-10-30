-- =====================================================================
-- Cambio de esquema: columnas de fecha y hora a timestamp with time zone
-- Fecha: 30/10/2026
--
-- Motivo: Django trabaja con USE_TZ = True. Con columnas "timestamp without
-- time zone", al volver a guardar un registro el valor leído (en UTC) se
-- interpretaba como hora de Bogotá y se desplazaba 5 horas en cada edición.
--
-- Los valores existentes están en UTC (la zona del servidor y de la sesión
-- de Django es UTC), por eso se convierten con AT TIME ZONE 'UTC'.
-- Todo se ejecuta en una sola transacción.
-- =====================================================================

BEGIN;

ALTER TABLE public.actividad
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC';

ALTER TABLE public.area
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC';

ALTER TABLE public.asistencia
    ALTER COLUMN fecha_registro TYPE timestamp with time zone USING fecha_registro AT TIME ZONE 'UTC';

ALTER TABLE public.auditoria
    ALTER COLUMN fecha TYPE timestamp with time zone USING fecha AT TIME ZONE 'UTC';

ALTER TABLE public.casa_vida
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC',
    ALTER COLUMN actualizado_en TYPE timestamp with time zone USING actualizado_en AT TIME ZONE 'UTC';

ALTER TABLE public.casa_vida_equipo
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC';

ALTER TABLE public.ofrenda
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC';

ALTER TABLE public.participante
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC',
    ALTER COLUMN actualizado_en TYPE timestamp with time zone USING actualizado_en AT TIME ZONE 'UTC';

ALTER TABLE public.proceso_formacion
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC',
    ALTER COLUMN actualizado_en TYPE timestamp with time zone USING actualizado_en AT TIME ZONE 'UTC';

ALTER TABLE public.reporte
    ALTER COLUMN enviado_en TYPE timestamp with time zone USING enviado_en AT TIME ZONE 'UTC';

ALTER TABLE public.rol
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC';

ALTER TABLE public.seguimiento
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC';

ALTER TABLE public.usuario
    ALTER COLUMN creado_en TYPE timestamp with time zone USING creado_en AT TIME ZONE 'UTC',
    ALTER COLUMN actualizado_en TYPE timestamp with time zone USING actualizado_en AT TIME ZONE 'UTC',
    ALTER COLUMN ultimo_acceso TYPE timestamp with time zone USING ultimo_acceso AT TIME ZONE 'UTC',
    ALTER COLUMN bloqueado_hasta TYPE timestamp with time zone USING bloqueado_hasta AT TIME ZONE 'UTC';

COMMIT;
