---
name: Plataforma Web CCMG Girón
description: Sistema de gestión del Plan Vida Abundante de la iglesia CCMG Girón
colors:
  verde-institucional: "#00674F"
  verde-profundo: "#004d3b"
  oro-ofrenda: "#CBB279"
  oro-texto: "#8a7439"
  carbon: "#2B2D2F"
  arena: "#F4F5F2"
  superficie: "#FFFFFF"
  superficie-2: "#FAFBF9"
  borde: "#E3E5E0"
  texto-suave: "#6B706E"
  oscuro-fondo: "#0F1714"
  oscuro-superficie: "#17221E"
  oscuro-superficie-2: "#1E2C27"
  oscuro-borde: "#2B3B35"
  oscuro-texto: "#E3E9E6"
  oscuro-texto-suave: "#9DB0A8"
  verde-claro-oscuro: "#5CC9A7"
typography:
  display:
    fontFamily: "Fraunces, Georgia, 'Times New Roman', serif"
    fontSize: "clamp(2.3rem, 5.2vw, 4rem)"
    fontWeight: 700
    lineHeight: 1.04
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Fraunces, Georgia, 'Times New Roman', serif"
    fontSize: "2rem"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Fraunces, Georgia, 'Times New Roman', serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Figtree, 'Segoe UI', system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Figtree, 'Segoe UI', system-ui, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 700
    letterSpacing: "0.09em"
  numeral:
    fontFamily: "Figtree, 'Segoe UI', system-ui, sans-serif"
    fontSize: "2rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
    fontFeature: "'lnum', 'tnum'"
rounded:
  sm: "8px"
  md: "10px"
  lg: "14px"
  xl: "18px"
  pill: "999px"
spacing:
  vista: "2rem 2.25rem"
  vista-movil: "1.25rem 1rem"
  tarjeta: "1.25rem"
components:
  button-primary:
    backgroundColor: "{colors.verde-institucional}"
    textColor: "{colors.superficie}"
    rounded: "{rounded.md}"
  button-primary-hover:
    backgroundColor: "{colors.verde-profundo}"
  button-oro:
    backgroundColor: "{colors.oro-ofrenda}"
    textColor: "{colors.carbon}"
    rounded: "{rounded.md}"
  card:
    backgroundColor: "{colors.superficie}"
    rounded: "{rounded.lg}"
    padding: "{spacing.tarjeta}"
  input:
    backgroundColor: "{colors.superficie}"
    rounded: "{rounded.md}"
  chip-modulo:
    backgroundColor: "rgba(0,103,79,.10)"
    textColor: "{colors.verde-institucional}"
    rounded: "{rounded.pill}"
  sidebar:
    backgroundColor: "{colors.verde-institucional}"
    textColor: "{colors.superficie}"
    width: "250px"
---

# Design System: Plataforma Web CCMG Girón

## Overview

**Creative North Star: "La Casa Ordenada"**

La plataforma se siente como entrar a una casa acogedora donde todo está en su lugar. El verde institucional da serenidad y autoridad; el oro aparece como un acento cálido y escaso, como la luz de una lámpara, no como decoración. Los títulos en serif (Fraunces) dan dignidad y calidez humana; la interfaz en sans (Figtree) mantiene todo legible y práctico.

Hay dos densidades. La página pública y el selector de módulo son espaciosos, con fotografía, degradados verdes y entradas animadas: invitan. Los paneles internos (PVA, Formación, Cuentas, Ofrendas) son más densos y tranquilos: fondo arena, tarjetas blancas de borde fino, tablas claras y cifras tabulares. Ahí la calidez vive en los detalles (esquinas suaves, color de acento en íconos, respuesta visible al pasar el mouse), nunca en efectos que estorben la tarea.

El modo oscuro es la misma casa de noche: superficies carbón con tinte verde, títulos en un verde claro del mismo tono y el oro intacto.

**Key Characteristics:**
- Verde institucional y oro oficiales, usados tal cual.
- Títulos en serif con carácter; interfaz y cifras en sans con números tabulares.
- Tarjetas blancas de borde fino, esquinas suaves y sombra suave que se levantan al pasar el mouse.
- Componentes cálidos y amables, pensados también para adultos mayores.
- Modo claro y oscuro con contraste AA verificado.

## Colors

Una paleta institucional de dos voces, verde sereno y oro cálido, sobre neutros arena con un leve tinte verde.

### Primary
- **Verde Institucional** (`verde-institucional`): color oficial de la iglesia. Barra lateral, barra pública, botón principal, encabezados de tabla en la página pública, enlaces y títulos en modo claro.
- **Verde Profundo** (`verde-profundo`): hover del botón principal, final del degradado de la barra lateral y de los encabezados, pie de la barra lateral.

### Secondary
- **Oro de Ofrenda** (`oro-ofrenda`): acento cálido oficial. Indicador activo en la navegación, íconos destacados, subrayado de los títulos de sección públicos, anillo de foco, módulo de Escuelas de Formación y botón dorado.
- **Oro para Texto** (`oro-texto`): versión oscurecida del oro para texto pequeño e íconos sobre fondo claro, donde el oro original no alcanza contraste.

