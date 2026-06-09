class Factura:
    def __init__(self, numero_factura=None, id_paciente=None, id_reserva=None, fecha_factura=None,
                 subtotal=0, igv=0, total=0, estado_pago="PENDIENTE", eliminado=0):
        self.numero_factura = numero_factura
        self.id_paciente = id_paciente
        self.id_reserva = id_reserva
        self.fecha_factura = fecha_factura
        self.subtotal = subtotal
        self.igv = igv
        self.total = total
        self.estado_pago = estado_pago
        self.eliminado = eliminado

    def save(self, cursor):
        sql = """
        INSERT INTO Factura (
            numero_factura, id_paciente, id_reserva, fecha_factura,
            subtotal, igv, total, estado_pago, eliminado
        )
        OUTPUT INSERTED.id_factura
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            self.numero_factura,
            self.id_paciente,
            self.id_reserva,
            self.fecha_factura,
            self.subtotal,
            self.igv,
            self.total,
            self.estado_pago,
            self.eliminado
        ))
        row = cursor.fetchone()
        return int(row[0]) if row and row[0] is not None else None
