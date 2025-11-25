-- Esquema NUEVO simplificado para devvproyectofinal_v2
-- Modelo: contribuyente -> 1..N domicilios, domicilio -> 1 rubro, actuacion -> domicilio

CREATE DATABASE IF NOT EXISTS devvproyectofinal_v2
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE devvproyectofinal_v2;

SET FOREIGN_KEY_CHECKS = 0;

-- =========================
--  CATÁLOGOS BÁSICOS
-- =========================

CREATE TABLE IF NOT EXISTS documento_tipo (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(10) NOT NULL UNIQUE,
  nombre VARCHAR(150) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS genero (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(10) NOT NULL UNIQUE,
  nombre VARCHAR(150) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rubro (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(128) NOT NULL UNIQUE,
  activo TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_rubro_nombre ON rubro (nombre);
CREATE INDEX idx_rubro_activo ON rubro (activo);


-- =========================
--  CONTRIBUYENTE
-- =========================

CREATE TABLE IF NOT EXISTS contribuyente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  apellido VARCHAR(128) NOT NULL,
  nombre VARCHAR(128) NOT NULL,

  doc_tipo_id INT NULL,
  genero_id INT NULL,
  doc_nro VARCHAR(20) NULL,

  telefono VARCHAR(30) NULL,
  email VARCHAR(128) NULL,

  activo TINYINT(1) NOT NULL DEFAULT 1,

  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT uq_contrib_doc UNIQUE (doc_tipo_id, doc_nro),

  CONSTRAINT fk_contrib_doc_tipo
    FOREIGN KEY (doc_tipo_id)
    REFERENCES documento_tipo(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,

  CONSTRAINT fk_contrib_genero
    FOREIGN KEY (genero_id)
    REFERENCES genero(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE INDEX idx_contrib_apellido_nombre ON contribuyente (apellido, nombre);
CREATE INDEX idx_contrib_doc_std ON contribuyente (doc_tipo_id, doc_nro);


-- =========================
--  DISTRITO / BARRIO
-- =========================

CREATE TABLE IF NOT EXISTS distrito (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero INT NOT NULL,
  nombre VARCHAR(150) NOT NULL,
  UNIQUE KEY uq_distrito_numero (numero)
);

CREATE TABLE IF NOT EXISTS barrio (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  distrito_id INT NULL,
  CONSTRAINT fk_barrio_distrito
    FOREIGN KEY (distrito_id)
    REFERENCES distrito(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);


-- =========================
--  DOMICILIO (apunta a contribuyente y rubro)
-- =========================

CREATE TABLE IF NOT EXISTS domicilio (
  id INT AUTO_INCREMENT PRIMARY KEY,
  calle VARCHAR(128) NOT NULL,
  numero VARCHAR(20) NULL,
  local VARCHAR(128) NULL,
  cp VARCHAR(10) NULL,

  barrio_id INT NULL,
  distrito_id INT NULL,

  contribuyente_id INT NULL,
  rubro_id INT NULL,

  lat DECIMAL(9,6) NULL,
  lon DECIMAL(9,6) NULL,

  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_domicilio_barrio
    FOREIGN KEY (barrio_id)
    REFERENCES barrio(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,

  CONSTRAINT fk_domicilio_distrito
    FOREIGN KEY (distrito_id)
    REFERENCES distrito(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,

  CONSTRAINT fk_domicilio_contribuyente
    FOREIGN KEY (contribuyente_id)
    REFERENCES contribuyente(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,

  CONSTRAINT fk_domicilio_rubro
    FOREIGN KEY (rubro_id)
    REFERENCES rubro(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);


-- =========================
--  TURNOS / INSPECTORES
-- =========================

CREATE TABLE IF NOT EXISTS turno (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(128) NOT NULL,
  descripcion TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inspector (
  id INT AUTO_INCREMENT PRIMARY KEY,
  legajo INT NOT NULL UNIQUE,
  apellido VARCHAR(128) NOT NULL,
  nombre VARCHAR(128) NOT NULL,
  turno_id INT NULL,
  email VARCHAR(150) NULL,
  telefono VARCHAR(50) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  INDEX idx_inspector_turno (turno_id),

  CONSTRAINT fk_inspector_turno
    FOREIGN KEY (turno_id)
    REFERENCES turno(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);


-- =========================
--  ORDEN DE TRABAJO
-- =========================

CREATE TABLE IF NOT EXISTS orden_trabajo (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero VARCHAR(6) NOT NULL UNIQUE,
  descripcion TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- =========================
--  ACTUACION (apunta directo a domicilio)
-- =========================

CREATE TABLE IF NOT EXISTS actuacion (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATE NOT NULL,
  tipo VARCHAR(20) NOT NULL,

  orden_trabajo_id INT NULL,
  domicilio_id INT NULL,

  contraproducencia TEXT NULL,
  observaciones TEXT NULL,

  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  UNIQUE KEY uq_act_ot (orden_trabajo_id),
  INDEX idx_act_fecha (fecha),
  INDEX idx_act_tipo (tipo),
  INDEX idx_act_dom (domicilio_id),

  CONSTRAINT fk_act_ot
    FOREIGN KEY (orden_trabajo_id)
    REFERENCES orden_trabajo(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,

  CONSTRAINT fk_act_domicilio
    FOREIGN KEY (domicilio_id)
    REFERENCES domicilio(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);


-- =========================
--  RELACIÓN ACTUACION - INSPECTOR
-- =========================

CREATE TABLE IF NOT EXISTS actuacion_inspector (
  actuacion_id INT NOT NULL,
  inspector_id INT NOT NULL,
  rol VARCHAR(20) NULL,
  asignado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (actuacion_id, inspector_id),

  CONSTRAINT fk_actinsp_actuacion
    FOREIGN KEY (actuacion_id)
    REFERENCES actuacion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  CONSTRAINT fk_actinsp_inspector
    FOREIGN KEY (inspector_id)
    REFERENCES inspector(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);


-- =========================
--  ACTA DE INSPECCION
-- =========================

CREATE TABLE IF NOT EXISTS acta_inspeccion (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero_acta VARCHAR(6) NOT NULL,
  anio SMALLINT NOT NULL,
  actuacion_id INT NULL,
  observaciones TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  UNIQUE KEY uq_ai_numero_anio (numero_acta, anio),

  CONSTRAINT fk_actins_actuacion
    FOREIGN KEY (actuacion_id)
    REFERENCES actuacion(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);


-- =========================
--  NOTIFICACIONES Y MOTIVOS
-- =========================

CREATE TABLE IF NOT EXISTS notificacion (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero_acta VARCHAR(6) NOT NULL,
  anio SMALLINT NOT NULL,
  observaciones TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  UNIQUE KEY uq_notif_numero_anio (numero_acta, anio)
);

CREATE TABLE IF NOT EXISTS motivo_notificacion (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(200) NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notificacion_motivo (
  notificacion_id INT NOT NULL,
  motivo_id INT NOT NULL,
  orden INT NULL,

  PRIMARY KEY (notificacion_id, motivo_id),

  CONSTRAINT fk_nm_notificacion
    FOREIGN KEY (notificacion_id)
    REFERENCES notificacion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  CONSTRAINT fk_nm_motivo
    FOREIGN KEY (motivo_id)
    REFERENCES motivo_notificacion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- =========================
--  ACTA DE COMPROBACION
-- =========================

CREATE TABLE IF NOT EXISTS acta_comprobacion (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero_acta VARCHAR(6) NOT NULL,
  anio SMALLINT NOT NULL,
  articulo_id INT NULL,
  actuada_dos_veces TINYINT(1) NOT NULL DEFAULT 0,
  observaciones TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  UNIQUE KEY uq_acp_numero_anio (numero_acta, anio)
);


-- =========================
--  ACTA DE CLAUSURA + MOTIVO
-- =========================

CREATE TABLE IF NOT EXISTS motivo_clausura (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(200) NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS acta_clausura (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero_acta VARCHAR(6) NOT NULL,
  anio SMALLINT NOT NULL,
  actuacion_id INT NULL,
  motivo_id INT NULL,
  observaciones TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  UNIQUE KEY uq_acl_numero_anio (numero_acta, anio),

  CONSTRAINT fk_acl_actuacion
    FOREIGN KEY (actuacion_id)
    REFERENCES actuacion(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,

  CONSTRAINT fk_acl_motivo
    FOREIGN KEY (motivo_id)
    REFERENCES motivo_clausura(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);


-- =========================
--  ACTA DE DECOMISO (cantidad + unidad)
-- =========================

CREATE TABLE IF NOT EXISTS acta_decomiso (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero_acta VARCHAR(6) NOT NULL,
  anio SMALLINT NOT NULL,

  cantidad DECIMAL(10,2) NULL,
  unidad VARCHAR(10) NULL,

  actuacion_id INT NULL,

  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  UNIQUE KEY uq_ad_numero_anio (numero_acta, anio),

  CONSTRAINT fk_ad_actuacion
    FOREIGN KEY (actuacion_id)
    REFERENCES actuacion(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);


-- =========================
--  RELACIONES ACTUACION ↔ NOTIF / COMPROB
-- =========================

CREATE TABLE IF NOT EXISTS actuacion_notificacion (
  actuacion_id INT NOT NULL,
  notificacion_id INT NOT NULL,
  contexto VARCHAR(50) NULL,

  PRIMARY KEY (actuacion_id, notificacion_id),

  CONSTRAINT fk_an_actuacion
    FOREIGN KEY (actuacion_id)
    REFERENCES actuacion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  CONSTRAINT fk_an_notificacion
    FOREIGN KEY (notificacion_id)
    REFERENCES notificacion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS actuacion_comprobacion (
  actuacion_id INT NOT NULL,
  acta_comprobacion_id INT NOT NULL,
  contexto VARCHAR(50) NULL,

  PRIMARY KEY (actuacion_id, acta_comprobacion_id),

  CONSTRAINT fk_ac_actuacion
    FOREIGN KEY (actuacion_id)
    REFERENCES actuacion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  CONSTRAINT fk_ac_comprobacion
    FOREIGN KEY (acta_comprobacion_id)
    REFERENCES acta_comprobacion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- =========================
--  EXPEDIENTE (1:1 con ACTUACION)
-- =========================

CREATE TABLE IF NOT EXISTS expediente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero_expediente VARCHAR(30) NOT NULL,
  anio SMALLINT NOT NULL,
  actuacion_id INT NOT NULL,
  observaciones TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  UNIQUE KEY uq_expediente_actuacion (actuacion_id),

  CONSTRAINT fk_exp_actuacion
    FOREIGN KEY (actuacion_id)
    REFERENCES actuacion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- =========================
--  OFICIO (apunta a ACTA_COMPROBACION)
-- =========================

CREATE TABLE IF NOT EXISTS oficio (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero_oficio VARCHAR(20) NOT NULL,
  anio SMALLINT NOT NULL,
  causa INT NULL,
  acta_comprobacion_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  UNIQUE KEY uq_oficio_numero_anio (numero_oficio, anio),

  CONSTRAINT fk_oficio_comprobacion
    FOREIGN KEY (acta_comprobacion_id)
    REFERENCES acta_comprobacion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


SET FOREIGN_KEY_CHECKS = 1;