### Neutral
- **Carbón** (`carbon`): texto principal en modo claro, pie de página y toasts.
- **Arena** (`arena`): fondo de los paneles y de las secciones alternas.
- **Superficie** (`superficie`) y **Superficie Suave** (`superficie-2`): tarjetas, barra superior, encabezados de tabla en los paneles.
- **Borde** (`borde`): bordes de tarjetas, tablas y separadores.
- **Texto Suave** (`texto-suave`): texto secundario, encabezados de tabla, estados vacíos.
- **Modo oscuro**: `oscuro-fondo`, `oscuro-superficie`, `oscuro-superficie-2`, `oscuro-borde`, `oscuro-texto`, `oscuro-texto-suave`; los títulos y enlaces pasan a **Verde Claro Nocturno** (`verde-claro-oscuro`).

### Named Rules
**The Official Colors Rule.** El verde `#00674F`, el oro `#CBB279` y el logo son la identidad oficial de la iglesia: no se ajustan, ni se sustituyen por variantes "parecidas". Solo se oscurecen o aclaran en los tokens ya definidos para contraste (`oro-texto`, `verde-claro-oscuro`).

**The Lamp Light Rule.** El oro es acento, no superficie: marca lo activo, lo destacado o lo que se toca. Nunca rellena grandes áreas ni compite con el verde.

## Typography

**Display Font:** Fraunces (con Georgia, Times New Roman)
**Body Font:** Figtree (con Segoe UI, system-ui)

**Character:** Fraunces aporta dignidad y calidez humana en títulos; Figtree es abierta, legible y práctica para formularios, tablas y botones.

### Hierarchy
- **Display** (700, `clamp(2.3rem, 5.2vw, 4rem)`, 1.04): solo el titular de la portada pública.
- **Headline** (600, 2rem; 1.65rem en móvil, 1.15): título de cada vista en los paneles y títulos de sección públicos (`clamp(2rem, 3.6vw, 2.8rem)`).
- **Title** (600, 1.25rem, 1.2): títulos de tarjeta y subsecciones.
- **Body** (400, 1rem, 1.6): texto general; párrafos públicos con un máximo de 60ch.
- **Label** (700, 0.68–0.72rem, 0.09em, MAYÚSCULAS): encabezados de tabla, etiquetas de indicadores, subtítulos de marca.
- **Numeral** (700, 2rem, números tabulares): cifras de los indicadores del panel.

### Named Rules
**The Serif for Meaning Rule.** Fraunces solo en títulos y en el mensaje de los estados vacíos; nunca en botones, campos, tablas ni cifras, que siempre van en Figtree.

## Layout

- Paneles: barra lateral fija de 250px a la izquierda y contenido con fondo arena; barra superior pegajosa de 64px. Por debajo de 992px la barra lateral se oculta y se abre como cajón.
- Relleno de cada vista: 2rem × 2.25rem en escritorio, 1.25rem × 1rem por debajo de 768px.
- El encabezado de cada vista (título + acciones) lleva una línea inferior de borde y 1.5rem de separación.
- Rejilla y puntos de quiebre de Bootstrap 5.3 (576, 768, 992, 1200px).
- Página pública: secciones de ancho completo con contenedor de Bootstrap; la portada pone la foto a la derecha con máscara en degradado y, en móvil, debajo del texto.

## Elevation & Depth

Sistema en capas suaves: las superficies tienen borde fino y una sombra corta y difusa en reposo, y se levantan al pasar el mouse con una sombra más amplia teñida de verde. En modo oscuro las sombras son negras y más densas.

### Shadow Vocabulary
- **Tarjeta en reposo** (`0 1px 2px rgba(15,32,28,.05), 0 4px 16px rgba(15,32,28,.06)`): tarjetas y tablas de los paneles.
- **Tarjeta levantada** (`0 16px 38px rgba(0,77,59,.12)`): hover de tarjetas públicas y de módulo.
- **Indicador levantado** (`0 10px 24px rgba(0,0,0,.09)`): hover de los indicadores del panel.
- **Flotante** (`0 12px 32px rgba(15,32,28,.14)`): listas de autocompletado y menús.
- **Escenario** (`0 30px 80px rgba(0,0,0,.35)`): la tarjeta del selector de módulo sobre el fondo verde.

### Named Rules
**The Gentle Lift Rule.** Lo que se puede tocar responde subiendo un poco (3–6px) y ampliando su sombra; lo que no se toca no se mueve. Con movimiento reducido, nada se desplaza.

## Shapes

Esquinas suaves y amables en todo el sistema: 8px en botones y campos pequeños, 10px en botones y campos, 14px en tarjetas, tablas y alertas, 18px en las tarjetas destacadas (módulos, acceso) y forma de píldora en etiquetas de módulo. Los íconos destacados van en cuadros redondeados de 12–18px.

## Components

