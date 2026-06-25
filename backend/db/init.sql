-- ============================================================================
-- DESENREDA - Esquema de Base de Datos PostgreSQL
-- Plataforma para ayudar a personas neurodivergentes a comprender
-- modismos chilenos.
-- ============================================================================
-- Version: 1.0.0
-- Fecha: 2026-06-03
-- ============================================================================

-- 0. Extensiones ------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS pg_trgm;          -- Trigramas para busqueda ILIKE
CREATE EXTENSION IF NOT EXISTS pgcrypto;         -- Funciones criptograficas
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";        -- Generacion de UUIDs (si se requiere)

-- 1. ENUM Types -------------------------------------------------------------

DO $$ BEGIN
    CREATE TYPE categoria_palabra AS ENUM (
        'modismo',
        'muletilla',
        'jerga',
        'insulto_ligero',
        'abreviacion'
    );
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE sugerencia_tipo AS ENUM (
        'palabra',
        'frase',
        'escenario'
    );
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE sugerencia_estado AS ENUM (
        'pendiente',
        'aprobado',
        'rechazado'
    );
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE tono_frase AS ENUM (
        'ironico',
        'sarcastico',
        'directo',
        'humoristico',
        'motivacional',
        'neutro'
    );
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- 2. Tablas -----------------------------------------------------------------

-- 2.1. Usuario
CREATE TABLE IF NOT EXISTS usuario (
    id              SERIAL          PRIMARY KEY,
    nombre          VARCHAR(100)    NOT NULL,
    email           VARCHAR(255)    NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255)    NOT NULL,
    preferencias    JSONB           DEFAULT NULL,
    activo          BOOLEAN         DEFAULT TRUE,
    fecha_registro  TIMESTAMPTZ     DEFAULT NOW(),
    ultima_conexion TIMESTAMPTZ     DEFAULT NULL,

    -- Restriccion: si existe preferencias, validar estructura basica
    CONSTRAINT preferencias_validas CHECK (
        preferencias IS NULL OR
        (
            (preferencias ? 'tono_explicacion' OR NOT preferencias ? 'tono_explicacion') AND
            (preferencias ? 'nivel_detalle' OR NOT preferencias ? 'nivel_detalle')
        )
    )
);

-- 2.2. Palabra
CREATE TABLE IF NOT EXISTS palabra (
    id                  SERIAL              PRIMARY KEY,
    palabra             VARCHAR(200)        NOT NULL,
    traduccion          VARCHAR(500)        NOT NULL,
    categoria           categoria_palabra   NOT NULL,
    nivel_formalidad    INTEGER             NOT NULL DEFAULT 2
                                            CHECK (nivel_formalidad BETWEEN 1 AND 5),
    nivel_ironia        INTEGER             NOT NULL DEFAULT 0
                                            CHECK (nivel_ironia BETWEEN 0 AND 10),
    nivel_sarcasmo      INTEGER             NOT NULL DEFAULT 0
                                            CHECK (nivel_sarcasmo BETWEEN 0 AND 10),
    pronunciacion_fonetica  VARCHAR(100)    DEFAULT NULL,
    ejemplo_uso         VARCHAR(500)        DEFAULT NULL,
    nota_cultural       VARCHAR(1000)       DEFAULT NULL,
    origen              VARCHAR(500)        DEFAULT NULL,
    variantes           JSONB               DEFAULT '[]'::jsonb,
    activo              BOOLEAN             DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ         DEFAULT NOW(),
    fecha_actualizacion TIMESTAMPTZ         DEFAULT NULL,

    -- Columna generada para busqueda de texto completo
    texto_busqueda      TSVECTOR            GENERATED ALWAYS AS (
        to_tsvector('spanish',
            COALESCE(palabra, '') || ' ' ||
            COALESCE(traduccion, '') || ' ' ||
            COALESCE(ejemplo_uso, '') || ' ' ||
            COALESCE(nota_cultural, '')
        )
    ) STORED
);

-- 2.3. Escenario
CREATE TABLE IF NOT EXISTS escenario (
    id                  SERIAL          PRIMARY KEY,
    nombre              VARCHAR(150)    NOT NULL,
    descripcion         VARCHAR(500)    NOT NULL,
    icono               VARCHAR(50)     DEFAULT NULL,
    activo              BOOLEAN         DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     DEFAULT NOW(),
    fecha_actualizacion TIMESTAMPTZ     DEFAULT NULL
);

