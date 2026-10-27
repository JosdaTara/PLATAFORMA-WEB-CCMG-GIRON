--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.8

-- Started on 2026-10-27 15:50:25

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 873 (class 1247 OID 25134)
-- Name: estado_general; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.estado_general AS ENUM (
    'ACTIVO',
    'INACTIVO'
);


ALTER TYPE public.estado_general OWNER TO postgres;

--
-- TOC entry 867 (class 1247 OID 25118)
-- Name: tipo_modulo; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tipo_modulo AS ENUM (
    'CASA_VIDA',
    'ESCUELAS_FORMACION'
);


ALTER TYPE public.tipo_modulo OWNER TO postgres;

--
-- TOC entry 870 (class 1247 OID 25124)
-- Name: tipo_proceso; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tipo_proceso AS ENUM (
    'ESCUELAS_VIDA',
    'MODULOS_LIDERAZGO',
    'PASOS_VIDA',
    'MISIONES'
);


ALTER TYPE public.tipo_proceso OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 234 (class 1259 OID 25304)
-- Name: actividad; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actividad (
    id_actividad integer NOT NULL,
    tipo_modulo public.tipo_modulo NOT NULL,
    id_casa_vida integer,
    id_proceso_formacion integer,
    titulo character varying(150) NOT NULL,
    fecha date NOT NULL,
    hora time without time zone,
    descripcion text,
    id_responsable integer,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_actividad_modulo CHECK ((((tipo_modulo = 'CASA_VIDA'::public.tipo_modulo) AND (id_casa_vida IS NOT NULL) AND (id_proceso_formacion IS NULL)) OR ((tipo_modulo = 'ESCUELAS_FORMACION'::public.tipo_modulo) AND (id_proceso_formacion IS NOT NULL) AND (id_casa_vida IS NULL))))
);


ALTER TABLE public.actividad OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 25303)
-- Name: actividad_id_actividad_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.actividad_id_actividad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.actividad_id_actividad_seq OWNER TO postgres;

--
-- TOC entry 5079 (class 0 OID 0)
-- Dependencies: 233
-- Name: actividad_id_actividad_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.actividad_id_actividad_seq OWNED BY public.actividad.id_actividad;


--
-- TOC entry 222 (class 1259 OID 25189)
-- Name: area; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.area (
    id_area integer NOT NULL,
    nombre character varying(100) NOT NULL,
    id_supervisor integer,
    estado public.estado_general DEFAULT 'ACTIVO'::public.estado_general,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.area OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 25188)
-- Name: area_id_area_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.area_id_area_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.area_id_area_seq OWNER TO postgres;

--
-- TOC entry 5080 (class 0 OID 0)
-- Dependencies: 221
-- Name: area_id_area_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.area_id_area_seq OWNED BY public.area.id_area;


--
-- TOC entry 236 (class 1259 OID 25330)
-- Name: asistencia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.asistencia (
    id_asistencia integer NOT NULL,
    id_actividad integer NOT NULL,
    id_participante integer NOT NULL,
    presente boolean DEFAULT false,
    observacion character varying(255),
    registrado_por integer,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.asistencia OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 25329)
-- Name: asistencia_id_asistencia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.asistencia_id_asistencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.asistencia_id_asistencia_seq OWNER TO postgres;

--
-- TOC entry 5081 (class 0 OID 0)
-- Dependencies: 235
-- Name: asistencia_id_asistencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.asistencia_id_asistencia_seq OWNED BY public.asistencia.id_asistencia;


--
-- TOC entry 220 (class 1259 OID 25176)
-- Name: auditoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auditoria (
    id_auditoria integer NOT NULL,
    id_usuario integer,
    accion character varying(100) NOT NULL,
    entidad character varying(50) NOT NULL,
    id_entidad integer,
    ip character varying(45),
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.auditoria OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 25175)
-- Name: auditoria_id_auditoria_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auditoria_id_auditoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auditoria_id_auditoria_seq OWNER TO postgres;

