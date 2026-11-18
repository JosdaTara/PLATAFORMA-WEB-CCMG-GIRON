"""Genera versiones AVIF y WebP de las imágenes estáticas, conservando los originales.

Los navegadores modernos descargan AVIF (o WebP) mediante <picture> / image-set();
los antiguos siguen usando el PNG/JPEG original. Ejecutar una vez tras cambiar una imagen:

    python scripts/convertir_imagenes.py
"""

from pathlib import Path

from PIL import Image

CARPETA = Path(__file__).resolve().parents[2] / "frontend" / "static" / "img"
ORIGINALES = ("logo.png", "logo-blanco.png", "hero-fondo.jpeg", "hero-fondo2.jpeg")


def convertir(ruta: Path) -> None:
    with Image.open(ruta) as img:
        img.load()
        con_alfa = img.mode in ("RGBA", "LA", "P")
        img = img.convert("RGBA" if con_alfa else "RGB")

        webp = ruta.with_suffix(".webp")
        if con_alfa:
            # Logos: se queda la variante (con o sin pérdida) que pese menos.
            img.save(webp, "WEBP", lossless=True, method=6)
            sin_perdida = webp.stat().st_size
            tmp = ruta.with_suffix(".tmp.webp")
            img.save(tmp, "WEBP", quality=88, method=6)
            if tmp.stat().st_size < sin_perdida:
                tmp.replace(webp)
            else:
                tmp.unlink()
        else:
            img.save(webp, "WEBP", quality=80, method=6)

        avif = ruta.with_suffix(".avif")
        img.save(avif, "AVIF", quality=40 if con_alfa else 50, speed=4)

    peso_avif = avif.stat().st_size
    if peso_avif >= webp.stat().st_size:
        # No tiene sentido servir un AVIF más pesado que el WebP: la plantilla usa solo WebP.
        avif.unlink()
        peso_avif = "(descartado)"
    print(f"{ruta.name:20} {ruta.stat().st_size:>8} B -> webp {webp.stat().st_size:>8} B, avif {peso_avif:>8} B")


if __name__ == "__main__":
    for nombre in ORIGINALES:
        convertir(CARPETA / nombre)
