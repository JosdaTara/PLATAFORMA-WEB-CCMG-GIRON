"""Experiencia de carga: skeletons, loader en botones, debounce/autocompletado e imágenes AVIF/WebP."""
import re

from django.conf import settings
from django.urls import reverse

from formacion.models import InscripcionFormacion, ProcesoFormacion
from nucleo.tests.test_tema import PLANTILLAS, plantillas_con_head
from pva.tests.test_casas_vida import BaseCasasVida

ESTATICOS = settings.FRONTEND_DIR / "static"


def leer(ruta):
    return (PLANTILLAS / ruta).read_text(encoding="utf-8")


class AutocompletarCasasTests(BaseCasasVida):
    url = reverse("pva:participantes_autocompletar")

    def nombres(self, q):
        resp = self.client.get(self.url, {"q": q})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/json")
        return [r["nombre"] for r in resp.json()["resultados"]]

    def test_requiere_sesion(self):
        resp = self.client.get(self.url, {"q": "Ana"})
        self.assertEqual(resp.status_code, 302)

    def test_menos_de_dos_caracteres_no_busca(self):
        self.entrar(self.pastor)
        self.assertEqual(self.nombres("a"), [])
        self.assertEqual(self.nombres(""), [])

    def test_sugiere_por_nombre_y_telefono_con_datos_para_mostrar(self):
        self.entrar(self.pastor)
        self.assertEqual(self.nombres("Ana"), ["Ana Pérez"])
        resp = self.client.get(self.url, {"q": "Ana"}).json()["resultados"][0]
        self.assertEqual(resp["url"], reverse("pva:participante_detalle", args=[self.ana.pk]))
        self.assertIn("Casa Norte", resp["detalle"])
        self.assertEqual(len(self.nombres("300123")), 3)

    def test_respeta_el_alcance_del_rol(self):
        self.entrar(self.lider)
        self.assertEqual(self.nombres("Carla"), [])          # Carla está en la Casa Sur
        self.assertCountEqual(self.nombres("300123"), ["Ana Pérez", "Beto Gómez"])

    def test_limita_el_numero_de_resultados(self):
        for i in range(12):
            self.participante(f"Persona Repetida {i}", f"90{i}", self.casa)
        self.entrar(self.pastor)
        self.assertEqual(len(self.nombres("Repetida")), 8)

    def test_rol_sin_modulo_no_accede(self):
        self.entrar(self.coord)
        self.assertEqual(self.client.get(self.url, {"q": "Ana"}).status_code, 403)


class AutocompletarFormacionTests(BaseCasasVida):
    url = reverse("formacion:participantes_autocompletar")

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        pasos = ProcesoFormacion.objects.create(nombre="Pasos", tipo_proceso="PASOS_VIDA", id_coordinador=cls.coord)
        InscripcionFormacion.objects.create(id_participante=cls.ana, id_proceso_formacion=pasos)

    def test_coordinador_solo_ve_sus_participantes(self):
        self.entrar(self.coord)
        # Busca por nombre o documento: Ana (1001) está en su proceso; Beto (1002) no está inscrito
        resp = self.client.get(self.url, {"q": "100"}).json()["resultados"]
        self.assertEqual([r["nombre"] for r in resp], ["Ana Pérez"])
        self.assertEqual(resp[0]["detalle"], "1001")
        self.assertEqual(resp[0]["url"], reverse("formacion:participante_detalle", args=[self.ana.pk]))


class DescargaTokenTests(BaseCasasVida):
    def test_la_descarga_devuelve_la_cookie_del_boton(self):
        self.entrar(self.superadmin)
        url = reverse("cuentas:auditoria")
        resp = self.client.get(url, {"formato": "xlsx", "descarga_token": "abc123XYZ"})
        self.assertIn("attachment", resp["Content-Disposition"])
        self.assertEqual(resp.cookies["descarga_token"].value, "abc123XYZ")

    def test_sin_token_o_sin_adjunto_no_hay_cookie(self):
        self.entrar(self.superadmin)
        url = reverse("cuentas:auditoria")
        self.assertNotIn("descarga_token", self.client.get(url, {"formato": "xlsx"}).cookies)
        self.assertNotIn("descarga_token", self.client.get(url, {"descarga_token": "abc123XYZ"}).cookies)
        self.assertNotIn("descarga_token", self.client.get(url, {"formato": "xlsx", "descarga_token": "<x>"}).cookies)