--
-- TOC entry 5082 (class 0 OID 0)
-- Dependencies: 219
-- Name: auditoria_id_auditoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auditoria_id_auditoria_seq OWNED BY public.auditoria.id_auditoria;


--
-- TOC entry 226 (class 1259 OID 25218)
-- Name: casa_vida; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.casa_vida (
    id_casa_vida integer NOT NULL,
    nombre character varying(100) NOT NULL,
    id_area integer,
    id_lider integer,
    id_supervisor integer,
    direccion text,
    estado public.estado_general DEFAULT 'ACTIVO'::public.estado_general,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    actualizado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.casa_vida OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 25217)
-- Name: casa_vida_id_casa_vida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.casa_vida_id_casa_vida_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.casa_vida_id_casa_vida_seq OWNER TO postgres;

--
-- TOC entry 5083 (class 0 OID 0)
-- Dependencies: 225
-- Name: casa_vida_id_casa_vida_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.casa_vida_id_casa_vida_seq OWNED BY public.casa_vida.id_casa_vida;


--
-- TOC entry 228 (class 1259 OID 25245)
-- Name: casa_vida_miembro; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.casa_vida_miembro (
    id_casa_vida_miembro integer NOT NULL,
    id_casa_vida integer NOT NULL,
    id_participante integer NOT NULL,
    fecha_ingreso date DEFAULT CURRENT_DATE,
    estado public.estado_general DEFAULT 'ACTIVO'::public.estado_general
);


ALTER TABLE public.casa_vida_miembro OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 25244)
-- Name: casa_vida_miembro_id_casa_vida_miembro_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.casa_vida_miembro_id_casa_vida_miembro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.casa_vida_miembro_id_casa_vida_miembro_seq OWNER TO postgres;

--
-- TOC entry 5084 (class 0 OID 0)
-- Dependencies: 227
-- Name: casa_vida_miembro_id_casa_vida_miembro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.casa_vida_miembro_id_casa_vida_miembro_seq OWNED BY public.casa_vida_miembro.id_casa_vida_miembro;


--
-- TOC entry 232 (class 1259 OID 25283)
-- Name: inscripcion_formacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inscripcion_formacion (
    id_inscripcion integer NOT NULL,
    id_participante integer NOT NULL,
    id_proceso_formacion integer NOT NULL,
    fecha_inscripcion date DEFAULT CURRENT_DATE,
    estado public.estado_general DEFAULT 'ACTIVO'::public.estado_general
);


ALTER TABLE public.inscripcion_formacion OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 25282)
-- Name: inscripcion_formacion_id_inscripcion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.inscripcion_formacion_id_inscripcion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inscripcion_formacion_id_inscripcion_seq OWNER TO postgres;

--
-- TOC entry 5085 (class 0 OID 0)
-- Dependencies: 231
-- Name: inscripcion_formacion_id_inscripcion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.inscripcion_formacion_id_inscripcion_seq OWNED BY public.inscripcion_formacion.id_inscripcion;


--
-- TOC entry 240 (class 1259 OID 25377)
-- Name: ofrenda; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ofrenda (
    id_ofrenda integer NOT NULL,
    fecha date DEFAULT CURRENT_DATE NOT NULL,
    concepto character varying(150) NOT NULL,
    valor numeric(12,2) NOT NULL,
    id_casa_vida integer,
    id_usuario_registro integer,
    observacion text,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.ofrenda OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 25376)
-- Name: ofrenda_id_ofrenda_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ofrenda_id_ofrenda_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ofrenda_id_ofrenda_seq OWNER TO postgres;

--
-- TOC entry 5086 (class 0 OID 0)
-- Dependencies: 239
-- Name: ofrenda_id_ofrenda_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ofrenda_id_ofrenda_seq OWNED BY public.ofrenda.id_ofrenda;


--
-- TOC entry 224 (class 1259 OID 25203)
-- Name: participante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participante (
    id_participante integer NOT NULL,
    nombres_apellidos character varying(150) NOT NULL,
    documento_identidad character varying(50) NOT NULL,
    fecha_nacimiento date,
    telefono character varying(20),
    direccion text,
    autorizacion_datos boolean DEFAULT false,
    estado public.estado_general DEFAULT 'ACTIVO'::public.estado_general,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    actualizado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.participante OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 25202)
