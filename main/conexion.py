import mysql.connector
import mysql
from mysql.connector import Error
from mysql.connector.abstracts import MySQLCursorAbstract
import pandas as pd
from pathlib import Path
from typing import Callable

class CMySQLConnection(mysql.connector.connection_cext.CMySQLConnection): ...
class DataFrame(pd.DataFrame): ...
class Series(pd.Series): ...

class Conector:
    def __init__(self, **kwargs):
        try:
            # Crear la conexión a la base de datos
            self.database = kwargs['database']
            connection = mysql.connector.connect(**kwargs)
            
            if connection.is_connected():
                print("Conexión exitosa a la base de datos")
                self.connection: CMySQLConnection = connection

        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    @property
    def tables(self) -> list[str]:
        self.cursor.execute("SHOW TABLES;")
        tables = list()
        for table in self.cursor.fetchall():
            tables.append(table[0])
        return tables
    
    @property
    def cursor(self) -> MySQLCursorAbstract:
        """Obtiene o crea el cursor único de la conexión."""
        if not hasattr(self, '_cursor'):
            self._cursor = self.connection.cursor()
        return self._cursor
    
    def resetCursor(self) -> None:
        """Cierra el cursor actual y crea uno nuevo."""
        if hasattr(self, 'cursor'):
            self.cursor.close()  # Cierra el cursor existente
        self._cursor = self.connection.cursor()  # Crea un nuevo cursor

    def clearCursorResults(self):
        """Limpia cualquier resultado pendiente en el cursor."""
        try:
            while self.cursor.nextset():
                pass
        except mysql.connector.errors.InterfaceError:
            # No hay más resultados pendientes
            pass

    def changeDatabase(self, database):
        try:
            # Ejecuta el comando para cambiar a la base de datos deseada
            self.cursor.execute(f"USE {database}")
            print(f"Base de datos cambiada a: {database}")
            self.resetCursor()
        except Error as e:
            print(f"Error al cambiar de base de datos: {e}")

    def dropTable(self, table: str) -> None:
        self.cursor.execute(f"DROP TABLE {table}")
        self.resetCursor()

    def loadTable(self, sourceArchive: Path):
        try:
            # Leer el contenido del archivo SQL
            with open(sourceArchive, 'r') as file:
                sql_commands = file.read()

            # Dividir los comandos si hay múltiples (separados por ';')
            for command in sql_commands.split(';'):
                if command.strip():  # Ejecutar solo si el comando no está vacío
                    self.cursor.execute(command)
            print(f"Archivo SQL '{sourceArchive}' ejecutado correctamente.")

        except Error as e:
            print(f"Error al ejecutar el archivo SQL: {e}")
        self.resetCursor()

    def commit(self, script: str) -> int:
        self.clearCursorResults()
        self.cursor.execute(script)
        self.connection.commit()
        rowcount = self.cursor.rowcount
        self.resetCursor()
        return rowcount

    def loadData(self, data: dict[str, list[str | int | tuple[str | int]]]) -> int:
        if isinstance(data['values'], list):
            data['values'] = ','.join([str(value) for value in data['values']])
        script = f"INSERT INTO {data['table']} ({','.join(data['fields'])}) VALUES {data['values']}"
        return self.commit(script)
    
    def whereCondition(self, script: str, whereCondition: str) -> str:
        if whereCondition: return f'{script} WHERE {whereCondition}'
        return f'{script}'

    def delRows(self, table: str, whereCondition: str = None) -> None:
        script = self.whereCondition(f'DELETE FROM {table}', whereCondition)
        return self.commit(script)

    def getTable(self, table: str, fields: str | list[str], whereCondition: str = False, orderBy: str = False) -> DataFrame:
        if isinstance(fields, list): fields = ','.join(fields)
        script = self.whereCondition(f'SELECT {fields} FROM {table}', whereCondition)
        if orderBy: script = f'{script} ORDER BY {orderBy}'
        
        self.cursor.execute(script)
        # Convertir los resultados en un DataFrame
        columnas = [col[0] for col in self.cursor.description]  # Nombres de columnas
        datos = self.cursor.fetchall()  # Datos de la tabla
        self.resetCursor()
        return pd.DataFrame(datos, columns=columnas)

    def getFields(self, table) -> list[str]:
        query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table}' AND TABLE_SCHEMA = '{self.database}';
        """
        self.cursor.execute(query)
        fields = [row[0] for row in self.cursor.fetchall()]
        self.resetCursor()
        return fields
        
    def update(self, table: str, values: dict[str, str], whereCondition: str):
        values = ", ".join([f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in values.items()])
        script = self.whereCondition(f'UPDATE {table} SET {values}', whereCondition)
        return self.commit(script)

# Uso del código
if __name__ == "__main__":
    host = "localhost"      # Cambia por tu host
    user = "root"           # Cambia por tu usuario
    password = "1075353"    # Cambia por tu contraseña
    database = "ESGARI"     # Cambia por el nombre de tu base de datos
    conn = Conector(host=host, user=user, password=password, database=database)
    if conn:
        conn.cursor.execute("SELECT passw FROM USER WHERE idNomina = ?", ('idNomina',))
        result = conn.cursor.fetchone()
        # Cierra la conexión
        conn.close_connection()
