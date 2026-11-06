# ==========================================
# MODULO DE USUARIOS - SISTEMA SGA
# CONEXION CON BASE DE DATOS SQLITE
# ==========================================

import hashlib
import secrets
import hmac
import sqlite3

from base_datos.conexion import (
    obtener_conexion,
    crear_tabla_usuarios
)


# ROLES DEL SISTEMA

ROLES = [
    "administrador",
    "coordinador",
    "docente",
    "estudiante"
]


# PERMISOS SEGUN EL ROL

PERMISOS = {

    "administrador": [
        "usuarios",
        "estudiantes",
        "docentes",
        "academico",
        "matriculas",
        "calificaciones",
        "reportes",
        "auditoria"
    ],

    "coordinador": [
        "estudiantes",
        "academico",
        "grupos",
        "matriculas",
        "reportes"
    ],

    "docente": [
        "grupos",
        "calificaciones"
    ],

    "estudiante": [
        "consulta_academica"
    ]
}


# PROTEGER CONTRASENAS

def proteger_contrasena(contrasena, sal=None):

    if sal is None:
        sal = secrets.token_bytes(16)

    clave = hashlib.pbkdf2_hmac(
        "sha256",
        contrasena.encode("utf-8"),
        sal,
        600000
    )

    return sal, clave


# REGISTRAR USUARIOS

def registrar_usuario(nombre, contrasena, rol):

    crear_tabla_usuarios()

    if not nombre or not contrasena:
        return False, "Los campos son obligatorios."

    nombre = nombre.strip().lower()
    rol = rol.strip().lower()

    if rol not in ROLES:
        return False, "El rol no es valido."

    sal, clave = proteger_contrasena(contrasena)

    conexion = obtener_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO usuarios
            (nombre, rol, sal, clave, activo)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, rol, sal, clave, 1))

        conexion.commit()

        return True, "Usuario registrado correctamente."

    except sqlite3.IntegrityError:

        return False, "El usuario ya existe."

    finally:

        conexion.close()


# INICIAR SESION

def iniciar_sesion(nombre, contrasena):

    crear_tabla_usuarios()

    nombre = nombre.strip().lower()

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT nombre, rol, sal, clave, activo
        FROM usuarios
        WHERE nombre = ?
    """, (nombre,))

    usuario = cursor.fetchone()

    conexion.close()

    if usuario is None:
        return None

    nombre, rol, sal, clave_guardada, activo = usuario

    if not activo:
        return None

    sal, clave = proteger_contrasena(
        contrasena,
        sal
    )

    if hmac.compare_digest(clave, clave_guardada):

        return {
            "nombre": nombre,
            "rol": rol,
            "activo": activo
        }

    return None


# VERIFICAR PERMISOS

def tiene_permiso(usuario, modulo):

    if usuario is None:
        return False

    rol = usuario["rol"]

    return modulo in PERMISOS.get(rol, [])
    