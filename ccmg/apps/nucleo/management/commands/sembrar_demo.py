"""Siembra usuarios y datos de ejemplo en la base de demostración.

Solo se ejecuta si el nombre de la base contiene «demo», para no tocar datos reales.
Todos los usuarios de demostración usan el dominio demo.test y la contraseña CLAVE_DEMO.
"""
import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from cuentas.models import Rol, Usuario
from formacion.models import InscripcionFormacion, ProcesoFormacion
from ofrendas.models import Ofrenda
from pva import periodos
from pva.models import (
    Actividad, Area, Asistencia, CasaVida, CasaVidaEquipo, CasaVidaMiembro, Participante, Reporte, Seguimiento,
)

CLAVE_DEMO = "DemoCCMG-Revision-2026"

USUARIOS = [
    ("pastor@demo.test", "Pastor Demo", "PASTOR"),
    ("supervisor@demo.test", "Carlos Supervisor", "SUPERVISOR_AREA"),
    ("lider@demo.test", "María Líder", "LIDER_CASA_VIDA"),
    ("apoyo@demo.test", "Pedro Anfitrión", "APOYO_CASA_VIDA"),
    ("coordinador@demo.test", "Laura Coordinadora", "COORDINADOR_FORMACION"),
]


class Command(BaseCommand):
    help = "Crea usuarios y datos de ejemplo en la base de demostración (config.settings.demo)."

    def handle(self, *args, **options):
        nombre_bd = connection.settings_dict["NAME"] or ""
        if "demo" not in nombre_bd.lower():
            raise CommandError(f"La base «{nombre_bd}» no es de demostración. Use --settings=config.settings.demo.")
        if Usuario.objects.filter(correo__endswith="@demo.test").exists():
            raise CommandError("La base de demostración ya tiene datos sembrados.")
        if not Rol.objects.exists():
            raise CommandError("La tabla rol está vacía; copie los roles antes de sembrar.")

        with transaction.atomic():
            self.sembrar()
        self.stdout.write(self.style.SUCCESS(f"Datos de demostración creados en «{nombre_bd}»."))
        self.stdout.write("Usuarios: " + ", ".join(c for c, _, _ in USUARIOS) + " (contraseña: CLAVE_DEMO en este archivo).")

    def sembrar(self):
        u = {}
        for correo, nombre, rol in USUARIOS:
            u[rol] = Usuario.objects.create_user(correo=correo, nombre_completo=nombre, rol=Rol.objects.get(nombre=rol), password=CLAVE_DEMO)
        hoy = datetime.date.today()
        semana_pasada = periodos.semana(hoy - datetime.timedelta(weeks=1))

        norte = Area.objects.create(nombre="Norte", id_supervisor=u["SUPERVISOR_AREA"])
        sur = Area.objects.create(nombre="Sur")
        esperanza = CasaVida.objects.create(
            nombre="Casa Esperanza", id_area=norte, id_lider=u["LIDER_CASA_VIDA"], id_supervisor=u["SUPERVISOR_AREA"],
            direccion="Calle 10 # 5-20, Girón",
        )
        fe = CasaVida.objects.create(nombre="Casa Fe", id_area=sur, direccion="Carrera 8 # 12-30, Girón")
        CasaVidaEquipo.objects.create(id_casa_vida=esperanza, id_usuario=u["APOYO_CASA_VIDA"], funcion="ANFITRION")

        personas = [
            ("Ana María Pérez", "1095000001", esperanza, True),
            ("José Núñez", "1095000002", esperanza, True),
            ("Lucía Gómez", "1095000003", esperanza, True),
            ("Andrés Rojas", "1095000004", esperanza, False),
            ("Sofía Martínez", "1095000005", fe, True),
            ("Tomás Herrera", "1095000006", fe, True),
        ]
        participantes = []
        for i, (nombre, doc, casa, autoriza) in enumerate(personas):
            p = Participante.objects.create(
                nombres_apellidos=nombre, documento_identidad=doc, fecha_nacimiento=datetime.date(1985 + i, 3, 10),
                telefono=f"30012345{i:02d}", direccion="Girón, Santander", autorizacion_datos=autoriza,
            )
            CasaVidaMiembro.objects.create(id_casa_vida=casa, id_participante=p, fecha_ingreso=hoy - datetime.timedelta(days=60))
            participantes.append(p)

        reunion = Actividad.objects.create(
            id_casa_vida=esperanza, titulo="Reunión semanal", fecha=semana_pasada.inicio + datetime.timedelta(days=2),
            id_responsable=u["LIDER_CASA_VIDA"], descripcion="Estudio y oración.",
        )
        for i, p in enumerate(participantes[:4]):
            Asistencia.objects.create(id_actividad=reunion, id_participante=p, presente=i != 2, registrado_por=u["LIDER_CASA_VIDA"])
        Reporte.objects.create(
            tipo_modulo="CASA_VIDA", tipo_reporte="CASA_VIDA", id_usuario_envia=u["LIDER_CASA_VIDA"],
            id_usuario_destino=u["SUPERVISOR_AREA"], id_casa_vida=esperanza, id_area=norte,
            periodo=semana_pasada.etiqueta, fecha_inicio=semana_pasada.inicio, fecha_fin=semana_pasada.fin,
            observaciones="Buena participación. Lucía estuvo enferma; se programó una visita.",
        )
        Seguimiento.objects.create(
            id_participante=participantes[2], id_usuario=u["PASTOR"], tipo="VISITA", estado="ABIERTO",
            observacion="Visita por enfermedad. Pendiente llamada de seguimiento.", tipo_modulo="CASA_VIDA",
        )

        escuela = ProcesoFormacion.objects.create(
            nombre="Escuela Vida Nivel 1 – 2026", tipo_proceso="ESCUELAS_VIDA", id_coordinador=u["COORDINADOR_FORMACION"],
            descripcion="Primer nivel de formación para nuevos creyentes.",
        )
        ProcesoFormacion.objects.create(nombre="Pasos de Vida – 2026", tipo_proceso="PASOS_VIDA", id_coordinador=u["COORDINADOR_FORMACION"])
        for p in participantes[:3]:
            InscripcionFormacion.objects.create(id_participante=p, id_proceso_formacion=escuela)
        clase = Actividad.objects.create(
            tipo_modulo="ESCUELAS_FORMACION", id_proceso_formacion=escuela, titulo="Clase 1: Fundamentos",
            fecha=hoy - datetime.timedelta(days=3), id_responsable=u["COORDINADOR_FORMACION"],
        )
        for i, p in enumerate(participantes[:3]):
            Asistencia.objects.create(id_actividad=clase, id_participante=p, presente=i < 2, registrado_por=u["COORDINADOR_FORMACION"])

        Ofrenda.objects.create(fecha=semana_pasada.inicio, concepto="Ofrenda semanal", valor=Decimal("185000"), id_casa_vida=esperanza, id_usuario_registro=u["PASTOR"])
        Ofrenda.objects.create(fecha=hoy, concepto="Ofrenda especial de misiones", valor=Decimal("320500"), id_usuario_registro=u["PASTOR"])