-- 2.4. Frase
CREATE TABLE IF NOT EXISTS frase (
    id                  SERIAL          PRIMARY KEY,
    escenario_id        INTEGER         NOT NULL
                                        REFERENCES escenario(id)
                                        ON DELETE CASCADE
                                        ON UPDATE CASCADE,
    frase_original      VARCHAR(500)    NOT NULL,
    traduccion          VARCHAR(500)    NOT NULL,
    explicacion         VARCHAR(1000)   DEFAULT NULL,
    tono                VARCHAR(50)     DEFAULT NULL
                                        CHECK (tono IS NULL OR tono IN (
                                            'ironico', 'sarcastico', 'directo',
                                            'humoristico', 'motivacional', 'neutro'
                                        )),
    intencion_real      VARCHAR(500)    DEFAULT NULL,
    nivel_formalidad    INTEGER         NOT NULL DEFAULT 3
                                        CHECK (nivel_formalidad BETWEEN 1 AND 5),
    nivel_ironia        INTEGER         NOT NULL DEFAULT 0
                                        CHECK (nivel_ironia BETWEEN 0 AND 10),
    nivel_sarcasmo      INTEGER         NOT NULL DEFAULT 0
                                        CHECK (nivel_sarcasmo BETWEEN 0 AND 10),
    ejemplo_uso         VARCHAR(500)    DEFAULT NULL,
    activo              BOOLEAN         DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     DEFAULT NOW(),
    fecha_actualizacion TIMESTAMPTZ     DEFAULT NULL
);

-- 2.5. Sugerencia
CREATE TABLE IF NOT EXISTS sugerencia (
    id                  SERIAL              PRIMARY KEY,
    usuario_id          INTEGER             DEFAULT NULL
                                            REFERENCES usuario(id)
                                            ON DELETE SET NULL
                                            ON UPDATE CASCADE,
    tipo                sugerencia_tipo     NOT NULL,
    contenido           JSONB               NOT NULL,
    estado              sugerencia_estado   DEFAULT 'pendiente',
    comentario_moderador VARCHAR(500)       DEFAULT NULL,
    usuario_email       VARCHAR(255)        DEFAULT NULL,
    fecha_creacion      TIMESTAMPTZ         DEFAULT NOW(),
    fecha_actualizacion TIMESTAMPTZ         DEFAULT NULL
);

-- 2.6. Conversacion (relacion 1:1 con Frase)
CREATE TABLE IF NOT EXISTS conversacion (
    id              SERIAL          PRIMARY KEY,
    frase_id        INTEGER         NOT NULL
                                    REFERENCES frase(id)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE
                                    UNIQUE,
    participantes   JSONB           NOT NULL DEFAULT '[]'::jsonb
);

-- 2.7. Mensaje (relacion N:1 con Conversacion)
CREATE TABLE IF NOT EXISTS mensaje (
    id              SERIAL          PRIMARY KEY,
    conversacion_id INTEGER         NOT NULL
                                    REFERENCES conversacion(id)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE,
    emisor          VARCHAR(200)    NOT NULL,
    texto           TEXT            NOT NULL,
    es_modismo      BOOLEAN         NOT NULL DEFAULT FALSE,
    orden           INTEGER         NOT NULL DEFAULT 0
);

-- 2.8. Tabla intermedia: Frase <-> Palabra (relacion N:M opcional)
CREATE TABLE IF NOT EXISTS frase_palabra (
    id                  SERIAL      PRIMARY KEY,
    frase_id            INTEGER     NOT NULL
                                    REFERENCES frase(id)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE,
    palabra_id          INTEGER     NOT NULL
                                    REFERENCES palabra(id)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE,
    relevancia          INTEGER     DEFAULT 1
                                    CHECK (relevancia BETWEEN 1 AND 5),
    UNIQUE (frase_id, palabra_id)
);

-- 3. Indices -----------------------------------------------------------------

-- 3.1. Indices para busqueda de texto completo (FTS) en palabra
CREATE INDEX IF NOT EXISTS idx_palabra_texto_busqueda
    ON palabra
    USING GIN (texto_busqueda);

