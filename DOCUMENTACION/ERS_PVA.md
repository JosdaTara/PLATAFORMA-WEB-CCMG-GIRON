| |
|---|
| |

Especificación de requisitos de software

Proyecto: Plataforma Web para la gestión y seguimiento del plan vida abundante de la iglesia CCMG de Girón

> 

| | | |
|---|---|---|
| | | Octubre de 2026 |

# Ficha del documento

Fecha
Revisión
Autor
Verificado dep. calidad.

29/09/2026
Revisión 1
Joshua David Tarazona Gómez
Karen Lizeth Arenas Medina

22/10/2026
Revisión 2
Joshua David Tarazona Gómez
Karen Lizeth Arenas Medina

| | |
|---|---|
| Por el cliente | Por el equipo desarrollador |
| | |
| | |

# Contenido

Ficha del documento 2

Contenido 3

1 Introducción 6

1.1 Propósito 6

1.2 Alcance 6

1.2.1 Gestión de Usuarios y Acceso 7

1.2.2 Gestión de Participantes 7

1.2.3 Gestión de Áreas 7

1.2.4 Gestión de Casas de Vida 7

1.2.5 Gestión de Asistencia 7

1.2.6 Gestión de Escuelas de Formación 7

1.2.7 Gestión de Ofrendas 7

1.2.8 Gestión de Reportes 7

1.3 Personal involucrado 8

1.4 Definiciones, acrónimos y abreviaturas 8

1.5 Referencias 10

1.6 Resumen 12

2 Descripción general 12

2.1 Perspectiva del producto 12

2.2 Funcionalidad del producto 13

2.3 Diagrama UML 15

2.4 Características de los usuarios 16

2.4.1 Historia de Usuarios 18

2.5 Restricciones 25

2.6 Suposiciones y dependencias 26

2.7 Evolución previsible del sistema 27

3 Requisitos específicos. 28

3.1 Requisitos comunes de los interfaces 28

3.1.1 Interfaces de usuario 29

3.1.2 Interfaces de hardware 29

3.1.3 Interfaces de software 30

3.1.4 Interfaces de comunicación 30

3.2 Requisitos funcionales 30

3.2.1 RF01 – Iniciar Sesión 30

3.2.2 RF02 – Cerrar Sesión 31

3.2.3 RF03 – Gestionar Usuarios 31

3.2.4 RF04 – Gestionar Roles y Permisos 31

3.2.5 RF05 – Gestionar Participantes 32

3.2.6 RF06 – Consultar Participantes 32

3.2.7 RF07 – Gestionar Casas de Vida 33

3.2.8 RF08 – Consultar Casas de Vida Asignadas 33

3.2.9 RF09 – Registrar Asistencia 33

3.2.10 RF10 – Consultar Asistencia 34

3.2.11 RF11 – Realizar Seguimiento a Participantes 34

3.2.12 RF12 – Gestionar Actividades 35

3.2.13 RF13 – Enviar Reportes Casa Vida 35

3.2.14 RF14 – Enviar Reporte al Supervisor de Área 35

3.2.15 RF15 – Consultar Reportes 36

3.2.16 RF16 – Generar Reportes 36

3.2.17 RF17 – Gestionar Ofrendas 37

3.2.18 RF18 – Gestionar Escuelas de Formación 37

3.2.19 RF19 – Gestionar Pasos de Vida 37

3.2.20 RF20 – Gestionar Escuelas Vida 38

3.2.21 RF21 – Gestionar Módulos de Liderazgo 38

3.2.22 RF22 – Gestionar Misiones 39

3.2.23 RF23 – Visualizar Panel Principal por Rol 39

3.2.24 RF24 – Consultar Información Pública de la Iglesia 39

3.2.25 RF25 – Recuperar y Cambiar Contraseña 40

3.2.26 RF26 – Importar Datos Existentes 40

3.2.27 RF27 – Exportar Reportes 41

3.2.28 RF28 – Desactivar y Reactivar Registros 41

3.2.29 Matriz de trazabilidad 41

3.3 Requisitos no funcionales 42

3.3.1 RNF01 – Usabilidad 43

3.3.2 RNF02 – Tiempo de Respuesta 43

3.3.3 RNF03 – Autenticación 43

3.3.4 RNF04 – Control de Acceso 43

3.3.5 RNF05 – Protección de Credenciales 44

3.3.6 RNF06 – Confidencialidad 44

3.3.7 RNF07 – Integridad de la Información 44

3.3.8 RNF08 – Disponibilidad 44

3.3.9 RNF09 – Compatibilidad 45

3.3.10 RNF10 – Diseño Adaptable 45

3.3.11 RNF11 – Mantenibilidad 45

3.3.12 RNF12 – Escalabilidad 46

3.3.13 RNF13 – Validación de Datos 46

3.3.14 RNF14 – Recuperación ante Errores 46

3.3.15 RNF15 – Pruebas del Sistema 46

3.3.16 RNF16 – Privacidad y Protección de Datos 47

3.3.17 RNF17 – Respaldo y Recuperación 47

3.3.18 RNF18 – Trazabilidad 47

3.3.19 RNF19 – Política de Contraseñas 48

3.3.20 RNF20 – Seguridad de Sesión y Acceso 48

3.3.21 RNF21 – Comunicación Segura (HTTPS) 48

3.4 Reglas de Negocio 48

3.4.1 RN01 — Acceso según rol 48

3.4.2 RN02 — Administración de usuarios 49

3.4.3 RN03 — Acceso del Supervisor de Área 49

3.4.4 RN04 — Acceso del Líder de Casa de Vida 49

3.4.5 RN05 — Participación de usuarios de apoyo 49

3.4.6 RN06 — Envío de reportes al Supervisor 49

3.4.7 RN07 — Envío de reportes al Pastor 49

3.4.8 RN08 — Registro de asistencia 49

3.4.9 RN09 — Información de participantes 49

3.4.10 RN10 — Seguimiento de participantes 49

3.4.11 RN11 — Reportes 50

3.4.12 RN12 — Información de Escuelas de Formación 50

3.4.13 RN13 — Acceso a información de formación 50

3.4.14 RN14 — Registro de ofrendas 50

3.4.15 RN15 — Actualización de información 50

3.4.16 RN16 — Integridad de registros 50

3.4.17 RN17 — Información histórica 50

3.4.18 RN18 — Generación de información 50

3.4.19 RN19 — Generación de reportes por el Pastor 50

3.4.20 RN20 — Administración exclusiva de Casas de Vida 50

3.4.21 RN21 — Módulos independientes 51

3.4.22 RN22 — Acceso del Miembro Asistente 51

3.4.23 RN23 — Protección de datos personales 51

3.4.24 RN24 — Baja lógica de registros 51

3.4.25 RN25 — Datos importados 51

# Introducción

El presente documento corresponde a la Especificación de Requisitos de Software (ERS) de la Plataforma Web que se va a desarrollar para la iglesia CCMG de Girón, con el fin de gestionar el PVA, plan de vida abundante, que se ofrece dentro de la iglesia.

En este documento se tiene como finalidad establecer de manera organizada, clara y verificable las necesidades que se deben atender a la solución de software, así mismo, delimitar su alcance, identificar las personas involucradas, establecer los principales términos utilizados en el proyecto y documentar las fuentes que sustentan la definición de los requisitos.

La elaboración de este documento toma como referencia la problemática presentada dentro de la iglesia, debido a que en su mayoría los procesos que se realizan dentro de la misma institución, se hacen a mano, o en el mejor caso en hojas de cálculo o formularios de Google, por ende surge el planteamiento de esta solución, y también se toma como referencia los principios de ingeniería de requisitos y especificación de sistemas y software \[Ref. 10\], complementados con criterios relacionados con calidad \[Ref. 08\], seguridad \[Ref. 05, Ref. 06, Ref. 07\] y protección de datos personales \[Ref. 09\]. La estructura del documento se adapta a las características particulares del servicio Plan Vida Abundante y a los objetivos establecidos para el proyecto de grado.

## Propósito

El propósito de esta Especificación de Requisitos de Software es definir y documentar los requisitos que orientarán el análisis, diseño, desarrollo y validación de plataforma web destinada a apoyar la gestión administrativa y operativa del servicio Plan Vida Abundante (PVA) de la iglesia CCMG de Girón.

La plataforma busca centralizar la información relacionada con los procesos que actualmente requieren actividades manuales o el uso de herramientas independientes, facilitando su registro, consulta, actualización y seguimiento desde un sistema de información integrado.

El documento servirá como referencia para los estudiantes responsables del desarrollo, los líderes y administradores involucrados en el servicio y las demás personas que participen en la validación de las necesidades del sistema. Asimismo, permitirá establecer una base común para determinar qué funcionalidades deberá proporcionar la plataforma y cuáles serán sus condiciones de calidad, seguridad y uso.

De acuerdo con la propuesta de trabajo de grado, el sistema estará orientado a apoyar procesos relacionados con la gestión de participantes, Áreas, Casas de Vida, asistencia, Escuelas de Formación, ofrendas y generación de reportes. Los requisitos definidos en este documento deberán ser suficientemente claros y verificables para que posteriormente puedan relacionarse con los casos de uso, módulos del sistema, interfaces, elementos de la base de datos y pruebas de software correspondientes.

## Alcance

El proyecto contempla el análisis, especificación y desarrollo de una plataforma web orientada a la gestión del servicio Plan Vida Abundante de la iglesia CCMG de Girón.

La solución tendrá como propósito centralizar la información asociada a los procesos administrativos y operativos del servicio, disminuyendo la dependencia de registros físicos, hojas de cálculo y herramientas independientes. La propuesta de trabajo de grado identifica precisamente estas condiciones como parte de la problemática actual y plantea como solución la implementación de un sistema de información web que permita centralizar los datos y automatizar actividades de gestión.

El alcance inicial de la plataforma comprende las siguientes áreas:

### Gestión de Usuarios y Acceso

El usuario podrá ingresar a la plataforma mediante sus credenciales de acceso. Dependiendo del rol asignado, podrá acceder a las funcionalidades disponibles para su perfil. También podrá cerrar sesión, cambiar su contraseña y recuperar el acceso si la olvida.

### Gestión de Participantes

El Pastor podrá registrar, consultar y actualizar la información de los participantes vinculados al Plan Vida Abundante, de acuerdo con los datos definidos por la iglesia. Los demás roles solo consultarán la información que corresponda a su Casa de Vida, área o proceso. El Pastor también podrá importar los datos que hoy se mantienen en hojas de cálculo y formularios de Google, y desactivar registros en lugar de eliminarlos.

### Gestión de Áreas

El Pastor podrá registrar, consultar y actualizar la información correspondiente a las Áreas que hacen parte de la organización del Plan Vida Abundante y asignar a cada una sus Casas de Vida y su Supervisor de Área.

### Gestión de Casas de Vida

El Pastor podrá registrar, consultar y actualizar la información de las Casas de Vida, incluyendo los miembros y responsables asociados a cada una. El Supervisor de Área solo podrá consultar las Casas de Vida de su área, y el Líder de Casa de Vida y los usuarios de apoyo solo la información de su propia Casa de Vida, sin poder modificarlas.

### Gestión de Asistencia

El Líder de Casa de Vida, el Aprendiz, el Anfitrión y el Maestro de Niños podrán llenar y enviar al Supervisor de Área los reportes de asistencia de su Casa de Vida, indicando la actividad, la fecha y los participantes. El Pastor, el Supervisor de Área y el Coordinador de Formación podrán consultar la asistencia que corresponda a su alcance.

### Gestión de Escuelas de Formación

El Coordinador de Formación podrá registrar y consultar la información relacionada con las Escuelas de Formación, entendidas como el conjunto de procesos formativos del PVA que integra las Escuelas Vida, los Módulos de Liderazgo, los Pasos de Vida y Misiones. Esta gestión se realizará en un módulo independiente del módulo de Casas de Vida del PVA.

### Gestión de Ofrendas

El Pastor, o el usuario que este autorice expresamente como responsable de ofrendas, podrá registrar y consultar la información correspondiente a las ofrendas recibidas dentro de las actividades del Plan Vida Abundante, de acuerdo con la información definida por la iglesia.

### Gestión de Reportes

El Pastor podrá generar reportes semanales, mensuales o anuales a partir de la información registrada y de los reportes que los líderes envían al Supervisor de Área y este al Pastor. El Pastor es el último receptor de los reportes y no los envía. Los demás roles consultarán los reportes que correspondan a su alcance. Los reportes podrán exportarse en formato PDF o Excel.

## Personal involucrado

| | |
|---|---|
| Nombre | Joshua David Tarazona Gómez |
| Rol | Desarrollador e integrante del equipo del proyecto |
| Categoría profesional | Estudiante de Ingeniería de Sistemas |
| Responsabilidades | Análisis y diseño de la aplicación web, desarrollo de funcionalidades, gestión de la base de datos y pruebas del sistema. |
| Información de contacto | joshuadtarazona@uts.edu.co |

| | |
|---|---|
| Nombre | Karen Lizeth Arenas Medina |
| Rol | Desarrolladora e integrante del equipo del proyecto |
| Categoría profesional | Estudiante de Ingeniería de Sistemas |
| Responsabilidades | Análisis y diseño de la aplicación web, diseño de la interfaz de usuario, desarrollo de funcionalidades, pruebas del sistema, documentación. |
| Información de contacto | klizetharenas@uts.edu.co |

| | |
|---|---|
| Nombre | Néstor Fabian Luna Mejia |
| Rol | Pastor y Líder del Plan Vida Abundante (Administrador del Sistema) |
| Categoría profesional | Responsable del Servicio |
| Responsabilidades | Como Pastor y Administrador del Sistema, proporcionar información sobre los procesos del Plan Vida Abundante, validar los requisitos y verificar que las funcionalidades propuestas respondan a las necesidades del servicio. |
| Información de contacto | N/A |

| | |
|---|---|
| Nombre | Marta Isabel Gómez Neira |
| Rol | Administrador del servicio |
| Categoría profesional | Responsable administrativo |
| Responsabilidades | Proporcionar información sobre los procesos administrativos, validar la información requerida por el sistema y revisar las funcionalidades relacionadas con la gestión del servicio. |
| Información de contacto | N/A |

| | |
|---|---|
| Nombre | Alexander Anchicoque Calderón |
| Rol | Director o responsable académico |
| Categoría profesional | Docente / Director de proyecto |
| Responsabilidades | Orientar y revisar el desarrollo académico del proyecto de grado y verificar el cumplimiento de los criterios establecidos para su elaboración. |
| Información de contacto | N/A |

## Definiciones, acrónimos y abreviaturas

