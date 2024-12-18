CREATE TABLE CLIENTE (
    idCliente INT AUTO_INCREMENT PRIMARY KEY,
    idSolicitud INT NOT NULL,
    nombreCliente VARCHAR(50) NOT NULL,
    nombreCorto VARCHAR(30) NOT NULL,
    nomenclatura VARCHAR(5) NOT NULL,
    CONSTRAINT fk_idSolicitud_cliente FOREIGN KEY (idSolicitud) REFERENCES SOLICITUD(idSolicitud)
);

ALTER TABLE CLIENTE AUTO_INCREMENT = 1000;