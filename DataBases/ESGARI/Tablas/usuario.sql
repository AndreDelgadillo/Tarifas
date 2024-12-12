-- Script para crear la tabla "usuarios"

CREATE TABLE USERS (
    idNomina VARCHAR(8) PRIMARY KEY,    -- Identificador único
    Nombre VARCHAR(100) NOT NULL,                 -- Nombre completo del usuario
    Nombre2 VARCHAR(100) DEFAULT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,          -- Correo electrónico único
    passw VARCHAR(255) NOT NULL,             -- Contraseña (almacenada en hash)
    rol VARCHAR(30) DEFAULT NULL, -- Rol del usuario
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    estadoUsuario BOOLEAN DEFAULT FALSE, -- Estado del usuario
    CONSTRAINT fk_rol FOREIGN KEY (rol) REFERENCES ROLES(idRol)
        ON UPDATE CASCADE
);

