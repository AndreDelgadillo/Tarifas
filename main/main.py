from conexion import Conector
from Usuario import Usuario
import interfaceUX as UX

host = "localhost"      # Cambia por tu host
user = "root"           # Cambia por tu usuario
password = "1075353"    # Cambia por tu contraseña
database = "ESGARI"     # Cambia por el nombre de tu base de datos
conn = Conector(host=host, user=user, password=password, database=database)
user = Usuario().iniciar_sesion('AD0773', '1075353', conn)
Inter = UX.API(conn, user)

idUbicacion = Inter.mkUbicacion('Casa de Karina', 'Mexico', 'Tlaquepaque', 'Jalisco', '45625')