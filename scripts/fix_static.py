import re, os

base = r"C:\Users\joshu\OneDrive\Escritorio\UTS\PROYECTO DE GRADO\templates"
files = ["index.html", "login.html", "selector-modulo.html", "panel.html", "panel-casas-vida.html", "panel-escuelas-formacion.html"]

for f in files:
    p = os.path.join(base, f)
    s = open(p, encoding="utf-8").read()
    if "{% load static %}" not in s:
        if s.startswith("<!DOCTYPE"):
            s = s.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n{% load static %}", 1)
        else:
            s = "{% load static %}\n" + s

    def repl_css(m):
        return 'href="{% static \'css/' + m.group(1) + '\' %}"'

    def repl_js(m):
        return 'src="{% static \'js/' + m.group(1) + '\' %}"'

    def repl_img_src(m):
        return 'src="{% static \'img/' + m.group(1) + '\' %}"'

    def repl_img_href(m):
        return 'href="{% static \'img/' + m.group(1) + '\' %}"'

    s = re.sub(r'href=["\']css/([^"\']+)["\']', repl_css, s)
    s = re.sub(r'src=["\']js/([^"\']+)["\']', repl_js, s)
    s = re.sub(r'src=["\']img/([^"\']+)["\']', repl_img_src, s)
    s = re.sub(r'href=["\']img/([^"\']+)["\']', repl_img_href, s)

    open(p, "w", encoding="utf-8").write(s)
    print("OK", f)
