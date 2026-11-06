# ==========================================
# CONEXION A LA BASE DE DATOS DEL SGA
# ==========================================

import sqlite3
from pathlib import Path


# UBICACION DE LA BASE DE DATOS

RUTA_BD = Path(__file__).resolve().parent / "sga.db"


# FUNCION PARA CONECTAR CON SQLITE

def obtener_conexion():

    conexion = sqlite3.connect(RUTA_BD)

    return conexion


# FUNCION PARA CREAR LA TABLA DE USUARIOS

def crear_tabla_usuarios():

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT UNIQUE NOT NULL,

            rol TEXT NOT NULL,

            sal BLOB NOT NULL,

            clave BLOB NOT NULL,

            activo INTEGER NOT NULL DEFAULT 1

        )
    """)

    conexion.commit()

    conexion.close()


# MENSAJE DE CONFIRMACION

if __name__ == "__main__":

    crear_tabla_usuarios()

    print("Base de datos creada correctamente.")
    print("Tabla de usuarios disponible.")
    