### Buttons
Cálidos y firmes: se entienden de un vistazo.
- **Shape:** esquinas suaves (10px; 8px en los pequeños).
- **Primary:** verde institucional con texto blanco, peso 600, sombra mínima y brillo interior sutil.
- **Hover / Focus:** pasa a verde profundo; foco con contorno oro de 2px separado 2px.
- **Oro:** fondo oro con texto carbón para acciones destacadas en contextos verdes.
- **Secundarios:** los contornos y botones claros de Bootstrap, con la misma forma.

### Chips
- **Style:** etiqueta de módulo en píldora, verde translúcido con texto verde (PVA) u oro translúcido con texto `oro-texto` (Escuelas).
- **Badges de estado:** los de Bootstrap con peso 600 y relleno generoso.

### Cards / Containers
- **Corner Style:** 14px (18px en tarjetas destacadas).
- **Background:** superficie blanca sobre fondo arena.
- **Shadow Strategy:** tarjeta en reposo; se levanta en hover (ver Elevation & Depth).
- **Border:** 1px `borde`.
- **Internal Padding:** 1.25rem.

### Inputs / Fields
- **Style:** borde de Bootstrap, esquinas de 10px, relleno vertical de 0.55rem; etiqueta en 600 a 0.86rem encima.
- **Focus:** borde verde y halo verde translúcido de 0.2rem (verde claro en modo oscuro).
- **Error / Disabled:** estados de validación de Bootstrap.

### Navigation
- **Barra lateral (paneles):** degradado de verde institucional a verde profundo; enlaces en blanco al 80 %, peso 500, esquinas de 10px; activo con fondo blanco al 16 %, peso 600 e ícono en oro; botón de salir pegado abajo.
- **Barra pública:** verde institucional con marca en Fraunces; enlaces blancos que pasan a oro, con un subrayado oro que crece de izquierda a derecha.
- **Móvil:** la barra lateral se vuelve cajón; la pública se colapsa con el menú de Bootstrap.

### Indicadores (stat)
Tarjeta con etiqueta en mayúsculas, cifra grande en Figtree con números tabulares y un ícono en cuadro oro translúcido (oculto en móvil).

### Tablas
Encabezado en `superficie-2` con etiquetas en mayúsculas y texto suave; filas con 0.75rem de relleno, hover verde muy tenue y enlaces en peso 600. Envueltas en un contenedor redondeado de 14px con borde y sombra de tarjeta.

### Estado vacío
Centrado: ícono oro grande, mensaje en Fraunces y texto suave debajo.

## Do's and Don'ts

### Do:
- **Do** usar los tokens de color (`var(--verde)`, `var(--oro)`, `var(--borde)`…) en lugar de valores sueltos, para que el modo oscuro herede todo.
- **Do** usar `oro-texto` para texto e íconos pequeños en oro sobre fondo claro.
- **Do** usar números tabulares en cifras y tablas.
- **Do** dar a todo lo que se toca un foco visible (contorno oro de 2px) y un hover claro.
- **Do** respetar `prefers-reduced-motion`: sin desplazamientos ni animaciones.

- **Do** dejar que las tablas de los paneles se apilen en tarjetas «etiqueta: valor» por debajo de 576px (clase `tabla-apilada`, la pone `interaccion.js`); usar `data-sin-apilar` en la envoltura solo cuando la tabla deba seguir siendo tabla.
- **Do** cuando una tarea semanal ya está hecha (por ejemplo, el reporte enviado), decirlo primero y ofrecer «ver» como acción principal; el formulario queda detrás de una acción secundaria.
- **Do** usar un solo `<h1>` por vista (el título de la vista), con el estilo de título de vista.
- **Do** mostrar un resumen («Revisa antes de enviar») antes de toda acción que no se pueda deshacer, como el envío del reporte semanal; el botón principal dice «Revisar y enviar».
- **Do** en los formularios que llenan los Líderes: botones de 44px (`btn-flujo`), títulos de sección en estilo Title (`titulo-seccion`), los campos principales destacados (`campo-principal`) y el botón de envío fijo abajo en el celular.
- **Do** poner primero, en el panel y en Asistencia del Líder y su equipo, el estado del reporte de la semana (`tarjeta-semana`: pendiente en oro, enviado en verde).

**The Instant Panel Rule.** En los paneles nada hace esperar al usuario por estética: sin pantallas de carga que tapen la página, sin esperas artificiales en botones y con entradas de vista de 200 ms como máximo. La espera real se muestra en el botón o con skeletons.

### Don't:
- **Don't** tapar la página con el loader al hacer clic o enviar un formulario, ni retrasar su salida.
- **Don't** usar animaciones infinitas decorativas ni apariciones de más de 450 ms (la página pública es la única que puede tener entradas escalonadas).
- **Don't** cambiar, aclarar ni sustituir el verde `#00674F`, el oro `#CBB279` o el logo fuera de los tokens definidos.
- **Don't** rellenar áreas grandes con oro ni ponerlo a competir con el verde.
- **Don't** usar Fraunces en botones, campos, tablas o cifras.
- **Don't** usar texto gris más claro que `texto-suave` sobre blanco: muchos usuarios son adultos mayores.