CREATE INDEX IF NOT EXISTS idx_palabra_palabra_trgm
    ON palabra
    USING GIN (palabra gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_palabra_traduccion_trgm
    ON palabra
    USING GIN (traduccion gin_trgm_ops);

-- 3.2. Indices JSONB
CREATE INDEX IF NOT EXISTS idx_usuario_preferencias
    ON usuario
    USING GIN (preferencias);

CREATE INDEX IF NOT EXISTS idx_palabra_variantes
    ON palabra
    USING GIN (variantes);

CREATE INDEX IF NOT EXISTS idx_sugerencia_contenido
    ON sugerencia
    USING GIN (contenido);

-- 3.3. Indices para busqueda por categoria y estado
CREATE INDEX IF NOT EXISTS idx_palabra_categoria
    ON palabra (categoria)
    WHERE activo = TRUE;

CREATE INDEX IF NOT EXISTS idx_palabra_activo
    ON palabra (activo);

CREATE INDEX IF NOT EXISTS idx_frase_escenario
    ON frase (escenario_id)
    WHERE activo = TRUE;

CREATE INDEX IF NOT EXISTS idx_sugerencia_estado
    ON sugerencia (estado);

CREATE INDEX IF NOT EXISTS idx_sugerencia_usuario
    ON sugerencia (usuario_id);

CREATE INDEX IF NOT EXISTS idx_sugerencia_tipo
    ON sugerencia (tipo);

-- 3.4. Indices para busqueda ILIKE en campos de texto
CREATE INDEX IF NOT EXISTS idx_frase_frase_original_trgm
    ON frase
    USING GIN (frase_original gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_frase_traduccion_trgm
    ON frase
    USING GIN (traduccion gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_escenario_nombre_trgm
    ON escenario
    USING GIN (nombre gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_escenario_descripcion_trgm
    ON escenario
    USING GIN (descripcion gin_trgm_ops);

-- 3.5. Indices unicos y compuestos
CREATE UNIQUE INDEX IF NOT EXISTS idx_usuario_email_lower
    ON usuario (LOWER(email));

CREATE INDEX IF NOT EXISTS idx_frase_tono
    ON frase (tono)
    WHERE tono IS NOT NULL;

-- 3.6. Indices para conversacion y mensaje
CREATE INDEX IF NOT EXISTS idx_conversacion_frase
    ON conversacion (frase_id);

CREATE INDEX IF NOT EXISTS idx_mensaje_conversacion
    ON mensaje (conversacion_id);

-- 4. Funciones y Triggers ----------------------------------------------------

-- 4.1. Trigger para actualizar fecha_actualizacion automaticamente
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a tablas con fecha_actualizacion
CREATE TRIGGER trg_palabra_actualizacion
    BEFORE UPDATE ON palabra
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_escenario_actualizacion
    BEFORE UPDATE ON escenario
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_frase_actualizacion
    BEFORE UPDATE ON frase
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_sugerencia_actualizacion
    BEFORE UPDATE ON sugerencia
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- 4.2. Trigger para actualizar ultima_conexion en usuario
CREATE OR REPLACE FUNCTION actualizar_ultima_conexion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.ultima_conexion = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_usuario_conexion
    BEFORE UPDATE OF contrasena_hash, preferencias, activo ON usuario
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION actualizar_ultima_conexion();

-- 5. Comentarios de tabla y columnas ----------------------------------------

COMMENT ON TABLE usuario IS 'Usuarios registrados de la plataforma Desenreda';
COMMENT ON COLUMN usuario.preferencias IS 'JSON con preferencias del usuario: {tono_explicacion, nivel_detalle}';

COMMENT ON TABLE palabra IS 'Catalogo de modismos, muletillas, jerga e insultos ligeros chilenos';
COMMENT ON COLUMN palabra.categoria IS 'Tipo de palabra: modismo, muletilla, jerga, insulto_ligero, abreviacion';
COMMENT ON COLUMN palabra.nivel_formalidad IS 'Escala 1-5: 1=informal, 5=formal';
COMMENT ON COLUMN palabra.variantes IS 'JSON array de variantes regionales o de uso: ["variante1", "variante2"]';
COMMENT ON COLUMN palabra.texto_busqueda IS 'Columna generada TSVECTOR para busqueda de texto completo';

COMMENT ON TABLE escenario IS 'Escenarios contextuales donde se usan las frases';
COMMENT ON TABLE frase IS 'Frases con modismos asociadas a escenarios especificos';
COMMENT ON COLUMN frase.tono IS 'Tono de la frase: ironico, sarcastico, directo, humoristico, motivacional, neutro';

COMMENT ON TABLE sugerencia IS 'Sugerencias de usuarios para nuevas palabras, frases o escenarios';
COMMENT ON COLUMN sugerencia.contenido IS 'JSON con los datos de la sugerencia segun el tipo';

COMMENT ON TABLE frase_palabra IS 'Relacion N:M entre frases y palabras (uso futuro con ML)';

COMMENT ON TABLE conversacion IS 'Conversacion asociada 1:1 a una frase, simulando un chat ejemplificador';
COMMENT ON COLUMN conversacion.participantes IS 'JSON array de strings con los nombres de los participantes';

COMMENT ON TABLE mensaje IS 'Mensajes individuales dentro de una conversacion';
COMMENT ON COLUMN mensaje.es_modismo IS 'Indica si el mensaje contiene el modismo/frase original';
COMMENT ON COLUMN mensaje.orden IS 'Orden de aparicion del mensaje en la conversacion';
