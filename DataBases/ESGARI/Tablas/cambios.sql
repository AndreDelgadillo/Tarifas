CREATE TABLE CAMBIOS (
    idCambio INT AUTO_INCREMENT PRIMARY KEY,
    lugarCambio VARCHAR(15) NOT NULL,
    campoCambio VARCHAR(30) NOT NULL,
    antes VARCHAR(200) NOT NULL,
    despues VARCHAR(200) NOT NULL,
    usuarioCambio VARCHAR(8) NOT NULL,
    fechaCambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuarioCambio FOREIGN KEY (usuarioCambio) REFERENCES USERS(idNomina)
        ON UPDATE CASCADE
);

ALTER TABLE CAMBIOS AUTO_INCREMENT = 1000;