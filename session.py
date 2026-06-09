# =========================================================
#  SESSION — almacena el usuario autenticado durante
#  toda la ejecución de la aplicación.
# =========================================================

_usuario_actual = None   # dict: datos del usuario autenticado y su rol principal


def iniciar_sesion(datos: dict):
    """Guarda los datos del usuario que acaba de loguearse."""
    global _usuario_actual
    _usuario_actual = datos


def cerrar_sesion():
    """Limpia la sesión actual."""
    global _usuario_actual
    _usuario_actual = None


def get_usuario():
    """Retorna el dict del usuario en sesión, o None si no hay sesión."""
    return _usuario_actual


def get_id_usuario() -> int | None:
    if _usuario_actual:
        return _usuario_actual.get("id_usuario")
    return None


def get_nombre_completo() -> str:
    if _usuario_actual:
        return f"{_usuario_actual.get('nombres', '')} {_usuario_actual.get('apellidos', '')}".strip()
    return "Sin sesión"


def get_rol() -> str:
    if _usuario_actual:
        return _usuario_actual.get("rol", "Sin rol")
    return "Sin rol"


def get_resumen_usuario() -> str:
    if not _usuario_actual:
        return "Sin sesión"

    nombre = get_nombre_completo()
    rol = get_rol()
    username = _usuario_actual.get("username", "")
    if username:
        return f"{nombre} | {rol} | @{username}"
    return f"{nombre} | {rol}"


def get_usuario_actual() -> dict | None:
    """Alias de get_usuario() para compatibilidad con controladores."""
    return _usuario_actual
