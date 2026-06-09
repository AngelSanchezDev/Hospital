from datetime import datetime

class Pago:
    """Modelo de datos para TipoPago (Pagos)"""
    
    def __init__(self, 
                 nombre,
                 descripcion=None,
                 id_pago=None,
                 estado=True,
                 eliminado=False,
                 fecha_creacion=None):
        """
        Inicializar un Tipo de Pago.
        """
        self.id_pago = id_pago
        self.nombre = nombre.strip() if nombre else ""
        self.descripcion = descripcion.strip() if descripcion else None
        self.estado = estado
        self.eliminado = eliminado
        self.fecha_creacion = fecha_creacion or datetime.now()
    
    def es_valido(self):
        """Validar que los datos requeridos estén presentes"""
        if not self.nombre or len(self.nombre) < 2:
            return False, "El nombre debe tener al menos 2 caracteres"
        return True, "OK"
    
    def guardar(self, cursor):
        """Inserta un nuevo tipo de pago en la base de datos"""
        sql = """
        INSERT INTO TipoPago (nombre, descripcion, estado, eliminado)
        OUTPUT INSERTED.id_pago
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (
            self.nombre,
            self.descripcion,
            self.estado,
            self.eliminado
        ))
        row = cursor.fetchone()
        if row:
            self.id_pago = int(row[0])
            return self.id_pago
        return None

    def actualizar(self, cursor):
        """Actualiza un tipo de pago existente"""
        sql = """
        UPDATE TipoPago
        SET nombre = ?, descripcion = ?, estado = ?
        WHERE id_pago = ?
        """
        cursor.execute(sql, (
            self.nombre,
            self.descripcion,
            self.estado,
            self.id_pago
        ))
        return cursor.rowcount > 0

    def eliminar(self, cursor):
        """Realiza una eliminación lógica del tipo de pago"""
        sql = "UPDATE TipoPago SET eliminado = 1 WHERE id_pago = ?"
        cursor.execute(sql, (self.id_pago,))
        return cursor.rowcount > 0

    @staticmethod
    def obtener_todos(cursor, incluir_inactivos=False):
        """Obtiene todos los tipos de pago que no están eliminados"""
        sql = "SELECT id_pago, nombre, descripcion, estado, fecha_creacion FROM TipoPago WHERE eliminado = 0"
        if not incluir_inactivos:
            sql += " AND estado = 1"
        sql += " ORDER BY nombre ASC"
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        pagos = []
        for row in rows:
            pago = Pago(
                id_pago=row[0],
                nombre=row[1],
                descripcion=row[2],
                estado=row[3],
                fecha_creacion=row[4]
            )
            pagos.append(pago)
        return pagos
