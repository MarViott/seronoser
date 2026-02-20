-- Agregar campo de rol a la tabla usuarios_auth
ALTER TABLE usuarios_auth 
ADD COLUMN rol ENUM('usuario', 'editor', 'administrador') DEFAULT 'usuario' AFTER activo;

-- Crear índice para optimizar búsquedas por rol
ALTER TABLE usuarios_auth 
ADD INDEX idx_rol (rol);

-- OPCIONAL: Actualizar usuarios existentes para darles roles
-- Descomenta las siguientes líneas si quieres asignar roles a usuarios existentes

-- Ejemplo: Hacer administrador al primer usuario registrado
-- UPDATE usuarios_auth SET rol = 'administrador' WHERE id = 1;

-- Ejemplo: Hacer administrador a un usuario específico por email
-- UPDATE usuarios_auth SET rol = 'administrador' WHERE email = 'tu-email@example.com';

-- Ejemplo: Hacer editor a varios usuarios
-- UPDATE usuarios_auth SET rol = 'editor' WHERE id IN (2, 3, 4);
