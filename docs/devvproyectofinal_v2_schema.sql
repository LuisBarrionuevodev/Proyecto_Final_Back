-- =====================================================
--  Esquema devvproyectofinal_v2
--  Generado a partir del dump (solo estructura)
-- =====================================================

CREATE DATABASE IF NOT EXISTS devvproyectofinal_v2
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE devvproyectofinal_v2;

SET FOREIGN_KEY_CHECKS = 0;

-- =========================
--  CATÁLOGOS BÁSICOS
-- =========================

CREATE TABLE IF NOT EXISTS documento_tipo (
  id INT NOT NULL AUTO_INCREMENT,
  codigo VARCHAR(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  nombre VARCHAR(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  activo TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY codigo (codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS genero (
  id INT NOT NULL AUTO_INCREMENT,
  codigo VARCHAR(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  nombre VARCHAR(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  activo TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY codigo (codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS rubro (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  activo TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY nombre (nombre),
  KEY idx_rubro_nombre (nombre),
  KEY idx_rubro_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Motivos (catálogos específicos)

CREATE TABLE IF NOT EXISTS motivo_notificacion (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  descripcion TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS motivo_clausura (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  descripcion TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  CONTRIBUYENTE
-- =========================

CREATE TABLE IF NOT EXISTS contribuyente (
  id INT NOT NULL AUTO_INCREMENT,
  apellido VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  nombre VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  doc_tipo_id INT DEFAULT NULL,
  genero_id INT DEFAULT NULL,
  doc_nro VARCHAR(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  telefono VARCHAR(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  email VARCHAR(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  activo TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_contrib_doc (doc_tipo_id, doc_nro),
  KEY fk_contrib_genero (genero_id),
  KEY idx_contrib_apellido_nombre (apellido, nombre),
  KEY idx_contrib_doc_std (doc_tipo_id, doc_nro),
  CONSTRAINT fk_contrib_doc_tipo FOREIGN KEY (doc_tipo_id)
    REFERENCES documento_tipo (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_contrib_genero FOREIGN KEY (genero_id)
    REFERENCES genero (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  DISTRITO / BARRIO
-- =========================

CREATE TABLE IF NOT EXISTS distrito (
  id INT NOT NULL AUTO_INCREMENT,
  numero INT NOT NULL,
  nombre VARCHAR(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_distrito_numero (numero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS barrio (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  distrito_id INT DEFAULT NULL,
  PRIMARY KEY (id),
  KEY fk_barrio_distrito (distrito_id),
  CONSTRAINT fk_barrio_distrito FOREIGN KEY (distrito_id)
    REFERENCES distrito (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  DOMICILIO
-- =========================

CREATE TABLE IF NOT EXISTS domicilio (
  id INT NOT NULL AUTO_INCREMENT,
  calle VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  numero VARCHAR(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  local VARCHAR(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  cp VARCHAR(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  barrio_id INT DEFAULT NULL,
  distrito_id INT DEFAULT NULL,
  contribuyente_id INT DEFAULT NULL,
  rubro_id INT DEFAULT NULL,
  lat DECIMAL(9,6) DEFAULT NULL,
  lon DECIMAL(9,6) DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY fk_domicilio_barrio (barrio_id),
  KEY fk_domicilio_distrito (distrito_id),
  KEY fk_domicilio_contribuyente (contribuyente_id),
  KEY fk_domicilio_rubro (rubro_id),
  CONSTRAINT fk_domicilio_barrio FOREIGN KEY (barrio_id)
    REFERENCES barrio (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_domicilio_contribuyente FOREIGN KEY (contribuyente_id)
    REFERENCES contribuyente (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_domicilio_distrito FOREIGN KEY (distrito_id)
    REFERENCES distrito (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_domicilio_rubro FOREIGN KEY (rubro_id)
    REFERENCES rubro (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  TURNOS / INSPECTORES
-- =========================

CREATE TABLE IF NOT EXISTS turno (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  descripcion TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS inspector (
  id INT NOT NULL AUTO_INCREMENT,
  legajo INT NOT NULL,
  apellido VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  nombre VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  turno_id INT DEFAULT NULL,
  email VARCHAR(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  telefono VARCHAR(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY legajo (legajo),
  KEY idx_inspector_turno (turno_id),
  CONSTRAINT fk_inspector_turno FOREIGN KEY (turno_id)
    REFERENCES turno (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  ORDEN DE TRABAJO
-- =========================

CREATE TABLE IF NOT EXISTS orden_trabajo (
  id INT NOT NULL AUTO_INCREMENT,
  numero VARCHAR(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  descripcion TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY numero (numero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  ACTUACION
-- =========================

CREATE TABLE IF NOT EXISTS actuacion (
  id INT NOT NULL AUTO_INCREMENT,
  fecha DATE NOT NULL,
  tipo VARCHAR(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  orden_trabajo_id INT DEFAULT NULL,
  domicilio_id INT DEFAULT NULL,
  contraproducencia TEXT COLLATE utf8mb4_unicode_ci,
  observaciones TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_act_ot (orden_trabajo_id),
  KEY idx_act_fecha (fecha),
  KEY idx_act_tipo (tipo),
  KEY idx_act_dom (domicilio_id),
  CONSTRAINT fk_act_domicilio FOREIGN KEY (domicilio_id)
    REFERENCES domicilio (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_act_ot FOREIGN KEY (orden_trabajo_id)
    REFERENCES orden_trabajo (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  RELACIÓN ACTUACION - INSPECTOR
-- =========================

CREATE TABLE IF NOT EXISTS actuacion_inspector (
  actuacion_id INT NOT NULL,
  inspector_id INT NOT NULL,
  rol VARCHAR(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  asignado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (actuacion_id, inspector_id),
  KEY fk_actinsp_inspector (inspector_id),
  CONSTRAINT fk_actinsp_actuacion FOREIGN KEY (actuacion_id)
    REFERENCES actuacion (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_actinsp_inspector FOREIGN KEY (inspector_id)
    REFERENCES inspector (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  ACTA DE INSPECCION
-- =========================

CREATE TABLE IF NOT EXISTS acta_inspeccion (
  id INT NOT NULL AUTO_INCREMENT,
  numero_acta VARCHAR(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  anio SMALLINT NOT NULL,
  actuacion_id INT DEFAULT NULL,
  observaciones TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_ai_numero_anio (numero_acta, anio),
  KEY fk_actins_actuacion (actuacion_id),
  CONSTRAINT fk_actins_actuacion FOREIGN KEY (actuacion_id)
    REFERENCES actuacion (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  NOTIFICACIONES + MOTIVOS
-- =========================

CREATE TABLE IF NOT EXISTS notificacion (
  id INT NOT NULL AUTO_INCREMENT,
  numero_acta VARCHAR(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  anio SMALLINT NOT NULL,
  observaciones TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_notif_numero_anio (numero_acta, anio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS notificacion_motivo (
  notificacion_id INT NOT NULL,
  motivo_id INT NOT NULL,
  orden INT DEFAULT NULL,
  PRIMARY KEY (notificacion_id, motivo_id),
  KEY fk_nm_motivo (motivo_id),
  CONSTRAINT fk_nm_motivo FOREIGN KEY (motivo_id)
    REFERENCES motivo_notificacion (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_nm_notificacion FOREIGN KEY (notificacion_id)
    REFERENCES notificacion (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS actuacion_notificacion (
  actuacion_id INT NOT NULL,
  notificacion_id INT NOT NULL,
  contexto VARCHAR(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (actuacion_id, notificacion_id),
  KEY fk_an_notificacion (notificacion_id),
  CONSTRAINT fk_an_actuacion FOREIGN KEY (actuacion_id)
    REFERENCES actuacion (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_an_notificacion FOREIGN KEY (notificacion_id)
    REFERENCES notificacion (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  ACTA DE COMPROBACION
-- =========================

CREATE TABLE IF NOT EXISTS acta_comprobacion (
  id INT NOT NULL AUTO_INCREMENT,
  numero_acta VARCHAR(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  anio SMALLINT NOT NULL,
  articulo_id INT DEFAULT NULL,
  actuada_dos_veces TINYINT(1) NOT NULL DEFAULT 0,
  observaciones TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_acp_numero_anio (numero_acta, anio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS actuacion_comprobacion (
  actuacion_id INT NOT NULL,
  acta_comprobacion_id INT NOT NULL,
  contexto VARCHAR(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (actuacion_id, acta_comprobacion_id),
  KEY fk_ac_comprobacion (acta_comprobacion_id),
  CONSTRAINT fk_ac_actuacion FOREIGN KEY (actuacion_id)
    REFERENCES actuacion (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_ac_comprobacion FOREIGN KEY (acta_comprobacion_id)
    REFERENCES acta_comprobacion (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  ACTA DE CLAUSURA
-- =========================

CREATE TABLE IF NOT EXISTS acta_clausura (
  id INT NOT NULL AUTO_INCREMENT,
  numero_acta VARCHAR(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  anio SMALLINT NOT NULL,
  actuacion_id INT DEFAULT NULL,
  motivo_id INT DEFAULT NULL,
  observaciones TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_acl_numero_anio (numero_acta, anio),
  KEY fk_acl_actuacion (actuacion_id),
  KEY fk_acl_motivo (motivo_id),
  CONSTRAINT fk_acl_actuacion FOREIGN KEY (actuacion_id)
    REFERENCES actuacion (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_acl_motivo FOREIGN KEY (motivo_id)
    REFERENCES motivo_clausura (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  ACTA DE DECOMISO
-- =========================

CREATE TABLE IF NOT EXISTS acta_decomiso (
  id INT NOT NULL AUTO_INCREMENT,
  numero_acta VARCHAR(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  anio SMALLINT NOT NULL,
  cantidad DECIMAL(10,2) DEFAULT NULL,
  unidad VARCHAR(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  actuacion_id INT DEFAULT NULL,
  observaciones TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_ad_numero_anio (numero_acta, anio),
  KEY fk_ad_actuacion (actuacion_id),
  CONSTRAINT fk_ad_actuacion FOREIGN KEY (actuacion_id)
    REFERENCES actuacion (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  EXPEDIENTE (1:1 con ACTUACION)
-- =========================

CREATE TABLE IF NOT EXISTS expediente (
  id INT NOT NULL AUTO_INCREMENT,
  numero_expediente VARCHAR(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  anio SMALLINT NOT NULL,
  actuacion_id INT NOT NULL,
  observaciones TEXT COLLATE utf8mb4_unicode_ci,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_expediente_actuacion (actuacion_id),
  CONSTRAINT fk_exp_actuacion FOREIGN KEY (actuacion_id)
    REFERENCES actuacion (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  OFICIO (apunta a ACTA_COMPROBACION)
-- =========================

CREATE TABLE IF NOT EXISTS oficio (
  id INT NOT NULL AUTO_INCREMENT,
  numero_oficio VARCHAR(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  anio SMALLINT NOT NULL,
  causa INT DEFAULT NULL,
  observaciones TEXT COLLATE utf8mb4_unicode_ci,
  acta_comprobacion_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_oficio_numero_anio (numero_oficio, anio),
  KEY fk_oficio_comprobacion (acta_comprobacion_id),
  CONSTRAINT fk_oficio_comprobacion FOREIGN KEY (acta_comprobacion_id)
    REFERENCES acta_comprobacion (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================
--  RELEVAMIENTOS
-- =========================

CREATE TABLE IF NOT EXISTS relevamiento (
  id INT NOT NULL AUTO_INCREMENT,
  fecha DATE NOT NULL,
  inspector_id INT DEFAULT NULL,
  domicilio_id INT NOT NULL,
  rubro_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY fk_rel_inspector (inspector_id),
  KEY fk_rel_dom (domicilio_id),
  KEY fk_rel_rubro (rubro_id),
  CONSTRAINT fk_rel_dom FOREIGN KEY (domicilio_id)
    REFERENCES domicilio (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_rel_inspector FOREIGN KEY (inspector_id)
    REFERENCES inspector (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_rel_rubro FOREIGN KEY (rubro_id)
    REFERENCES rubro (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS relevamiento_simple (
  id INT NOT NULL AUTO_INCREMENT,
  fecha DATE NOT NULL,
  inspector VARCHAR(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  direccion VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  rubro VARCHAR(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


SET FOREIGN_KEY_CHECKS = 1;
