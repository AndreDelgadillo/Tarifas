CREATE TABLE SOLICITUD (
    idSolicitud INT AUTO_INCREMENT PRIMARY KEY,
    solicitante VARCHAR(8) NOT NULL, -- Quien Solicita
    resolutiva VARCHAR(8) DEFAULT NULL, -- Quien responde
    fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de solicitud
    fechaRespuesta DATETIME DEFAULT NULL, -- Fecha y hora de solicitud
    estadoSolicitud BOOLEAN DEFAULT NULL,-- Null para no respondida, True para aceptada, False para rechazada
    tipoSolicitud VARCHAR(20) NOT NULL, -- Dice a que tabla está haciendo la solicitud
    CONSTRAINT fk_solicitante FOREIGN KEY (solicitante) REFERENCES USERS(idNomina)
        ON UPDATE CASCADE,
    CONSTRAINT fk_resolutiva FOREIGN KEY (resolutiva) REFERENCES USERS(idNomina)
        ON UPDATE CASCADE
);

ALTER TABLE SOLICITUD AUTO_INCREMENT = 1000;