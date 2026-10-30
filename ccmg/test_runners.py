"""Test runner que gestiona las tablas usuario/rol durante los tests."""
from django.test.runner import DiscoverRunner
from django.apps import apps
from django.db import connection


class CcmgTestRunner(DiscoverRunner):
    """Crea las tablas usuario y rol en la BD de test si no existen."""

    def build_suite(self, test_labels=None, **kwargs):
        # Las apps viven en apps/ (sin __init__.py), así que el descubrimiento
        # por defecto desde la raíz no las encuentra: se busca allí directamente.
        if not test_labels:
            from django.conf import settings
            test_labels = [str(settings.APPS_DIR)]
        return super().build_suite(test_labels, **kwargs)

    def setup_databases(self, **kwargs):
        old_config = super().setup_databases(**kwargs)
        # Crear tablas rol y usuario en la BD de test si no existen
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS public.rol (
                    id_rol serial PRIMARY KEY,
                    nombre varchar(50) NOT NULL UNIQUE,
                    descripcion text,
                    acceso_casas_vida boolean DEFAULT false,
                    acceso_escuelas_formacion boolean DEFAULT false,
                    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS public.usuario (
                    id_usuario serial PRIMARY KEY,
                    nombre_completo varchar(150) NOT NULL,
                    correo varchar(150) NOT NULL UNIQUE,
                    username varchar(50) UNIQUE,
                    password_hash varchar(255) NOT NULL,
                    id_rol integer NOT NULL REFERENCES public.rol(id_rol),
                    activo boolean DEFAULT true,
                    intentos_fallidos integer DEFAULT 0,
                    bloqueado_hasta timestamp without time zone,
                    ultimo_acceso timestamp without time zone,
                    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                    actualizado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                    creado_por integer REFERENCES public.usuario(id_usuario),
                    modificado_por integer REFERENCES public.usuario(id_usuario)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS public.area (
                    id_area serial PRIMARY KEY,
                    nombre varchar(100) NOT NULL,
                    id_supervisor integer REFERENCES public.usuario(id_usuario),
                    estado varchar(10) DEFAULT 'ACTIVO',
                    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS public.casa_vida (
                    id_casa_vida serial PRIMARY KEY,
                    nombre varchar(100) NOT NULL,
                    id_area integer REFERENCES public.area(id_area),
                    id_lider integer REFERENCES public.usuario(id_usuario),
                    id_supervisor integer REFERENCES public.usuario(id_usuario),
                    direccion text,
                    estado varchar(10) DEFAULT 'ACTIVO',
                    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                    actualizado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS public.casa_vida_equipo (
                    id_casa_vida_equipo serial PRIMARY KEY,
                    id_casa_vida integer NOT NULL REFERENCES public.casa_vida(id_casa_vida),
                    id_usuario integer NOT NULL REFERENCES public.usuario(id_usuario),
                    funcion varchar(20) NOT NULL CHECK (funcion IN ('APRENDIZ', 'ANFITRION', 'MAESTRO_NINOS')),
                    activo boolean DEFAULT true NOT NULL,
                    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (id_casa_vida, id_usuario)
                );
            """)
            cursor.execute("""
                ALTER TABLE public.usuario ADD COLUMN IF NOT EXISTS debe_cambiar_password BOOLEAN DEFAULT FALSE NOT NULL;
            """)
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS uq_area_supervisor
                ON public.area (id_supervisor) WHERE id_supervisor IS NOT NULL;
            """)
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS uq_cve_usuario_activo
                ON public.casa_vida_equipo (id_usuario) WHERE activo;
            """)
        return old_config

    def teardown_databases(self, old_config, **kwargs):
        super().teardown_databases(old_config, **kwargs)
