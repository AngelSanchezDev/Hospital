import os
import sys
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.conexion import conexion


class HospitalQueries:
    """Clase para manejar consultas específicas del sistema hospitalario"""
    
    def __init__(self):
        self._conexion = conexion
        self._validar_conexion()
    
    def _validar_conexion(self):
        """Validar que la conexión a la BD sea válida"""
        try:
            if not self._conexion:
                raise Exception("Conexión no disponible")
            cursor = self._conexion.cursor()
            cursor.execute("SELECT 1")
        except Exception as e:
            raise Exception(f"Error validando conexión: {str(e)}")
    
    def _cursor(self):
        """Obtener un cursor de la conexión"""
        try:
            return self._conexion.cursor()
        except Exception as e:
            raise Exception(f"Error obteniendo cursor: {str(e)}")
    
    def _fetch_one(self, sql, params=None):
        """Ejecutar consulta y obtener un registro"""
        cursor = None
        try:
            cursor = self._cursor()
            cursor.execute(sql, params or ())
            return cursor.fetchone()
        except Exception as e:
            raise Exception(f"Error en consulta (fetch_one): {str(e)}")
    
    def _fetch_all(self, sql, params=None):
        """Ejecutar consulta y obtener todos los registros"""
        cursor = None
        try:
            cursor = self._cursor()
            cursor.execute(sql, params or ())
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error en consulta (fetch_all): {str(e)}")
    
    # ==================== MÉTODOS DE CONSULTA ====================
    
    def get_total_ventas_mes(self):
        """
        Obtener el total de ventas del mes actual.
        
        Returns:
            float: Suma de la columna total en tabla Factura para el mes actual.
                   Retorna 0.0 si no hay datos o hay error.
        """
        try:
            sql = """
            SELECT ISNULL(SUM(total), 0) as total_ventas
            FROM Factura
            WHERE eliminado = 0
            AND MONTH(fecha_factura) = MONTH(GETDATE())
            AND YEAR(fecha_factura) = YEAR(GETDATE())
            """
            resultado = self._fetch_one(sql)
            return float(resultado[0]) if resultado and resultado[0] else 0.0
        except Exception as e:
            raise Exception(f"Error obteniendo total de ventas del mes: {str(e)}")
    
    def get_proximas_citas(self, limit=5):
        """
        Obtener las próximas citas (reservaciones) ordenadas por fecha.
        
        Args:
            limit (int): Cantidad de registros a retornar (default: 5)
        
        Returns:
            list: Lista de diccionarios con los datos de las próximas citas.
                  Estructura: [{'id': int, 'paciente': str, 'fecha': date, 'hora': time, 'estado': str}, ...]
        """
        try:
            sql = f"""
            SELECT TOP {limit}
                r.id_reservacion,
                p.nombres as paciente,
                r.fecha_reservacion as fecha,
                r.hora_reservacion as hora,
                r.estado
            FROM Reservacion r
            INNER JOIN Paciente p ON r.id_paciente = p.id_paciente
            WHERE r.eliminado = 0
            AND r.fecha_reservacion >= CAST(GETDATE() AS DATE)
            ORDER BY r.fecha_reservacion ASC, r.hora_reservacion ASC
            """
            resultados = self._fetch_all(sql)
            
            citas = []
            if resultados:
                for row in resultados:
                    cita = {
                        'id': row[0],
                        'paciente': row[1],
                        'fecha': row[2],
                        'hora': row[3],
                        'estado': row[4]
                    }
                    citas.append(cita)
            
            return citas
        except Exception as e:
            raise Exception(f"Error obteniendo próximas citas: {str(e)}")
    
    def get_ingresos_por_metodo(self):
        """
        Obtener los ingresos agrupados por método de pago (TipoPago).
        
        Returns:
            list: Lista de diccionarios con método de pago y monto total.
                  Estructura: [{'metodo': str, 'monto': float, 'cantidad': int}, ...]
        """
        try:
            sql = """
            SELECT 
                tp.nombre as metodo_pago,
                ISNULL(SUM(f.total), 0) as monto_total,
                COUNT(f.id_factura) as cantidad_facturas
            FROM TipoPago tp
            LEFT JOIN Factura f ON tp.id_tipo_pago = f.id_tipo_pago
            AND f.eliminado = 0
            AND MONTH(f.fecha_factura) = MONTH(GETDATE())
            AND YEAR(f.fecha_factura) = YEAR(GETDATE())
            WHERE tp.eliminado = 0
            GROUP BY tp.nombre, tp.id_tipo_pago
            ORDER BY monto_total DESC
            """
            resultados = self._fetch_all(sql)
            
            ingresos = []
            if resultados:
                for row in resultados:
                    ingreso = {
                        'metodo': row[0],
                        'monto': float(row[1]) if row[1] else 0.0,
                        'cantidad': row[2] if row[2] else 0
                    }
                    ingresos.append(ingreso)
            
            return ingresos
        except Exception as e:
            raise Exception(f"Error obteniendo ingresos por método: {str(e)}")
    
    # ==================== MÉTODOS DE PACIENTES ====================
    
    def get_todos_pacientes(self, solo_activos=False):
        """
        Obtener lista de todos los pacientes.
        
        Args:
            solo_activos (bool): Si True, solo retorna pacientes no eliminados
        
        Returns:
            list: Lista de diccionarios con datos de pacientes
        """
        try:
            sql = """
            SELECT 
                id_paciente,
                nombres,
                apellidos,
                genero,
                fecha_nacimiento,
                email,
                telefono,
                direccion,
                grupo_sanguineo,
                contacto_emergencia,
                telefono_emergencia,
                alergias,
                enfermedades_cronicas,
                observaciones,
                estado,
                eliminado,
                fecha_creacion,
                fecha_actualizacion
            FROM Paciente
            WHERE eliminado = 0
            ORDER BY nombres ASC, apellidos ASC
            """
            resultados = self._fetch_all(sql)
            
            pacientes = []
            if resultados:
                for row in resultados:
                    paciente = {
                        'id_paciente': row[0],
                        'nombres': row[1],
                        'apellidos': row[2],
                        'genero': row[3],
                        'fecha_nacimiento': row[4],
                        'email': row[5],
                        'telefono': row[6],
                        'direccion': row[7],
                        'grupo_sanguineo': row[8],
                        'contacto_emergencia': row[9],
                        'telefono_emergencia': row[10],
                        'alergias': row[11],
                        'enfermedades_cronicas': row[12],
                        'observaciones': row[13],
                        'estado': row[14],
                        'eliminado': row[15],
                        'fecha_creacion': row[16],
                        'fecha_actualizacion': row[17]
                    }
                    pacientes.append(paciente)
            
            return pacientes
        except Exception as e:
            raise Exception(f"Error obteniendo pacientes: {str(e)}")
    
    def get_paciente_por_id(self, id_paciente):
        """
        Obtener un paciente por su ID.
        
        Args:
            id_paciente (int): ID del paciente
        
        Returns:
            dict: Diccionario con datos del paciente o None si no existe
        """
        try:
            sql = """
            SELECT 
                id_paciente,
                nombres,
                apellidos,
                genero,
                fecha_nacimiento,
                email,
                telefono,
                direccion,
                grupo_sanguineo,
                contacto_emergencia,
                telefono_emergencia,
                alergias,
                enfermedades_cronicas,
                observaciones,
                estado,
                eliminado,
                fecha_creacion,
                fecha_actualizacion
            FROM Paciente
            WHERE id_paciente = ? AND eliminado = 0
            """
            resultado = self._fetch_one(sql, (id_paciente,))
            
            if resultado:
                return {
                    'id_paciente': resultado[0],
                    'nombres': resultado[1],
                    'apellidos': resultado[2],
                    'genero': resultado[3],
                    'fecha_nacimiento': resultado[4],
                    'email': resultado[5],
                    'telefono': resultado[6],
                    'direccion': resultado[7],
                    'grupo_sanguineo': resultado[8],
                    'contacto_emergencia': resultado[9],
                    'telefono_emergencia': resultado[10],
                    'alergias': resultado[11],
                    'enfermedades_cronicas': resultado[12],
                    'observaciones': resultado[13],
                    'estado': resultado[14],
                    'eliminado': resultado[15],
                    'fecha_creacion': resultado[16],
                    'fecha_actualizacion': resultado[17]
                }
            return None
        except Exception as e:
            raise Exception(f"Error obteniendo paciente por ID: {str(e)}")
    
    def buscar_pacientes(self, termino):
        """
        Buscar pacientes por nombres, apellidos, email o teléfono.
        
        Args:
            termino (str): Término de búsqueda
        
        Returns:
            list: Lista de diccionarios con pacientes encontrados
        """
        try:
            sql = """
            SELECT 
                id_paciente,
                nombres,
                apellidos,
                genero,
                fecha_nacimiento,
                email,
                telefono,
                direccion,
                grupo_sanguineo,
                contacto_emergencia,
                telefono_emergencia,
                alergias,
                enfermedades_cronicas,
                observaciones,
                estado,
                eliminado,
                fecha_creacion,
                fecha_actualizacion
            FROM Paciente
            WHERE eliminado = 0
            AND (
                nombres LIKE ? OR 
                apellidos LIKE ? OR 
                email LIKE ? OR 
                telefono LIKE ?
            )
            ORDER BY nombres ASC, apellidos ASC
            """
            param = f"%{termino}%"
            resultados = self._fetch_all(sql, (param, param, param, param))
            
            pacientes = []
            if resultados:
                for row in resultados:
                    paciente = {
                        'id_paciente': row[0],
                        'nombres': row[1],
                        'apellidos': row[2],
                        'genero': row[3],
                        'fecha_nacimiento': row[4],
                        'email': row[5],
                        'telefono': row[6],
                        'direccion': row[7],
                        'grupo_sanguineo': row[8],
                        'contacto_emergencia': row[9],
                        'telefono_emergencia': row[10],
                        'alergias': row[11],
                        'enfermedades_cronicas': row[12],
                        'observaciones': row[13],
                        'estado': row[14],
                        'eliminado': row[15],
                        'fecha_creacion': row[16],
                        'fecha_actualizacion': row[17]
                    }
                    pacientes.append(paciente)
            
            return pacientes
        except Exception as e:
            raise Exception(f"Error buscando pacientes: {str(e)}")
    
    def crear_paciente(self, paciente_dict):
        """
        Crear un nuevo paciente en la BD.
        
        Args:
            paciente_dict (dict): Diccionario con datos del paciente
        
        Returns:
            int: ID del paciente creado
        """
        try:
            sql = """
            INSERT INTO Paciente (
                nombres, apellidos, genero, fecha_nacimiento, email, telefono,
                direccion, grupo_sanguineo, contacto_emergencia, telefono_emergencia,
                alergias, enfermedades_cronicas, observaciones, estado, eliminado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor = self._cursor()
            cursor.execute(sql, (
                paciente_dict.get('nombres'),
                paciente_dict.get('apellidos'),
                paciente_dict.get('genero', 'M'),
                paciente_dict.get('fecha_nacimiento'),
                paciente_dict.get('email'),
                paciente_dict.get('telefono'),
                paciente_dict.get('direccion'),
                paciente_dict.get('grupo_sanguineo'),
                paciente_dict.get('contacto_emergencia'),
                paciente_dict.get('telefono_emergencia'),
                paciente_dict.get('alergias'),
                paciente_dict.get('enfermedades_cronicas'),
                paciente_dict.get('observaciones'),
                paciente_dict.get('estado', 1),
                0  # no eliminado
            ))
            cursor.execute("SELECT SCOPE_IDENTITY()")
            row = cursor.fetchone()
            nuevo_id = int(row[0]) if row and row[0] is not None else None
            self._conexion.commit()
            return nuevo_id
        except Exception as e:
            self._conexion.rollback()
            raise Exception(f"Error creando paciente: {str(e)}")
    
    def actualizar_paciente(self, id_paciente, paciente_dict):
        """
        Actualizar un paciente existente.
        
        Args:
            id_paciente (int): ID del paciente
            paciente_dict (dict): Diccionario con datos actualizados
        
        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            sql = """
            UPDATE Paciente SET
                nombres = ?,
                apellidos = ?,
                genero = ?,
                fecha_nacimiento = ?,
                email = ?,
                telefono = ?,
                direccion = ?,
                grupo_sanguineo = ?,
                contacto_emergencia = ?,
                telefono_emergencia = ?,
                alergias = ?,
                enfermedades_cronicas = ?,
                observaciones = ?,
                estado = ?,
                fecha_actualizacion = GETDATE()
            WHERE id_paciente = ? AND eliminado = 0
            """
            cursor = self._cursor()
            cursor.execute(sql, (
                paciente_dict.get('nombres'),
                paciente_dict.get('apellidos'),
                paciente_dict.get('genero', 'M'),
                paciente_dict.get('fecha_nacimiento'),
                paciente_dict.get('email'),
                paciente_dict.get('telefono'),
                paciente_dict.get('direccion'),
                paciente_dict.get('grupo_sanguineo'),
                paciente_dict.get('contacto_emergencia'),
                paciente_dict.get('telefono_emergencia'),
                paciente_dict.get('alergias'),
                paciente_dict.get('enfermedades_cronicas'),
                paciente_dict.get('observaciones'),
                paciente_dict.get('estado', 1),
                id_paciente
            ))
            self._conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self._conexion.rollback()
            raise Exception(f"Error actualizando paciente: {str(e)}")
    
    def eliminar_paciente_logico(self, id_paciente):
        """
        Eliminar un paciente de forma lógica (marca como eliminado).
        
        Args:
            id_paciente (int): ID del paciente
        
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            sql = """
            UPDATE Paciente SET
                eliminado = 1,
                fecha_actualizacion = GETDATE()
            WHERE id_paciente = ?
            """
            cursor = self._cursor()
            cursor.execute(sql, (id_paciente,))
            self._conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self._conexion.rollback()
            raise Exception(f"Error eliminando paciente: {str(e)}")


if __name__ == "__main__":
    # Ejemplo de uso
    try:
        queries = HospitalQueries()
        
        # Probar get_total_ventas_mes
        total = queries.get_total_ventas_mes()
        print(f"Total ventas del mes: S/. {total:,.2f}")
        
        # Probar get_proximas_citas
        citas = queries.get_proximas_citas()
        print(f"\nPróximas citas:")
        for cita in citas:
            print(f"  - {cita['paciente']} - {cita['fecha']} {cita['hora']} ({cita['estado']})")
        
        # Probar get_ingresos_por_metodo
        ingresos = queries.get_ingresos_por_metodo()
        print(f"\nIngresos por método:")
        for ingreso in ingresos:
            print(f"  - {ingreso['metodo']}: S/. {ingreso['monto']:,.2f} ({ingreso['cantidad']} facturas)")
    
    except Exception as e:
        print(f"Error: {e}")
