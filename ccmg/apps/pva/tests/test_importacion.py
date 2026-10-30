"""Pruebas de importación de datos: RF26, HU-42 (criterios 1–4) y RN25."""
import datetime
import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from openpyxl import Workbook, load_workbook

from nucleo.models import Auditoria
from pva.models import CasaVida, Participante

from .test_casas_vida import BaseCasasVida

ENCABEZADOS_P = ["Nombres y apellidos", "Documento de identidad", "Fecha de nacimiento", "Teléfono", "Dirección", "Casa de Vida", "Autorización de datos"]


def xlsx(filas, nombre="datos.xlsx"):
    libro = Workbook()
    hoja = libro.active
    for fila in filas:
        hoja.append(fila)
    salida = io.BytesIO()
    libro.save(salida)
    return SimpleUploadedFile(nombre, salida.getvalue())


def csv(texto, nombre="datos.csv", codificacion="utf-8"):
    return SimpleUploadedFile(nombre, texto.encode(codificacion))


class ImportacionTests(BaseCasasVida):
    def setUp(self):
        self.entrar(self.pastor)

    def subir(self, tipo, archivo):
        return self.client.post(reverse("pva:importar"), {"tipo": tipo, "archivo": archivo})

    def previa(self):
        return self.client.get(reverse("pva:importar_vista_previa")).context

    def test_vista_previa_sin_guardar_y_confirmacion(self):
        archivo = xlsx([
            ENCABEZADOS_P,
            ["Diana López", 3001, datetime.datetime(1990, 5, 1), 3109876543, "Calle 1", "casa norte", "Sí"],
            ["Ernesto Ruiz", "3002", "02/02/1985", "310 555 1234", "Calle 2", "Casa Sur", ""],
        ])
        resp = self.subir("participantes", archivo)
        self.assertRedirects(resp, reverse("pva:importar_vista_previa"))
        ctx = self.previa()
        self.assertEqual(ctx["conteo"]["validas"], 2)
        self.assertEqual(ctx["conteo"]["pendientes"], 1)
        self.assertFalse(Participante.objects.filter(documento_identidad__in=["3001", "3002"]).exists())

        resp = self.client.post(reverse("pva:importar_vista_previa"))
        self.assertRedirects(resp, reverse("pva:importar_resultado"))
        diana = Participante.objects.get(documento_identidad="3001")
        ernesto = Participante.objects.get(documento_identidad="3002")
        self.assertEqual((diana.fecha_nacimiento, diana.telefono, diana.membresia_activa.id_casa_vida), (datetime.date(1990, 5, 1), "3109876543", self.casa))
        self.assertTrue(diana.autorizacion_datos)
        self.assertFalse(ernesto.autorizacion_datos)  # RN25: autorización pendiente
        self.assertEqual(ernesto.fecha_nacimiento, datetime.date(1985, 2, 2))
        self.assertEqual(Auditoria.objects.filter(accion="IMPORTAR", id_usuario=self.pastor).count(), 2)

    def test_no_duplica_ni_en_base_ni_en_archivo(self):
        archivo = csv(
            "documento;nombres;nacimiento;celular;direccion;casa\n"
            "1001;Ana Pérez;1990-01-01;3001234567;Calle;Casa Norte\n"
            "4001;Nueva;1990-01-01;3001234567;Calle;Casa Norte\n"
            "4001;Nueva otra vez;1990-01-01;3001234567;Calle;Casa Norte\n"
        )
        self.subir("participantes", archivo)
        estados = [r["estado"] for r in self.previa()["resultados"]]
        self.assertEqual(estados, ["omitida", "valida", "error"])
        self.client.post(reverse("pva:importar_vista_previa"))
        self.assertEqual(Participante.objects.filter(documento_identidad="4001").count(), 1)
        self.assertEqual(Participante.objects.get(documento_identidad="1001").nombres_apellidos, "Ana Pérez")

    def test_aplica_las_reglas_del_registro_manual(self):
        archivo = xlsx([
            ENCABEZADOS_P,
            ["Sin teléfono", "5001", "1990-01-01", "", "Calle", "Casa Norte", "Sí"],
            ["Casa inexistente", "5002", "1990-01-01", "3001234567", "Calle", "Casa Fantasma", "Sí"],
            ["Fecha futura", "5003", "2999-01-01", "3001234567", "Calle", "Casa Norte", "Sí"],
        ])
        self.subir("participantes", archivo)
        resultados = self.previa()["resultados"]
        self.assertTrue(all(r["estado"] == "error" for r in resultados))
        self.assertIn("Teléfono", resultados[0]["mensajes"][0])
        self.assertIn("Casa Fantasma", resultados[1]["mensajes"][0])
        self.assertIn("futura", resultados[2]["mensajes"][0])

    def test_importa_casas_de_vida(self):
        archivo = csv(
            "Nombre de la Casa de Vida,Área,Dirección,Correo del Líder\n"
            "Casa Nueva,norte,Calle 9,\n"
            "Casa Norte,Norte,Calle 1,\n"
            "Casa Lejana,Oriente,Calle 3,\n"
            "Casa Liderada,Sur,Calle 4,lider@ccmg.org\n"
        )
        self.subir("casas", archivo)
        resultados = self.previa()["resultados"]
        self.assertEqual([r["estado"] for r in resultados], ["valida", "omitida", "error", "error"])
        self.assertIn("ya está asignado", resultados[3]["mensajes"][0])
        self.client.post(reverse("pva:importar_vista_previa"))
        nueva = CasaVida.objects.get(nombre="Casa Nueva")
        self.assertEqual((nueva.id_area, nueva.id_supervisor), (self.area, self.supervisor))

    def test_archivo_invalido(self):
        resp = self.subir("participantes", csv("hola,mundo\n1,2\n"))
        self.assertIn("Faltan columnas obligatorias", resp.context["form"].errors["archivo"][0])
        resp = self.subir("participantes", SimpleUploadedFile("datos.pdf", b"%PDF"))
        self.assertIn("Formato no admitido", resp.context["form"].errors["archivo"][0])
        resp = self.subir("participantes", SimpleUploadedFile("datos.xlsx", b"no es excel"))
        self.assertIn("No se pudo leer", resp.context["form"].errors["archivo"][0])

    def test_csv_en_latin1(self):
        texto = "Nombres y apellidos;Documento de identidad;Fecha de nacimiento;Teléfono;Dirección;Casa de Vida\nJosé Núñez;6001;01/01/1990;3001234567;Calle;Casa Norte\n"
        self.subir("participantes", csv(texto, codificacion="latin-1"))
        self.assertEqual(self.previa()["resultados"][0]["datos"]["nombres_apellidos"], "José Núñez")

    def test_no_se_confirma_dos_veces(self):
        self.subir("participantes", xlsx([ENCABEZADOS_P, ["X", "7001", "1990-01-01", "3001234567", "C", "Casa Norte", "si"]]))
        self.client.post(reverse("pva:importar_vista_previa"))
        resp = self.client.post(reverse("pva:importar_vista_previa"))
        self.assertRedirects(resp, reverse("pva:importar_resultado"))
        self.assertEqual(Participante.objects.filter(documento_identidad="7001").count(), 1)

    def test_detalle_de_errores_descargable(self):
        self.subir("participantes", csv("documento;nombres;nacimiento;celular;direccion;casa\n1001;Ana;1990-01-01;300;C;Casa Norte\n8001;B;1990-01-01;1;C;Casa Norte\n"))
        resp = self.client.get(reverse("pva:importar_detalle"))
        contenido = resp.content.decode("utf-8-sig")
        self.assertEqual(resp["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("Omitida", contenido)
        self.assertIn("Error", contenido)
        self.assertIn("8001", contenido)

    def test_plantillas(self):
        for tipo, primera in (("casas", "Nombre de la Casa de Vida"), ("participantes", "Nombres y apellidos")):
            resp = self.client.get(reverse("pva:importar_plantilla", args=[tipo]))
            libro = load_workbook(io.BytesIO(resp.content))
            self.assertEqual(libro.worksheets[0]["A1"].value, primera)
            self.assertIn("Instrucciones", libro.sheetnames)
        self.assertEqual(self.client.get(reverse("pva:importar_plantilla", args=["otro"])).status_code, 404)

    def test_solo_el_pastor_importa(self):
        for user in (self.supervisor, self.lider, self.coord):
            self.entrar(user)
            for ruta in (reverse("pva:importar"), reverse("pva:importar_plantilla", args=["casas"])):
                self.assertEqual(self.client.get(ruta).status_code, 403, (user.correo, ruta))