-- Name: participante_id_participante_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participante_id_participante_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.participante_id_participante_seq OWNER TO postgres;

--
-- TOC entry 5087 (class 0 OID 0)
-- Dependencies: 223
-- Name: participante_id_participante_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participante_id_participante_seq OWNED BY public.participante.id_participante;


--
-- TOC entry 230 (class 1259 OID 25266)
-- Name: proceso_formacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proceso_formacion (
    id_proceso_formacion integer NOT NULL,
    nombre character varying(150) NOT NULL,
    tipo_proceso public.tipo_proceso NOT NULL,
    id_coordinador integer NOT NULL,
    descripcion text,
    estado public.estado_general DEFAULT 'ACTIVO'::public.estado_general,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    actualizado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.proceso_formacion OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 25265)
-- Name: proceso_formacion_id_proceso_formacion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proceso_formacion_id_proceso_formacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.proceso_formacion_id_proceso_formacion_seq OWNER TO postgres;

--
-- TOC entry 5088 (class 0 OID 0)
-- Dependencies: 229
-- Name: proceso_formacion_id_proceso_formacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proceso_formacion_id_proceso_formacion_seq OWNED BY public.proceso_formacion.id_proceso_formacion;


--
-- TOC entry 242 (class 1259 OID 25398)
-- Name: reporte; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reporte (
    id_reporte integer NOT NULL,
    tipo_modulo public.tipo_modulo NOT NULL,
    id_usuario_envia integer NOT NULL,
    id_usuario_destino integer,
    periodo character varying(20) NOT NULL,
    observaciones text,
    ruta_archivo character varying(255),
    enviado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.reporte OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 25397)
-- Name: reporte_id_reporte_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reporte_id_reporte_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reporte_id_reporte_seq OWNER TO postgres;

--
-- TOC entry 5089 (class 0 OID 0)
-- Dependencies: 241
-- Name: reporte_id_reporte_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reporte_id_reporte_seq OWNED BY public.reporte.id_reporte;


--
-- TOC entry 216 (class 1259 OID 25140)
-- Name: rol; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rol (
    id_rol integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion text,
    acceso_casas_vida boolean DEFAULT false,
    acceso_escuelas_formacion boolean DEFAULT false,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.rol OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 25139)
-- Name: rol_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rol_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rol_id_rol_seq OWNER TO postgres;

--
-- TOC entry 5090 (class 0 OID 0)
-- Dependencies: 215
-- Name: rol_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rol_id_rol_seq OWNED BY public.rol.id_rol;


--
-- TOC entry 238 (class 1259 OID 25356)
-- Name: seguimiento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seguimiento (
    id_seguimiento integer NOT NULL,
    id_participante integer NOT NULL,
    id_usuario integer NOT NULL,
    fecha date DEFAULT CURRENT_DATE NOT NULL,
    observacion text NOT NULL,
    tipo_modulo public.tipo_modulo NOT NULL,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.seguimiento OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 25355)
-- Name: seguimiento_id_seguimiento_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seguimiento_id_seguimiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seguimiento_id_seguimiento_seq OWNER TO postgres;

--
-- TOC entry 5091 (class 0 OID 0)
-- Dependencies: 237
-- Name: seguimiento_id_seguimiento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.seguimiento_id_seguimiento_seq OWNED BY public.seguimiento.id_seguimiento;


--
-- TOC entry 218 (class 1259 OID 25154)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    nombre_completo character varying(150) NOT NULL,
    correo character varying(150) NOT NULL,
    username character varying(50),
    password_hash character varying(255) NOT NULL,
    id_rol integer NOT NULL,
    activo boolean DEFAULT true,
    intentos_fallidos integer DEFAULT 0,
    bloqueado_hasta timestamp without time zone,
    ultimo_acceso timestamp without time zone,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    actualizado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    creado_por integer,
    modificado_por integer
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 5092 (class 0 OID 0)
-- Dependencies: 218
-- Name: COLUMN usuario.creado_por; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuario.creado_por IS 'Usuario que creó el registro';


