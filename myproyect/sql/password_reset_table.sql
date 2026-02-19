-- Tabla para tokens de recuperación de contraseña
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    token VARCHAR(100) NOT NULL UNIQUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion DATETIME NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    INDEX idx_token (token),
    INDEX idx_usuario (usuario_id),
    INDEX idx_expiracion (fecha_expiracion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
