-- =====================================================================
-- Cambio de esquema: quitar la columna redundante casa_vida.id_supervisor
-- Fecha: 04/11/2026
--
--   El Supervisor de una Casa de Vida es siempre el de su Área (RN03), así
--   que casa_vida.id_supervisor repetía area.id_supervisor: una dependencia
--   transitiva (casa → área → supervisor) que incumplía la tercera forma
--   normal y había que sincronizar a mano. La aplicación ya obtiene el
--   Supervisor desde el Área (CasaVida.supervisor), por lo que la columna
--   deja de usarse.
--
--   Antes de ejecutarlo, haga un respaldo:
--     pg_dump -U postgres -d CCMG_GIRON -f respaldo_antes_de_quitar_supervisor.sql
--   Uso:
--     psql -U postgres -d CCMG_GIRON -f cambios/2026-11-04_quitar_supervisor_casa_vida.sql
-- =====================================================================

SET client_encoding = 'UTF8';

BEGIN;

ALTER TABLE public.casa_vida DROP CONSTRAINT IF EXISTS casa_vida_id_supervisor_fkey;
ALTER TABLE public.casa_vida DROP COLUMN IF EXISTS id_supervisor;

COMMIT;