--
-- TOC entry 5093 (class 0 OID 0)
-- Dependencies: 218
-- Name: COLUMN usuario.modificado_por; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.usuario.modificado_por IS 'Usuario que modificó el registro por última vez';


--
-- TOC entry 217 (class 1259 OID 25153)
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_usuario_seq OWNER TO postgres;

--
-- TOC entry 5094 (class 0 OID 0)
-- Dependencies: 217
-- Name: usuario_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_usuario_seq OWNED BY public.usuario.id_usuario;


--
-- TOC entry 4842 (class 2604 OID 25307)
-- Name: actividad id_actividad; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actividad ALTER COLUMN id_actividad SET DEFAULT nextval('public.actividad_id_actividad_seq'::regclass);


--
-- TOC entry 4820 (class 2604 OID 25192)
-- Name: area id_area; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.area ALTER COLUMN id_area SET DEFAULT nextval('public.area_id_area_seq'::regclass);


--
-- TOC entry 4844 (class 2604 OID 25333)
-- Name: asistencia id_asistencia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia ALTER COLUMN id_asistencia SET DEFAULT nextval('public.asistencia_id_asistencia_seq'::regclass);


--
-- TOC entry 4818 (class 2604 OID 25179)
-- Name: auditoria id_auditoria; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria ALTER COLUMN id_auditoria SET DEFAULT nextval('public.auditoria_id_auditoria_seq'::regclass);


--
-- TOC entry 4828 (class 2604 OID 25221)
-- Name: casa_vida id_casa_vida; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida ALTER COLUMN id_casa_vida SET DEFAULT nextval('public.casa_vida_id_casa_vida_seq'::regclass);


--
-- TOC entry 4832 (class 2604 OID 25248)
-- Name: casa_vida_miembro id_casa_vida_miembro; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida_miembro ALTER COLUMN id_casa_vida_miembro SET DEFAULT nextval('public.casa_vida_miembro_id_casa_vida_miembro_seq'::regclass);


--
-- TOC entry 4839 (class 2604 OID 25286)
-- Name: inscripcion_formacion id_inscripcion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripcion_formacion ALTER COLUMN id_inscripcion SET DEFAULT nextval('public.inscripcion_formacion_id_inscripcion_seq'::regclass);


--
-- TOC entry 4850 (class 2604 OID 25380)
-- Name: ofrenda id_ofrenda; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofrenda ALTER COLUMN id_ofrenda SET DEFAULT nextval('public.ofrenda_id_ofrenda_seq'::regclass);


--
-- TOC entry 4823 (class 2604 OID 25206)
-- Name: participante id_participante; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participante ALTER COLUMN id_participante SET DEFAULT nextval('public.participante_id_participante_seq'::regclass);


--
-- TOC entry 4835 (class 2604 OID 25269)
-- Name: proceso_formacion id_proceso_formacion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proceso_formacion ALTER COLUMN id_proceso_formacion SET DEFAULT nextval('public.proceso_formacion_id_proceso_formacion_seq'::regclass);


--
-- TOC entry 4853 (class 2604 OID 25401)
-- Name: reporte id_reporte; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte ALTER COLUMN id_reporte SET DEFAULT nextval('public.reporte_id_reporte_seq'::regclass);


--
-- TOC entry 4809 (class 2604 OID 25143)
-- Name: rol id_rol; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol ALTER COLUMN id_rol SET DEFAULT nextval('public.rol_id_rol_seq'::regclass);


--
-- TOC entry 4847 (class 2604 OID 25359)
-- Name: seguimiento id_seguimiento; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seguimiento ALTER COLUMN id_seguimiento SET DEFAULT nextval('public.seguimiento_id_seguimiento_seq'::regclass);


