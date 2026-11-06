# ==========================================
# SISTEMA DE GESTION ACADEMICA (SGA)
# PROGRAMA PRINCIPAL
# ==========================================

from modulos.usuarios import (
    registrar_usuario,
    iniciar_sesion,
    tiene_permiso
)


def main():

    print("====================================")
    print("     SISTEMA DE GESTION ACADEMICA")
    print("====================================")

    # REGISTRAR ADMINISTRADOR

    resultado, mensaje = registrar_usuario(
        "admin_sga",
        "Admin123*",
        "administrador"
    )

    print("\nREGISTRO DE USUARIO:")
    print(mensaje)

    # INICIAR SESION

    usuario = iniciar_sesion(
        "admin_sga",
        "Admin123*"
    )

    print("\nINICIO DE SESION:")

    if usuario:

        print("Acceso autorizado")
        print("Usuario:", usuario["nombre"])
        print("Rol:", usuario["rol"])

        # VERIFICAR PERMISOS

        print("\nPERMISOS DEL USUARIO:")

        modulos = [
            "usuarios",
            "estudiantes",
            "matriculas",
            "calificaciones",
            "reportes"
        ]

        for modulo in modulos:

            if tiene_permiso(usuario, modulo):
                print(modulo, ": PERMITIDO")
            else:
                print(modulo, ": DENEGADO")

    else:
        print("Credenciales incorrectas")

    # PRUEBA DE SEGURIDAD

    print("\nPRUEBA DE CONTRASENA INCORRECTA:")

    usuario_invalido = iniciar_sesion(
        "admin_sga",
        "ClaveIncorrecta123"
    )

    if usuario_invalido is None:
        print("Acceso rechazado correctamente.")
    else:
        print("Error: el sistema permitio el acceso.")

    print("\n====================================")
    print("       SISTEMA FINALIZADO")
    print("====================================")


if __name__ == "__main__":
    main()
    