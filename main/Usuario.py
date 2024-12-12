from datetime import datetime
import pandas as pd
from typing import Self, Callable
import bcrypt
from conexion import Conector

class Usuario:
    def __init__(self,
                idNomina: str = None,
                Nombre: str = None,
                Nombre2: str = None,
                correo: str = None,
                passw: str = None,
                rol: str = None,
                fechaCreacion: datetime = None,
                estadoUsuario: str = None,
                conn: Conector = None) -> None:
        self.idNomina = idNomina
        self.Nombre = Nombre
        self.Nombre2 = Nombre2
        self.correo = correo
        self.passw = passw
        self.rol = rol
        self.fechaCreacion = fechaCreacion
        self.estadoUsuari0 = estadoUsuario
        self.conn = conn

#--------------------------------------------------------------------------------------------------------
#----------------------------Decoradores-----------------------------------------------------------------


    def mkChange(self, other: Self, function: Callable, whereCondition: str) -> bool:
        def decorador(func):
            def warpper(*args, **kwargs):
                func()
                self.conn.update('USERS', kwargs, whereCondition)

#--------------------------------------------------------------------------------------------------------
#----------------------------Generadores-----------------------------------------------------------------

    def hash_password(self, password: str) -> str:
        """Genera un hash seguro para una contraseña."""
        salt = bcrypt.gensalt()  # Genera un salt aleatorio
        hashed = bcrypt.hashpw(password.encode(), salt)  # Crea el hash
        return hashed.decode()  # Devuelve el hash como una cadena de texto

#--------------------------------------------------------------------------------------------------------
#----------------------------Validadores-----------------------------------------------------------------

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifica si una contraseña coincide con su hash almacenado."""
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def iniciar_sesion(self, idNomina: str, password :str, conn: Conector):
        """Valida las credenciales del usuario."""

        # Busca al usuario por nombre
        result = conn.getTable('USERS', '*', f'idNomina = "{idNomina}"')

        if not result.empty:
            # Obtiene el hash de la base de datos
            stored_hash = result['passw'].iloc[0]

            # Verifica la contraseña ingresada contra el hash almacenado
            if self.verify_password(password, stored_hash):
                print(f"Inicio de sesión exitoso.\nBienvenido {idNomina}")
                usuario = result.to_dict(orient='records')[0]
                return Usuario(**usuario)
            else:
                print("Contraseña incorrecta.")
        else:
            print("Usuario no encontrado.")
        
        return False
    
#--------------------------------------------------------------------------------------------------------
#----------------------------Actualizaciones-------------------------------------------------------------

    def cambiarPassw(self, other: Self, newPass: str, oldPassw: str) -> bool:
        oldPassw = self.hash_password(oldPassw)
        if self.verify_password(newPass, self.passw if other.rol == 'ADMIN' else oldPassw):
            newPass = self.hash_password(newPass)
            self.passw = newPass