--
-- TOC entry 4813 (class 2604 OID 25157)
-- Name: usuario id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuario_id_usuario_seq'::regclass);


--
-- TOC entry 4892 (class 2606 OID 25313)
-- Name: actividad actividad_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actividad
    ADD CONSTRAINT actividad_pkey PRIMARY KEY (id_actividad);


--
-- TOC entry 4872 (class 2606 OID 25196)
-- Name: area area_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.area
    ADD CONSTRAINT area_pkey PRIMARY KEY (id_area);


--
-- TOC entry 4895 (class 2606 OID 25339)
-- Name: asistencia asistencia_id_actividad_id_participante_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia
    ADD CONSTRAINT asistencia_id_actividad_id_participante_key UNIQUE (id_actividad, id_participante);


--
-- TOC entry 4897 (class 2606 OID 25337)
-- Name: asistencia asistencia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia
    ADD CONSTRAINT asistencia_pkey PRIMARY KEY (id_asistencia);


--
-- TOC entry 4870 (class 2606 OID 25182)
-- Name: auditoria auditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria
    ADD CONSTRAINT auditoria_pkey PRIMARY KEY (id_auditoria);


--
-- TOC entry 4882 (class 2606 OID 25254)
-- Name: casa_vida_miembro casa_vida_miembro_id_casa_vida_id_participante_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida_miembro
    ADD CONSTRAINT casa_vida_miembro_id_casa_vida_id_participante_key UNIQUE (id_casa_vida, id_participante);


--
-- TOC entry 4884 (class 2606 OID 25252)
-- Name: casa_vida_miembro casa_vida_miembro_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida_miembro
    ADD CONSTRAINT casa_vida_miembro_pkey PRIMARY KEY (id_casa_vida_miembro);


--
-- TOC entry 4878 (class 2606 OID 25228)
-- Name: casa_vida casa_vida_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida
    ADD CONSTRAINT casa_vida_pkey PRIMARY KEY (id_casa_vida);


--
-- TOC entry 4888 (class 2606 OID 25292)
-- Name: inscripcion_formacion inscripcion_formacion_id_participante_id_proceso_formacion_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripcion_formacion
    ADD CONSTRAINT inscripcion_formacion_id_participante_id_proceso_formacion_key UNIQUE (id_participante, id_proceso_formacion);


--
-- TOC entry 4890 (class 2606 OID 25290)
-- Name: inscripcion_formacion inscripcion_formacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripcion_formacion
    ADD CONSTRAINT inscripcion_formacion_pkey PRIMARY KEY (id_inscripcion);


--
-- TOC entry 4903 (class 2606 OID 25386)
-- Name: ofrenda ofrenda_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofrenda
    ADD CONSTRAINT ofrenda_pkey PRIMARY KEY (id_ofrenda);


--
-- TOC entry 4874 (class 2606 OID 25216)
-- Name: participante participante_documento_identidad_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participante
    ADD CONSTRAINT participante_documento_identidad_key UNIQUE (documento_identidad);


--
-- TOC entry 4876 (class 2606 OID 25214)
-- Name: participante participante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participante
    ADD CONSTRAINT participante_pkey PRIMARY KEY (id_participante);


--
-- TOC entry 4886 (class 2606 OID 25276)
-- Name: proceso_formacion proceso_formacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proceso_formacion
    ADD CONSTRAINT proceso_formacion_pkey PRIMARY KEY (id_proceso_formacion);


--
-- TOC entry 4905 (class 2606 OID 25406)
-- Name: reporte reporte_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_pkey PRIMARY KEY (id_reporte);


--
-- TOC entry 4857 (class 2606 OID 25152)
-- Name: rol rol_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_nombre_key UNIQUE (nombre);


--
-- TOC entry 4859 (class 2606 OID 25150)
-- Name: rol rol_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id_rol);


--
-- TOC entry 4901 (class 2606 OID 25365)
-- Name: seguimiento seguimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seguimiento
    ADD CONSTRAINT seguimiento_pkey PRIMARY KEY (id_seguimiento);


