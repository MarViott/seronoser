-- Schema PostgreSQL para el sistema de teatro e-commerce
-- Compatible con Render PostgreSQL

-- Extensiones útiles (opcionales)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tipos personalizados
CREATE TYPE estado_orden AS ENUM ('pendiente', 'confirmada', 'cancelada');
CREATE TYPE rol_usuario AS ENUM ('usuario', 'editor', 'administrador');

-- Tabla de usuarios para autenticación
CREATE TABLE IF NOT EXISTS usuarios_auth (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    rol rol_usuario DEFAULT 'usuario'
);

-- Índices para usuarios_auth
CREATE INDEX IF NOT EXISTS idx_email ON usuarios_auth(email);
CREATE INDEX IF NOT EXISTS idx_rol ON usuarios_auth(rol);

-- Tabla de obras de teatro
CREATE TABLE IF NOT EXISTS obras (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(150),
    director VARCHAR(150),
    descripcion TEXT,
    imagen VARCHAR(255),
    precio DECIMAL(10, 2) DEFAULT 0.00,
    fecha_estreno DATE,
    teatro VARCHAR(150),
    duracion INT, -- en minutos
    es_estreno BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Función para actualizar fecha_actualizacion automáticamente
CREATE OR REPLACE FUNCTION update_fecha_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar fecha_actualizacion en obras
CREATE TRIGGER trigger_update_fecha_actualizacion
BEFORE UPDATE ON obras
FOR EACH ROW
EXECUTE FUNCTION update_fecha_actualizacion();

-- Tabla de compras/órdenes
CREATE TABLE IF NOT EXISTS ordenes (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    estado estado_orden DEFAULT 'pendiente',
    fecha_orden TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios_auth(id) ON DELETE CASCADE
);

-- Índices para ordenes
CREATE INDEX IF NOT EXISTS idx_usuario ON ordenes(usuario_id);
CREATE INDEX IF NOT EXISTS idx_fecha ON ordenes(fecha_orden);

-- Tabla de detalle de órdenes (entradas compradas)
CREATE TABLE IF NOT EXISTS orden_detalles (
    id SERIAL PRIMARY KEY,
    orden_id INT NOT NULL,
    obra_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    fecha_funcion DATE,
    FOREIGN KEY (orden_id) REFERENCES ordenes(id) ON DELETE CASCADE,
    FOREIGN KEY (obra_id) REFERENCES obras(id) ON DELETE CASCADE
);

-- Índices para orden_detalles
CREATE INDEX IF NOT EXISTS idx_orden ON orden_detalles(orden_id);
CREATE INDEX IF NOT EXISTS idx_obra ON orden_detalles(obra_id);

-- Tabla para tokens de recuperación de contraseña
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    token VARCHAR(100) NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios_auth(id) ON DELETE CASCADE
);

-- Índices para password_reset_tokens
CREATE INDEX IF NOT EXISTS idx_token ON password_reset_tokens(token);
CREATE INDEX IF NOT EXISTS idx_usuario_reset ON password_reset_tokens(usuario_id);
CREATE INDEX IF NOT EXISTS idx_expiracion ON password_reset_tokens(fecha_expiracion);

-- Tabla auxiliar de usuarios (para el CRUD simple)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    ocupacion VARCHAR(100)
);

-- Insertar obras de ejemplo (cartelera actual)
INSERT INTO obras (titulo, autor, director, descripcion, imagen, precio, teatro, es_estreno) VALUES
('Hamlet', 'William Shakespeare', 'Rubén Szuchmacher', 
 'Hamlet es una tragedia de William Shakespeare, escrita entre 1599 y 1601. La obra, situada en Dinamarca. La obra se considera una de las más poderosas e influyentes tragedias en la literatura inglesa. Protagonizada por Joaquín Furriel.',
 '3c25305cf51a4a8c81322786cecf1db9.jpg', 8500.00, 'Teatro San Martín', FALSE),

('Un tranvía llamado deseo', 'Tennessee Williams', 'Daniel Veronese',
 'Un tranvía llamado Deseo es una obra de teatro de Tennessee Williams escrita en 1947. Protagonizada por Diego Peretti y Erica Rivas.',
 '600expte2.jpg', 9000.00, 'Teatro Coliseo', FALSE),

('La muerte de un viajante', 'Arthur Miller', NULL,
 'La muerte de un viajante es una obra de teatro de Arthur Miller escrita en 1949. La obra se estrenó en Broadway el 10 de febrero de 1949.',
 '600expte4.jpg', 7500.00, 'Teatro Córdoba', FALSE),

('El acompañamiento', 'Carlos Gorostiza', NULL,
 'El acompañamiento es una obra de teatro de Carlos Gorostiza escrita en 1962. Laura y Lidia Bortnik, dos hermanas, se reencuentran en el escenario para interpretar a dos amigas de toda la vida.',
 'acompaña2.jpg', 7000.00, 'Teatro del Pueblo', FALSE),

('Mi hijo sólo camina más lento', 'Thierry Illouz', NULL,
 'Mi hijo sólo camina más lento es una obra de teatro de Thierry Illouz escrita en 2016. La obra cuenta la historia de un padre que se enfrenta a la realidad de su hijo con discapacidad.',
 'mihijosolocaminaunpocomaslento.jpg', 6500.00, 'Teatro del Pueblo', FALSE),

('El campeón', 'Fernando Zabala', 'Mariano Dossena',
 'El campeón cuenta la historia de un boxeador retirado. Dirigida por Mariano Dossena y protagonizada por Christian Thorsen, con el asesoramiento en boxeo de Sergio Maravilla Martínez.',
 'boxeo.jpg', 8000.00, 'Teatro Alternativa', TRUE)
ON CONFLICT DO NOTHING;

-- Comentarios sobre las tablas
COMMENT ON TABLE usuarios_auth IS 'Tabla de usuarios con autenticación para el sistema';
COMMENT ON TABLE obras IS 'Catálogo de obras de teatro disponibles';
COMMENT ON TABLE ordenes IS 'Registro de compras de entradas';
COMMENT ON TABLE orden_detalles IS 'Detalle de las entradas compradas en cada orden';
COMMENT ON TABLE password_reset_tokens IS 'Tokens para recuperación de contraseña';
COMMENT ON TABLE usuarios IS 'Tabla auxiliar para CRUD de usuarios simple';
