# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Personas de la iglesia Centro Cristiano Misión Global (CCMG) de Girón, Santander, que sirven en el Plan Vida Abundante (PVA). La mayoría son voluntarios, no personal técnico; el grupo es mixto en edad e incluye muchos adultos mayores o personas con poca experiencia digital.

- **Líder de Casa de Vida y su equipo de apoyo** (Aprendiz, Anfitrión, Maestro de Niños): llenan cada semana el reporte de asistencia con los totales de la reunión y registran a las personas nuevas (nombre y teléfono). Lo hacen más o menos mitad desde el celular y mitad desde el computador.
- **Supervisor de Área**: consulta las Casas de Vida de su Área, recibe los reportes semanales y envía el reporte general mensual al Pastor.
- **Pastor** (Administrador): ve toda la información, gestiona cuentas, Áreas, Casas de Vida y ofrendas, recibe los reportes generales y genera consolidados semanales, mensuales o anuales. Concentra la mayor carga de administración.
- **Coordinador de Formación**: gestiona los procesos de las Escuelas de Formación que coordina (inscripciones, actividades, asistencia, reportes).
- **Super Administrador**: el desarrollador; todo lo del Pastor más la bitácora de auditoría y la gestión de Administradores.
- **Visitante / Miembro Asistente**: solo ve la página pública con información de la iglesia y contacto.

## Product Purpose

Sistema de información web que centraliza la gestión y el seguimiento del Plan Vida Abundante, que antes se llevaba en papel, hojas de cálculo y formularios sueltos. Cada persona ve y gestiona solo lo que le corresponde según su rol. Éxito: que el reporte semanal llegue completo y a tiempo del Líder al Supervisor y del Supervisor al Pastor, y que el Pastor tenga la información consolidada sin perseguirla a mano.

Es el proyecto de grado de Tecnología en Desarrollo de Sistemas Informáticos de las Unidades Tecnológicas de Santander (UTS); su especificación está en `DOCUMENTACION/ERS_PVA.md` (28 RF, 21 RNF, 25 reglas de negocio).

## Positioning

Está hecho a la medida del PVA de CCMG Girón: usa su jerarquía real (Pastor → Supervisor de Área → Líder de Casa de Vida → apoyo), su vocabulario (Casas de Vida, Áreas, Pasos de Vida, Escuelas Vida, VEA) y el formato de reporte de asistencia que la iglesia ya usaba en papel. No es un software genérico de gestión de iglesias.

## Operating Context

- Ciclo semanal: reunión de la Casa de Vida → el Líder o su equipo llena el reporte (asistentes, niños, nuevos, conversiones, Escuelas de Formación, VEA, sábado, dominical, ofrenda) → llega al Supervisor.
- Ciclo mensual: el Supervisor envía el reporte general al Pastor; el Pastor genera consolidados y los exporta a PDF o Excel.
- Carga inicial y masiva de Casas de Vida y participantes desde CSV o Excel, con vista previa y validación por fila.
- Módulos independientes: Página pública, PVA – Casas de Vida, Escuelas de Formación, Ofrendas, Administración.

## Capabilities and Constraints

- Django 5.2 + PostgreSQL 16, plantillas renderizadas en el servidor con Bootstrap 5.3 y Bootstrap Icons; JavaScript sin framework.
- Los permisos se validan en el servidor: fuera de alcance responde 403; registro ajeno responde 404.
- Baja lógica: nada se borra, se desactiva y se conserva el historial.
- Ofrendas solo para el Pastor o el responsable que él autorice.
- Modo oscuro con la paleta institucional; páginas de error propias.
- Requisitos de interfaz del ERS: RNF01 (90 % de los usuarios completa las tareas principales en menos de 2 minutos sin ayuda; la interfaz del Pastor es distinta y más completa), RNF02 (95 % de las solicitudes en ≤ 3 s), RNF09 (Chrome, Edge, Firefox y Safari de escritorio; Chrome Android y Safari iOS), RNF10 (legible y funcional en computador, tableta y teléfono).
- Fuera de alcance: aplicación móvil nativa independiente.

## Brand Commitments

- Nombre: Centro Cristiano Misión Global (CCMG) Girón; programa: Plan Vida Abundante (PVA).
- El logo, el verde institucional `#00674F`, el oro y el nombre «CCMG Girón» son la identidad oficial de la iglesia y se respetan tal cual.
- Idioma: español de Colombia, con el vocabulario propio de la iglesia.

## Evidence on Hand

- Logos: `ccmg/frontend/static/img/logo.png` (y `.webp`), `logo-blanco.png` (y `.avif`, `.webp`).
- Fotos de fondo de la página pública: `ccmg/frontend/static/img/hero-fondo*` y `hero-fondo2*`.
- Datos de demostración por rol: comando `sembrar_demo` (dominio `demo.test`).
- No hay testimonios, cifras de uso ni fotos de personas reales en el repositorio: no se inventan.

## Product Principles

1. **El reporte semanal primero.** Lo que el Líder hace cada semana debe ser lo más rápido y claro de toda la plataforma.
2. **Cada rol ve solo lo suyo.** La interfaz refleja el alcance del rol; nunca insinúa información a la que no se tiene acceso.
3. **Para quien no es técnico.** Lenguaje de la iglesia, pasos evidentes y errores que dicen cómo corregirse; pensado también para adultos mayores.
4. **Nada se pierde.** Baja lógica, confirmaciones claras y trazabilidad de quién hizo qué.
5. **Igual de útil en celular y en computador.**

## Accessibility & Inclusion

Muchos usuarios son adultos mayores o tienen poca experiencia digital: texto legible, buen contraste, objetivos táctiles cómodos, movimiento moderado y respeto por la preferencia de movimiento reducido. No se ha fijado formalmente un nivel WCAG; WCAG 2.1 AA es la referencia de trabajo.
