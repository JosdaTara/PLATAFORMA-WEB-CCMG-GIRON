<div align="center">

# Plataforma Web CCMG Girón · Plan Vida Abundante

**Sistema de información web para la gestión y el seguimiento del Plan Vida Abundante (PVA) de la iglesia Centro Cristiano Misión Global (CCMG) de Girón, Santander.**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![Pruebas](https://img.shields.io/badge/pruebas-187%20pasando-00674F)
![Requisitos](https://img.shields.io/badge/requisitos%20funcionales-28%2F28-CBB279)

Proyecto de grado · Tecnología en Desarrollo de Sistemas Informáticos · Unidades Tecnológicas de Santander (UTS)

</div>

---

## Tabla de contenido
- [Descripción](#descripción)
- [Funcionalidades](#funcionalidades)
- [Roles y permisos](#roles-y-permisos)
- [Tecnologías](#tecnologías)
- [Arquitectura y estructura](#arquitectura-y-estructura)
- [Instalación](#instalación)
- [Entorno de demostración](#entorno-de-demostración)
- [Pruebas](#pruebas)
- [Documentación](#documentación)
- [Seguridad y protección de datos](#seguridad-y-protección-de-datos)
- [Autores](#autores)

## Descripción
En la iglesia CCMG de Girón, el registro de miembros, la asistencia, el seguimiento del discipulado, las Casas de Vida y las ofrendas se llevaban en papel, hojas de cálculo y formularios sueltos. Esta plataforma **centraliza esa información** en un solo sistema web. Cada persona ve y gestiona solo lo que le corresponde según su rol.

La plataforma se organiza en **módulos independientes** (RN21):

| Módulo | Para qué sirve |
|---|---|
| **Página pública** | Información de la iglesia y contacto, sin iniciar sesión. |
| **PVA – Casas de Vida** | Áreas, Casas de Vida, participantes, asistencia, seguimiento y reportes. |
| **Escuelas de Formación** | Pasos de Vida, Escuelas Vida, Módulos de Liderazgo y Misiones. |
| **Ofrendas** | Registro y consulta de ofrendas. |
| **Administración** | Usuarios, roles, asignaciones e importación de datos. |

## Funcionalidades
Están implementados los **28 requisitos funcionales** de la [Especificación de Requisitos (ERS)](DOCUMENTACION/ERS_PVA.md).

**Acceso y usuarios**
- Inicio de sesión por correo o usuario, bloqueo tras 5 intentos fallidos y sesión que expira por inactividad (RF01, RF02).
- Gestión de usuarios con contraseña temporal que se debe cambiar en el primer ingreso (RF03, RF04).
- Recuperación de contraseña por correo (RF25).
- Panel por rol (RF23).

**Casas de Vida**
- Áreas, Casas de Vida y participantes con los datos mínimos y la autorización de tratamiento de datos (RF05–RF08).
- Asistencia por actividad, registrada por el Líder o su equipo de apoyo (RF09, RF10).
- Seguimiento pastoral de cada participante (RF11).
- Flujo de reportes (RF12–RF16):
  - el Líder o su equipo envían el **reporte semanal** al Supervisor;
  - el Supervisor envía el **reporte general mensual** al Pastor;
  - el Pastor genera **reportes consolidados** semanales, mensuales o anuales.

**Escuelas de Formación** (RF18–RF22)
- Procesos de las cuatro escuelas, cada uno con su coordinador.
- Inscripciones, sin duplicar personas.
- Actividades con asistencia solo de los inscritos.
- Seguimiento y reportes por periodo.

**Ofrendas** (RF17)
- Registro y consulta por rango de fechas.
- Acceso solo para el Pastor o el responsable que él autorice.

**Datos y reportes**
- **Importación** de Casas de Vida y participantes desde CSV o Excel, con vista previa y validación de cada fila (RF26).
- **Exportación** de reportes a PDF y Excel con periodo, fecha de generación y solo la información que el rol puede ver (RF27).
- **Baja lógica:** nada se borra; se desactiva y se conserva el historial (RF28).

**Interfaz**
- Diseño adaptable a celulares.
- **Modo oscuro** con la paleta institucional.
- Páginas de error propias.

## Roles y permisos
| Rol | Alcance |
|---|---|
| **Super Administrador** | Todo lo del Pastor en ambos módulos, más la bitácora de auditoría. Es el **único** que crea, edita, desactiva o reactiva Administradores (Pastor) y otros Super Administradores. |
| **Pastor** (Administrador) | Toda la información de ambos módulos. Gestiona las cuentas de Supervisores, Coordinadores, Líderes y su equipo, las Áreas, las Casas de Vida y las ofrendas. No ve ni modifica a otros Administradores ni puede cambiar su propio rol. Recibe los reportes generales y genera los consolidados. |
| **Supervisor de Área** | Solo las Casas de Vida de su Área, en modo de consulta. Recibe los reportes semanales y envía el general al Pastor. |
| **Líder de Casa de Vida** | Solo su Casa de Vida. Registra la asistencia y envía el reporte semanal. |
| **Apoyo** (Aprendiz, Anfitrión, Maestro de Niños) | Igual que el Líder para la asistencia y el reporte de su casa. |
| **Coordinador de Formación** | Solo los procesos de formación que coordina. |

Los permisos se validan **en el servidor**. Una página fuera del alcance responde 403, y un registro ajeno responde 404, para no revelar que existe.

## Tecnologías
- **Backend:** Python 3.11 y Django 5.2.
- **Base de datos:** PostgreSQL 16. El esquema está diseñado en SQL y los modelos de Django lo usan con `managed = False`.
- **Frontend:** HTML5, CSS3, JavaScript y Bootstrap 5.3 con Bootstrap Icons, en plantillas renderizadas en el servidor.
- **Reportes:** `openpyxl` para Excel y `reportlab` para PDF.
- **Pruebas:** el framework de pruebas de Django, sobre PostgreSQL.

## Arquitectura y estructura
Arquitectura cliente-servidor con el patrón MVT de Django. Cada módulo del ERS es una app de Django. La carpeta `ccmg` separa el **backend** (código Django y base de datos) del **frontend** (plantillas HTML y archivos estáticos).

```
PLATAFORMA-WEB-CCMG-GIRON/
├── ccmg/                              # Plataforma web
│   ├── backend/                       # Django: lógica, permisos, modelos y base de datos
│   │   ├── apps/
│   │   │   ├── cuentas/               # Autenticación, usuarios, roles, contraseñas
│   │   │   ├── nucleo/                # Permisos, auditoría, exportación PDF/Excel, utilidades
│   │   │   ├── publico/               # Página pública
│   │   │   ├── pva/                   # Casas de Vida: áreas, participantes, asistencia, reportes, importación
│   │   │   ├── formacion/             # Escuelas de Formación
│   │   │   └── ofrendas/              # Ofrendas
│   │   ├── config/settings/           # base · development · demo · production
│   │   ├── base_datos/                # esquema.sql, datos_iniciales.sql, cambios/
│   │   ├── manage.py
│   │   └── requirements.txt
│   └── frontend/                      # Interfaz de usuario
│       ├── templates/                 # Plantillas HTML por módulo
│       └── static/                    # css · img · js (comun, cuentas, pva, formacion)
├── DOCUMENTACION/
│   ├── ERS_PVA.md                     # Especificación de requisitos para leer en GitHub
│   ├── IEEE_PLATAFORMA_WEB_CCMG.pdf   # La misma especificación en formato IEEE (PDF)
│   └── diagramas/                     # Casos de uso y entidad-relación (PNG y SVG)
├── .env.example                       # Variables de entorno de ejemplo
├── .gitignore
└── README.md
```

## Instalación

### Requisitos
- Python 3.11
- PostgreSQL 16 (con `psql`, o pgAdmin)
- Git

### 1. Clonar e instalar dependencias
```bash
git clone https://github.com/JosdaTara/PLATAFORMA-WEB-CCMG-GIRON.git
cd PLATAFORMA-WEB-CCMG-GIRON/ccmg
python -m venv venv
venv\Scripts\activate          # Windows  (en Linux/macOS: source venv/bin/activate)
pip install -r backend/requirements.txt
cd backend                     # los comandos siguientes se ejecutan desde ccmg/backend
```

### 2. Crear la base de datos
```bash
createdb -U postgres CCMG_GIRON
psql -U postgres -d CCMG_GIRON -f base_datos/esquema.sql
psql -U postgres -d CCMG_GIRON -f base_datos/datos_iniciales.sql
```
`esquema.sql` ya incluye todos los cambios de [`cambios/`](ccmg/backend/base_datos/cambios). Esos scripts solo hacen falta para actualizar una base creada con una versión anterior.

### 3. Configurar las variables de entorno
Copie [`.env.example`](.env.example) como `.env` en la raíz del proyecto y complete los datos de conexión.

### 4. Crear las primeras cuentas e iniciar
```bash
python manage.py crear_superadmin   # cuenta del desarrollador: pide correo, nombre y contraseña
python manage.py crear_pastor       # cuenta del Pastor (mínimo 15 caracteres en la contraseña)
python manage.py runserver
```
Para convertir una cuenta existente en Super Administrador, sin cambiar su contraseña: `python manage.py crear_superadmin --promover correo@dominio`.
Abra http://127.0.0.1:8000. Desde la cuenta del Super Administrador se crean los Administradores; desde la del Pastor, los demás usuarios, las Áreas y las Casas de Vida, o se importan desde Excel.

## Entorno de demostración
Una base aparte con usuarios de cada rol y datos de ejemplo, útil para presentaciones:
```bash
createdb -U postgres CCMG_GIRON_demo
psql -U postgres -d CCMG_GIRON_demo -f base_datos/esquema.sql
psql -U postgres -d CCMG_GIRON_demo -f base_datos/datos_iniciales.sql
python manage.py sembrar_demo --settings=config.settings.demo
python manage.py runserver 8001 --settings=config.settings.demo
```
La demo corre en http://127.0.0.1:8001, aparte de la plataforma real (puerto 8000): **cada una usa su propia base de datos**, así que las cuentas de una no sirven en la otra.
Los usuarios de demostración usan el dominio `demo.test` (`superadmin@`, `pastor@`, `supervisor@`, `lider@`, `apoyo@`, `coordinador@`). Su contraseña es la constante `CLAVE_DEMO` de [`sembrar_demo.py`](ccmg/backend/apps/nucleo/management/commands/sembrar_demo.py). El comando se niega a ejecutarse sobre una base cuyo nombre no contenga «demo».

## Pruebas
```bash
cd ccmg/backend
python manage.py test --noinput
```
Son **187 pruebas automatizadas** sobre PostgreSQL. Cubren:
- los permisos y el alcance de cada rol;
- las reglas de negocio del ERS;
- los flujos de reportes;
- la importación y la exportación;
- el modo oscuro;
- regresiones encontradas al recorrer la plataforma con cada rol.

## Documentación
| Documento | Contenido |
|---|---|
| [ERS_PVA.md](DOCUMENTACION/ERS_PVA.md) | Especificación de requisitos (IEEE / ISO 29148): 28 RF, 21 RNF, 25 reglas de negocio, 44 historias de usuario, casos de uso y diagramas. |
| [IEEE_PLATAFORMA_WEB_CCMG.pdf](DOCUMENTACION/IEEE_PLATAFORMA_WEB_CCMG.pdf) | La misma especificación en el formato IEEE, en PDF. |
| [diagramas/](DOCUMENTACION/diagramas) | Diagrama general y por módulo de casos de uso, jerarquía de usuarios y modelo entidad-relación (PNG y SVG). |
| [esquema.sql](ccmg/backend/base_datos/esquema.sql) | Modelo relacional completo de PostgreSQL. |
| [cambios/](ccmg/backend/base_datos/cambios) | Scripts de cambio de esquema aplicados durante el desarrollo, con su motivo. |

## Seguridad y protección de datos
- **Contraseñas:**
  - con hash, de mínimo 15 caracteres;
  - bloqueo tras 5 intentos fallidos;
  - cambio obligatorio de la contraseña temporal (RNF05, RNF19, RNF20).
- **Control de acceso** por rol y por alcance, siempre en el servidor (RNF04, RNF06).
- **Auditoría:** quién inició sesión, creó, modificó, desactivó o importó cada registro, y cuándo, consultable y exportable por el Super Administrador (RNF18).
- **Ley 1581 de 2012:**
  - autorización de tratamiento de datos para cada participante;
  - aviso de confidencialidad en los reportes exportados (RN23, RNF16).
- **Producción:** HTTPS, cookies seguras y HSTS (RNF21).
- **Credenciales:** solo en `.env`, que no se versiona.

## Autores
- **Joshua David Tarazona Gómez**
- **Karen Lizeth Arenas Medina**

**Director:** Alexander Anchicoque Calderón, Grupo de Investigación en Ingeniería del Software (GRIIS).

Unidades Tecnológicas de Santander · Facultad de Ciencias Naturales e Ingenierías · Bucaramanga, 2026.

---
<sub>Proyecto de grado académico desarrollado para la iglesia CCMG de Girón.</sub>