--
-- TOC entry 4862 (class 2606 OID 25167)
-- Name: usuario usuario_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_correo_key UNIQUE (correo);


--
-- TOC entry 4865 (class 2606 OID 25165)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 4867 (class 2606 OID 25169)
-- Name: usuario usuario_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_username_key UNIQUE (username);


--
-- TOC entry 4893 (class 1259 OID 25420)
-- Name: idx_actividad_fecha; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_actividad_fecha ON public.actividad USING btree (fecha);


--
-- TOC entry 4898 (class 1259 OID 25421)
-- Name: idx_asistencia_actividad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_asistencia_actividad ON public.asistencia USING btree (id_actividad);


--
-- TOC entry 4879 (class 1259 OID 25418)
-- Name: idx_casa_vida_area; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_casa_vida_area ON public.casa_vida USING btree (id_area);


--
-- TOC entry 4880 (class 1259 OID 25419)
-- Name: idx_casa_vida_lider; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_casa_vida_lider ON public.casa_vida USING btree (id_lider);


--
-- TOC entry 4899 (class 1259 OID 25422)
-- Name: idx_seguimiento_participante; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_seguimiento_participante ON public.seguimiento USING btree (id_participante);


--
-- TOC entry 4860 (class 1259 OID 25417)
-- Name: idx_usuario_rol; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_usuario_rol ON public.usuario USING btree (id_rol);


--
-- TOC entry 4863 (class 1259 OID 25424)
-- Name: usuario_correo_lower_uk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX usuario_correo_lower_uk ON public.usuario USING btree (lower((correo)::text));


--
-- TOC entry 4868 (class 1259 OID 25425)
-- Name: usuario_username_lower_uk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX usuario_username_lower_uk ON public.usuario USING btree (lower((username)::text)) WHERE (username IS NOT NULL);


--
-- TOC entry 4919 (class 2606 OID 25314)
-- Name: actividad actividad_id_casa_vida_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actividad
    ADD CONSTRAINT actividad_id_casa_vida_fkey FOREIGN KEY (id_casa_vida) REFERENCES public.casa_vida(id_casa_vida);


--
-- TOC entry 4920 (class 2606 OID 25319)
-- Name: actividad actividad_id_proceso_formacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actividad
    ADD CONSTRAINT actividad_id_proceso_formacion_fkey FOREIGN KEY (id_proceso_formacion) REFERENCES public.proceso_formacion(id_proceso_formacion);


--
-- TOC entry 4921 (class 2606 OID 25324)
-- Name: actividad actividad_id_responsable_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actividad
    ADD CONSTRAINT actividad_id_responsable_fkey FOREIGN KEY (id_responsable) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4910 (class 2606 OID 25197)
-- Name: area area_id_supervisor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.area
    ADD CONSTRAINT area_id_supervisor_fkey FOREIGN KEY (id_supervisor) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4922 (class 2606 OID 25340)
-- Name: asistencia asistencia_id_actividad_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia
    ADD CONSTRAINT asistencia_id_actividad_fkey FOREIGN KEY (id_actividad) REFERENCES public.actividad(id_actividad);


--
-- TOC entry 4923 (class 2606 OID 25345)
-- Name: asistencia asistencia_id_participante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia
    ADD CONSTRAINT asistencia_id_participante_fkey FOREIGN KEY (id_participante) REFERENCES public.participante(id_participante);


--
-- TOC entry 4924 (class 2606 OID 25350)
-- Name: asistencia asistencia_registrado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencia
    ADD CONSTRAINT asistencia_registrado_por_fkey FOREIGN KEY (registrado_por) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4909 (class 2606 OID 25183)
-- Name: auditoria auditoria_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria
    ADD CONSTRAINT auditoria_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4911 (class 2606 OID 25229)
-- Name: casa_vida casa_vida_id_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida
    ADD CONSTRAINT casa_vida_id_area_fkey FOREIGN KEY (id_area) REFERENCES public.area(id_area);


