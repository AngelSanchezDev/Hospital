"""
Módulo de conexión a la base de datos.

Este archivo ahora maneja la ausencia de `pyodbc` durante la importación
para evitar que la aplicación falle en tiempo de importación cuando la
dependencia no esté instalada o cuando no exista un servidor SQL local.
Si no hay conexión disponible, la variable `conexion` será `None`.
"""

conexion = None

try:
    import pyodbc
except Exception as e:
    pyodbc = None
    print(f"pyodbc no disponible: {e}")

# Datos del servidor (ajusta según tu entorno)
server = r'(localdb)\MSSQLLocalDB'
database = 'Hospital'
driver = '{ODBC Driver 18 for SQL Server}'

if pyodbc is not None:
    try:
        conn_str = (
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'Trusted_Connection=yes;'
            f'Encrypt=no;'
            f'TrustServerCertificate=yes;'
        )

        conexion = pyodbc.connect(conn_str)
        print("Conexión ODBC establecida correctamente.")

        # Prueba de consulta (opcional)
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT name FROM sys.databases")
            print("Bases de datos disponibles:")
            for db in cursor:
                print(f"- {db[0]}")
        except Exception:
            # No bloquear la aplicación si la consulta de prueba falla
            pass

    except Exception as e:
        print(f"Error de conexión: {e}")
        conexion = None
else:
    print("Aviso: pyodbc no está instalado. La aplicación funcionará sin acceso a BD.")

