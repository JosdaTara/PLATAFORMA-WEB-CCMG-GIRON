"""Test runner que gestiona las tablas usuario/rol durante los tests."""
from django.test.runner import DiscoverRunner
from django.apps import apps
from django.db import connection


class CcmgTestRunner(DiscoverRunner):
    """Crea las tablas usuario y rol en la BD de test si no existen."""

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
        return old_config

    def teardown_databases(self, old_config, **kwargs):
        super().teardown_databases(old_config, **kwargs)