En esta sección se van a presentar las palabras clave por decirlo de alguna manera, que serán utilizadas en el presente documento, con el propósito de facilitar la comprensión de lo que se quiere lograr con la plataforma web.

**Tabla 1. Definiciones, acrónimos y abreviaturas**

| | |
|---|---|
| **TERMINO** | **DEFINICIÓN** |
| **CCMG** | Iglesia en la cual se desarrolla el servicio Plan Vida Abundante objeto del presente proyecto. |
| **PVA** | Plan Vida Abundante. Servicio ofrecido a los miembros de la iglesia CCMG de Girón y cuya gestión será apoyada mediante la plataforma web. |
| **ERS** | Especificación de Requisitos de Software. Documento que describe las necesidades, funcionalidades y condiciones que deberá cumplir el sistema. |
| **Usuario** | Persona que utiliza la plataforma de acuerdo con las funciones y permisos que tenga asignados. |
| **Requisito funcional (RF)** | Describen las funciones, servicios, entradas, salidas y reglas de negocio específicas que el software debe ejecutar. |
| **Requisito no funcional (RNF)** | Establecen las características de calidad, restricciones técnicas, seguridad, rendimiento y escalabilidad del sistema. |
| **Rol** | Conjunto de permisos y funciones asignados a un usuario dentro de la plataforma. |
| **Autenticación** | Proceso mediante el cual el sistema verifica la identidad de un usuario antes de permitirle el acceso. |
| **Autorización** | Proceso mediante el cual el sistema determina las funciones o información a las que puede acceder un usuario. |
| **Miembro** | Persona registrada dentro de la información gestionada por el Plan Vida Abundante. |
| **Área** | Estructura de organización del Plan Vida Abundante que agrupa y relaciona diferentes Casas de Vida. |
| **Casa de Vida** | Grupo o espacio de reunión perteneciente al Plan Vida Abundante y gestionado dentro de la plataforma. |
| **Escuelas Vida** | Proceso o espacio de formación desarrollado dentro del Plan Vida Abundante, cuya información podrá ser gestionada mediante la plataforma. |
| **Ofrenda** | Registro de información relacionada con las ofrendas recibidas dentro de las actividades contempladas en el Plan Vida Abundante. |
| **Reporte** | Información organizada que presenta datos registrados en el sistema para facilitar su consulta y seguimiento. |
| **Indicador** | Valor obtenido a partir de información registrada en el sistema que permite realizar seguimiento a determinados aspectos del Plan Vida Abundante. |
| **Base de Datos** | Conjunto organizado de información almacenada y gestionada por el sistema. |
| **Interfaz de Usuario** | Medio mediante el cual el usuario interactúa con las funcionalidades de la plataforma. |
| **API** | Application Programming Interface. Interfaz que permite la comunicación entre diferentes componentes de software. |
| **REST** | Representational State Transfer. Estilo arquitectónico que permite la comunicación entre sistemas mediante recursos y operaciones HTTP |
| **UML** | Unified Modeling Language. Lenguaje utilizado para representar mediante diagramas diferentes aspectos de un sistema. |
| **HU** | Historia de Usuario. Descripción de una funcionalidad desde la perspectiva de la persona que utilizará el sistema. |
| **CU** | Caso de Uso. Descripción de la interacción entre un usuario y el sistema para alcanzar un objetivo específico. |
| **RF** | Requisito Funcional. Funcionalidad o comportamiento que el sistema deberá proporcionar para satisfacer una necesidad determinada. |
| **RNF** | Requisito No Funcional. Condición o característica de calidad que deberá cumplir el sistema, como seguridad, rendimiento, usabilidad o disponibilidad. |
| **CRUD** | Create, Read, Update, Delete. Operaciones básicas para crear, consultar, actualizar y eliminar información. |
| **HTTPS** | Hypertext Transfer Protocol Secure. Versión segura del protocolo HTTP que utiliza mecanismos de cifrado para proteger la comunicación. |
| **PostgreSQL** | Sistema de gestión de bases de datos relacional que se contempla dentro de la propuesta tecnológica del proyecto |
| **Frontend** | Parte de la plataforma web con la que interactúa directamente el usuario, incluyendo las páginas, formularios, botones, gráficos y demás elementos visuales. |
| **Backend** | Parte de la plataforma encargada de procesar la información, gestionar las solicitudes, comunicarse con la base de datos y realizar la integración con servicios externos. |
| **Reporte de asistencia** | Documento que el Líder de Casa de Vida o un usuario de apoyo llena con la actividad, la fecha y los participantes que asistieron, y envía al Supervisor de Área. Cuando uno de ellos lo envía, aparece como enviado para todo el equipo de la Casa de Vida. |
| **Pastor** | Responsable del servicio Plan Vida Abundante y Administrador del Sistema. Gestiona usuarios, roles, Casas de Vida, ofrendas y reportes, y es el último receptor de los reportes: no los envía. |
| **Supervisor de Área** | Rol que consulta, en modo de solo lectura, las Casas de Vida de su área, recibe los reportes de asistencia de los líderes y envía al Pastor un reporte general de sus Casas de Vida. |
| **Líder de Casa de Vida** | Responsable de una Casa de Vida. Consulta la información de su Casa de Vida, sin poder editarla, y llena y envía los reportes de asistencia al Supervisor de Área. |
| **Aprendiz** | Usuario de apoyo de una Casa de Vida. Consulta la información de su Casa de Vida y, igual que el Líder, llena y envía los reportes de asistencia al Supervisor de Área. |
| **Anfitrión** | Usuario de apoyo de una Casa de Vida. Consulta la información de su Casa de Vida y, igual que el Líder, llena y envía los reportes de asistencia al Supervisor de Área. |
| **Maestro de Niños** | Usuario de apoyo de una Casa de Vida. Consulta la información de su Casa de Vida y, igual que el Líder, llena y envía los reportes de asistencia al Supervisor de Área. |
| **Coordinador de Formación** | Rol que gestiona los procesos de las Escuelas de Formación (Pasos de Vida, Escuelas Vida, Módulos de Liderazgo y Misiones) en el módulo Escuelas de Formación. |
| **Miembro Asistente** | Persona que asiste a los cultos o es nueva en la iglesia y no tiene cuenta en la plataforma. Solo puede ver la página pública con la información de la iglesia y de contacto. |
| **Escuelas de Formación** | Conjunto de procesos formativos del PVA que integra las Escuelas Vida, los Módulos de Liderazgo, los Pasos de Vida y Misiones. |
| **Baja lógica** | Desactivación de un registro que lo marca como inactivo sin borrarlo físicamente, de modo que se conserva para el historial y los reportes. |
| **Sesión** | Periodo durante el cual un usuario autenticado mantiene su acceso a la plataforma, hasta que cierra sesión o esta expira por inactividad. |
| **Criterio de aceptación** | Condición verificable que debe cumplirse para dar por terminada una historia de usuario. |
| **MoSCoW** | Método de priorización de requisitos: M (debe tener), S (debería tener) y C (podría tener). |

## Referencias

Las siguientes referencias corresponden a estándares, herramientas, tecnologías y documentación oficial como una fuente de apoyo para este documento, y que se tenga una mayor claridad de lo que se va a realizar.Las referencias están relacionadas con el desarrollo del sistema comprenden las tecnologías utilizadas para la construcción de la interfaz web, el desarrollo del servidor, la gestión de la base de datos, la seguridad y la protección de datos personales. En el texto se citan con el formato \[Ref. nn\].

