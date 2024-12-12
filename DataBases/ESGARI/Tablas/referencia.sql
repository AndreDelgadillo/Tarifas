CREATE TABLE REFERENCIA (
    idReferencia VARCHAR(15) PRIMARY KEY,
    idSolicitud INT NOT NULL,
    nombreReferencia VARCHAR(20) NOT NULL,
    descripcionReferencia VARCHAR(100) NOT NULL,
    refiereA VARCHAR(15) NOT NULL,
    tipoReferencia VARCHAR(15) NOT NULL,
    CONSTRAINT fk_idSolicitud_referencia FOREIGN KEY (idSolicitud) REFERENCES SOLICITUD(idSolicitud)
);