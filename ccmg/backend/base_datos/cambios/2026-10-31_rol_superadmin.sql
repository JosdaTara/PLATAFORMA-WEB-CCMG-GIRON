-- =====================================================================
-- Cambio de datos: rol Super Administrador
-- Fecha: 31/10/2026
--
--   Rol del desarrollador de la plataforma. Tiene todo lo del Pastor en
--   ambos módulos, más la bitácora de auditoría y la gestión de otros
--   Super Administradores. El Pastor no ve ni modifica estas cuentas.
--   No cambia el esquema: solo agrega una fila a la tabla rol.
-- =====================================================================

SET client_encoding = 'UTF8';

INSERT INTO public.rol (id_rol, nombre, descripcion, acceso_casas_vida, acceso_escuelas_formacion)
VALUES (6, 'SUPERADMIN', 'Super Administrador (desarrollador)', true, true)
ON CONFLICT (id_rol) DO NOTHING;

SELECT setval(pg_get_serial_sequence('public.rol', 'id_rol'), (SELECT MAX(id_rol) FROM public.rol));