| | | | | |
|---|---|---|---|---|
| **Referencia** | **Titulo** | **Ruta** | **Fecha** | **Autor** |
| \[Ref. 01\] | Tecnología web para desarrolladores | [MDN Web Docs – https://developer.mozilla.org/](https://developer.mozilla.org/en-US/docs/Web) | 2026 | Mozilla Developer Network (MDN) |
| \[Ref. 02\] | HTML: Lenguaje de Marcado de Hipertexto | [MDN Web Docs – https://developer.mozilla.org/en-US/docs/Web/HTML](https://developer.mozilla.org/es/docs/Web/HTML) | 2026 | Mozilla Developer Network (MDN) |
| \[Ref. 03\] | Approach – Bootstrap | [https://getbootstrap.com/docs/](https://getbootstrap.com/docs/5.3/getting-started/introduction/) | 2026 | The Bootstrap Authors |
| \[Ref. 04\] | Part I. Tutorial – PostgreSQL | [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/current/tutorial.html) | 2026 | PostgreSQL Global Development Group |
| \[Ref. 05\] | Authorization Cheat Sheet | | 2026 | OWASP Foundation |
| \[Ref. 06\] | Digital Identity Guidelines | [https://pages.nist.gov/800-63-4/](https://pages.nist.gov/800-63-4/sp800-63.html) | 2025 | National Institute of Standards and Technology (NIST) |
| \[Ref. 07\] | Digital Identity Guidelines: Authentication and Authenticator Management | | 2025 | National Institute of Standards and Technology (NIST) |
| \[Ref. 08\] | Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model | [ISO/IEC 25010:2023 – https://www.iso.org](https://www.iso.org/standard/78176.html) | 2023 | International Organization for Standardization (ISO) |
| \[Ref. 09\] | Ley Estatutaria 1581 de 2012 – Régimen general de protección de datos personales (habeas data) | | 2012 | Congreso de la República de Colombia |
| \[Ref. 10\] | Systems and software engineering — Life cycle processes — Requirements engineering | [ISO/IEC/IEEE 29148:2018 – https://www.iso.org](https://www.iso.org/standard/72089.html) | 2018 | ISO / IEC / IEEE |

## Resumen

El presente proyecto tiene como propósito desarrollar un sistema de información web para la gestión y administración del Plan Vida Abundante de la Iglesia CCMG de Girón. La propuesta surge a partir de las dificultades identificadas en los procesos administrativos de la iglesia, donde actividades como el registro de nuevos miembros, control de asistencia, seguimiento de participantes, gestión de Áreas y Casas de Vida, así como el control de ofrendas, se realizan principalmente mediante documentos físicos y herramientas ofimáticas independientes.

Ante esta situación, se plantea el desarrollo de una plataforma web que permita centralizar la información y facilitar la gestión de los diferentes procesos relacionados con el Plan Vida Abundante. El sistema contempla módulos orientados al registro y seguimiento de participantes, gestión de Áreas y Casas de Vida, control de asistencia, Escuelas de Formación, administración de ofrendas y generación de reportes, proporcionando a los líderes de la iglesia una herramienta para consultar y administrar la información de manera organizada.

El desarrollo del proyecto comprende el levantamiento de requerimientos con los líderes y administradores de la iglesia, el diseño de la arquitectura y la base de datos, la creación de interfaces orientadas a facilitar la interacción de los usuarios, la implementación de los módulos definidos y la incorporación de mecanismos de autenticación y control de acceso. Finalmente, se realizarán pruebas funcionales, de seguridad y usabilidad para verificar el correcto funcionamiento de la plataforma y corregir los posibles errores identificados.

Como resultado, se espera obtener una plataforma web funcional que contribuya a mejorar la organización y centralización de la información del Plan Vida Abundante, facilite el seguimiento de sus participantes y apoye a los líderes de la Iglesia CCMG en la consulta de información y en la toma de decisiones. Además, se contempla la elaboración de un manual de usuario, un manual de instalación y un documento técnico final que describa el desarrollo y los resultados obtenidos.

# Descripción general

## Perspectiva del producto

La plataforma web para la gestión y seguimiento del Plan Vida Abundante (PVA) de la Iglesia CCMG de Girón será una página orientada a centralizar y organizar la información relacionada con las actividades, participantes, Casas de Vida y escuelas de formación de la iglesia.

El producto permitirá reemplazar progresivamente el manejo de información mediante documentos físicos, registros independientes y herramientas no integradas, proporcionando un espacio centralizado para consultar, registrar y actualizar la información del PVA de acuerdo con los permisos asignados a cada usuario.

La plataforma estará organizada en módulos independientes: el módulo PVA – Casas de Vida (Casas de Vida, participantes, asistencia y reportes), el módulo Escuelas de Formación (Pasos de Vida, Escuelas Vida, Módulos de Liderazgo y Misiones), el panel de administración del Pastor y una página pública informativa de la iglesia. Aunque los módulos están relacionados, separarlos evita concentrar toda la información en un único módulo y permite que cada rol trabaje solo con lo que le corresponde.

El sistema será accesible mediante un navegador web y contará con mecanismos de identificación y control de acceso para proteger la información. El Pastor tendrá acceso a toda la información del PVA y de las Escuelas de Formación, con una interfaz propia, más completa e intuitiva que la de los demás roles por gestionar más funciones. El Supervisor de Área, el Líder de Casa de Vida y los usuarios de apoyo accederán solo a la información de su área o Casa de Vida y no podrán modificar las Casas de Vida; el Coordinador de Formación gestionará los procesos de las Escuelas de Formación; y el Miembro Asistente solo podrá ver la página pública de información y contacto de la iglesia.

La plataforma también permitirá generar información de apoyo para el seguimiento de las actividades del PVA, facilitando la consulta de registros y la elaboración de reportes que puedan contribuir a la gestión y toma de decisiones de los líderes de la Iglesia CCMG.

## Funcionalidad del producto

El sistema permitirá gestionar de manera centralizada la información relacionada con el Plan Vida Abundante de la Iglesia CCMG de Girón. Las principales funcionalidades del producto estarán organizadas de acuerdo con las áreas y responsabilidades de los usuarios.

Entre las funcionalidades principales se contemplan:

- **Gestión de usuarios:** permitir el registro, consulta y administración de los usuarios que tendrán acceso a la plataforma, de acuerdo con el rol asignado.

- **Gestión de participantes:** registrar y consultar la información de las personas vinculadas al Plan Vida Abundante, permitiendo realizar seguimiento a su participación dentro de las diferentes actividades.

- **Gestión de Casas de Vida:** administrar la información de las Casas de Vida, sus integrantes, responsables y actividades realizadas.

- **Seguimiento de Casas de Vida:** permitir al Supervisor de Área y al Líder de Casa de Vida consultar, en modo de solo lectura, la información relacionada con el funcionamiento de las Casas de Vida que les corresponden, y recibir o enviar los reportes de asistencia según su rol.

- **Gestión de asistencia:** registrar y consultar la asistencia de los participantes a las actividades correspondientes.

- **Gestión de Escuelas de Formación:** administrar la información relacionada con las diferentes escuelas, sus participantes, responsables y actividades de formación.

- **Gestión de módulos de liderazgo:** permitir el seguimiento de los participantes vinculados a los módulos de formación de liderazgo.

- **Gestión de Pasos de Vida:** registrar y consultar la información relacionada con el proceso de formación correspondiente a Pasos de Vida.

- **Gestión de Misiones:** administrar la información relacionada con las actividades y participantes vinculados al área de Misiones.

- **Gestión de ofrendas:** registrar y consultar la información relacionada con las ofrendas administradas dentro del Plan Vida Abundante, de acuerdo con los permisos establecidos.

- **Generación de reportes:** permitir al Pastor generar reportes semanales, mensuales o anuales a partir de la información registrada y de los reportes enviados por los líderes a través de los supervisores; los demás roles consultan los reportes que correspondan a su alcance.

- **Importación de datos:** permitir al Pastor cargar los datos de participantes y Casas de Vida que hoy se llevan en hojas de cálculo y formularios de Google.

- **Exportación de reportes:** permitir exportar en PDF o Excel los reportes que cada rol puede consultar.

- **Desactivación de registros:** desactivar usuarios, participantes y Casas de Vida en lugar de eliminarlos, conservando el historial.

- **Control de acceso:** restringir el acceso a las funciones de acuerdo con el rol y las responsabilidades asignadas a cada usuario.

Estas funcionalidades estarán orientadas a facilitar la administración del Plan Vida Abundante, reducir el manejo manual de información y proporcionar a los responsables una visión organizada de los procesos bajo su gestión.

## Diagrama UML

La Figura 1 presenta el diagrama de casos de uso de la plataforma, con los actores descritos en la sección 2.4 y las funcionalidades que cada uno puede realizar según su rol.

*Figura 1. Diagrama de casos de uso de la plataforma web PVA*

La Figura 2 presenta un modelo conceptual preliminar de las clases principales y sus relaciones, derivado de los requisitos y las reglas de negocio; podrá ajustarse durante el diseño de la base de datos.

*Figura 2. Modelo conceptual de clases de la plataforma web PVA (preliminar)*

## Características de los usuarios

Los usuarios del sistema estarán conformados por integrantes de la Iglesia CCMG que participan en la administración, coordinación, supervisión y desarrollo de las actividades del Plan Vida Abundante. Cada usuario tendrá diferentes responsabilidades y acceso a las funcionalidades de acuerdo con su rol.

| | |
|---|---|
| Tipo de usuario | Pastor (Administrador del Sistema) |
| Formación | N/A |
| Habilidades | Manejo básico de dispositivos tecnológicos, navegación web |
| Actividades | Usuario con responsabilidad administrativa general y último receptor de los reportes. Tiene acceso a toda la información del PVA y de las Escuelas de Formación; gestiona usuarios, roles y permisos, Casas de Vida (función exclusiva del Pastor) y ofrendas; y genera reportes semanales, mensuales o anuales con la información que envían los líderes a través de los supervisores. No envía reportes. Su interfaz es diferente a la de los demás roles y más intuitiva, porque gestiona más funciones. |

| | |
|---|---|
| Tipo de usuario | Supervisor de Área |
| Formación | N/A |
| Habilidades | Manejo básico de dispositivos tecnológicos, navegación web. |
| Actividades | Usuario que supervisa, en modo de solo lectura, únicamente las Casas de Vida de su área; no puede modificarlas, pues esa función corresponde al Pastor. Consulta la información de cada Casa de Vida y de sus participantes, recibe los reportes del Líder de Casa de Vida y de su equipo, y envía al Pastor un reporte general de las Casas de Vida que tiene asignadas. |

| | |
|---|---|
| Tipo de usuario | Líder de Casa de Vida |
| Formación | N/A |
| Habilidades | Manejo básico de dispositivos tecnológicos, navegación web. |
| Actividades | Usuario que consulta únicamente la información de su Casa de Vida, sin poder editarla ni modificarla. Llena los reportes de asistencia que se le solicitan y los envía al Supervisor de Área. |

| | |
|---|---|
| Tipo de usuario | Aprendiz |
| Formación | N/A |
| Habilidades | Manejo básico de dispositivos tecnológicos, navegación web. |
| Actividades | Usuario de apoyo de la Casa de Vida que consulta únicamente la información de su Casa de Vida y, igual que el Líder, llena y envía los reportes de asistencia al Supervisor de Área. Si cualquiera de ellos envía el reporte, este aparece como enviado para los demás integrantes de la Casa de Vida. |

| | |
|---|---|
| Tipo de usuario | Anfitrión |
| Formación | N/A |
| Habilidades | Manejo básico de dispositivos tecnológicos, navegación web. |
| Actividades | Usuario de apoyo de la Casa de Vida que consulta únicamente la información de su Casa de Vida y, igual que el Líder, llena y envía los reportes de asistencia al Supervisor de Área. Si cualquiera de ellos envía el reporte, este aparece como enviado para los demás integrantes de la Casa de Vida. |

| | |
|---|---|
| Tipo de usuario | Maestro de Niños |
| Formación | N/A |
| Habilidades | Manejo básico de dispositivos tecnológicos, navegación web. |
| Actividades | Usuario de apoyo de la Casa de Vida que consulta únicamente la información de su Casa de Vida y, igual que el Líder, llena y envía los reportes de asistencia al Supervisor de Área. Si cualquiera de ellos envía el reporte, este aparece como enviado para los demás integrantes de la Casa de Vida. |

| | |
|---|---|
| Tipo de usuario | Coordinador de Formación |
| Formación | N/A |
| Habilidades | Manejo básico de dispositivos tecnológicos, navegación web. |
| Actividades | Usuario que gestiona todos los procesos de las Escuelas de Formación del PVA: Pasos de Vida, Escuelas Vida, Misiones y Módulos de Liderazgo (participantes, actividades, asistencia y seguimiento). Trabaja en el módulo Escuelas de Formación, independiente del módulo PVA – Casas de Vida. |

| | |
|---|---|
| Tipo de usuario | Miembro Asistente |
| Formación | N/A |
| Habilidades | Manejo básico de dispositivos tecnológicos, navegación web. |
| Actividades | Usuario que asiste a los cultos o es nuevo en la iglesia y no tiene membresía de servicio en el PVA. No inicia sesión: solo puede ver la página pública con la información de la iglesia y de contacto. |

### Historia de Usuarios

**HU-01 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero iniciar sesión en la plataforma para acceder de manera segura a las funcionalidades correspondientes a mi rol.

**Criterios de aceptación:** (1) Con credenciales válidas, el sistema abre el panel del Pastor; (2) con credenciales inválidas, muestra un mensaje de error sin indicar cuál dato falló; (3) tras cinco intentos fallidos consecutivos, bloquea el acceso temporalmente (RNF20).

**HU-02 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero gestionar los usuarios para crear, actualizar, consultar y controlar las cuentas que tendrán acceso a la plataforma.

**Criterios de aceptación:** (1) El Pastor puede crear una cuenta indicando nombre, correo, rol y estado; (2) el sistema no permite dos cuentas con el mismo correo; (3) al desactivar una cuenta, el usuario ya no puede iniciar sesión y la cuenta permanece registrada.

**HU-03 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero asignar roles y permisos a los usuarios para controlar el acceso a las diferentes funcionalidades del sistema.

**Criterios de aceptación:** (1) Al asignar un rol, el usuario solo ve las opciones y datos de ese rol; (2) todo cambio de rol queda registrado con fecha y responsable; (3) un usuario sin rol asignado no puede acceder a funciones protegidas.

**HU-04 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero gestionar la información de los participantes para mantener un registro organizado y actualizado de las personas vinculadas al Plan Vida Abundante.

**Criterios de aceptación:** (1) No se guarda un participante sin los datos mínimos de RN09, incluida la autorización de tratamiento de datos; (2) el Pastor puede actualizar los datos y cada cambio queda con fecha y usuario; (3) cada participante queda asociado a una Casa de Vida.

**HU-05 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero gestionar las Casas de Vida para registrar y mantener actualizada la información relacionada con ellas.

**Criterios de aceptación:** (1) Solo el Pastor ve las opciones para crear y editar Casas de Vida; (2) cada Casa de Vida queda asignada a un Área, un Supervisor de Área y un Líder; (3) cada cambio queda registrado con fecha y usuario.

**HU-06 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero gestionar las Escuelas de Formación para administrar la información correspondiente a los diferentes procesos de formación.

**Criterios de aceptación:** (1) El Pastor puede registrar y editar Pasos de Vida, Escuelas Vida, Módulos de Liderazgo y Misiones; (2) cada proceso queda asociado a su área de formación; (3) la información se muestra en el módulo Escuelas de Formación, separado del de Casas de Vida.

**HU-07 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero consultar la asistencia reportada por las Casas de Vida y las Escuelas de Formación para llevar un control organizado de la participación en las diferentes actividades del Plan Vida Abundante.

**Criterios de aceptación:** (1) El Pastor puede filtrar la asistencia por fecha, Casa de Vida o escuela y actividad; (2) ve la asistencia de todas las Casas de Vida y Escuelas de Formación; (3) desde esta vista no puede modificar los registros.

**HU-08 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero registrar y consultar las ofrendas para mantener organizada la información relacionada con los registros de ofrendas del Plan Vida Abundante.

**Criterios de aceptación: (1) El registro de una ofrenda exige fecha, valor y concepto; (2) no se guarda una ofrenda con valor vacío o menor o igual a cero; (3) las ofrendas pueden consultarse por rango de fechas; (4) solo el Pastor o el usuario que él autorice como responsable de ofrendas accede a este módulo.**

**HU-09 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero acceder a toda la información del Plan Vida Abundante y de las Escuelas de Formación desde una interfaz diferente y más intuitiva, para conocer el estado de sus participantes, Casas de Vida y procesos de formación.

**Criterios de aceptación:** (1) Al iniciar sesión, el Pastor ve un panel propio con accesos a usuarios, roles, Casas de Vida, Escuelas de Formación, ofrendas y reportes; (2) el panel muestra un resumen de la información de su alcance; (3) los demás roles no ven este panel.

**HU-10 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero generar reportes semanales, mensuales o anuales con la información que los líderes envían a través de los supervisores, para facilitar el seguimiento y la toma de decisiones, entendiendo que soy el último receptor y no envío reportes.

**Criterios de aceptación:** (1) El Pastor puede elegir periodo semanal, mensual o anual y un rango de fechas; (2) el reporte se construye con los registros y los reportes enviados por los supervisores; (3) el Pastor no dispone de opción para enviar reportes.

**HU-11 — Supervisor de Área** Como supervisor de área, quiero consultar únicamente las Casas de Vida que están en mi área para realizar seguimiento a las actividades y participantes bajo mi responsabilidad, sin poder modificarlas.

**Criterios de aceptación:** (1) El Supervisor ve solo las Casas de Vida de su área; (2) no dispone de opciones de edición; (3) no puede abrir Casas de Vida de otras áreas.

**HU-12 — Supervisor de Área** Como supervisor de área, quiero consultar la información de los participantes de las Casas de Vida asignadas para conocer su participación y proceso.

**Criterios de aceptación:** (1) El Supervisor ve los participantes de las Casas de Vida de su área; (2) los datos se muestran en solo lectura; (3) no ve participantes de otras áreas.

**HU-13 — Supervisor de Área** Como supervisor de área, quiero consultar la asistencia reportada por las Casas de Vida de mi área para mantener actualizado el seguimiento de participación.

**Criterios de aceptación:** (1) El Supervisor puede consultar la asistencia reportada por las Casas de Vida de su área, filtrando por fecha; (2) no ve la asistencia de otras áreas; (3) puede identificar qué Casas de Vida ya enviaron su reporte.

**HU-14 — Supervisor de Área** Como supervisor de área, quiero consultar la información de cada Casa de Vida de mi área para conocer su desarrollo y las situaciones que requieran atención.

**Criterios de aceptación:** (1) El detalle de cada Casa de Vida muestra líder, usuarios de apoyo, participantes y actividades; (2) la información se muestra en solo lectura; (3) solo se accede a las Casas de Vida del área del Supervisor.

**HU-15 — Supervisor de Área** Como supervisor de área, quiero recibir y consultar los reportes que envían los líderes de Casa de Vida y su equipo para analizar la información de las actividades y participantes bajo mi responsabilidad.

**Criterios de aceptación:** (1) El Supervisor ve en una lista los reportes recibidos con fecha, Casa de Vida y remitente; (2) puede abrir y consultar cada reporte; (3) solo recibe reportes de las Casas de Vida de su área.

**HU-16 — Supervisor de Área** Como supervisor de área, quiero enviar al Pastor un reporte general de las Casas de Vida que tengo asignadas para comunicar el estado y los resultados de los procesos bajo mi supervisión.

**Criterios de aceptación:** (1) El Supervisor puede elegir el periodo y reunir los reportes recibidos de sus Casas de Vida; (2) al enviar, el reporte queda registrado como enviado con fecha y llega al Pastor; (3) el sistema confirma el envío.

**HU-17 — Líder de Casa de Vida** Como líder de Casa de Vida, quiero consultar la información de mi Casa de Vida y de sus participantes, sin poder editarla, para mantener un seguimiento organizado de las personas que participan en ella.

**Criterios de aceptación:** (1) El Líder ve la información de su Casa de Vida y de sus participantes; (2) no dispone de opciones de edición; (3) no puede abrir otras Casas de Vida.

**HU-18 — Líder de Casa de Vida** Como líder de Casa de Vida, quiero llenar los reportes de asistencia que se me piden y enviarlos al Supervisor de Área para mantener informado el estado de participación de mi Casa de Vida.

**Criterios de aceptación:** (1) El formulario del reporte pide actividad, fecha y asistencia de cada participante; (2) no se envía un reporte sin actividad, fecha o asistencia; (3) al enviar, el reporte llega al Supervisor de Área y el sistema confirma el envío.

**HU-19 — Líder de Casa de Vida** Como líder de Casa de Vida, quiero ver si el reporte de asistencia ya fue enviado, por mí o por alguien de mi equipo, para evitar envíos duplicados.

**Criterios de aceptación:** (1) El reporte muestra su estado (pendiente o enviado) y la fecha de envío; (2) si cualquier integrante del equipo ya lo envió, el sistema no permite enviarlo de nuevo; (3) el estado es el mismo para todos los integrantes de la Casa de Vida.

**HU-20 — Líder de Casa de Vida** Como líder de Casa de Vida, quiero incluir en el reporte la información de las actividades realizadas para que el Supervisor de Área conozca el desarrollo de mi Casa de Vida.

**Criterios de aceptación:** (1) El reporte permite registrar una o más actividades realizadas con nombre y fecha; (2) las actividades quedan asociadas a la Casa de Vida; (3) el Supervisor las ve al abrir el reporte.

**HU-21 — Aprendiz / Anfitrión / Maestro de Niños** Como usuario de apoyo de una Casa de Vida, quiero consultar la información de mi Casa de Vida correspondiente a mi función para conocer las actividades y participantes relacionados con mis responsabilidades.

**Criterios de aceptación:** (1) El usuario de apoyo ve la información de su Casa de Vida; (2) la información se muestra en solo lectura; (3) no puede abrir otras Casas de Vida.

**HU-22 — Aprendiz / Anfitrión / Maestro de Niños** Como usuario de apoyo, quiero llenar los reportes de asistencia de mi Casa de Vida, igual que el líder, para mantener informado al Supervisor de Área.

**Criterios de aceptación:** (1) El formulario del reporte pide actividad, fecha y asistencia de cada participante; (2) no se envía un reporte sin actividad, fecha o asistencia; (3) al enviar, el reporte llega al Supervisor de Área y el sistema confirma el envío.

**HU-23 — Aprendiz / Anfitrión / Maestro de Niños** Como usuario de apoyo, quiero ver que el reporte aparece como enviado cuando el líder u otro integrante del equipo ya lo envió para no repetirlo.

**Criterios de aceptación:** (1) Si el Líder u otro integrante ya envió el reporte, este aparece como enviado para el usuario de apoyo; (2) el sistema no permite enviarlo de nuevo; (3) se muestra la fecha del envío.

**HU-24 — Aprendiz / Anfitrión / Maestro de Niños** Como usuario de apoyo, quiero enviar el reporte de asistencia al Supervisor de Área para comunicar la información de las actividades y participantes de mi Casa de Vida.

**Criterios de aceptación:** (1) El usuario de apoyo puede enviar el reporte al Supervisor de Área de su Casa de Vida; (2) el sistema confirma el envío y marca el reporte como enviado para todo el equipo; (3) queda registrado quién lo envió y cuándo.

**HU-25 — Coordinador de Formación (Pasos de Vida)** Como Coordinador de Formación, quiero gestionar la información de los participantes de Pasos de Vida para realizar seguimiento a su proceso de formación.

**Criterios de aceptación:** (1) El Coordinador de Formación puede registrar y editar participantes de Pasos de Vida; (2) no se guarda un participante sin los datos obligatorios y la autorización de tratamiento de datos (RN09); (3) cada participante queda asociado a ese proceso.

**HU-26 — Coordinador de Formación (Pasos de Vida)** Como Coordinador de Formación, quiero registrar las actividades y asistencia de Pasos de Vida para mantener actualizado el proceso de formación.

**Criterios de aceptación:** (1) El Coordinador puede crear una actividad de Pasos de Vida con nombre, fecha y descripción; (2) puede registrar la asistencia de cada participante a la actividad; (3) no puede registrar asistencia de una persona que no esté vinculada a ese proceso.

**HU-27 — Coordinador de Formación (Pasos de Vida)** Como Coordinador de Formación, quiero consultar los reportes de Pasos de Vida para conocer el desarrollo y la participación en el proceso.

**Criterios de aceptación:** (1) El Coordinador puede consultar los reportes de Pasos de Vida filtrando por periodo; (2) la información corresponde únicamente a ese proceso; (3) puede exportar el reporte en PDF o Excel (RF27).

**HU-28 — Coordinador de Formación (Escuelas Vida)** Como Coordinador de Formación, quiero gestionar la información de los participantes de las Escuelas Vida para mantener actualizado el registro de formación.

**Criterios de aceptación:** (1) El Coordinador de Formación puede registrar y editar participantes de las Escuelas Vida; (2) no se guarda un participante sin los datos obligatorios y la autorización de tratamiento de datos (RN09); (3) cada participante queda asociado a ese proceso.

**HU-29 — Coordinador de Formación (Escuelas Vida)** Como Coordinador de Formación, quiero registrar actividades y asistencia de las Escuelas Vida para llevar un control de la participación.

**Criterios de aceptación:** (1) El Coordinador puede crear una actividad de las Escuelas Vida con nombre, fecha y descripción; (2) puede registrar la asistencia de cada participante a la actividad; (3) no puede registrar asistencia de una persona que no esté vinculada a ese proceso.

**HU-30 — Coordinador de Formación (Escuelas Vida)** Como Coordinador de Formación, quiero consultar los reportes de las Escuelas Vida para realizar seguimiento al desarrollo de las actividades y participantes.

**Criterios de aceptación:** (1) El Coordinador puede consultar los reportes de las Escuelas Vida filtrando por periodo; (2) la información corresponde únicamente a ese proceso; (3) puede exportar el reporte en PDF o Excel (RF27).

**HU-31 — Coordinador de Formación (Módulos de Liderazgo)** Como Coordinador de Formación, quiero gestionar la información de los participantes de los Módulos de Liderazgo para realizar seguimiento a su proceso de formación.

**Criterios de aceptación:** (1) El Coordinador de Formación puede registrar y editar participantes de los Módulos de Liderazgo; (2) no se guarda un participante sin los datos obligatorios y la autorización de tratamiento de datos (RN09); (3) cada participante queda asociado a ese proceso.

**HU-32 — Coordinador de Formación (Módulos de Liderazgo)** Como Coordinador de Formación, quiero registrar actividades y asistencia de los Módulos de Liderazgo para mantener actualizado el proceso de formación.

**Criterios de aceptación:** (1) El Coordinador puede crear una actividad de los Módulos de Liderazgo con nombre, fecha y descripción; (2) puede registrar la asistencia de cada participante a la actividad; (3) no puede registrar asistencia de una persona que no esté vinculada a ese proceso.

**HU-33 — Coordinador de Formación (Módulos de Liderazgo)** Como Coordinador de Formación, quiero consultar los reportes de los Módulos de Liderazgo para conocer su desarrollo y la participación de los usuarios.

**Criterios de aceptación:** (1) El Coordinador puede consultar los reportes de los Módulos de Liderazgo filtrando por periodo; (2) la información corresponde únicamente a ese proceso; (3) puede exportar el reporte en PDF o Excel (RF27).

**HU-34 — Coordinador de Formación (Misiones)** Como Coordinador de Formación, quiero gestionar la información de los participantes de Misiones para mantener actualizado el registro de las personas vinculadas.

**Criterios de aceptación:** (1) El Coordinador de Formación puede registrar y editar participantes de Misiones; (2) no se guarda un participante sin los datos obligatorios y la autorización de tratamiento de datos (RN09); (3) cada participante queda asociado a ese proceso.

**HU-35 — Coordinador de Formación (Misiones)** Como Coordinador de Formación, quiero registrar las actividades y asistencia de Misiones para llevar un control de la participación.

**Criterios de aceptación:** (1) El Coordinador puede crear una actividad de Misiones con nombre, fecha y descripción; (2) puede registrar la asistencia de cada participante a la actividad; (3) no puede registrar asistencia de una persona que no esté vinculada a ese proceso.

**HU-36 — Coordinador de Formación (Misiones)** Como Coordinador de Formación, quiero realizar seguimiento a las actividades y participantes de Misiones para conocer el desarrollo de sus procesos.

**Criterios de aceptación:** (1) El Coordinador puede registrar observaciones de seguimiento de un participante de Misiones con fecha y responsable (RN10); (2) puede consultar el historial de seguimiento de cada participante; (3) puede ver las actividades de Misiones y la participación de cada persona.

**HU-37 — Miembro Asistente** Como miembro asistente, quiero acceder a la página de inicio pública de la plataforma para visualizar información general de la congregación y sus datos de contacto sin necesidad de iniciar sesión.

**Criterios de aceptación:** (1) La página pública se abre sin iniciar sesión; (2) muestra la información de la iglesia y los datos de contacto; (3) no muestra datos de miembros, Casas de Vida, reportes ni ofrendas.

**HU-38 — Miembro Asistente** Como miembro asistente, quiero consultar la información general de qué es el Plan Vida Abundante (PVA) para conocer los procesos de formación y cómo puedo integrarme a una Casa de Vida.

**Criterios de aceptación:** (1) La información sobre el Plan Vida Abundante es accesible sin iniciar sesión; (2) explica los procesos de formación; (3) indica cómo contactar a la iglesia para integrarse a una Casa de Vida.

**HU-39 — Todos los usuarios autenticados** Como usuario autenticado, quiero cerrar sesión para proteger mi cuenta cuando termine de usar la plataforma, especialmente en equipos compartidos.

**Criterios de aceptación:** (1) La opción de cerrar sesión está visible en todas las pantallas autenticadas; (2) al cerrarla, el sistema redirige a la pantalla de inicio de sesión; (3) al volver atrás en el navegador no se muestra información protegida sin autenticarse de nuevo.

**HU-40 — Supervisor de Área / Líder de Casa de Vida / Aprendiz / Anfitrión / Maestro de Niños / Coordinador de Formación** Como usuario con cuenta, quiero iniciar sesión con mis credenciales para acceder únicamente a las funcionalidades de mi rol.

**Criterios de aceptación:** (1) Con credenciales válidas, el sistema abre el panel correspondiente a mi rol; (2) con credenciales inválidas, muestra un mensaje de error sin indicar cuál dato falló; (3) una cuenta desactivada no puede iniciar sesión; (4) tras cinco intentos fallidos consecutivos, el acceso se bloquea temporalmente (RNF20).

**HU-41 — Usuarios con cuenta** Como usuario con cuenta, quiero cambiar mi contraseña y recuperar el acceso si la olvido para no depender del Pastor cada vez que tenga un problema de acceso.

**Criterios de aceptación:** (1) Al solicitar la recuperación con un correo, el sistema muestra el mismo mensaje exista o no la cuenta; (2) el enlace recibido es de un solo uso y vence a los 60 minutos; (3) la nueva contraseña debe cumplir la política de RNF19; (4) al cambiarla, se cierran las demás sesiones activas.

**HU-42 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero importar los datos que hoy tengo en hojas de cálculo y formularios de Google para no volver a digitar la información existente.

**Criterios de aceptación:** (1) El sistema acepta archivos CSV o Excel (.xlsx) con la plantilla definida; (2) antes de confirmar, muestra una vista previa y las filas con errores; (3) no crea duplicados de una misma persona (mismo documento de identidad); (4) los participantes sin autorización de tratamiento de datos quedan marcados como autorización pendiente.

**HU-43 — Pastor / Supervisor de Área / Coordinador de Formación** Como usuario que consulta reportes, quiero exportarlos en PDF o Excel para compartirlos o archivarlos fuera de la plataforma.

**Criterios de aceptación:** (1) Cada reporte consultado ofrece la opción de exportar en PDF o Excel; (2) el archivo contiene solo la información que mi rol puede ver; (3) el archivo indica el periodo del reporte y la fecha de generación.

**HU-44 — Pastor / Administrador del Sistema** Como administrador del sistema, quiero desactivar usuarios, participantes y Casas de Vida en lugar de borrarlos para conservar el historial del Plan Vida Abundante.

**Criterios de aceptación:** (1) La acción disponible es desactivar, no eliminar; (2) los registros desactivados no aparecen en los listados habituales pero se conservan en los reportes históricos; (3) el Pastor puede reactivarlos; (4) cada cambio queda registrado con fecha y usuario.

## Restricciones

**Restricciones de alcance**

El sistema será desarrollado como una plataforma web orientada a la gestión y administración del Plan Vida Abundante de la Iglesia CCMG de Girón. El alcance inicial estará limitado a las funcionalidades definidas para el proyecto de grado.

El sistema no contempla inicialmente:

- Gestión completa de todos los procesos administrativos de la Iglesia que no estén relacionados con el Plan Vida Abundante.

- Integración directa con sistemas externos que no hayan sido definidos dentro del alcance del proyecto.

- Desarrollo de una aplicación móvil independiente.

- Automatización de procesos que requieran intervención externa a la plataforma.

- Implementación de funcionalidades que no hayan sido definidas y validadas durante el levantamiento de requerimientos.

- El proyecto de grado comprende el análisis, diseño, desarrollo y pruebas de la plataforma. Su despliegue en un servidor de producción y su puesta en uso por la congregación se realizarán con posterioridad y quedan fuera del alcance del proyecto de grado.

**Restricciones de acceso**

El acceso a la información y funcionalidades estará determinado por el rol asignado a cada usuario.

- El Pastor tendrá acceso a las funciones administrativas generales del sistema.

- Los Supervisores de Área tendrán acceso a la información relacionada con las Casas de Vida bajo su responsabilidad.

- Los Líderes de Casa de Vida y usuarios de apoyo tendrán acceso de acuerdo con las funciones asignadas.

- Los coordinadores de las Escuelas de Formación tendrán acceso a la información correspondiente a sus respectivas áreas.

- Los usuarios no podrán acceder a información que no corresponda a sus responsabilidades.

**Restricciones de información**

La información registrada en el sistema dependerá de los datos proporcionados por los responsables de cada área.

- La información deberá ser registrada por usuarios autorizados.

- Los registros deberán mantenerse actualizados.

- La generación de reportes dependerá de la información previamente registrada.

- La información relacionada con participantes, asistencia, seguimiento y ofrendas deberá manejarse de acuerdo con los permisos establecidos.

**Restricciones de seguridad**

El sistema deberá contar con mecanismos de identificación y control de acceso para proteger la información administrada.

Los usuarios deberán utilizar sus credenciales correspondientes para ingresar al sistema y las funcionalidades disponibles estarán condicionadas por su rol.

**Restricciones de desarrollo**

El sistema deberá mantenerse dentro del alcance y tiempo establecido para el proyecto de grado, por lo que cualquier nueva funcionalidad que surja durante el desarrollo deberá ser evaluada antes de incorporarse al proyecto.

Las funcionalidades futuras que no puedan ser desarrolladas durante el periodo establecido podrán quedar planteadas como posibles evoluciones del sistema.

## Suposiciones y dependencias

El funcionamiento de la plataforma estará sujeto a determinadas condiciones y recursos externos. Se consideran las siguientes suposiciones y dependencias:

**Disponibilidad de Internet**

Se supone que los usuarios contarán con una conexión a Internet para acceder a la plataforma web y utilizar las funcionalidades del sistema.

**Disponibilidad del servidor**

Se supone que el servidor donde se encuentre alojada la plataforma estará disponible para procesar las solicitudes realizadas por los usuarios y permitir el acceso a la información. Dado que se prevé un servicio de alojamiento de capacidad básica, la disponibilidad objetivo se define en el requisito RNF08.

**Disponibilidad de la base de datos**

El sistema dependerá de una base de datos disponible y correctamente configurada para almacenar y consultar la información relacionada con usuarios, participantes, Casas de Vida, asistencia, formación, seguimiento y demás procesos administrados.

**Disponibilidad de la plataforma**

Se supone que la plataforma estará disponible para los usuarios autorizados durante los periodos en los que la Iglesia requiera realizar las actividades de gestión y seguimiento del Plan Vida Abundante.

**Correcto registro de información**

Se supone que los usuarios responsables de cada área proporcionarán información correcta, completa y actualizada. La calidad de los reportes y consultas dependerá de la información registrada en el sistema.

**Participación de los responsables**

Se supone que el Pastor, Supervisores de Área, Líderes de Casa de Vida y coordinadores de las diferentes áreas participarán en la validación de los requerimientos y funcionalidades correspondientes a sus responsabilidades.

**Disponibilidad de los usuarios para las pruebas**

Se supone que los responsables de las diferentes áreas estarán disponibles durante las etapas de prueba y validación para comprobar que las funcionalidades desarrolladas respondan a las necesidades del Plan Vida Abundante.

**Compatibilidad del navegador**

Se supone que los usuarios accederán a la plataforma mediante alguno de los navegadores web indicados en el requisito RNF09.

**Evolución de las tecnologías**

Se asume que las tecnologías seleccionadas para el desarrollo estarán disponibles durante el periodo de ejecución del proyecto. Cambios importantes en dichas tecnologías podrían requerir modificaciones en la implementación.

**Dependencia de los requerimientos de la Iglesia**

La evolución y funcionamiento de determinadas funcionalidades dependerán de las necesidades y procesos definidos por la Iglesia CCMG. Cualquier cambio significativo en la forma de administrar el Plan Vida Abundante podrá requerir ajustes en el sistema.

## Evolución previsible del sistema

Aunque la primera versión de la plataforma estará enfocada en las funcionalidades definidas para la gestión y administración del Plan Vida Abundante, se contempla la posibilidad de incorporar nuevas características en futuras versiones de acuerdo con las necesidades de la Iglesia CCMG.

Entre las posibles mejoras se encuentran:

**Aplicación móvil**

Desarrollar una versión móvil de la plataforma para facilitar el acceso a la información y el registro de actividades desde teléfonos inteligentes y tabletas.

**Ampliación de los módulos**

Incorporar nuevos módulos relacionados con otros procesos administrativos y ministeriales de la Iglesia que actualmente no formen parte del alcance inicial.

**Notificaciones**

Incorporar notificaciones para informar a los usuarios sobre actividades pendientes, nuevos registros, reportes enviados, procesos de seguimiento y otras situaciones que requieran atención.

**Reportes e indicadores**

Ampliar las opciones de generación de reportes e incorporar indicadores que permitan analizar el crecimiento y comportamiento de las Casas de Vida, participantes y Escuelas de Formación.

**Seguimiento de participantes**

Ampliar las funcionalidades de seguimiento para permitir un registro más detallado del proceso de los participantes dentro del Plan Vida Abundante.

**Integración con otros sistemas**

En futuras versiones podría estudiarse la integración de la plataforma con otros sistemas o herramientas utilizadas por la Iglesia, con el propósito de evitar la duplicación de información y facilitar el intercambio de datos.

**Comunicación con participantes**

Incorporar funcionalidades que permitan facilitar la comunicación entre los responsables del Plan Vida Abundante y los participantes, de acuerdo con las necesidades de la Iglesia.

**Historial y análisis de información**

Incorporar herramientas para consultar información histórica y analizar la evolución de las Casas de Vida, procesos de formación, asistencia y participación a lo largo del tiempo.

**Ampliación de seguridad y permisos**

A medida que aumente el número de usuarios y la cantidad de información administrada, podrán incorporarse nuevos mecanismos de seguridad y opciones de control de acceso. Estas funcionalidades corresponden a posibles evoluciones del sistema y no hacen parte del alcance inicial definido para el presente proyecto de grado.

# Requisitos específicos.

## Requisitos comunes de los interfaces

La plataforma web para la gestión del Plan Vida Abundante de la Iglesia CCMG de Girón permitirá a los usuarios interactuar con la información correspondiente a sus funciones y responsabilidades, también habrá un apartado general donde usuarios comunes pueden interactuar con la plataforma, siendo este un apartado de información sobre la congregación. La plataforma contará con una interfaz gráfica para realizar consultas, registros, actualizaciones, seguimiento y generación de reportes.

El sistema también deberá comunicarse con los componentes necesarios para almacenar y consultar la información, principalmente la base de datos y los servicios utilizados para el funcionamiento de la plataforma.

### Interfaces de usuario

La plataforma contará con una interfaz web sencilla, organizada e intuitiva, que permita a los usuarios realizar las actividades correspondientes a su rol.

Las principales interfaces contempladas serán:

- **Inicio de sesión:** permitirá a los usuarios autenticarse para acceder al sistema, cerrar sesión y recuperar la contraseña.

- **Panel principal:** mostrará las opciones disponibles según el rol del usuario. El Pastor contará con un panel de administración propio, diferente al de los demás roles, más completo e intuitivo por concentrar más funciones (usuarios, roles, Casas de Vida, Escuelas de Formación, ofrendas y reportes).

- **Gestión de usuarios:** permitirá al Pastor administrar las cuentas de los usuarios.

- **Gestión de participantes:** permitirá registrar, consultar y actualizar la información de los participantes.

- **Módulo PVA – Casas de Vida:** el Pastor podrá registrar y administrar las Casas de Vida; el Supervisor de Área (las de su área), el Líder de Casa de Vida y los usuarios de apoyo (la suya) solo podrán consultarlas.

- **Asistencia:** permitirá al Líder de Casa de Vida y a los usuarios de apoyo llenar y enviar el reporte de asistencia, y a los demás roles consultarla según su alcance.

- **Ofrendas:** permitirá registrar y consultar la información correspondiente a las ofrendas.

- **Módulo Escuelas de Formación:** módulo independiente del de Casas de Vida, donde el Coordinador de Formación y el Pastor gestionan Pasos de Vida, Escuelas Vida, Módulos de Liderazgo y Misiones.

- **Reportes:** permitirá enviar el reporte de asistencia al Supervisor (Líder y usuarios de apoyo), enviar un reporte general al Pastor (Supervisor de Área) y generar reportes semanales, mensuales o anuales (Pastor). Los reportes podrán exportarse en PDF o Excel.

- **Perfil de usuario:** permitirá consultar y actualizar la información correspondiente a la cuenta del usuario.

- **Página pública de la iglesia:** permitirá al Miembro Asistente ver la información de la iglesia, del Plan Vida Abundante y de contacto, sin iniciar sesión.

Las opciones y funcionalidades visibles estarán condicionadas por el rol y los permisos asignados a cada usuario.

### Interfaces de hardware

La plataforma no requerirá hardware especializado.

Los usuarios podrán acceder al sistema mediante:

- Computadores de escritorio.

- Computadores portátiles.

- Tabletas.

- Teléfonos inteligentes.

Los dispositivos deberán contar con un navegador web compatible y conexión a Internet para acceder a la plataforma.

### Interfaces de software

La plataforma será desarrollada utilizando tecnologías web para la construcción de la interfaz, procesamiento de información y almacenamiento de datos.

Entre las tecnologías contempladas se encuentran:

- **HTML5:** para la estructura de las páginas web \[Ref. 02\].

- **CSS3:** para la presentación y diseño visual \[Ref. 01\].

- **JavaScript:** para la interacción y comportamiento de la interfaz \[Ref. 01\].

- **Bootstrap:** para apoyar la construcción de interfaces organizadas y adaptables \[Ref. 03\].

- **PostgreSQL:** para el almacenamiento y gestión de la información \[Ref. 04\].

- **Arquitectura cliente-servidor:** para separar la interfaz utilizada por los usuarios de los procesos de gestión de información.

Las tecnologías específicas utilizadas para el backend podrán definirse durante la etapa de diseño e implementación, de acuerdo con los requerimientos técnicos del proyecto.

### Interfaces de comunicación

La comunicación entre el navegador del usuario y el servidor se realizará mediante el protocolo seguro HTTPS (véase RNF21).

La aplicación deberá permitir el intercambio de información entre la interfaz, el servidor y la base de datos para realizar operaciones de consulta, registro, actualización y desactivación de información de acuerdo con los permisos del usuario.

Cuando se utilicen servicios o APIs para la comunicación entre componentes, el intercambio de información deberá realizarse mediante mecanismos definidos durante el diseño de la arquitectura del sistema.

## Requisitos funcionales

La prioridad de cada requisito se indica con el método MoSCoW: M — Debe tener (indispensable para la primera versión), S — Debería tener (importante, pero la plataforma puede operar sin él si el tiempo es limitado) y C — Podría tener (deseable). Los requisitos no funcionales usan la misma escala. Los requisitos se redactan siguiendo las recomendaciones de la norma ISO/IEC/IEEE 29148 \[Ref. 10\].

### RF01 – Iniciar Sesión

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF01 |
| **Nombre** | Iniciar Sesión |
| **Descripción** | El sistema permitirá a los usuarios ingresar a la plataforma mediante sus credenciales de acceso para utilizar las funcionalidades correspondientes a su rol. Tras varios intentos fallidos consecutivos, el sistema bloqueará temporalmente el acceso (véase RNF20). |
| **Actores** | Pastor, Supervisor de Área, Líder de Casa de Vida, Aprendiz, Anfitrión, Maestro de Niños y Coordinador de Formación. |
| **Entradas** | Usuario o correo electrónico y contraseña. |
| **Procesamiento** | El sistema validará las credenciales y verificará el rol y permisos asociados al usuario. |
| **Salidas** | Acceso al sistema o mensaje indicando que las credenciales no son válidas. |
| **Requisitos relacionados** | RNF03, RNF05, RNF14, RNF19, RNF20. |
| **Prioridad** | **M — Debe tener** |

### RF02 – Cerrar Sesión

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF02 |
| **Nombre** | Cerrar sesión |
| **Descripción** | El sistema permitirá al usuario cerrar su sesión para finalizar el acceso a la plataforma. |
| **Actores** | Todos los usuarios autenticados. |
| **Entradas** | Solicitud de cierre de sesión. |
| **Procesamiento** | El sistema finalizará la sesión activa del usuario. |
| **Salidas** | Redirección a la pantalla de inicio de sesión. |
| **Requisitos relacionados** | RNF03, RNF20. |
| **Prioridad** | **M — Debe tener** |

### RF03 – Gestionar Usuarios

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF03 |
| **Nombre** | Gestionar usuarios |
| **Descripción** | El sistema permitirá al Pastor crear, consultar, actualizar y desactivar las cuentas de los usuarios de la plataforma. La desactivación se realiza como baja lógica (véase RF28). |
| **Actores** | Pastor / Administrador del Sistema. |
| **Entradas** | Datos personales, información de acceso y estado del usuario. |
| **Procesamiento** | El sistema validará la información y almacenará o actualizará los datos correspondientes. |
| **Salidas** | Usuario registrado, actualizado, consultado o desactivado. |
| **Requisitos relacionados** | RNF04, RNF05, RNF07, RNF13, RNF18. |
| **Prioridad** | **M — Debe tener** |

### RF04 – Gestionar Roles y Permisos

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF04 |
| **Nombre** | Gestionar roles y permisos |
| **Descripción** | El sistema permitirá al administrador asignar y modificar los roles y permisos de los usuarios para controlar el acceso a las funcionalidades. |
| **Actores** | Pastor / Administrador del Sistema. |
| **Entradas** | Usuario, rol y permisos correspondientes. |
| **Procesamiento** | El sistema asociará los permisos definidos con el usuario seleccionado. |
| **Salidas** | Confirmación de la asignación o actualización de permisos. |
| **Requisitos relacionados** | RNF04, RNF06, RNF18. |
| **Prioridad** | **M — Debe tener** |

### RF05 – Gestionar Participantes

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF05 |
| **Nombre** | Gestionar Participantes |
| **Descripción** | El sistema permitirá al Pastor registrar y actualizar la información de las personas vinculadas al Plan Vida Abundante, y al Coordinador de Formación registrar y actualizar los participantes de las Escuelas de Formación. La consulta de participantes se describe en RF06, la importación de datos existentes en RF26 y la desactivación de registros en RF28. |
| **Actores** | Pastor / Administrador del Sistema y Coordinador de Formación (participantes de las Escuelas de Formación). |
| **Entradas** | Datos personales, datos relacionados con la participación en el PVA y autorización de tratamiento de datos personales (del representante legal si es menor de edad). |
| **Procesamiento** | El sistema validará y almacenará la información del participante. |
| **Salidas** | Registro creado o actualizado. |
| **Requisitos relacionados** | RNF04, RNF06, RNF07, RNF13, RNF16, RNF18. |
| **Prioridad** | **M — Debe tener** |

### RF06 – Consultar Participantes

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF06 |
| **Nombre** | Consultar Participantes |
| **Descripción** | Este requisito concentra la consulta de participantes para todos los roles; el registro y la actualización se describen en RF05. El sistema permitirá consultar la información de los participantes de acuerdo con el rol del usuario, en modo de solo lectura para el Supervisor de Área, el Líder de Casa de Vida y los usuarios de apoyo. |
| **Actores** | Pastor (todos los participantes), Supervisor de Área (Casas de Vida de su área), Líder de Casa de Vida y usuarios de apoyo (su Casa de Vida) y Coordinador de Formación (participantes de las Escuelas de Formación). |
| **Entradas** | Criterios de búsqueda o selección. |
| **Procesamiento** | El sistema realizará la búsqueda dentro de la información disponible para el usuario. |
| **Salidas** | Información de los participantes encontrados. |
| **Requisitos relacionados** | RNF02, RNF04, RNF06, RNF16. |
| **Prioridad** | **M — Debe tener** |

### RF07 – Gestionar Casas de Vida

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF07 |
| **Nombre** | Gestionar Casas de Vida |
| **Descripción** | El sistema permitirá al Pastor, de forma exclusiva, registrar, consultar y actualizar las Casas de Vida y asignar a cada una su Área, su Supervisor de Área, su Líder y sus integrantes. Ningún otro rol podrá modificar las Casas de Vida. |
| **Actores** | Pastor / Administrador del Sistema (exclusivo). |
| **Entradas** | Nombre de la Casa de Vida, Área, Supervisor de Área, Líder, usuarios de apoyo, participantes y demás datos requeridos. |
| **Procesamiento** | El sistema validará y almacenará la información de la Casa de Vida. |
| **Salidas** | Casa de Vida registrada, actualizada o consultada. |
| **Requisitos relacionados** | RNF04, RNF07, RNF13, RNF18. |
| **Prioridad** | **M — Debe tener** |

### RF08 – Consultar Casas de Vida Asignadas

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF08 |
| **Nombre** | Consultar Casas de Vida asignadas |
| **Descripción** | El sistema permitirá al Supervisor de Área consultar, en modo de solo lectura, únicamente las Casas de Vida de su área, con su información y la de sus participantes. No podrá modificarlas. |
| **Actores** | Supervisor de Área. |
| **Entradas** | Usuario autenticado. |
| **Procesamiento** | El sistema identificará las Casas de Vida del área del Supervisor, mostrará su información y bloqueará cualquier acción de edición. |
| **Salidas** | Listado e información de las Casas de Vida asignadas. |
| **Requisitos relacionados** | RNF02, RNF04, RNF06. |
| **Prioridad** | **M — Debe tener** |

### RF09 – Registrar Asistencia

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF09 |
| **Nombre** | Registrar asistencia |
| **Descripción** | El sistema permitirá al Líder de Casa de Vida y a los usuarios de apoyo llenar la asistencia de los participantes a las actividades de su Casa de Vida como parte del reporte de asistencia, y al Coordinador de Formación registrar la asistencia de sus procesos. |
| **Actores** | Líder de Casa de Vida, Aprendiz, Anfitrión, Maestro de Niños y Coordinador de Formación. |
| **Entradas** | Participante, actividad, fecha y estado de asistencia. |
| **Procesamiento** | El sistema validará la información y almacenará el registro de asistencia. |
| **Salidas** | Confirmación del registro o mensaje de error. |
| **Requisitos relacionados** | RNF02, RNF04, RNF07, RNF10, RNF13. |
| **Prioridad** | **M — Debe tener** |

### RF10 – Consultar Asistencia

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF10 |
| **Nombre** | Consultar asistencia |
| **Descripción** | El sistema permitirá consultar los registros de asistencia de acuerdo con el rol y las responsabilidades del usuario. |
| **Actores** | Pastor (toda la asistencia), Supervisor de Área (Casas de Vida de su área), Líder de Casa de Vida y usuarios de apoyo (su Casa de Vida) y Coordinador de Formación (sus procesos). |
| **Entradas** | Fecha, actividad, Casa de Vida, escuela u otros criterios de consulta. |
| **Procesamiento** | El sistema filtrará los registros disponibles para el usuario. |
| **Salidas** | Listado de registros de asistencia. |
| **Requisitos relacionados** | RNF02, RNF04, RNF06. |
| **Prioridad** | **M — Debe tener** |

### RF11 – Realizar Seguimiento a Participantes

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF11 |
| **Nombre** | Realizar seguimiento |
| **Descripción** | El sistema permitirá registrar y consultar información relacionada con el seguimiento de los participantes. El Pastor y el Coordinador de Formación pueden registrarlo; el Supervisor de Área y el Líder de Casa de Vida solo lo consultan, y las observaciones de seguimiento llegan a través de los reportes. |
| **Actores** | Pastor, Coordinador de Formación (registro y consulta); Supervisor de Área y Líder de Casa de Vida (solo consulta). |
| **Entradas** | Participante, fecha, observaciones, estado y datos del seguimiento. |
| **Procesamiento** | El sistema asociará el seguimiento con el participante correspondiente y almacenará la información. |
| **Salidas** | Registro de seguimiento creado o actualizado. |
| **Requisitos relacionados** | RNF04, RNF06, RNF07, RNF16, RNF18. |
| **Prioridad** | **S — Debería tener** |

### RF12 – Gestionar Actividades

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF12 |
| **Nombre** | Gestionar actividades |
| **Descripción** | El sistema permitirá al Pastor y al Coordinador de Formación registrar y consultar las actividades de los procesos de formación, y al Líder de Casa de Vida y a los usuarios de apoyo informar las actividades realizadas en su Casa de Vida dentro del reporte de asistencia. |
| **Actores** | Pastor, Líder de Casa de Vida, Aprendiz, Anfitrión, Maestro de Niños y Coordinador de Formación. |
| **Entradas** | Nombre, fecha, descripción, responsable y demás información de la actividad. |
| **Procesamiento** | El sistema almacenará y relacionará la actividad con el área correspondiente. |
| **Salidas** | Actividad registrada, actualizada o consultada. |
| **Requisitos relacionados** | RNF04, RNF07, RNF13. |
| **Prioridad** | **S — Debería tener** |

### RF13 – Enviar Reportes Casa Vida

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF13 |
| **Nombre** | Enviar Reportes Casa Vida |
| **Descripción** | El sistema permitirá al Supervisor de Área enviar al Pastor un reporte general de las Casas de Vida que tiene asignadas, construido a partir de los reportes recibidos de los líderes y su equipo. |
| **Actores** | Supervisor de Área. |
| **Entradas** | Periodo, Casas de Vida del área, reportes recibidos y observaciones. |
| **Procesamiento** | El sistema almacenará el reporte general y lo asociará al Supervisor, a su área y a sus Casas de Vida. |
| **Salidas** | Confirmación del envío del reporte al Pastor. |
| **Requisitos relacionados** | RNF04, RNF07, RNF18. |
| **Prioridad** | **M — Debe tener** |

### RF14 – Enviar Reporte al Supervisor de Área

| | |
|---|---|
| Campo | Descripción |
| Identificador | RF14 |
| Nombre | Enviar reporte de asistencia al Supervisor |
| Descripción | El sistema permitirá al Líder de Casa de Vida, Aprendiz, Anfitrión y Maestro de Niños llenar el reporte de asistencia de su Casa de Vida y enviarlo al Supervisor de Área. Cuando uno de ellos lo envía, el reporte aparecerá como enviado para los demás integrantes de la Casa de Vida. |
| Actores | Líder de Casa de Vida, Aprendiz, Anfitrión y Maestro de Niños. |
| Entradas | Información del reporte, actividad, fecha, participantes y observaciones. |
| Procesamiento | El sistema almacenará el reporte, lo asociará a la Casa de Vida y al Supervisor correspondiente y lo marcará como enviado para todo el equipo de la Casa de Vida. |
| Salidas | Confirmación del envío y estado «enviado» visible para los integrantes de la Casa de Vida. |
| Requisitos relacionados | RNF04, RNF07, RNF10, RNF18. |
| Prioridad | **M — Debe tener** |

### RF15 – Consultar Reportes

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF15 |
| **Nombre** | Consultar reportes |
| **Descripción** | El sistema permitirá consultar los reportes ya enviados o generados (su creación se describe en RF13, RF14 y RF16) de acuerdo con el rol: el Pastor, los reportes generales de los supervisores; el Supervisor de Área, los reportes de los líderes y su equipo; el Líder de Casa de Vida, los de su Casa de Vida; y el Coordinador de Formación, los de sus procesos. La exportación se describe en RF27. |
| **Actores** | Pastor, Supervisor de Área, Líder de Casa de Vida y Coordinador de Formación. |
| **Entradas** | Periodo, área, Casa de Vida o tipo de reporte. |
| **Procesamiento** | El sistema filtrará y organizará los reportes disponibles. |
| **Salidas** | Información de los reportes consultados. |
| **Requisitos relacionados** | RNF02, RNF04, RNF06. |
| **Prioridad** | **M — Debe tener** |

### RF16 – Generar Reportes

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF16 |
| **Nombre** | Generar reportes |
| **Descripción** | El sistema permitirá al Pastor generar reportes semanales, mensuales o anuales a partir de la información registrada y de los reportes enviados por los líderes a través de los supervisores. El Pastor es el último receptor de los reportes y no los envía. Este requisito cubre la generación de nuevos reportes consolidados; la consulta de reportes ya enviados o generados se describe en RF15. |
| **Actores** | Pastor / Administrador del Sistema y Coordinador de Formación (reportes de sus procesos). |
| **Entradas** | Tipo de periodo (semanal, mensual o anual), rango de fechas, área o Casa de Vida. |
| **Procesamiento** | El sistema recopilará y organizará la información correspondiente. |
| **Salidas** | Reporte generado con la información solicitada. |
| **Requisitos relacionados** | RNF02, RNF04, RNF06. |
| **Prioridad** | **M — Debe tener** |

### RF17 – Gestionar Ofrendas

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF17 |
| **Nombre** | Gestionar ofrendas |
| **Descripción** | El sistema permitirá registrar y consultar la información correspondiente a las ofrendas administradas dentro del Plan Vida Abundante. |
| **Actores** | Pastor / Administrador del Sistema (y el usuario que el Pastor autorice expresamente como responsable de ofrendas). |
| **Entradas** | Fecha, valor, concepto y demás información definida para el registro. |
| **Procesamiento** | El sistema validará y almacenará la información de la ofrenda. |
| **Salidas** | Registro de ofrenda creado o consultado. |
| **Requisitos relacionados** | RNF04, RNF06, RNF07, RNF13, RNF16, RNF18. |
| **Prioridad** | **S — Debería tener** |

### RF18 – Gestionar Escuelas de Formación

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF18 |
| **Nombre** | Gestionar Escuelas de Formación |
| **Descripción** | El sistema permitirá administrar la información de las Escuelas de Formación del Plan Vida Abundante, entendidas como el marco general que integra las Escuelas Vida, los Módulos de Liderazgo, los Pasos de Vida y Misiones, en un módulo independiente del módulo PVA – Casas de Vida. |
| **Actores** | Pastor / Administrador del Sistema y Coordinador de Formación. |
| **Entradas** | Nombre de la escuela o proceso, responsable, participantes, actividades y demás información correspondiente. |
| **Procesamiento** | El sistema almacenará y actualizará la información de las escuelas y procesos de formación. |
| **Salidas** | Información de las Escuelas de Formación registrada o consultada. |
| **Requisitos relacionados** | RNF04, RNF07, RNF13. |
| **Prioridad** | **S — Debería tener** |

### RF19 – Gestionar Pasos de Vida

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF19 |
| **Nombre** | Gestionar Pasos de Vida |
| **Descripción** | El sistema permitirá al Coordinador de Formación gestionar la información de los participantes y actividades relacionadas con este proceso de formación. |
| **Actores** | Pastor / Administrador del Sistema y Coordinador de Formación. |
| **Entradas** | Participantes, actividades, asistencia y seguimiento. |
| **Procesamiento** | El sistema registrará y relacionará la información con el proceso de Pasos de Vida. |
| **Salidas** | Información registrada, actualizada o consultada. |
| **Requisitos relacionados** | RNF04, RNF07, RNF13. |
| **Prioridad** | **S — Debería tener** |

### RF20 – Gestionar Escuelas Vida

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF20 |
| **Nombre** | Gestionar Escuelas Vida |
| **Descripción** | El sistema permitirá al Coordinador de Formación gestionar participantes, actividades, asistencia y seguimiento relacionados con las Escuelas Vida, como proceso específico dentro de las Escuelas de Formación. |
| **Actores** | Pastor / Administrador del Sistema y Coordinador de Formación. |
| **Entradas** | Participantes, actividades, asistencia y datos de seguimiento. |
| **Procesamiento** | El sistema almacenará y relacionará la información con las Escuelas Vida correspondientes. |
| **Salidas** | Información registrada, actualizada o consultada. |
| **Requisitos relacionados** | RNF04, RNF07, RNF13. |
| **Prioridad** | **S — Debería tener** |

### RF21 – Gestionar Módulos de Liderazgo

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF21 |
| **Nombre** | Gestionar Módulos de Liderazgo |
| **Descripción** | El sistema permitirá al Coordinador de Formación gestionar la información de participantes, actividades, asistencia y seguimiento relacionados con los módulos. |
| **Actores** | Pastor / Administrador del Sistema y Coordinador de Formación. |
| **Entradas** | Participantes, actividades, asistencia y seguimiento. |
| **Procesamiento** | El sistema almacenará y relacionará la información con los módulos correspondientes. |
| **Salidas** | Información registrada, actualizada o consultada. |
| **Requisitos relacionados** | RNF04, RNF07, RNF13. |
| **Prioridad** | **S — Debería tener** |

### RF22 – Gestionar Misiones

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF22 |
| **Nombre** | Gestionar Misiones |
| **Descripción** | El sistema permitirá al Coordinador de Formación gestionar la información de participantes, actividades, asistencia y seguimiento relacionados con las actividades de Misiones. |
| **Actores** | Pastor / Administrador del Sistema y Coordinador de Formación. |
| **Entradas** | Participantes, actividades, asistencia y seguimiento. |
| **Procesamiento** | El sistema almacenará y relacionará la información con las actividades de Misiones. |
| **Salidas** | Información registrada, actualizada o consultada. |
| **Requisitos relacionados** | RNF04, RNF07, RNF13. |
| **Prioridad** | **S — Debería tener** |

### RF23 – Visualizar Panel Principal por Rol

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF23 |
| **Nombre** | Visualizar panel principal por rol |
| **Descripción** | El sistema mostrará a cada usuario autenticado un panel principal propio de su rol, con accesos a los módulos que le corresponden y un resumen de la información de su alcance (por ejemplo, para el Pastor: totales de Casas de Vida, participantes y reportes recibidos). El panel no sustituye las consultas detalladas descritas en RF06, RF10 y RF15. |
| **Actores** | Todos los usuarios autenticados. |
| **Entradas** | Usuario autenticado y rol asignado. |
| **Procesamiento** | El sistema verificará el rol y los permisos y mostrará solo los módulos y resúmenes disponibles para el usuario. |
| **Salidas** | Panel principal con los accesos y resúmenes correspondientes al rol. |
| **Requisitos relacionados** | RNF01, RNF02, RNF04, RNF06. |
| **Prioridad** | **S — Debería tener** |

### RF24 – Consultar Información Pública de la Iglesia

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF24 |
| **Nombre** | Consultar información pública |
| **Descripción** | El sistema permitirá al Miembro Asistente, sin necesidad de iniciar sesión, ver la página pública con la información de la iglesia, qué es el Plan Vida Abundante y los datos de contacto. |
| **Actores** | Miembro Asistente (visitante sin cuenta). |
| **Entradas** | Solicitud de acceso a la página de inicio pública. |
| **Procesamiento** | El sistema mostrará la información pública sin requerir autenticación y no dará acceso a información de miembros, Casas de Vida, reportes ni ofrendas. |
| **Salidas** | Página pública con información de la iglesia, del PVA y de contacto. |
| **Requisitos relacionados** | RNF02, RNF06, RNF09, RNF10. |
| **Prioridad** | **S — Debería tener** |

### RF25 – Recuperar y Cambiar Contraseña

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF25 |
| **Nombre** | Recuperar y cambiar contraseña |
| **Descripción** | El sistema permitirá a los usuarios con cuenta cambiar su contraseña estando autenticados y recuperar el acceso cuando la olviden, mediante un enlace temporal enviado a su correo electrónico registrado. |
| **Actores** | Pastor, Supervisor de Área, Líder de Casa de Vida, Aprendiz, Anfitrión, Maestro de Niños y Coordinador de Formación. |
| **Entradas** | Correo electrónico registrado (recuperación); contraseña actual y nueva contraseña (cambio). |
| **Procesamiento** | El sistema generará un enlace de un solo uso con vigencia limitada (RNF20), validará que la nueva contraseña cumpla la política de RNF19, la almacenará protegida (RNF05) y cerrará las demás sesiones activas del usuario. |
| **Salidas** | Mensaje de confirmación. El sistema responderá igual exista o no el correo en la plataforma, para no revelar qué cuentas existen. |
| **Requisitos relacionados** | RNF05, RNF19, RNF20, RNF21. |
| **Prioridad** | **M — Debe tener** |

### RF26 – Importar Datos Existentes

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF26 |
| **Nombre** | Importar datos existentes |
| **Descripción** | El sistema permitirá al Pastor cargar los datos de participantes y Casas de Vida que hoy se mantienen en hojas de cálculo y formularios de Google, a partir de archivos CSV o Excel. Otros conjuntos de datos se definirán con la iglesia. |
| **Actores** | Pastor / Administrador del Sistema. |
| **Entradas** | Archivo CSV o Excel (.xlsx) con la plantilla definida por el sistema. |
| **Procesamiento** | El sistema validará el formato y los datos obligatorios (RN09), detectará duplicados por documento de identidad, mostrará una vista previa con los errores encontrados y cargará los datos solo después de la confirmación del Pastor. Los participantes sin autorización de tratamiento de datos quedarán marcados con autorización pendiente (RN25) y se registrará el usuario y la fecha de la importación. |
| **Salidas** | Resumen con registros importados, omitidos y con error, y archivo descargable con el detalle de los errores. |
| **Requisitos relacionados** | RNF07, RNF13, RNF16, RNF18. |
| **Prioridad** | **S — Debería tener** |

### RF27 – Exportar Reportes

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF27 |
| **Nombre** | Exportar reportes |
| **Descripción** | El sistema permitirá exportar en formato PDF o Excel (.xlsx) los reportes que el usuario puede consultar según RF15 y RF16. |
| **Actores** | Pastor, Supervisor de Área, Líder de Casa de Vida y Coordinador de Formación. |
| **Entradas** | Reporte seleccionado y formato de exportación. |
| **Procesamiento** | El sistema generará el archivo solo con la información que el rol del usuario puede ver, e incluirá el periodo del reporte y la fecha de generación. |
| **Salidas** | Archivo PDF o Excel descargable. |
| **Requisitos relacionados** | RNF02, RNF04, RNF06, RNF16. |
| **Prioridad** | **S — Debería tener** |

### RF28 – Desactivar y Reactivar Registros

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RF28 |
| **Nombre** | Desactivar y reactivar registros |
| **Descripción** | En lugar de eliminar información, el sistema desactivará (baja lógica) los usuarios, participantes, Áreas, Casas de Vida y procesos de formación. Los registros desactivados dejan de aparecer en los listados y selecciones habituales, pero se conservan para el historial y los reportes (RN17) y pueden reactivarse. |
| **Actores** | Pastor / Administrador del Sistema. |
| **Entradas** | Registro seleccionado, acción (desactivar o reactivar) y motivo opcional. |
| **Procesamiento** | El sistema marcará el estado del registro, guardará el usuario y la fecha del cambio y advertirá si el registro tiene relaciones activas (por ejemplo, una Casa de Vida con participantes). No se eliminará físicamente ningún registro. |
| **Salidas** | Registro desactivado o reactivado. |
| **Requisitos relacionados** | RNF07, RNF18. |
| **Prioridad** | **M — Debe tener** |

### Matriz de trazabilidad

La siguiente matriz relaciona cada requisito funcional con las historias de usuario, las reglas de negocio y los requisitos no funcionales que lo sustentan.

| **Requisito** | **Historias de usuario** | **Reglas de negocio** | **RNF relacionados** |
|---|---|---|---|
| **RF01** | HU-01, HU-40 | RN01 | RNF03, RNF05, RNF14, RNF19, RNF20 |
| **RF02** | HU-39 | RN01 | RNF03, RNF20 |
| **RF03** | HU-02 | RN02 | RNF04, RNF05, RNF07, RNF13, RNF18 |
| **RF04** | HU-03 | RN01, RN02 | RNF04, RNF06, RNF18 |
| **RF05** | HU-04 | RN09, RN15, RN23 | RNF04, RNF06, RNF07, RNF13, RNF16, RNF18 |
| **RF06** | HU-12, HU-17, HU-21 | RN03, RN04, RN05, RN13 | RNF02, RNF04, RNF06, RNF16 |
| **RF07** | HU-05 | RN20 | RNF04, RNF07, RNF13, RNF18 |
| **RF08** | HU-11, HU-14 | RN03 | RNF02, RNF04, RNF06 |
| **RF09** | HU-18, HU-22, HU-26, HU-29, HU-32, HU-35 | RN08 | RNF02, RNF04, RNF07, RNF10, RNF13 |
| **RF10** | HU-07, HU-13 | RN08 | RNF02, RNF04, RNF06 |
| **RF11** | HU-36 | RN10 | RNF04, RNF06, RNF07, RNF16, RNF18 |
| **RF12** | HU-20, HU-26, HU-29, HU-32, HU-35 | RN12 | RNF04, RNF07, RNF13 |
| **RF13** | HU-16 | RN07 | RNF04, RNF07, RNF18 |
| **RF14** | HU-18, HU-19, HU-22, HU-23, HU-24 | RN06 | RNF04, RNF07, RNF10, RNF18 |
| **RF15** | HU-15, HU-27, HU-30, HU-33 | RN18 | RNF02, RNF04, RNF06 |
| **RF16** | HU-10 | RN11, RN19 | RNF02, RNF04, RNF06 |
| **RF17** | HU-08 | RN14 | RNF04, RNF06, RNF07, RNF13, RNF16, RNF18 |
| **RF18** | HU-06 | RN12, RN13, RN21 | RNF04, RNF07, RNF13 |
| **RF19** | HU-25, HU-26, HU-27 | RN12, RN13 | RNF04, RNF07, RNF13 |
| **RF20** | HU-28, HU-29, HU-30 | RN12, RN13 | RNF04, RNF07, RNF13 |
| **RF21** | HU-31, HU-32, HU-33 | RN12, RN13 | RNF04, RNF07, RNF13 |
| **RF22** | HU-34, HU-35, HU-36 | RN12, RN13 | RNF04, RNF07, RNF13 |
| **RF23** | HU-09 | RN18 | RNF01, RNF02, RNF04, RNF06 |
| **RF24** | HU-37, HU-38 | RN22 | RNF02, RNF06, RNF09, RNF10 |
| **RF25** | HU-41 | RN01 | RNF05, RNF19, RNF20, RNF21 |
| **RF26** | HU-42 | RN09, RN16, RN23, RN25 | RNF07, RNF13, RNF16, RNF18 |
| **RF27** | HU-43 | RN18 | RNF02, RNF04, RNF06, RNF16 |
| **RF28** | HU-44 | RN17, RN24 | RNF07, RNF18 |

Los requisitos no funcionales RNF01 (usabilidad), RNF08 (disponibilidad), RNF09 (compatibilidad), RNF11 (mantenibilidad), RNF12 (escalabilidad), RNF15 (pruebas del sistema) y RNF17 (respaldo y recuperación) y RNF21 (comunicación segura) aplican de forma transversal a todos los requisitos funcionales.

## Requisitos no funcionales

Los requisitos no funcionales se clasifican tomando como referencia las características de calidad del producto del modelo ISO/IEC 25010 \[Ref. 08\], como usabilidad, seguridad, compatibilidad y mantenibilidad. Los requisitos de seguridad adicionales (RNF19 a RNF21) complementan la autenticación y el control de acceso.

### RNF01 – Usabilidad

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF01 |
| **Nombre** | Usabilidad |
| **Descripción** | La plataforma deberá presentar interfaces sencillas, organizadas y comprensibles para facilitar el uso por parte de los diferentes usuarios. La interfaz del Pastor será diferente a la de los demás roles y más intuitiva, por concentrar más funciones de administración. |
| **Métrica** | El 90 % de los usuarios debe completar las tareas principales en menos de 2 minutos sin ayuda externa. |
| **Prioridad** | M — Debe tener |

### RNF02 – Tiempo de Respuesta

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF02 |
| **Nombre** | Tiempo de respuesta |
| **Descripción** | El sistema deberá responder oportunamente a las solicitudes realizadas por los usuarios bajo condiciones normales de funcionamiento. |
| **Métrica** | El 95 % de las solicitudes principales deberá responder en un tiempo igual o inferior a 3 segundos bajo condiciones normales de conexión y carga. |
| **Prioridad** | M — Debe tener |

### RNF03 – Autenticación

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF03 |
| **Nombre** | Autenticación |
| **Descripción** | Las funcionalidades privadas del sistema deberán requerir que el usuario se encuentre autenticado. Se siguen las recomendaciones de identidad digital y autenticación de \[Ref. 06\] y \[Ref. 07\]. |
| **Métrica** | El 100 % de las funcionalidades protegidas deberá requerir una sesión válida para su acceso. |
| **Prioridad** | M — Debe tener |

### RNF04 – Control de Acceso

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF04 |
| **Nombre** | Control de acceso |
| **Descripción** | El acceso a la información y funcionalidades deberá estar controlado de acuerdo con el rol y los permisos asignados al usuario. Se toman como guía las buenas prácticas de autorización de \[Ref. 05\]. |
| **Métrica** | El 100 % de las funcionalidades protegidas deberá verificar los permisos correspondientes antes de permitir el acceso. |
| **Prioridad** | M — Debe tener |

### RNF05 – Protección de Credenciales

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF05 |
| **Nombre** | Protección de credenciales |
| **Descripción** | Las contraseñas y credenciales de los usuarios deberán protegerse para evitar su exposición dentro del sistema. Para su gestión se toman como referencia las recomendaciones de \[Ref. 07\]. |
| **Métrica** | Las contraseñas no deberán almacenarse en texto plano dentro de la base de datos. |
| **Prioridad** | M — Debe tener |

### RNF06 – Confidencialidad

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF06 |
| **Nombre** | Confidencialidad |
| **Descripción** | La información de participantes, asistencia, seguimiento, ofrendas y demás datos del PVA deberá estar protegida contra accesos no autorizados. |
| **Métrica** | Los usuarios sin los permisos correspondientes deberán ser rechazados al intentar acceder a información protegida. |
| **Prioridad** | M — Debe tener |

### RNF07 – Integridad de la Información

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF07 |
| **Nombre** | Integridad de la información |
| **Descripción** | El sistema deberá mantener la consistencia de la información registrada y evitar datos incompletos o relaciones incorrectas. |
| **Métrica** | Los datos obligatorios y las relaciones entre registros deberán validarse antes de ser almacenados. |
| **Prioridad** | M — Debe tener |

### RNF08 – Disponibilidad

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF08 |
| **Nombre** | Disponibilidad |
| **Descripción** | La plataforma deberá estar disponible para los usuarios durante el horario de uso definido por la iglesia, teniendo en cuenta que se prevé alojarla en un servicio de capacidad básica. |
| **Métrica** | Disponibilidad mensual de al menos 95 % durante el horario de uso definido por la iglesia, sin contar los mantenimientos programados avisados con al menos 24 horas de anticipación. |
| **Prioridad** | S — Debería tener |

### RNF09 – Compatibilidad

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF09 |
| **Nombre** | Compatibilidad |
| **Descripción** | La plataforma deberá funcionar correctamente en los navegadores web modernos más usados por los usuarios, en computador y en dispositivos móviles. |
| **Métrica** | Las funciones principales deberán ejecutarse sin errores bloqueantes en las dos últimas versiones estables de Google Chrome, Microsoft Edge, Mozilla Firefox y Safari (escritorio), y en Chrome (Android) y Safari (iOS), verificadas en las pruebas del sistema. |
| **Prioridad** | S — Debería tener |

### RNF10 – Diseño Adaptable

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF10 |
| **Nombre** | Diseño adaptable |
| **Descripción** | La interfaz deberá adaptarse a diferentes tamaños de pantalla para facilitar su utilización desde computadores, tabletas y dispositivos móviles. |
| **Métrica** | Las pantallas principales deberán conservar su legibilidad y funcionalidad en computadores, tabletas y teléfonos inteligentes. |
| **Prioridad** | S — Debería tener |

### RNF11 – Mantenibilidad

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF11 |
| **Nombre** | Mantenibilidad |
| **Descripción** | El sistema deberá mantener una estructura organizada y modular (módulo PVA – Casas de Vida, módulo Escuelas de Formación y panel de administración) que facilite la corrección de errores y la realización de cambios posteriores. |
| **Métrica** | Los módulos y componentes principales deberán estar organizados y documentados de manera que permitan realizar modificaciones controladas. |
| **Prioridad** | S — Debería tener |

### RNF12 – Escalabilidad

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF12 |
| **Nombre** | Escalabilidad |
| **Descripción** | El sistema deberá soportar el crecimiento esperado en cantidad de usuarios, participantes, Casas de Vida y procesos de formación sin degradar su desempeño y sin necesidad de modificar el código para agregar Áreas, Casas de Vida o procesos de formación. |
| **Métrica** | Soportar hasta 500 participantes, 60 Casas de Vida y 100 cuentas de usuario, con 30 usuarios conectados simultáneamente, cumpliendo RNF02. Agregar nuevas Áreas, Casas de Vida y procesos de formación desde la interfaz, sin cambios en el código. |
| **Prioridad** | S — Debería tener |

### RNF13 – Validación de Datos

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF13 |
| **Nombre** | Validación de datos |
| **Descripción** | El sistema deberá validar la información ingresada por los usuarios antes de almacenarla. |
| **Métrica** | Los campos obligatorios, formatos y valores permitidos deberán ser verificados antes de guardar la información. |
| **Prioridad** | M — Debe tener |

### RNF14 – Recuperación ante Errores

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF14 |
| **Nombre** | Recuperación ante errores |
| **Descripción** | El sistema deberá informar de manera clara los errores que se presenten y evitar el almacenamiento de información inválida. |
| **Métrica** | Los errores de validación y procesamiento deberán generar mensajes comprensibles y no deberán producir registros inválidos. |
| **Prioridad** | S — Debería tener |

### RNF15 – Pruebas del Sistema

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF15 |
| **Nombre** | Pruebas del sistema |
| **Descripción** | El sistema deberá ser sometido a pruebas funcionales, de seguridad y de usabilidad antes de su entrega final. |
| **Métrica** | Cada requisito funcional definido como obligatorio deberá contar con al menos un caso de prueba documentado y ejecutado. |
| **Prioridad** | M — Debe tener |

### RNF16 – Privacidad y Protección de Datos

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF16 |
| **Nombre** | Privacidad y protección de datos |
| **Descripción** | El sistema deberá tratar los datos personales de los participantes de acuerdo con las políticas de privacidad de la iglesia y con la Ley Estatutaria 1581 de 2012 \[Ref. 09\] (protección de datos personales) y su reglamentación. Se requiere la autorización previa, expresa e informada del titular o, en el caso de menores de edad, de su representante legal, y la información de la finalidad del tratamiento. La pertenencia a la iglesia puede revelar convicciones religiosas, por lo que podrá considerarse dato sensible. |
| **Métrica** | Ningún participante podrá registrarse sin la autorización de tratamiento de sus datos; los datos personales solo serán accesibles para los usuarios autorizados y no se compartirán con terceros sin consentimiento; la iglesia definirá y publicará su política de tratamiento de datos. |
| **Prioridad** | M — Debe tener |

### RNF17 – Respaldo y Recuperación

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF17 |
| **Nombre** | Respaldo y recuperación |
| **Descripción** | El sistema deberá contemplar mecanismos de respaldo de la información para permitir su recuperación ante fallos. |
| **Métrica** | Deberá realizarse al menos un respaldo semanal de la base de datos y documentarse el procedimiento de restauración. |
| **Prioridad** | S — Debería tener |

### RNF18 – Trazabilidad

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF18 |
| **Nombre** | Trazabilidad |
| **Descripción** | El sistema deberá registrar información que permita identificar al usuario responsable de las operaciones de creación, actualización y desactivación de registros. |
| **Métrica** | Cada registro deberá almacenar al menos el usuario creador, la fecha de creación y la fecha de última modificación. |
| **Prioridad** | S — Debería tener |

### RNF19 – Política de Contraseñas

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF19 |
| **Nombre** | Política de contraseñas |
| **Descripción** | Las contraseñas deberán cumplir una política que dificulte su adivinación, siguiendo las recomendaciones de \[Ref. 07\]. |
| **Métrica** | Longitud mínima de 15 caracteres, sin exigir combinaciones obligatorias de tipos de caracteres, rechazando contraseñas comunes o de uso frecuente y sin vencimiento periódico obligatorio. |
| **Prioridad** | M — Debe tener |

### RNF20 – Seguridad de Sesión y Acceso

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF20 |
| **Nombre** | Seguridad de sesión y acceso |
| **Descripción** | El sistema deberá limitar la duración de las sesiones inactivas y protegerse contra intentos repetidos de adivinar credenciales. |
| **Métrica** | La sesión expira tras 30 minutos de inactividad. Tras 5 intentos fallidos consecutivos de inicio de sesión se bloquea el acceso durante 15 minutos. Los enlaces de recuperación de contraseña son de un solo uso y vencen a los 60 minutos. |
| **Prioridad** | M — Debe tener |

### RNF21 – Comunicación Segura (HTTPS)

| | |
|---|---|
| **Campo** | **Descripción** |
| **Identificador** | RNF21 |
| **Nombre** | Comunicación segura (HTTPS) |
| **Descripción** | Toda la comunicación entre el navegador del usuario y el servidor deberá cifrarse mediante HTTPS. |
| **Métrica** | El 100 % de las solicitudes se atienden por HTTPS con un certificado válido y TLS 1.2 o superior; las solicitudes HTTP se redirigen a HTTPS. |
| **Prioridad** | M — Debe tener |

## Reglas de Negocio

### RN01 — Acceso según rol

Cada usuario deberá acceder únicamente a las funcionalidades que correspondan al rol y permisos asignados dentro de la plataforma.

### RN02 — Administración de usuarios

La creación, actualización, desactivación y administración de roles de los usuarios estará a cargo del Pastor como Administrador del Sistema.

### RN03 — Acceso del Supervisor de Área

El Supervisor de Área podrá consultar, en modo de solo lectura, únicamente las Casas de Vida de su área. No podrá modificarlas.

### RN04 — Acceso del Líder de Casa de Vida

El Líder de Casa de Vida podrá consultar únicamente la información de su propia Casa de Vida y no podrá editarla. Su gestión se limita a llenar y enviar los reportes de asistencia al Supervisor de Área.

### RN05 — Participación de usuarios de apoyo

El Aprendiz, Anfitrión y Maestro de Niños podrán consultar únicamente la información de su Casa de Vida y llenar y enviar los reportes de asistencia, igual que el Líder.

### RN06 — Envío de reportes al Supervisor

El Líder de Casa de Vida y los usuarios de apoyo podrán enviar el reporte de asistencia al Supervisor de Área de su Casa de Vida. Si uno de ellos envía el reporte, este aparecerá como enviado para los demás integrantes de la Casa de Vida.

### RN07 — Envío de reportes al Pastor

El Supervisor de Área podrá enviar al Pastor un reporte general de las Casas de Vida que tiene asignadas. El Pastor es el último receptor de los reportes y no puede enviarlos.

### RN08 — Registro de asistencia

Cada registro de asistencia deberá estar relacionado con un participante, una actividad o proceso y una fecha determinada.

### RN09 — Información de participantes

Un participante deberá contar con la información mínima requerida para poder ser registrado en el sistema, la cual comprende: nombres y apellidos, documento de identidad, fecha de nacimiento, teléfono de contacto, dirección, Casa de Vida a la que pertenece y la autorización para el tratamiento de sus datos personales.

### RN10 — Seguimiento de participantes

Los registros de seguimiento deberán estar asociados al participante correspondiente y deberán permitir identificar la fecha y responsable del registro.

### RN11 — Reportes

Los reportes generados por el sistema deberán construirse a partir de la información registrada en la plataforma.

### RN12 — Información de Escuelas de Formación

Cada proceso de formación deberá estar asociado al área correspondiente, como Pasos de Vida, Escuelas Vida, Módulos de Liderazgo o Misiones.

### RN13 — Acceso a información de formación

El Coordinador de Formación podrá consultar y gestionar la información de los procesos de las Escuelas de Formación (Pasos de Vida, Escuelas Vida, Módulos de Liderazgo y Misiones).

### RN14 — Registro de ofrendas

La información de las ofrendas solo podrá ser registrada y consultada por el Pastor o por el usuario que este autorice expresamente como responsable de ofrendas.

### RN15 — Actualización de información

Los usuarios autorizados podrán actualizar únicamente la información que se encuentre dentro de sus responsabilidades.

### RN16 — Integridad de registros

El sistema no deberá permitir guardar registros que incumplan los datos obligatorios o las relaciones requeridas para mantener la consistencia de la información.

### RN17 — Información histórica

Los registros que sean necesarios para el seguimiento histórico del Plan Vida Abundante deberán conservarse de acuerdo con las políticas que defina la Iglesia CCMG.

### RN18 — Generación de información

La información presentada en consultas y reportes deberá corresponder a los datos registrados en la plataforma y a los permisos del usuario que realiza la consulta.

### RN19 — Generación de reportes por el Pastor

El Pastor podrá generar reportes semanales, mensuales o anuales a partir de la información registrada y de los reportes enviados por los líderes a través de los supervisores. El Pastor es el último receptor de los reportes y no los envía.

### RN20 — Administración exclusiva de Casas de Vida

Solo el Pastor podrá crear, modificar y asignar Casas de Vida, Áreas y Supervisores. Los demás roles solo podrán consultar la información que les corresponda.

### RN21 — Módulos independientes

La plataforma se organizará en módulos independientes: PVA – Casas de Vida y Escuelas de Formación, además del panel de administración del Pastor y la página pública. Cada rol accederá únicamente a los módulos de su responsabilidad.

### RN22 — Acceso del Miembro Asistente

El Miembro Asistente no inicia sesión y solo podrá ver la página pública con la información de la iglesia y de contacto.

### RN23 — Protección de datos personales

El tratamiento de los datos personales de los participantes requerirá la autorización previa, expresa e informada de su titular o, en el caso de menores de edad, de su representante legal, conforme a la Ley 1581 de 2012. Los datos se utilizarán únicamente para las finalidades informadas por la iglesia.

### RN24 — Baja lógica de registros

Los usuarios, participantes, Áreas, Casas de Vida y procesos de formación no se eliminan físicamente: se desactivan y se conservan para el historial, conforme a RN17. Solo el Pastor puede desactivarlos o reactivarlos.

### RN25 — Datos importados

Los datos cargados mediante importación deben cumplir las mismas reglas que los registrados manualmente (RN09 y RN16). Los participantes importados sin autorización de tratamiento de datos quedan marcados con autorización pendiente, y su autorización debe obtenerse conforme a RN23.

## Descripción de casos de uso

### CU01 — Iniciar sesión

Campo
Descripción

Identificador
CU01

Nombre
Iniciar sesión

Actores
Pastor, Supervisor de Área, Líder de Casa de Vida, Aprendiz, Anfitrión, Maestro de Niños y Coordinador de Formación.

Precondiciones
El usuario tiene una cuenta activa.

Flujo principal
1. El usuario abre la página de inicio de sesión.
2. Ingresa su usuario o correo y su contraseña.
3. El sistema valida las credenciales, el estado de la cuenta y el rol.
4. El sistema muestra el panel principal correspondiente al rol.

Flujos alternos
Credenciales inválidas: el sistema muestra un mensaje de error y no concede el acceso.
Tras 5 intentos fallidos consecutivos el acceso se bloquea temporalmente (RNF20).
Cuenta desactivada: el sistema informa que no puede ingresar.

Postcondiciones
Sesión activa con los permisos del rol.

Requisitos relacionados
RF01, RF02, RF25.

### CU02 — Llenar y enviar reporte de asistencia

Campo
Descripción

Identificador
CU02

Nombre
Llenar y enviar reporte de asistencia

Actores
Líder de Casa de Vida, Aprendiz, Anfitrión y Maestro de Niños.

Precondiciones
Sesión iniciada y reporte del periodo aún no enviado.

Flujo principal
1. El usuario abre el reporte de asistencia de su Casa de Vida.
2. Selecciona la actividad y la fecha.
3. Marca la asistencia de los participantes y agrega actividades y observaciones.
4. Envía el reporte al Supervisor de Área.
5. El sistema valida y guarda el reporte, lo marca como enviado para todo el equipo de la Casa de Vida y confirma el envío.

Flujos alternos
Si otro integrante ya envió el reporte, el sistema lo muestra como enviado y no permite reenviarlo.
Si faltan datos obligatorios, el sistema muestra un error de validación y no guarda.

Postcondiciones
Reporte almacenado y visible para el Supervisor de Área.

Requisitos relacionados
RF09, RF12, RF14.

### CU03 — Enviar reporte general al Pastor

Campo
Descripción

Identificador
CU03

Nombre
Enviar reporte general al Pastor

Actores
Supervisor de Área.

Precondiciones
Sesión iniciada y reportes recibidos de las Casas de Vida de su área.

Flujo principal
1. El supervisor consulta los reportes recibidos de su área.
2. Selecciona el periodo y las Casas de Vida del área.
3. Agrega observaciones generales.
4. Envía el reporte general al Pastor.
5. El sistema guarda el reporte, lo asocia al supervisor y a sus Casas de Vida y confirma el envío.

Flujos alternos
Si no hay reportes en el periodo, el sistema informa y no permite el envío vacío.

Postcondiciones
Reporte general disponible para consulta del Pastor.

Requisitos relacionados
RF13, RF15.

### CU04 — Generar reportes

Campo
Descripción

Identificador
CU04

Nombre
Generar reportes

Actores
Pastor / Administrador del Sistema (y Coordinador de Formación para sus procesos).

Precondiciones
Sesión iniciada y datos registrados en el sistema.

Flujo principal
1. El usuario elige el tipo de periodo (semanal, mensual o anual) y el rango de fechas.
2. Opcionalmente filtra por Área, Casa de Vida o proceso de formación.
3. El sistema recopila la información registrada y muestra el reporte.
4. Opcionalmente, el usuario exporta el reporte a PDF o Excel.

Flujos alternos
Si no hay datos para el periodo, el sistema muestra un mensaje informativo.

Postcondiciones
Reporte generado. El Pastor no lo envía a nadie, porque es el último receptor.

Requisitos relacionados
RF16, RF27.

### CU05 — Gestionar Casas de Vida

Campo
Descripción

Identificador
CU05

Nombre
Gestionar Casas de Vida

Actores
Pastor / Administrador del Sistema.

Precondiciones
Sesión iniciada; Áreas y usuarios ya registrados.

Flujo principal
1. El Pastor abre el módulo PVA – Casas de Vida.
2. Crea una Casa de Vida o selecciona una existente.
3. Ingresa o actualiza nombre, Área, Supervisor, Líder y usuarios de apoyo.
4. Guarda los cambios.
5. El sistema valida y almacena la información.

Flujos alternos
Si faltan datos obligatorios, el sistema muestra un error y no guarda.
Para desactivar una Casa de Vida, el sistema aplica baja lógica y conserva su historial (RN24).

Postcondiciones
Casa de Vida registrada o actualizada y visible, en solo lectura, para su Supervisor y su Líder.

Requisitos relacionados
RF07, RF28.

### CU06 — Registrar participante

Campo
Descripción

Identificador
CU06

Nombre
Registrar participante

Actores
Pastor / Administrador del Sistema y Coordinador de Formación.

Precondiciones
Sesión iniciada; la Casa de Vida o el proceso de formación ya existen.

Flujo principal
1. El usuario abre el formulario de registro de participantes.
2. Ingresa los datos mínimos (RN09).
3. Registra la autorización de tratamiento de datos (del representante legal si es menor de edad).
4. Guarda el registro.
5. El sistema valida y almacena al participante asociado a su Casa de Vida o proceso.

Flujos alternos
Sin autorización de tratamiento de datos, el sistema no guarda el registro.
Si el documento de identidad ya existe, el sistema informa del duplicado.

Postcondiciones
Participante registrado y asociado a su Casa de Vida o proceso de formación.

Requisitos relacionados
RF05, RF26.

