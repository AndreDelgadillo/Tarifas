CREATE TABLE TARIFA (
    idTarifa INT AUTO_INCREMENT PRIMARY KEY,
    idSolicitud INT NOT NULL,
    idCliente INT NOT NULL,
    tipoServicio VARCHAR(15) NOT NULL,
    tipoUnidad VARCHAR(15) NOT NULL,
    tipoMercancia VARCHAR(15) NOT NULL,
    tipoRuta VARCHAR(15) NOT NULL,
    modalidad VARCHAR(15) NOT NULL,
    volumenFrecuencia VARCHAR(15) NOT NULL,
    origen INT NOT NULL,
    destino INT NOT NULL,
    puntoCruce VARCHAR(30) NOT NULL,
    pesoKg INT NOT NULL,
    maniobraOrigen BOOLEAN DEFAULT FALSE,
    maniobraDestino BOOLEAN DEFAULT FALSE,
    almacenajePuerto BOOLEAN DEFAULT NULL, -- NULL para sin almacenaje, FALSE para aeropuerto, TRUE para puerto marítimo
    aduana BOOLEAN DEFAULT NULL,          -- NULL para no especificado, FALSE para sin aduana, TRUE para con aduana
    ingresoZR BOOLEAN DEFAULT NULL,       -- NULL para no especificado, FALSE para sin ZR, TRUE para con ZR (Zona Residencial)
    CONSTRAINT fk_cliente FOREIGN KEY (idCliente) REFERENCES CLIENTE(idCliente),
    CONSTRAINT fk_origen FOREIGN KEY (origen) REFERENCES UBICACIONES(idUbicacion),
    CONSTRAINT fk_destino FOREIGN KEY (destino) REFERENCES UBICACIONES(idUbicacion),
    CONSTRAINT fk_tipoServicio FOREIGN KEY (tipoServicio) REFERENCES REFERENCIA(idReferencia),
    CONSTRAINT fk_tipoUnidad FOREIGN KEY (tipoUnidad) REFERENCES REFERENCIA(idReferencia),
    CONSTRAINT fk_tipoMercancia FOREIGN KEY (tipoMercancia) REFERENCES REFERENCIA(idReferencia),
    CONSTRAINT fk_tipoRuta FOREIGN KEY (tipoRuta) REFERENCES REFERENCIA(idReferencia),
    CONSTRAINT fk_modalidad FOREIGN KEY (modalidad) REFERENCES REFERENCIA(idReferencia),
    CONSTRAINT fk_volumenFrecuencia FOREIGN KEY (volumenFrecuencia) REFERENCES REFERENCIA(idReferencia),
    CONSTRAINT fk_solicitud FOREIGN KEY (idSolicitud) REFERENCES SOLICITUD(idSolicitud)
);

-- Establecer el valor inicial del AUTO_INCREMENT
ALTER TABLE TARIFA AUTO_INCREMENT = 1000;