--
-- TOC entry 4912 (class 2606 OID 25234)
-- Name: casa_vida casa_vida_id_lider_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida
    ADD CONSTRAINT casa_vida_id_lider_fkey FOREIGN KEY (id_lider) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4913 (class 2606 OID 25239)
-- Name: casa_vida casa_vida_id_supervisor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida
    ADD CONSTRAINT casa_vida_id_supervisor_fkey FOREIGN KEY (id_supervisor) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4914 (class 2606 OID 25255)
-- Name: casa_vida_miembro casa_vida_miembro_id_casa_vida_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida_miembro
    ADD CONSTRAINT casa_vida_miembro_id_casa_vida_fkey FOREIGN KEY (id_casa_vida) REFERENCES public.casa_vida(id_casa_vida);


--
-- TOC entry 4915 (class 2606 OID 25260)
-- Name: casa_vida_miembro casa_vida_miembro_id_participante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.casa_vida_miembro
    ADD CONSTRAINT casa_vida_miembro_id_participante_fkey FOREIGN KEY (id_participante) REFERENCES public.participante(id_participante);


--
-- TOC entry 4917 (class 2606 OID 25293)
-- Name: inscripcion_formacion inscripcion_formacion_id_participante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripcion_formacion
    ADD CONSTRAINT inscripcion_formacion_id_participante_fkey FOREIGN KEY (id_participante) REFERENCES public.participante(id_participante);


--
-- TOC entry 4918 (class 2606 OID 25298)
-- Name: inscripcion_formacion inscripcion_formacion_id_proceso_formacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inscripcion_formacion
    ADD CONSTRAINT inscripcion_formacion_id_proceso_formacion_fkey FOREIGN KEY (id_proceso_formacion) REFERENCES public.proceso_formacion(id_proceso_formacion);


--
-- TOC entry 4927 (class 2606 OID 25387)
-- Name: ofrenda ofrenda_id_casa_vida_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofrenda
    ADD CONSTRAINT ofrenda_id_casa_vida_fkey FOREIGN KEY (id_casa_vida) REFERENCES public.casa_vida(id_casa_vida);


--
-- TOC entry 4928 (class 2606 OID 25392)
-- Name: ofrenda ofrenda_id_usuario_registro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofrenda
    ADD CONSTRAINT ofrenda_id_usuario_registro_fkey FOREIGN KEY (id_usuario_registro) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4916 (class 2606 OID 25277)
-- Name: proceso_formacion proceso_formacion_id_coordinador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proceso_formacion
    ADD CONSTRAINT proceso_formacion_id_coordinador_fkey FOREIGN KEY (id_coordinador) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4929 (class 2606 OID 25412)
-- Name: reporte reporte_id_usuario_destino_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_id_usuario_destino_fkey FOREIGN KEY (id_usuario_destino) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4930 (class 2606 OID 25407)
-- Name: reporte reporte_id_usuario_envia_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_id_usuario_envia_fkey FOREIGN KEY (id_usuario_envia) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4925 (class 2606 OID 25366)
-- Name: seguimiento seguimiento_id_participante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seguimiento
    ADD CONSTRAINT seguimiento_id_participante_fkey FOREIGN KEY (id_participante) REFERENCES public.participante(id_participante);


--
-- TOC entry 4926 (class 2606 OID 25371)
-- Name: seguimiento seguimiento_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seguimiento
    ADD CONSTRAINT seguimiento_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4906 (class 2606 OID 25426)
-- Name: usuario usuario_creado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_creado_por_fkey FOREIGN KEY (creado_por) REFERENCES public.usuario(id_usuario);


--
-- TOC entry 4907 (class 2606 OID 25170)
-- Name: usuario usuario_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.rol(id_rol);


--
-- TOC entry 4908 (class 2606 OID 25431)
-- Name: usuario usuario_modificado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_modificado_por_fkey FOREIGN KEY (modificado_por) REFERENCES public.usuario(id_usuario);


-- Completed on 2026-10-27 15:50:26

--
-- PostgreSQL database dump complete
--

