import pandas as pd
from typing import TypeAlias, Literal
from conexion import Conector
from datetime import datetime
from Usuario import Usuario


LiteralIdSolicitud: TypeAlias = int

class API:
    def __init__(self, conn: Conector, user: Usuario) -> None:
        self.conn = conn
        self.user = user

    def mk(self, table: str, data: dict[str, str]) -> bool:
        try:
            self.conn.loadData(data)
            return True
        except: return False

    def mkSolicitud(self, tipoSolicitud: str) -> Literal[False] | LiteralIdSolicitud:
        table = 'SOLICITUD'
        data = {'table': table, 'fields': ('tipoSolicitud', 'solicitante'), 'values': (tipoSolicitud, self.user.idNomina)}
        if self.mk(None, data): return self.conn.getTable(table, 'idSolicitud', f'solicitante = "{self.user.idNomina}"', 'fechaCreacion DESC')['idSolicitud'].iloc[0]
        return False

    def mkSolucion(self, idSolicitud: str, estadoSolicitud: bool) -> bool:
        data = {'resolutiva': self.user.idNomina, 'fechaRespuesta': str(datetime.now()), 'estadoSolicitud': int(estadoSolicitud)}
        try:
            self.conn.update('SOLICITUD', data, f'idSolicitud = {idSolicitud}')
            return True
        except: return False

    def checkIfAproved(self): ...

    def mkCascade(self, idSolicitud, table: str, **kargs): ...

    def data(self, **kwargs) -> dict[str, tuple[str | tuple[str]]]: ...

    def mkUbicacion(self, nombre: str, pais: str, ciudad: str, estado: str, codigoPostal: str) -> bool:
        table = 'UBICACIONES'
        idSolicitud = int(self.mkSolicitud(table))
        if not idSolicitud: return False
        data = {'table': table, 'fields': ('idSolicitud', 'nombre', 'pais', 'ciudad', 'estado', 'codigoPostal'), 'values': (idSolicitud, nombre, pais, ciudad, estado, codigoPostal)}
        if self.mk(table, data): return self.conn.getTable(table, 'idUbicacion', f'idSolicitud = {idSolicitud}')['idUbicacion'].iloc[0]
        return False

    def mkTarifa(self) -> bool:
        table = 'TARIFA'
        idSolicitud = self.mkSolicitud(table)
        if idSolicitud:
            data = {'table': table}
            self.mk(table, )