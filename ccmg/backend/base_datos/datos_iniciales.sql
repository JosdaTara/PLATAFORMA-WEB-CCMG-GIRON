-- =====================================================================
-- Datos iniciales: roles del sistema (RF04, RN01)
-- Ejecutar una sola vez después de esquema.sql.
-- =====================================================================

SET client_encoding = 'UTF8';

INSERT INTO public.rol (id_rol, nombre, descripcion, acceso_casas_vida, acceso_escuelas_formacion) VALUES
    (1, 'PASTOR',                'Pastor / Administrador del Sistema',       true,  true),
    (2, 'SUPERVISOR_AREA',       'Supervisor de Área',                       true,  false),
    (3, 'LIDER_CASA_VIDA',       'Líder de Casa de Vida',                    true,  false),
    (4, 'APOYO_CASA_VIDA',       'Aprendiz / Anfitrión / Maestro de Niños',  true,  false),
    (5, 'COORDINADOR_FORMACION', 'Coordinador de Formación',                 false, true),
    (6, 'SUPERADMIN',            'Super Administrador (desarrollador)',      true,  true)
ON CONFLICT (id_rol) DO NOTHING;

SELECT setval(pg_get_serial_sequence('public.rol', 'id_rol'), (SELECT MAX(id_rol) FROM public.rol));