class MarcadoDeCargaTests(BaseCasasVida):
    def test_las_bases_cargan_interaccion_js(self):
        for ruta in ("pva/base.html", "pva/panel.html", "formacion/panel.html", "cuentas/_base_cuenta.html",
                     "cuentas/login.html", "cuentas/selector_modulo.html"):
            self.assertIn("js/comun/interaccion.js", leer(ruta), ruta)

    def test_interaccion_js_define_debounce_y_loader(self):
        js = (ESTATICOS / "js" / "comun" / "interaccion.js").read_text(encoding="utf-8")
        for fragmento in ("function debounce", "botonCargando", "descarga_token", "AbortController", "pageshow"):
            self.assertIn(fragmento, js)

    def test_estilos_de_skeleton_y_boton_con_modo_oscuro(self):
        css = (ESTATICOS / "css" / "styles.css").read_text(encoding="utf-8")
        for clase in (".skeleton", ".btn-cargando", ".autocompletar-lista", "@keyframes shimmer"):
            self.assertIn(clase, css)
        self.assertIn('[data-theme="dark"]{--skeleton-base', css)

    def test_descargas_marcadas(self):
        self.assertEqual(leer("pva/_exportar.html").count("data-descarga"), 2)
        self.assertIn("data-descarga", leer("pva/importar.html"))

    def test_listados_con_filtro_vivo_y_skeleton(self):
        for ruta in ("pva/participantes_lista.html", "pva/seguimientos_lista.html", "formacion/participantes_lista.html",
                     "ofrendas/lista.html", "cuentas/auditoria.html"):
            texto = leer(ruta)
            self.assertIn("data-filtro-vivo", texto, ruta)
            self.assertIn("<tbody data-skeleton>", texto, ruta)
        self.assertIn("data-autocompletar=", leer("pva/participantes_lista.html"))

    def test_lista_renderiza_el_autocompletado(self):
        self.entrar(self.pastor)
        resp = self.client.get(reverse("pva:participantes"))
        self.assertContains(resp, f'data-autocompletar="{reverse("pva:participantes_autocompletar")}"')
        self.assertContains(resp, "<tbody data-skeleton>")


class ImagenesModernasTests(BaseCasasVida):
    def test_existen_versiones_webp_y_avif(self):
        img = ESTATICOS / "img"
        for nombre in ("logo", "logo-blanco", "hero-fondo", "hero-fondo2"):
            self.assertTrue((img / f"{nombre}.webp").exists(), nombre)
        for nombre in ("logo-blanco", "hero-fondo", "hero-fondo2"):
            self.assertTrue((img / f"{nombre}.avif").exists(), nombre)

    def test_las_imagenes_de_paginas_usan_picture(self):
        """Toda <img> de static/img (menos el favicon) va dentro de <picture> con WebP."""
        patron = re.compile(r"(<picture>(?:(?!</picture>).)*?)?<img\s+src=\"\{% static 'img/([\w-]+)\.\w+' %\}\"", re.S)
        for ruta, texto in plantillas_con_head():
            for m in patron.finditer(texto):
                self.assertTrue(m.group(1) and f"img/{m.group(2)}.webp" in m.group(1), f"{ruta}: {m.group(2)}")

    def test_fondo_css_con_image_set(self):
        css = (ESTATICOS / "css" / "styles.css").read_text(encoding="utf-8")
        self.assertIn("url('../img/hero-fondo.avif') type('image/avif')", css)
